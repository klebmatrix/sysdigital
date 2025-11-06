import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # para sessões

# Configuração do Banco de Dados
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Importa modelos e rotas
from models import Admin, Professor, Aluno, Atividade, Resposta
from routes.admin_routes import admin_bp
from routes.professor_routes import professor_bp
from routes.aluno_routes import aluno_bp

# Registra blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(professor_bp, url_prefix='/professor')
app.register_blueprint(aluno_bp, url_prefix='/aluno')

# Tela de login
@app.route('/')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
