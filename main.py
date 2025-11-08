import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis de ambiente (em local)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_secreta_padrao")

# ⚙️ Configuração Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_SENHA = os.getenv("SUPER_ADMIN_SENHA")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("⚠️ Supabase não configurada. Variáveis ausentes.")

# 🧪 Verificar se o Render está lendo as variáveis
@app.route("/verificar_ambiente")
def verificar_ambiente():
    return jsonify({
        "SUPABASE_URL": bool(SUPABASE_URL),
        "SUPABASE_KEY": bool(SUPABASE_KEY),
        "SUPER_ADMIN_EMAIL": bool(SUPER_ADMIN_EMAIL),
        "SUPER_ADMIN_SENHA": bool(SUPER_ADMIN_SENHA),
        "SECRET_KEY": bool(app.secret_key)
    })

# 🏠 Página inicial
@app.route("/")
def index():
    if "usuario" in session:
        return render_template("index.html", usuario=session["usuario"])
    return redirect(url_for("login"))

# 🔐 Página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Admin local (do Render)
        if email == SUPER_ADMIN_EMAIL and senha == SUPER_ADMIN_SENHA:
            session["usuario"] = {"email": email, "tipo": "admin"}
            return redirect(url_for("index"))

        # Login via Supabase
        if supabase:
            try:
                data = supabase.auth.sign_in_with_password({"email": email, "password": senha})
                if data.user:
                    session["usuario"] = {"email": email, "tipo": "supabase"}
                    return redirect(url_for("index"))
            except Exception as e:
                print(f"Erro Supabase: {e}")

        return render_template("login.html", erro="Credenciais inválidas!")

    return render_template("login.html")

# 🚪 Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

# 🚀 Inicialização
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
