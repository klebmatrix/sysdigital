from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from utils import verificar_professor, verificar_aluno

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave_temporaria")

SUPER_ADMIN_EMAIL = os.environ.get("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_SENHA = os.environ.get("SUPER_ADMIN_SENHA")

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('password')

    if email == SUPER_ADMIN_EMAIL and senha == SUPER_ADMIN_SENHA:
        session['user'] = 'admin'
        return redirect(url_for('dashboard'))

    if verificar_professor(email, senha):
        session['user'] = 'professor'
        return redirect(url_for('dashboard'))

    if verificar_aluno(email, senha):
        session['user'] = 'aluno'
        return redirect(url_for('dashboard'))

    flash("Usuário ou senha inválidos")
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
