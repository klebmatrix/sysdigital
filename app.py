from flask import Flask, render_template

app = Flask(__name__)

# Rota da página inicial
@app.route("/")
def index():
    # Renderiza index.html, que pode incluir login.html
    return render_template("index.html")

# Rota da página de login
@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    # debug=True para ver erros na hora
    app.run(host="0.0.0.0", port=5000, debug=True)
