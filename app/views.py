import sys, os
app_path=os.getcwd()+"/app"
sys.path.append(app_path)
from app import app
from forms import *
from flask import render_template,request,redirect, make_response, session, escape, url_for, flash

@app.route('/', methods=["POST", "GET"])
def inicio():
	return render_template("login.html")