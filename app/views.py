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


@app.route('/', methods=["POST", "GET"])
def ingresar():
	form = loginForm(request.form)
	return render_template("login.html", form = form)

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
			return redirect(url_for('index_venta'))
		else:
			return redirect(url_for('login')) 
	return render_template("login.html", form = form)

@app.route('/pedido', methods=["POST", "GET"])
def pedido():
	if obtener_tipo(session["usuario"])[1] == 1 or obtener_tipo(session["usuario"])[1] == 2:
		form = BuscarPedidoForm()
		codigo_producto = request.form
		pedidos = obtener_pedidos()
		if pedidos == None:
			pedidos = ()
		if request.method == "POST" and form.validate():
			pedidos_filtrados = obtener_pedidos_filtrados(codigo_producto[0],codigo_producto[1])
			return render_template("pedido.html",vista = "Pedidos Filtrados",pedidos = pedidos_filtrados,form = form)
		return render_template("pedido.html",vista = "Pedidos",pedidos = pedidos,form = form)
	return redirect(url_for('login'))

###############################################################
#															  #
#						VISTAS ADMIN						  #
#															  #
###############################################################

@app.route('/index', methods=["POST", "GET"])
def vista_admin():
	if obtener_tipo(session["usuario"])[1] == 1:
		return redirect(url_for('pedido'))
	else:
		return redirect(url_for('login'))

@app.route('/crear_usuario', methods=["POST", "GET"])
def crear_usuario():
	return render_template("register.html")

@app.route('/detalle', methods=["POST", "GET"])
def detalle():
	return render_template("detalle.html")	

@app.route('/proveedor', methods=["POST", "GET"])
def proveedor():
	return render_template("proveedor.html")	

@app.route('/lista_proveedores', methods=["POST", "GET"])
def listaproveedor():
	return render_template("lista_proveedores.html")	


@app.route('/formulario', methods = ["POST", "GET"])
def formulario():
	return render_template("upload.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
	form = ingresarPedidoForm()
	proveedores = obtener_proveedores()
	if request.method == 'POST':
		f = request.files['file']
		filename = f.filename
		if filename == '':
			return render_template("upload2.html",aux=0, message="Porfavor seleccione un archivo excel", vista ="Ingresar Pedidos", form=form)
		data_xls = pd.read_excel(f)
		arr=data_xls.to_numpy()
		filas, columnas= arr.shape

		#print("======================")
		#print("filas columnas:", filas, columnas)
		#for i in range(filas):
		#	print("codigo: ",arr[i][0],"|","descripcion: ",arr[i][1],"|","cantidad: ",arr[i][2])
		#print("======================")

		#return data_xls.to_html()
		return render_template("upload2.html",data=arr,cant=filas,aux=1,message="Pedidos actualizados exitosamente", vista ="Ingresar Pedidos", form=form)
	return render_template("upload2.html",aux=0,message="Porfavor seleccione un archivo excel", vista ="Ingresar Pedidos", form=form)


'''
@app.route('/upload', methods = ["POST", "GET"])
def upload():

	if request.method == "POST":
		if 'file' not in request.files:
			return render_template("upload.html", message = "File not selected")

		file = request.files["file"]
		filename = file.filename
		if filename == '':
			return render_template("upload.html", message = "Seleccione un archivo")

		file.save(os.path.join("uploads", file.filename))

		excel_document = load_workbook(os.path.join("uploads", file.filename), data_only=True)
		filetype= type(excel_document)
		sheet = excel_document.get_sheet_by_name('Hoja1')
		resultados=[]
		reader = openpyxl_dictreader.DictReader(os.path.join("uploads", file.filename),'Hoja1')

		for row in reader :
			resultados.append(dict(row))

		return render_template("upload.html", resultados=resultados)
	else:
		return render_template("upload.html", message = "Upload")

'''





@app.route('/aux', methods = ["POST", "GET"])
def aux():
	return render_template("charts.html")

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
	return render_template("vista_vendedor.html",vista = "Pedidos")	