import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_login import LoginManager
from sqlalchemy import create_engine

from .enums import *

app = Flask(__name__)
app.secret_key = "'\xbd\xa6\x1fU\x9d\xa3\xde\x17\xe4\x0c\xdb\xeb{j\x826"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/dbhotelapp?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =True
app.config["FLASK_ADMIN_SWATCH"] = 'sandstone'  # https://bootswatch.com/

app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20


engine = create_engine("mysql+pymysql://root:123456@localhost/dbhotelapp?charset=utf8mb4", pool_timeout=20, pool_recycle=299)

db = SQLAlchemy(app)

admin = Admin(app, name="QUẢN TRỊ KHÁCH SẠN", template_mode="bootstrap3", index_view=AdminIndexView("Trang chủ"))
login = LoginManager(app=app)


sqlalchemy.pool_recycle = 299
sqlalchemy.pool_timeout = 20


