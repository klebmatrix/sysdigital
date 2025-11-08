from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-secreta")

# 🔗 Conexão com Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔐 Credenciais do admin
ADMIN_EMAIL = os.environ.get("SUPER_ADMIN_EMAIL")
ADMIN_SENHA = os.environ.get("SUPER_ADMIN_SENHA")

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        # 🧠 Verifica se é o admin
        if email == ADMIN_EMAIL and senha == ADMIN_SENHA:
            session['user'] = {'email': email, 'role': 'admin'}
            flash('Bem-vindo, administrador!', 'success')
            return redirect(url_for('admin_dashboard'))

        # 🔎 Caso contrário, busca usuário comum no Supabase
        try:
            response = supabase.table("usuarios").select("*").eq("email", email).eq("senha", senha).execute()
            user = response.data[0] if response.data else None

            if user:
                session['user'] = user
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Credenciais inválidas.', 'danger')
        except Exception as e:
            flash(f'Erro ao acessar o banco: {e}', 'danger')

    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if 'user' not in session or session['user'].get('role') != 'admin':
        flash('Acesso restrito ao administrador.', 'warning')
        return redirect(url_for('login'))
    return render_template('admin.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sessão encerrada com sucesso!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
