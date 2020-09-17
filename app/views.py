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

###############################################################
#															  #
#						VISTAS ADMIN						  #
#															  #
###############################################################

@app.route('/', methods=["POST", "GET"])
def inicio():
	return render_template("login.html")



#vista principal admin
@app.route('/index', methods=["POST", "GET"])
def index():
	return render_template("vista_admin.html")


@app.route('/crear_usuario', methods=["POST", "GET"])
def crear_usuario():
	return render_template("register.html")

@app.route('/pedido', methods=["POST", "GET"])
def pedido():
	return render_template("pedido.html")

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

@app.route("/upload2", methods=['GET', 'POST'])
def upload2():
	if request.method == 'POST':
		print(request.files['file'])
		f = request.files['file']
		data_xls = pd.read_excel(f)
		arr=data_xls.to_numpy()
		filas, columnas= arr.shape
		print("======================")
		print("filas columnas:", filas, columnas)
		for i in range(filas):
			print("codigo: ",arr[i][0],"|","descripcion: ",arr[i][1],"|","cantidad: ",arr[i][2])
		print("======================")

		#return data_xls.to_html()
		return render_template("upload2.html",data=arr,cant=filas )
	return render_template("upload2.html")

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







##@app.route('/upload', methods = ["POST", "GET"])
##def uploader():
	##if request.methods == 'POST':
	##	f = request.form['excel']



###############################################################
#															  #
#						VISTAS VENDEDOR	     			      #
#															  #
###############################################################

#unica vista de un vendedor
@app.route('/index_venta', methods=["POST", "GET"])
def index2():
	return render_template("vista_vendedor.html")	