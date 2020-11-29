import sys, os
app_path=os.getcwd()+"/app"
sys.path.append(app_path)
from app import app
from forms import *
from flask import render_template,request,redirect, make_response, session, escape, url_for, flash
from werkzeug.utils import secure_filename
from openpyxl import load_workbook
import openpyxl_dictreader
import pandas as pd
import re


app.secret_key = "PCPORTAL"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/', methods=["POST", "GET"])
def ingresar():
	form = loginForm(request.form)
	return render_template("login.html", form = form)

@app.route('/logout', methods=["POST", "GET"])
def logout():
	session.pop("usuario",None)
	print("Cookies borradas")
	return redirect(url_for('login'))

@app.route('/login', methods=["POST", "GET"])
def login():
	form = loginForm()
	if request.method == "POST" and form.validate():
		user = request.form
		aux = datos_usuario(user['email'])
		session["usuario"] = aux[3]
		if aux[1] == 1:
			return redirect(url_for('pedido'))
		elif aux[1] == 2:
			return redirect(url_for('vista_vendedor'))
		else:
			return redirect(url_for('login')) 
	return render_template("login.html", form = form)



###############################################################
#															  #
#						VISTAS ADMIN						  #
#															  #
###############################################################

@app.route('/pedido', methods=["POST", "GET"])
def pedido():
	form = BuscarPedidoForm()
	codigo_producto = request.form
	pedidos = obtener_pedidos()
	proveedores = obtener_proveedores()
	proveedores.insert(0,(0,"Elija un proveedor"))
	form.proveedor.choices =[(tipo[0],tipo[1])for tipo in proveedores]
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			if pedidos == None:
				pedidos = ()
			if request.method == "POST" and form.validate():
				pedidos_filtrados = obtener_pedidos_filtrados(codigo_producto.get('codigo'),codigo_producto.get('nombre'),codigo_producto.get('numero_de_orden'),codigo_producto.get('proveedor'))
				return render_template("pedido.html",vista = "Pedidos Filtrados",pedidos = pedidos_filtrados,form = form)
			return render_template("pedido.html",vista = "Pedidos",pedidos = pedidos,form = form)
	else:
		return redirect(url_for('login'))

@app.route('/index', methods=["POST", "GET"])
def vista_admin():
	form = BuscarPedidoForm()
	pedidos = obtener_pedidos()
	proveedores = obtener_proveedores()
	proveedores.insert(0,(0,"Elija un proveedor"))
	form.proveedor.choices =[(tipo[0],tipo[1])for tipo in proveedores]
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			return render_template("pedido.html",vista = "Pedidos",pedidos = pedidos,form = form)
		else:
			return redirect(url_for('login'))
	else:
			return redirect(url_for('login'))

@app.route('/crear_usuario', methods=["POST", "GET"])
def crear_usuario():
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			form = crearUsuariosForm()
			datos = request.form
			if request.method == "POST" and datos.get('desactivar') != None:
				cambiar_estado(datos['id_usuario'],False)
				usuarios = obtener_todos_usuarios()
				return render_template("register.html",vista="Crear usuario", form=form, usuarios = usuarios)

			if request.method == "POST" and datos.get('activar') != None:
				cambiar_estado(datos['id_usuario'],True)
				usuarios = obtener_todos_usuarios()
				return render_template("register.html",vista="Crear usuario", form=form, usuarios = usuarios)

			if request.method == "POST" and form.validate():
				crear_usuarios(datos['email'],datos['password'],datos['nombre_usuario'],datos['apellido1_usuario'],datos['apellido2_usuario'],datos['tipo_cuenta'])
				usuarios = obtener_todos_usuarios()
				return render_template("register.html",vista="Crear usuario", form=form, usuarios = usuarios)
			usuarios = obtener_todos_usuarios()
			return render_template("register.html",vista="Crear usuario", form=form, usuarios = usuarios)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))

@app.route('/detalle/<id>', methods=["POST", "GET"])
def detalle(id):
	if re.findall("\A[0-9]+\Z", str(id)):
		form = botonesForm()
		proveedores = obtener_proveedores()
		form.proveedor.choices =[(tipo[0],tipo[1])for tipo in proveedores]
		boton = request.form
		if request.method == "POST" and boton.get('confirmar') != None:
			eliminar_pedido(id)
			mensaje = "Orden eliminada."
			datos = list()
			return render_template("detalle.html", vista="Detalle Pedido", datos = datos,mensaje = mensaje, form = form)

		if request.method == "POST" and boton.get('editar') != None and form.validate():
			mensaje = "Orden actualizada"
			actualizar_orden(boton['proveedor'],boton['numero_de_orden'],boton['descripcion'],boton['fecha_de_arribo'],boton['id_oferta'])
			datos = obtener_productos_pedido(id)
			return render_template("detalle.html", vista="Detalle Pedido", datos = datos,mensaje = mensaje, form = form)

		datos = obtener_productos_pedido(id)
		if len(datos) == 0:
			datos = list()
			mensaje = "Orden no encontrada."
			return render_template("detalle.html", vista="Detalle Pedido", datos = datos,mensaje = mensaje, form = form)

		mensaje = ""
		return render_template("detalle.html", vista="Detalle Pedido", datos = datos,mensaje = mensaje, form = form)
	datos = list()
	mensaje = "Orden no encontrada."
	return render_template("detalle.html", vista="Detalle Pedido", datos = datos,mensaje = mensaje)

@app.route('/proveedor', methods=["POST", "GET"])
def proveedor():
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			form = crearProveedorForm()
			datos = request.form
			if request.method == "POST" and datos.get('desactivar') != None:
				cambiar_estado_proveedor(datos['id_proveedor'],False)
				proveedores = obtener_proveedores_todos()
				return render_template("proveedor.html", vista="Ingresar Proveedor", form=form, proveedores = proveedores)

			if request.method == "POST" and datos.get('activar') != None:
				cambiar_estado_proveedor(datos['id_proveedor'],True)
				proveedores = obtener_proveedores_todos()
				return render_template("proveedor.html", vista="Ingresar Proveedor", form=form, proveedores = proveedores)

			if request.method == 'POST' and form.validate():
				datos = request.form
				crear_proveedor(datos['nombre_proveedor'],datos['descripcion'])
				proveedores = obtener_proveedores_todos()
				return render_template("proveedor.html", vista="Ingresar Proveedor", form=form, proveedores = proveedores)
			proveedores = obtener_proveedores_todos()
			return render_template("proveedor.html", vista="Ingresar Proveedor", form=form, proveedores = proveedores)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))



@app.route("/upload", methods=['GET', 'POST'])
def upload():
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			form = ingresarPedidoForm()
			proveedores = obtener_proveedores()
			form.proveedor.choices =[(tipo[0],tipo[1])for tipo in proveedores]
			if request.method == 'POST' and form.validate():
				datos = request.form
				f = request.files['file']
				filename = f.filename
				if filename == '':
					return render_template("upload2.html",aux=0, message="Por favor cargue un archivo con extensión xlsx.", vista ="Ingresar Pedidos", form=form)
				data_xls = pd.read_excel(f)
				arr=data_xls.to_numpy()
				filas, columnas= arr.shape
				funciona = crear_pedido(session["usuario"],datos['proveedor'],datos['numero_de_orden'],datos['descripcion'],datos['fecha_de_arribo'],arr)
				if funciona == True:
					return render_template("upload2.html",data=arr,cant=filas,aux=1,message="Orden ingresada exitosamente.", vista ="Ingresar Pedidos", form=form)
				else:
					return render_template("upload2.html",data=arr,cant=filas,aux=1,message="No puede haber campos vacíos de información o se ha sobrepasado el límite de carácteres.", vista ="Ingresar Pedidos", form=form)
			return render_template("upload2.html",aux=0,message="Por favor cargue un archivo con extensión xlsx.", vista ="Ingresar Pedidos", form=form)
		return redirect(url_for('login'))
	return redirect(url_for('login')) 



# @app.route('/aux', methods = ["POST", "GET"])
# def aux():
# 	return render_template("404.html")

# @app.route('/aux2', methods = ["POST", "GET"])
# def aux2():
# 	return render_template("tables.html")



###############################################################
#															  #
#						VISTAS VENDEDOR	     			      #
#															  #
###############################################################

#unica vista de un vendedor
@app.route('/index_venta', methods=["POST", "GET"])
def vista_vendedor():
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 2:
			form = BuscarPedidoForm()
			codigo_producto = request.form
			pedidos = obtener_pedidos()
			if pedidos == None:
				pedidos = ()
			if request.method == "POST" and form.validate():
				pedidos_filtrados = obtener_pedidos_filtrados(codigo_producto.get('codigo'),codigo_producto.get('nombre'),codigo_producto.get('numero_de_orden'),codigo_producto.get('proveedor'))
				return render_template("pedido_vendedor.html",vista = "Pedidos Filtrados",pedidos = pedidos_filtrados,form = form)
			return render_template("pedido_vendedor.html",vista = "Pedidos",pedidos = pedidos,form = form)
	else:
		return redirect(url_for('login'))

@app.route('/detalle_v/<id>', methods=["POST", "GET"])
def detalle_v(id):
	datos = obtener_productos_pedido(id)
	return render_template("detalle_vendedor.html", vista="Detalle Pedido", datos = datos)