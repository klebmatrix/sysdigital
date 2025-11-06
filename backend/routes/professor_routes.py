from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import Professor, Atividade

professor_bp = Blueprint('professor', __name__)

# Painel professor
@professor_bp.route('/')
def dashboard():
    atividades = Atividade.query.all()
    return render_template('professor.html', atividades=atividades)

# Criar atividade
@professor_bp.route('/criar_atividade', methods=['POST'])
def criar_atividade():
    titulo = request.form.get('titulo')
    tipo = request.form.get('tipo')  # multipla_escolha ou resposta_correta
    gabarito = request.form.get('gabarito')  # JSON string
    professor_email = request.form.get('professor_email')

    atividade = Atividade(
        titulo=titulo,
        tipo=tipo,
        gabarito=gabarito,
        professor_email=professor_email
    )
    db.session.add(atividade)
    db.session.commit()
    flash("Atividade criada!", "success")
    return redirect(url_for('professor.dashboard'))
