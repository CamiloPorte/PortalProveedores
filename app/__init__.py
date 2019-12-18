from flask import Flask
login_manager = LoginManager()
app = Flask(__name__, template_folder='templates')
login_manager.init_app(app)
from app import views