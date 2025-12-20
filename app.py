from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", levels=list(LEVELS.keys()))


@app.route("/play/<level>")
def play(level):
    payload = LEVELS.get(level)
    if not payload:
        return "Level not found", 404
    return render_template("index.html", payload=payload)


if __name__ == "__main__":
    app.run(debug=True)
