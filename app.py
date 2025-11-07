
from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['POST'])  # Só aceita POST
def login():
    data = request.form
    return f"Usuário: {data['username']}"

# Rota da página de login
@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    # debug=True para ver erros na hora
    app.run(host="0.0.0.0", port=5000, debug=True)

