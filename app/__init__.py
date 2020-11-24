from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY']= 'ac6c8838606aa4f6b68fa6c6dfd056da5600f54074b7c4f1f8f617fc87d405b4'
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqldb://dbms:DBMS2020@localhost/comp3161?host=localhost?port=32768?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config['UPLOAD_FOLDER'] = './app/static/uploads'

db = SQLAlchemy(app)
db.autoflush = False



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please login first"

app.config.from_object(__name__)
from app import views