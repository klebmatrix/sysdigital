from flask import Blueprint, render_template, flash

aluno_bp = Blueprint("aluno", __name__)

@aluno_bp.route("/")
def dashboard():
    flash("Bem-vindo ao seu painel de aluno!", "info")
    return render_template("aluno.html")
