#!/usr/bin/python
# -*- coding: utf-8 -*-
# Archivo ejemplo.py

from app import app
from flask import jsonify, render_template, request, redirect, Response, url_for, session, abort
from flask_login import LoginManager, login_required, login_user, logout_user 
from ctypes import *
import xml.etree.ElementTree as ET
import app.tcputils as tcp
from app.xmlutils import XMLMaker

# ===== MAIN CONFIGURATION =======

TCP_IP = "45.79.37.223"
TCP_PORT = 25000

# ===== HELPER FUNCTIONS =======

def get_ott(xmlstring):
    return ET.fromstring(xmlstring).find("ott").text


def get_dat(xmlstring):
	return ET.fromstring(xmlstring).find("info").find("dat").text


def contar(length, text, looking_for):
    count = 0
    for char in text:
        if char == looking_for:
            count += 1
    return count

# ===== MAIN FUNCTIONALITY =======

@app.route('/clientes', methods=['GET'])
@login_required
def clientes():
	#Conectar
	s = tcp.connect(TCP_IP, TCP_PORT)
	#Get ott
	ott_id = enviar_y_obtener_ott(s)
	#Crear xml query
	sql_query = "select clie_name!01, clie_id!02 from CLIENTES order by clie_name"
	xml_maker = armar_xml_desde_query(ott_id, sql_query)
	xml_request = str(xml_maker)
	#Enviar xml
	tcp.send(s, xml_request)
	xml_received = tcp.receive(s)
	row_list = ET.fromstring(xml_received).find("info").find("dat").findall("row")
	data = []
	for row in row_list:
		data.append({"name": row.find("f01").text, "id": row.find("f02").text})
	#print(data)
	return render_template("clientes.html", data=data)

def enviar_y_obtener_ott(socket):
	message = "<tx id='borja'><req>auten</req><usr>walker</usr><psw>walker</psw></tx>"
	tcp.send(socket, message)
	#Obtener respuesta OTT
	xml_received = tcp.receive(socket)
	return get_ott(xml_received)

def armar_xml_desde_query(ott_id, query):
	xml_maker = XMLMaker()
	xml_maker.open_tag("tx", properties={"id": "borja"})
	xml_maker.open_close_tag("req", text="dbxml")
	xml_maker.open_close_tag("ott", text=str(ott_id))
	xml_maker.open_tag("prm")
	xml_maker.open_tag("sql", text=query)
	xml_maker.finish()
	return xml_maker

@app.route('/procesos_full', methods=['GET'])
@login_required
def procesos_full():
	date = request.args.get("date")
	#Conectar
	s = tcp.connect(TCP_IP, TCP_PORT)
	#Get ott
	ott_id = enviar_y_obtener_ott(s)
	#Crear xml query: Obtener los log id y nombre empresa que corresponden a tdos los clientes
	sql_query = "select cuelogs.log_id!01, empresas.emp_name!02, cuelogs.files!03, portales.port_name!04, clientes.clie_name!05 from cuelogs, cuentas, empresas, clientes, portales where cuelogs.cuen_id = cuentas.cuen_id and cuentas.emp_id = empresas.emp_id and cuentas.port_id = portales.port_id and empresas.clie_id = clientes.clie_id"
	xml_maker = armar_xml_desde_query(ott_id, sql_query)
	xml_request = str(xml_maker)
	#Enviar xml
	tcp.send(s, xml_request)
	xml_received = tcp.receive(s)
	#print(xml_received)
	#Procesar log id y emp name
	client_log_ids = {}
	row_list = ET.fromstring(xml_received).find("info").find("dat").findall("row")
	for row in row_list:
		k = row.find("f01").text
		v = {"emp": row.find("f02").text, 
			"fil": row.find("f03").text,
			"port": row.find("f04").text,
			"cli": row.find("f05").text,
		}
		client_log_ids[k] = v
	#print("client_log_ids: ", client_log_ids)
	#Crear xml query: dblog
	ott_id = enviar_y_obtener_ott(s)
	xml_maker = XMLMaker()
	xml_maker.open_tag("tx", properties={"id": "borja"})
	xml_maker.open_close_tag("req", text="dblog")
	xml_maker.open_close_tag("ott", text=str(ott_id))
	xml_maker.open_tag("prm")
	xml_maker.open_tag("sql", text="log.log_id!"+date)
	xml_maker.finish()
	xml_request = str(xml_maker)
	#Enviar xml
	tcp.send(s, xml_request)
	xml_received = tcp.receive(s)
	#print(xml_received)
	#Procesar xml
	check_data = []
	row_list = get_rowlist(xml_received)
	for row in row_list:
		ncu = row.find("ncu").text
		iti = row.find("iti").text
		lid = row.find("lid").text
		aid = row.find("aid").text
		sid = row.find("sid").text
		nfi = row.find("nfi").text
		img = row.find("img").text
		lti = row.find("lti").text
		check_data.append({"ncu": ncu, "iti": iti, "lid": lid, "aid": aid, "sid": sid, "nfi": nfi, "img": img, "lti": lti})
	#print("check_data: ", check_data)
	#Filtrado
	data = []
	for value in check_data:
		if value["lid"] in client_log_ids:
			value["emp"] = client_log_ids[value["lid"]]["emp"]
			value["fil"] = client_log_ids[value["lid"]]["fil"]
			value["port"] = client_log_ids[value["lid"]]["port"]
			value["cli"] = client_log_ids[value["lid"]]["cli"]
			data.append(value)
	#print("data: ", data)
	#Procesamiento final
	tabla = []
	for fila in data:
		percent = int(fila["nfi"]) * 100 / int(fila["fil"])
		camino = []
		camino.append(fila["lid"])
		camino.append(fila["cli"]+":"+fila["emp"])
		camino.append(fila["port"])
		camino.append(fila["aid"])
		camino.append(fila["sid"])
		camino.append(fila["iti"].split(" ")[1])
		camino.append(fila["lti"].split(" ")[1])
		camino.append(str(int(percent)))
		tabla.append(camino)
	#print(matriz)
	return jsonify(matriz=tabla)

@app.route('/procesos', methods=['GET'])
@login_required
def procesos():
	cliente_id = request.args.get("id")
	date = request.args.get("date")
	#Conectar
	s = tcp.connect(TCP_IP, TCP_PORT)
	#Get ott
	ott_id = enviar_y_obtener_ott(s)
	#Crear xml query: Obtener los log id y nombre empresa que corresponden un cliente
	sql_query = "select cuelogs.log_id!01, empresas.emp_name!02, cuelogs.files!03, portales.port_name!04 from cuelogs, cuentas, empresas, clientes, portales where cuelogs.cuen_id = cuentas.cuen_id and cuentas.emp_id = empresas.emp_id and cuentas.port_id = portales.port_id and empresas.clie_id = clientes.clie_id and clientes.clie_id = %s" % (cliente_id)
	xml_maker = armar_xml_desde_query(ott_id, sql_query)
	xml_request = str(xml_maker)
	#Enviar xml
	tcp.send(s, xml_request)
	xml_received = tcp.receive(s)
	#print(xml_received)
	#Procesar log id y emp name
	client_log_ids = {}
	row_list = ET.fromstring(xml_received).find("info").find("dat").findall("row")
	for row in row_list:
		k = row.find("f01").text
		v = {"emp": row.find("f02").text, 
			"fil": row.find("f03").text,
			"port": row.find("f04").text,
		}
		client_log_ids[k] = v
	#print("client_log_ids: ", client_log_ids)
	#Crear xml query: dblog
	ott_id = enviar_y_obtener_ott(s)
	xml_maker = XMLMaker()
	xml_maker.open_tag("tx", properties={"id": "borja"})
	xml_maker.open_close_tag("req", text="dblog")
	xml_maker.open_close_tag("ott", text=str(ott_id))
	xml_maker.open_tag("prm")
	xml_maker.open_tag("sql", text="log.log_id!"+date)
	xml_maker.finish()
	xml_request = str(xml_maker)
	#Enviar xml
	tcp.send(s, xml_request)
	xml_received = tcp.receive(s)
	#print(xml_received)
	#Procesar xml
	check_data = []
	row_list = get_rowlist(xml_received)
	for row in row_list:
		ncu = row.find("ncu").text
		iti = row.find("iti").text
		lid = row.find("lid").text
		aid = row.find("aid").text
		sid = row.find("sid").text
		nfi = row.find("nfi").text
		img = row.find("img").text
		lti = row.find("lti").text
		check_data.append({"ncu": ncu, "iti": iti, "lid": lid, "aid": aid, "sid": sid, "nfi": nfi, "img": img, "lti": lti})
	#print("check_data: ", check_data)
	#Filtrado
	data = []
	for value in check_data:
		if value["lid"] in client_log_ids:
			value["emp"] = client_log_ids[value["lid"]]["emp"]
			value["fil"] = client_log_ids[value["lid"]]["fil"]
			value["port"] = client_log_ids[value["lid"]]["port"]
			data.append(value)
	#print("data: ", data)
	#Procesamiento final
	tabla = []
	for fila in data:
		percent = int(fila["nfi"]) * 100 / int(fila["fil"])
		camino = []
		camino.append(fila["lid"])
		camino.append(fila["emp"])
		camino.append(fila["port"])
		camino.append(fila["aid"])
		camino.append(fila["sid"])
		camino.append(fila["iti"].split(" ")[1])
		camino.append(fila["lti"].split(" ")[1])
		camino.append(str(int(percent)))
		tabla.append(camino)
	#print(matriz)
	return jsonify(matriz=tabla)

def camino_common(name="", ajaxurl="procesos"):
	s = tcp.connect(TCP_IP, TCP_PORT)
	ott_id = enviar_y_obtener_ott(s)
	xml_maker = armar_xml_desde_query(ott_id, "select acc_id!01, acc_desc!02 from acciones")
	tcp.send(s, str(xml_maker))
	xml_received_acc = tcp.receive(s)
	ott_id = enviar_y_obtener_ott(s)
	xml_maker_stat = armar_xml_desde_query(ott_id, "select stat_id!01, stat_desc!02 from status")
	tcp.send(s, str(xml_maker_stat))
	xml_received_stat = tcp.receive(s)
	#Obtener acciones
	rowlist = get_rowlist(xml_received_acc)
	acciones = {}
	for row in rowlist:
		acciones[row.find("f01").text] = row.find("f02").text
	rowlist = get_rowlist(xml_received_stat)
	status = {}
	for row in rowlist:
		status[row.find("f01").text] = row.find("f02").text
	#print(acciones, status)
	return render_template("tables.html", name=name, acciones=acciones, status=status, ajaxurl=ajaxurl)

@app.route('/camino', methods=["GET"])
@login_required
def camino():
	cliente_name = request.args.get("name")
	cliente_id = request.args.get("id")
	#Conectar
	return camino_common(name=cliente_name, ajaxurl="procesos")

@app.route('/camino_full', methods=["GET"])
@login_required
def camino_full():
	return camino_common(name="Todos los caminos", ajaxurl="procesos_full")

def get_rowlist(xml_string):
	return ET.fromstring(xml_string).find("info").find("dat").findall("row")
