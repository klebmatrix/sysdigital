import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'chave_padrao_secreta')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'

# Usuários permitidos (3 usuários)
USERS = {
    os.environ.get('USER1_EMAIL'): os.environ.get('USER1_PASSWORD'),
    os.environ.get('USER2_EMAIL'): os.environ.get('USER2_PASSWORD'),
    os.environ.get('USER3_EMAIL'): os.environ.get('USER3_PASSWORD'),
}

# Lista de professores cadastrados (em memória)
professores = []

# Rota login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in USERS and USERS[email] == password:
            session['admin_email'] = email
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('admin.html')

# Painel admin
@app.route('/admin')
def admin_dashboard():
    if 'admin_email' not in session:
        flash('Faça login para acessar o painel.', 'warning')
        return redirect(url_for('login'))
    return render_template('admin.html', professores=professores)

# Logout
@app.route('/logout')
def logout():
    session.pop('admin_email', None)
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('login'))

# Cadastrar professor
@app.route('/admin/cadastrar', methods=['POST'])
def cadastrar_professor():
    if 'admin_email' not in session:
        flash('Faça login para cadastrar.', 'warning')
        return redirect(url_for('login'))

    email = request.form.get('email')
    senha_inicial = request.form.get('senha_inicial')
    expira_em = request.form.get('expira_em')

    professores.append({
        'email': email,
        'senha_inicial': senha_inicial,
        'expira_em': expira_em
    })
    flash(f'Professor {email} cadastrado com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

# Excluir professor
@app.route('/admin/excluir/<email>')
def excluir_professor(email):
    global professores
    professores = [p for p in professores if p['email'] != email]
    flash(f'Professor {email} excluído.', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
