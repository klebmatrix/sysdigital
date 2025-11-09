from flask import Flask, render_template, request, redirect, url_for
from routes.professor import verificar_professor, cadastrar_professor
from routes.admin import verificar_admin
from routes.aluno import verificar_aluno

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if verificar_admin(usuario, senha):
        return redirect(url_for('admin_dashboard'))
    elif verificar_professor(usuario, senha):
        return redirect(url_for('professor_dashboard'))
    else:
        return "Usuário ou senha incorretos"

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/professor_dashboard')
def professor_dashboard():
    return render_template('professor_dashboard.html')

@app.route('/cadastrar_professor', methods=['GET', 'POST'])
def cadastrar_professor_route():
    if request.method == 'POST':
        nome = request.form['nome']
        usuario = request.form['usuario']
        senha = request.form['senha']
        cadastrar_professor(nome, usuario, senha)
        return redirect(url_for('professor_dashboard'))
    return render_template('cadastrar_professor.html')

if __name__ == '__main__':
    app.run(debug=True)
