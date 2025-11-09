import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import verificar_professor, verificar_aluno  # funções do seu models.py

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "minha_chave_secreta")

# Variáveis de ambiente do Admin
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('password')

    # Login Admin
    if email == ADMIN_EMAIL and senha == ADMIN_PASSWORD:
        session['user'] = 'admin'
        return redirect(url_for('dashboard'))

    # Login Professor
    if verificar_professor(email, senha):
        session['user'] = 'professor'
        return redirect(url_for('dashboard'))

    # Login Aluno
    if verificar_aluno(email, senha):
        session['user'] = 'aluno'
        return redirect(url_for('dashboard'))

    flash("Usuário ou senha inválidos", "danger")
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template("dashboard.html", user=user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
