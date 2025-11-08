# main.py
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from rotes.professor import verificar_professor
from rotes.aluno import verificar_aluno

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")

# Admin
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin")  # opcional, default "admin"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Login Admin
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session["user_role"] = "admin"
            session["user_email"] = email
            return redirect(url_for("admin_dashboard"))

        # Login Professor
        if verificar_professor(email, password):
            session["user_role"] = "professor"
            session["user_email"] = email
            return redirect(url_for("professor_dashboard"))

        # Login Aluno
        if verificar_aluno(email, password):
            session["user_role"] = "aluno"
            session["user_email"] = email
            return redirect(url_for("aluno_dashboard"))

        flash("Credenciais inválidas!", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")

# Dashboards
@app.route("/admin")
def admin_dashboard():
    if session.get("user_role") != "admin":
        flash("Acesso negado!", "danger")
        return redirect(url_for("login"))
    return render_template("admin.html")

@app.route("/professor")
def professor_dashboard():
    if session.get("user_role") != "professor":
        flash("Acesso negado!", "danger")
        return redirect(url_for("login"))
    return render_template("professor.html")

@app.route("/aluno")
def aluno_dashboard():
    if session.get("user_role") != "aluno":
        flash("Acesso negado!", "danger")
        return redirect(url_for("login"))
    return render_template("aluno.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
