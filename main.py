from flask import Flask, render_template, request, redirect, url_for
from routes.professor import verificar_professor, cadastrar_professor
from routes.admin import verificar_admin
from routes.aluno import verificar_aluno

app = Flask(__name__)
app.secret_key = "uma_chave_secreta_qualquer"

# Rota inicial: login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        # Verifica tipo de usuário
        if verificar_admin(usuario, senha):
            return redirect(url_for("dashboard_admin"))
        elif verificar_professor(usuario, senha):
            return redirect(url_for("dashboard_professor"))
        elif verificar_aluno(usuario, senha):
            return redirect(url_for("dashboard_aluno"))
        else:
            return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")

# Dashboards de exemplo
@app.route("/dashboard/admin")
def dashboard_admin():
    return render_template("dashboard.html", tipo="Admin")

@app.route("/dashboard/professor")
def dashboard_professor():
    return render_template("dashboard.html", tipo="Professor")

@app.route("/dashboard/aluno")
def dashboard_aluno():
    return render_template("dashboard.html", tipo="Aluno")


if __name__ == "__main__":
    app.run(debug=True)
