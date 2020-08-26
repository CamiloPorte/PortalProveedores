from flask import Flask

app = Flask(__name__, template_folder='startbootstrap-sb-admin-2-gh-pages')
from app import views