import sys, os
app_path=os.getcwd()+"/app"
sys.path.append(app_path)
from app import app
from forms import *
from flask import render_template,request,redirect, make_response, session, escape, url_for, flash
from werkzeug.utils import secure_filename
from openpyxl import load_workbook
import openpyxl_dictreader

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

#ver pedido
@app.route('/pedido', methods=["POST", "GET"])
def pedido():
	return render_template("pedido.html")


@app.route('/detalle', methods=["POST", "GET"])
def detalle():
	return render_template("detalle.html")	

@app.route('/signup', methods=["POST", "GET"])
def signup():
	return render_template("register.html")

@app.route('/formulario', methods = ["POST", "GET"])
def formulario():
	return render_template("upload.html")

@app.route('/upload', methods = ["POST", "GET"])
def uploadsd():

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