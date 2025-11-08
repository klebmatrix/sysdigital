import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from supabase import create_client, Client
from datetime import timedelta

# -----------------------------------------------------------
# CONFIGURAÇÃO DO FLASK
# -----------------------------------------------------------

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_secreta_local")
app.permanent_session_lifetime = timedelta(hours=4)

# -----------------------------------------------------------
# CONFIGURAÇÃO SUPABASE
# -----------------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_SENHA = os.getenv("SUPER_ADMIN_SENHA")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("⚠️  Supabase não configurada. Variáveis de ambiente ausentes.")

# -----------------------------------------------------------
# LOGIN REQUIRED DECORATOR
# -----------------------------------------------------------

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------------------------------------
# ROTA DE LOGIN
# -----------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "").strip()

        if not email or not senha:
            return render_template("login.html", erro="Preencha todos os campos!")

        # 🔑 Verifica se é admin do ambiente
        if email == SUPER_ADMIN_EMAIL and senha == SUPER_ADMIN_SENHA:
            session["user_email"] = email
            session["is_admin"] = True
            return redirect(url_for("index"))

        # 🔐 Verifica Supabase (usuário normal)
        if supabase:
            try:
                response = supabase.auth.sign_in_with_password({"email": email, "password": senha})
                if response.user:
                    session["user_email"] = email
                    session["is_admin"] = False
                    return redirect(url_for("index"))
            except Exception:
                pass

        return render_template("login.html", erro="E-mail ou senha inválidos!")

    return render_template("login.html")

# -----------------------------------------------------------
# ROTA PRINCIPAL (PROTEGIDA)
# -----------------------------------------------------------

@app.route("/index")
@login_required
def index():
    email = session.get("user_email")
    return render_template("index.html", email=email)

# -----------------------------------------------------------
# LOGOUT
# -----------------------------------------------------------

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

# -----------------------------------------------------------
# INÍCIO DO APP
# -----------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
