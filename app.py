from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Api
from flask_login import LoginManager, login_required, login_user, current_user
from dotenv import load_dotenv
from db import db
from controllers.guarderia import GuarderiaController
from controllers.perro import PerroController
from controllers.cuidador import Cuidador
from models.user import User
import os

load_dotenv()

secret_key = os.urandom(24)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}/{os.getenv("SCHEMA_DB")}'
app.config["SECRET_KEY"] = secret_key
db.init_app(app)
api = Api(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    return None

@app.route("/")
def main():
    return "Ingresé al sistema"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:

            login_user(user)
            if user.is_admin:
                
                return redirect(url_for("perrocontroller"))
            else:
                return redirect(url_for("cuidadorcontroller"))
        
    return render_template("login.html")

api.add_resource(GuarderiaController, '/guarderias')
api.add_resource(PerroController, '/perros')
api.add_resource(Cuidador, '/cuidadores')
