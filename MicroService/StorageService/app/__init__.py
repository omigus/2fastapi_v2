from flask import Flask
from flask_cors import CORS
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__ , static_folder='static')
CORS(app)
SECRET_KEY = '$29h4u@q$goi15@a40d!0-az5o9)qpry#d)y$+=6=yf$ixmbap'
EndPoint = "/api"
UPLOADED_FOLDER =  'app/static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

from app.Storage.view import StorageService

app.register_blueprint(StorageService)

