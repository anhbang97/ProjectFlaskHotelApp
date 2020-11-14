from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from .statusenum import *
from flask_login import LoginManager
from PIL import Image
from io import BytesIO
import base64


app = Flask(__name__)
app.secret_key="'\xbd\xa6\x1fU\x9d\xa3\xde\x17\xe4\x0c\xdb\xeb{j\x826"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/dbhotelapp?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =True

db = SQLAlchemy(app)

admin = Admin(app, name="HỆ THỐNG QUẢN LÝ KHÁCH SẠN", template_mode="bootstrap4", )

login = LoginManager(app=app)


