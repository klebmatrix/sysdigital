import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from rotes import admin, professor, aluno  # importando os blueprints

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'chave_padrao_secreta')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'

# Usuários permitidos (exemplo)
USERS = {
    os.environ.get('ADMIN_EMAIL'): 'admin',
    os.environ.get('PROF_EMAIL'): 'professor',
    os.environ.get('ALUNO_EMAIL'): 'aluno',
}

# Registrar blueprints
app.register_blueprint(admin.admin_bp)
app.register_blueprint(professor.prof_bp)
app.register_blueprint(aluno.aluno_bp)

# Tela de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Checa se o email existe
        if email in USERS and password == '123':  # ou use senhas do .env
            session['user_email'] = email
            role = USERS[email]
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
