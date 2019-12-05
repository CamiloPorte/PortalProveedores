#!/usr/bin/python
# -*- coding: utf-8 -*-
# Archivo ejemplo.py

from app import app
from flask import render_template,request,redirect
import numpy as np
from ctypes import *
import xml.etree.ElementTree as ET
import socket
TCP_IP = "45.79.37.223"
TCP_PORT = 25000
BUFFER_SIZE = 1024

def tcp_connect(ip, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	r = socket.gethostbyname(ip)
	s.connect((r, port))
	return s

def tcp_send(s, message):
	strlen = str(len(message)).zfill(5)
	s.send(bytes(strlen + str(message), 'utf-8'))

def tcp_receive(s):
	result = b""
	received = s.recv(BUFFER_SIZE)
	result += received
	rec_len = get_response_length(received)
	rec_len -= BUFFER_SIZE
	while rec_len > 0:
		received = s.recv(BUFFER_SIZE)
		result += received
		rec_len -= BUFFER_SIZE
	return result

def get_response_length(message):
	return int(message[:5])
def cut_response_length(message):
	return message[5:]
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

@app.route('/', methods=["POST", "GET"])
def formulario():

	s = tcp_connect(TCP_IP, TCP_PORT)
	message = "<tx id='borja'><req>auten</req><usr>walker</usr><psw>walker</psw></tx>"
	tcp_send(s, message)
	xml_received = cut_response_length(tcp_receive(s))
	ott_id = get_ott(xml_received)
	xml_request = "<tx id='borja'>"
	xml_request += "<req>dbcur</req>"
	xml_request += "<ott>%s</ott>" % (ott_id)
	xml_request += "<prm>"
	xml_request += "<sql>"
	xml_request += "select log.log_id ||'|'|| acciones.acc_desc ||'|'|| status.stat_desc ||'|'|| to_char(log.log_time , 'dd/mm/yy hh24:mi:ss') from log, acciones, status where log.acc_id = acciones.acc_id and log.stat_id = status.stat_id and log.log_time > current_date order by log_id, log_time;"
	xml_request += "</sql>"
	xml_request += "</prm>"
	xml_request += "</tx>"
	tcp_send(s, xml_request)
	xml_received = cut_response_length(tcp_receive(s))
	print(xml_received)
	texto = get_dat(xml_received)
	filas = texto.split("~")
	matriz = []
	for fila in filas:
		matriz.append(fila.split("|"))
	print(matriz)
	"""
	matriz = []
	aux = []
	ans =[]
	ciclos = 0
	datos = str(texto).split("|")
	aux.append(datos[0].split("'")[1])
	for i in range(filas+1):
	    for j in range(1,3):
	    	aux.append(datos[j+ciclos])
	    ciclos = ciclos + 3
	    aux.append(datos[ciclos].split('~')[0])
	    matriz.append(aux)
	    aux =[]
	    if i <filas:
 	   		aux.append(datos[ciclos].split('~')[1])
	

	for i in range(len(matriz)):
		if i < len(matriz)-1:
			if matriz[i][0] != matriz[i+1][0]:
				ans.append(matriz[i])
		else:
			print(matriz[i])
			ans.append(matriz[i])
	print(matriz)
	"""
	return render_template("tables.html",matriz=matriz)





