from flask_login import UserMixin
from backend.database import db
from werkzeug.security import generate_password_hash, check_password_hash

# -----------------------
# MODELO: ADMINISTRADOR
# -----------------------
class Admin(UserMixin, db.Model):
    __tablename__ = "admins"
    email = db.Column(db.String(100), primary_key=True)
    senha_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, email, senha):
        self.email = email
        self.set_senha(senha)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def get_id(self):
        return self.email


# -----------------------
# MODELO: PROFESSOR
# -----------------------
class Professor(UserMixin, db.Model):
    __tablename__ = "professores"
    email = db.Column(db.String(100), primary_key=True)
    senha_hash = db.Column(db.String(200))
    expira_em = db.Column(db.String(20))

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def get_id(self):
        return self.email


# -----------------------
# MODELO: ALUNO
# -----------------------
class Aluno(UserMixin, db.Model):
    __tablename__ = "alunos"
    matricula = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    senha_hash = db.Column(db.String(200))

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def get_id(self):
        return str(self.matricula)






