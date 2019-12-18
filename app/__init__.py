from flask import Flask, request, redirect, Response, url_for, session, abort
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
	u = User(i)
	u.set_name(k)
	u.set_password(v)
	users.append(u)

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)

# somewhere to login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if username in users_data:
            if users_data[username]["password"] == md5ify(password):
                id = users_data[username]["id"]
                user = User(id)
                login_user(user)
                return redirect(request.args.get("next"))
        return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

from app import views