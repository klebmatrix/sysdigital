from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.database import db
from models import Admin, Professor
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
def dashboard():
    professores = Professor.query.all()
    return render_template("admin.html", professores=professores)

@admin_bp.route("/cadastrar_professor", methods=["POST"])
def cadastrar_professor():
    email = request.form.get("email")
    senha = request.form.get("senha_inicial")
    expira_em = request.form.get("expira_em")

    if Professor.query.get(email):
        flash("Professor já cadastrado!", "danger")
        return redirect(url_for("admin.dashboard"))

    novo = Professor(email=email, expira_em=expira_em)
    novo.set_senha(senha)
    db.session.add(novo)
    db.session.commit()
    flash("Professor cadastrado com sucesso!", "success")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/excluir_professor/<email>")
def excluir_professor(email):
    prof = Professor.query.get(email)
    if prof:
        db.session.delete(prof)
        db.session.commit()
        flash("Professor excluído com sucesso!", "success")
    else:
        flash("Professor não encontrado!", "danger")
    return redirect(url_for("admin.dashboard"))
