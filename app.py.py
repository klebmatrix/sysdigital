from flask import Flask, render_template

app = Flask(__name__)

LEVELS = {
    "facil": {
        "title": "Nível Fácil",
        "description": "Perguntas básicas"
    },
    "medio": {
        "title": "Nível Médio",
        "description": "Perguntas intermediárias"
    },
    "dificil": {
        "title": "Nível Difícil",
        "description": "Perguntas avançadas"
    }
}

@app.route("/")
def index():
    return render_template("index.html", levels=LEVELS.keys())

@app.route("/play/<level>")
def play(level):
    payload = LEVELS.get(level)
    if not payload:
        return "Level not found", 404
    return render_template("index.html", payload=payload)

if __name__ == "__main__":
    app.run(debug=True)

