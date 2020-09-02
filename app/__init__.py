from flask import Flask

app = Flask(__name__, template_folder='startbootstrap-sb-admin')
from app import views
