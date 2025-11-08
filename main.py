import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

# Variáveis de ambiente
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'chave_padrao_secreta')
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Preencha todos os campos!', 'error')
            return redirect(url_for('login'))

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user'] = username
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
            return redirect(url_for('login'))

    # Mantém exatamente a tela de login que você já tinha
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
