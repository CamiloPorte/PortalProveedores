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
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			form = BuscarPedidoForm()
			codigo_producto = request.form
			pedidos = obtener_pedidos()
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
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			form = BuscarPedidoForm()
			pedidos = obtener_pedidos()
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
			usuarios = obtener_usuarios()
			if request.method == "POST" and form.validate():
				datos = request.form
				crear_usuarios(datos['email'],datos['password'],datos['nombre_usuario'],datos['apellido1_usuario'],datos['apellido2_usuario'],datos['tipo_cuenta'])
				return render_template("register.html",vista="Crear usuario", form=form, usuarios = usuarios)
			return render_template("register.html",vista="Crear usuario", form=form, usuarios = usuarios)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))

@app.route('/detalle/<id>', methods=["POST", "GET"])
def detalle(id):
	datos = obtener_productos_pedido(id)
	return render_template("detalle.html", vista="Detalle Pedido", datos = datos)

@app.route('/proveedor', methods=["POST", "GET"])
def proveedor():
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			form = crearProveedorForm()
			proveedores = obtener_proveedores()
			if request.method == 'POST' and form.validate():
				datos = request.form
				crear_proveedor(datos['nombre_proveedor'],datos['descripcion'])
				return render_template("proveedor.html", vista="Ingresar Proveedor", form=form, proveedores = proveedores)
			return render_template("proveedor.html", vista="Ingresar Proveedor", form=form, proveedores = proveedores)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/lista_proveedores', methods=["POST", "GET"])
def listaproveedor():
	return render_template("lista_proveedores.html")	



@app.route("/upload", methods=['GET', 'POST'])
def upload():
	if session.get('usuario')!= None:
		if obtener_tipo(session["usuario"])[1] == 1:
			form = ingresarPedidoForm()
			if request.method == 'POST' and form.validate():
				datos = request.form
				f = request.files['file']
				filename = f.filename
				if filename == '':
					return render_template("upload2.html",aux=0, message="Por favor cargue un archivo con extensión xlsx.", vista ="Ingresar Pedidos", form=form)
				data_xls = pd.read_excel(f)
				arr=data_xls.to_numpy()
				filas, columnas= arr.shape
				crear_pedido(session["usuario"],datos['proveedor'],datos['numero_de_orden'],datos['descripcion'],datos['fecha_de_arribo'],arr)

				return render_template("upload2.html",data=arr,cant=filas,aux=1,message="Pedidos actualizados exitosamente", vista ="Ingresar Pedidos", form=form)
			return render_template("upload2.html",aux=0,message="Por favor cargue un archivo con extensión xlsx.", vista ="Ingresar Pedidos", form=form)
		return redirect(url_for('login'))
	return redirect(url_for('login')) 



@app.route('/aux', methods = ["POST", "GET"])
def aux():
	return render_template("404.html")

@app.route('/aux2', methods = ["POST", "GET"])
def aux2():
	return render_template("tables.html")



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