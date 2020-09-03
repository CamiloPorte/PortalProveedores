import sys, os
app_path=os.getcwd()+"/app"
sys.path.append(app_path)
from app import app
from forms import *
from flask import render_template,request,redirect, make_response, session, escape, url_for, flash
from werkzeug.utils import secure_filename


###############################################################
#															  #
#						VISTAS ADMIN						  #
#															  #
###############################################################

@app.route('/', methods=["POST", "GET"])
def inicio():
	return render_template("login.html")

@app.route('/signup', methods=["POST", "GET"])
def signup():
	return render_template("register.html")

@app.route('/formulario', methods = ["POST", "GET"])
def formulario():
	return render_template("index2.html")

@app.route('/upload', methods = ["POST", "GET"])
def uploadsd():
	if request.method == "POST":
		file = request.files["file"]
		file.save(os.path.join("uploads", file.filename))
		return render_template("index2.html", message = "success")
	return render_template("index2.html", message = "Upload")



##@app.route('/upload', methods = ["POST", "GET"])
##def uploader():
	##if request.methods == 'POST':
	##	f = request.form['excel']



###############################################################
#															  #
#						VISTAS VENDERDOR	     			  #
#															  #
###############################################################
