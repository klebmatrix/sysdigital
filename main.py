import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'chave_padrao_secreta')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Preencha todos os campos!', 'error')
            return render_template('login.html')

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user'] = email
            flash('Login bem-sucedido!', 'success')
            return render_template('login.html', logged_in=True, user=email)
        else:
            flash('Email ou senha inválidos.', 'error')
            return render_template('login.html')

    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
