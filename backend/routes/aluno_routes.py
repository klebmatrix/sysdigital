from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import Aluno, Atividade, Resposta
import json

aluno_bp = Blueprint('aluno', __name__)

# Painel aluno
@aluno_bp.route('/')
def dashboard():
    atividades = Atividade.query.all()
    return render_template('aluno.html', atividades=atividades)

# Enviar resposta
@aluno_bp.route('/responder/<int:atividade_id>', methods=['POST'])
def responder(atividade_id):
    aluno_email = request.form.get('aluno_email')
    resposta = request.form.get('resposta')  # JSON string
    resposta_obj = Resposta(
        atividade_id=atividade_id,
        aluno_email=aluno_email,
        resposta=json.loads(resposta),
        nota=None
    )
    db.session.add(resposta_obj)
    db.session.commit()
    flash("Resposta enviada!", "success")
    return redirect(url_for('aluno.dashboard'))
