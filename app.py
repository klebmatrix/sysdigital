from flask import Flask, render_template, redirect, url_for, session
from backend.database import db
from backend.routes.admin_routes import admin_bp
from backend.routes.professor_routes import professor_bp
from backend.routes.aluno_routes import aluno_bp
from models import Admin, Professor, Aluno

from flask_login import LoginManager

# =============================
# Inicialização do Flask
# =============================
app = Flask(__name__)
app.secret_key = "chave-super-secreta"  # Troque por uma chave forte

# =============================
# Banco de Dados
# =============================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///escola.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# =============================
# Gerenciador de Login
# =============================
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# =============================
# Registro das rotas (Blueprints)
# =============================
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(professor_bp, url_prefix="/professor")
app.register_blueprint(aluno_bp, url_prefix="/aluno")

# =============================
# Modelo de LoginManager
# =============================
@login_manager.user_loader
def load_user(user_id):
    # Tenta encontrar o usuário em todas as tabelas
    user = Admin.query.get(user_id)
    if not user:
        user = Professor.query.get(user_id)
    if not user:
        user = Aluno.query.get(user_id)
    return user

# =============================
# Página inicial (Login)
# =============================
@app.route("/")
def index():
    if "usuario" in session:
        tipo = session.get("tipo")
        if tipo == "admin":
            return redirect(url_for("admin.dashboard"))
        elif tipo == "professor":
            return redirect(url_for("professor.dashboard"))
        elif tipo == "aluno":
            return redirect(url_for("aluno.dashboard"))
    return render_template("login.html")

# =============================
# Inicialização do banco
# =============================
@app.before_first_request
def criar_banco():
    db.create_all()
    if not Admin.query.first():
        admin_padrao = Admin(email="admin@escola.com", senha="1234")
        db.session.add(admin_padrao)
        db.session.commit()

# =============================
# Executar servidor
# =============================
if __name__ == "__main__":
    app.run(debug=True)
