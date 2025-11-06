from app import db
from flask_login import UserMixin
from datetime import datetime

# =================================
# Admin
# =================================
class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    email = db.Column(db.String, primary_key=True)
    senha = db.Column(db.String, nullable=False)

# =================================
# Professor
# =================================
class Professor(UserMixin, db.Model):
    __tablename__ = 'professores'
    email = db.Column(db.String, primary_key=True)
    senha_inicial = db.Column(db.String, nullable=False)
    expira_em = db.Column(db.Date, nullable=False)

# =================================
# Aluno
# =================================
class Aluno(UserMixin, db.Model):
    __tablename__ = 'alunos'
    email = db.Column(db.String, primary_key=True)
    senha = db.Column(db.String, nullable=False)
    turma = db.Column(db.String, nullable=False)
    professor_email = db.Column(db.String, db.ForeignKey('professores.email', ondelete='CASCADE'))

# =================================
# Atividades
# =================================
class Atividade(db.Model):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)  # 'multipla_escolha' ou 'resposta_correta'
    gabarito = db.Column(db.JSON, nullable=False)
    professor_email = db.Column(db.String, db.ForeignKey('professores.email', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =================================
# Respostas
# =================================
class Resposta(db.Model):
    __tablename__ = 'respostas'
    id = db.Column(db.Integer, primary_key=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id', ondelete='CASCADE'))
    aluno_email = db.Column(db.String, db.ForeignKey('alunos.email', ondelete='CASCADE'))
    resposta = db.Column(db.JSON, nullable=False)
    nota = db.Column(db.Integer)
    enviada_em = db.Column(db.DateTime, default=datetime.utcnow)
