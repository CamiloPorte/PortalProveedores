import sys, os
app_path=os.getcwd()+"/app"
sys.path.append(app_path)
from app import app
from forms import *
from flask import render_template,request,redirect, make_response, session, escape, url_for, flash


###############################################################
#															  #
#						VISTAS ADMIN						  #
#															  #
###############################################################

@app.route('/', methods=["POST", "GET"])
def inicio():
	return render_template("login.html")

<<<<<<< HEAD
@app.route('/index', methods=["POST", "GET"])
def index():
	return render_template("index.html")
=======
@app.route('/signup', methods=["POST", "GET"])
def signup():
	return render_template("register.html")


###############################################################
#															  #
#						VISTAS VENDERDOR	     			  #
#															  #
###############################################################
>>>>>>> 1d020ff6ec331a5191432194b1da81e712fa3305
