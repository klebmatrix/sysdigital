import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from rotes.admin import admin_bp
from rotes.professor import prof_bp
from rotes.aluno import aluno_bp

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'chave_padrao_secreta')

# Blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(prof_bp, url_prefix='/professor')
app.register_blueprint(aluno_bp, url_prefix='/aluno')

# Usuários de teste
USUARIOS = {
    'admin@example.com': 'admin123',
    'professor@example.com': 'prof123',
    'aluno@example.com': 'aluno123'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in USUARIOS and USUARIOS[email] == password:
            session['user'] = email
            flash('Login bem-sucedido!', 'success')
            # Redireciona conforme o tipo de usuário
            if email == 'admin@example.com':
                return redirect(url_for('admin.dashboard'))
            elif email == 'professor@example.com':
                return redirect(url_for('professor.dashboard'))
            else:
                return redirect(url_for('aluno.dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    # Mantém a tela original de login
    return render_template('login.html', debug_env_url='#')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
