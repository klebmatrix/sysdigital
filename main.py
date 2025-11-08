import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client, Client

# Inicialização Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-secreta-local")

# Configuração Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("⚠️ Supabase não configurada! Variáveis de ambiente ausentes.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Rota: login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se é o admin direto do ambiente
        admin_email = os.environ.get("SUPER_ADMIN_EMAIL")
        admin_senha = os.environ.get("SUPER_ADMIN_SENHA")

        if email == admin_email and senha == admin_senha:
            session['usuario'] = 'admin'
            flash('Login de administrador bem-sucedido.', 'success')
            return redirect(url_for('admin'))

        # Caso contrário, tenta autenticar pelo Supabase
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": senha})
            if user and user.user:
                session['usuario'] = user.user.email
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Usuário ou senha incorretos.', 'danger')
        except Exception as e:
            print("Erro Supabase:", e)
            flash('Erro ao autenticar no Supabase.', 'danger')

    return render_template('login.html')


# Rota: dashboard (usuário comum)
@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', usuario=session['usuario'])


# Rota: admin
@app.route('/admin')
def admin():
    if session.get('usuario') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')


# Rota: logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('login'))


# Início do servidor local
if __name__ == '__main__':
    app.run(debug=True)
