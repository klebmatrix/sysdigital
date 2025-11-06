# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import bcrypt

# 🔹 Carrega variáveis de ambiente
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Service Role Key
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@exemplo.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "SUA_SENHA")

# 🔹 Inicializa Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# 🔹 Inicializa Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 Cria admin automaticamente se não existir
def create_admin_if_not_exists():
    resp = supabase.table("admin").select("*").eq("email", ADMIN_EMAIL).execute()
    if not resp.data:
        hashed_pw = bcrypt.hashpw(ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()
        supabase.table("admin").insert({
            "email": ADMIN_EMAIL,
            "password": hashed_pw,
            "status_admin": True
        }).execute()
        print("✅ Admin criado:", ADMIN_EMAIL)
    else:
        print("⚡ Admin já existe.")

create_admin_if_not_exists()

# 🔹 Rota login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        resp = supabase.table("admin").select("*").eq("email", email).execute()
        if resp.data:
            user = resp.data[0]
            if bcrypt.checkpw(password.encode(), user["password"].encode()):
                session["user"] = user["email"]
                flash("Login bem-sucedido!", "success")
                return redirect(url_for("dashboard"))
        flash("Credenciais inválidas", "danger")

    return render_template("login.html")

# 🔹 Rota dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"Bem-vindo, {session['user']}! 🎉"

# 🔹 Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# 🔹 Executa app
if __name__ == "__main__":
    app.run(debug=True)
