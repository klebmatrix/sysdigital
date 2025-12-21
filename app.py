from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# Banco de relações por nível
LEVELS = {
    "facil": {
        "name": "Fácil",
        "entities": ["Josh", "Linda", "Andrew", "Ben"],
        "relations": [
            {"pair": ["Linda", "Josh"], "text": "Linda is Josh's mother"},
            {"pair": ["Andrew", "Josh"], "text": "Andrew is Josh's father"},
            {"pair": ["Ben", "Josh"], "text": "Ben is Josh's brother"}
        ]
    },
    "medio": {
        "name": "Médio",
        "entities": ["Alice", "Josh", "Carol", "Eve", "Frank", "George"],
        "relations": [
            {"pair": ["Alice", "Josh"], "text": "Alice is Josh's teacher"},
            {"pair": ["Carol", "Josh"], "text": "Carol is Josh's mentor"},
            {"pair": ["Eve", "Frank"], "text": "Eve is Frank's manager"},
            {"pair": ["George", "Eve"], "text": "George is Eve's colleague"}
        ]
    },
    "dificil": {
        "name": "Difícil",
        "entities": ["John", "Mary", "Lucy", "Sara", "Tom", "Olivia", "Sophia", "Mia"],
        "relations": [
            {"pair": ["Lucy", "Sara"], "text": "Lucy is Sara's friend"},
            {"pair": ["Tom", "Olivia"], "text": "Tom is Olivia's friend"},
            {"pair": ["Sophia", "Mia"], "text": "Sophia is Mia's mother"},
            {"pair": ["John", "Mary"], "text": "John is Mary's husband"}
        ]
    }
}


@app.route("/")
def index():
    return render_template("index.html", levels=list(LEVELS.keys()))


@app.route("/play/<level>")
def play(level):
    payload = LEVELS.get(level)
    if not payload:
        return "Level not found", 404
    return render_template("game.html", payload=payload)


if __name__ == "__main__":
    app.run(debug=True)
