import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

# ====================================================
# CONFIGURAÇÃO DO FLASK
# ====================================================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")  # chave secreta do Flask

# ====================================================
# VARIÁVEIS DE AMBIENTE DO SUPER ADMIN
# ====================================================
SUPER_ADMIN_EMAIL = os.environ.get("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_SENHA = os.environ.get("SUPER_ADMIN_SENHA")

# ====================================================
# ROTAS
# ====================================================

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Verifica Super Admin
        if email == SUPER_ADMIN_EMAIL and senha == SUPER_ADMIN_SENHA:
            session["super_admin"] = True
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Email ou senha inválidos!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")  # Crie login.html na pasta templates

@app.route("/dashboard")
def dashboard():
    if not session.get("super_admin"):
        flash("Acesso negado!", "danger")
        return redirect(url_for("login"))

    return render_template("dashboard.html")  # Crie dashboard.html na pasta templates

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu com sucesso!", "info")
    return redirect(url_for("login"))

# ====================================================
# EXECUÇÃO
# ====================================================
if __name__ == "__main__":
    app.run(debug=True)
