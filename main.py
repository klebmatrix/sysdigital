import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Importando blueprints corretamente
from rotes.admin import admin_bp
from rotes.professor import prof_bp
from rotes.aluno import aluno_bp

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'chave_padrao_secreta')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'

# Registrar blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(prof_bp)
app.register_blueprint(aluno_bp)

# Usuários (pode colocar senhas no .env)
USERS = {
    os.environ.get('ADMIN_EMAIL', 'admin@example.com'): 'admin',
    os.environ.get('PROF_EMAIL', 'prof@example.com'): 'professor',
    os.environ.get('ALUNO_EMAIL', 'aluno@example.com'): 'aluno'
}

# Tela de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica usuário e senha
        if email in USERS and password == '123':  # ou coloque senhas reais no .env
            session['user_email'] = email
            role = USERS[email]
            # Redireciona para o painel correto
            if role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'professor':
                return redirect(url_for('professor.dashboard'))
            elif role == 'aluno':
                return redirect(url_for('aluno.dashboard'))
        else:
            flash('Email ou senha inválidos!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout geral
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
