import os
from flask import Flask, request, session, redirect, url_for, flash, render_template

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")  # pega a secret do Render

SUPER_ADMIN_EMAIL = os.environ.get("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_SENHA = os.environ.get("SUPER_ADMIN_SENHA")

# Função de verificação do super admin
def verificar_super_admin(email, senha):
    return email == SUPER_ADMIN_EMAIL and senha == SUPER_ADMIN_SENHA

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        if verificar_super_admin(email, senha):
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciais incorretas!")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return "Bem-vindo ao painel do Super Admin!"
