from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.database import db
from models import Professor, Aluno

professor_bp = Blueprint("professor", __name__)

@professor_bp.route("/")
def dashboard():
    alunos = Aluno.query.all()
    return render_template("professor.html", alunos=alunos)

@professor_bp.route("/cadastrar_aluno", methods=["POST"])
def cadastrar_aluno():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    if Aluno.query.filter_by(email=email).first():
        flash("Aluno já cadastrado!", "danger")
        return redirect(url_for("professor.dashboard"))

    aluno = Aluno(nome=nome, email=email)
    aluno.set_senha(senha)
    db.session.add(aluno)
    db.session.commit()
    flash("Aluno cadastrado com sucesso!", "success")
    return redirect(url_for("professor.dashboard"))

@professor_bp.route("/excluir_aluno/<int:matricula>")
def excluir_aluno(matricula):
    aluno = Aluno.query.get(matricula)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        flash("Aluno excluído com sucesso!", "success")
    else:
        flash("Aluno não encontrado!", "danger")
    return redirect(url_for("professor.dashboard"))
