from backend.database import db

class Professor(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    senha_inicial = db.Column(db.String(255), nullable=False)
    expira_em = db.Column(db.String(10), nullable=False)

class Aluno(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    nome = db.Column(db.String(120), nullable=False)

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(50))
    gabarito = db.Column(db.Text)
    professor_email = db.Column(db.String(120), db.ForeignKey('professor.email'))

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividade.id'))
    aluno_email = db.Column(db.String(120), db.ForeignKey('aluno.email'))
    resposta = db.Column(db.Text)
    nota = db.Column(db.Float)
