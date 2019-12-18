from flask import Flask, request, redirect, Response, url_for, session, abort, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import json
import hashlib
from users_utils import *

app = Flask(__name__, template_folder='templates')

app.secret_key = b'Y\x14zs\x0faN\x93\x13\xb4\x07\x95\xa2j\x9c\xf7'

#Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = ""
        self.password = ""
    def set_name(self, name):
        self.name = name
    def set_password(self, pswd):
        self.password = pswd
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

# ===== LOGIN FUNCTIONALITY ======

# Load users
#users = [User(id) for id in range(1, 21)]
users_data = load_users_data()
users = []
i = 0
for k, v in users_data.items():
	u = User(k)
	u.set_name(k)
	u.set_password(v)
	users.append(u)

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)

# somewhere to login

@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if username in users_data:
            if users_data[username]["password"] == md5ify(password):
                id = username
                user = User(id)
                login_user(user)
                nxt = "clientes"
                if request.args.get("next") != None:
                	nxt = request.args.get("next")
                return redirect(nxt)
        return abort(401)
    else:
        return render_template("login.html")

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login?message_code=success_logout")

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return redirect("/login?message_code=login_failed")

from app import views