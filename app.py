from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="templates")

# Rota principal – Jogo
@app.route("/")
def index():
    return render_template("index.html")

# Rota do Tutor IA
@app.route("/tutor")
def tutor():
    return render_template("tutor.html")

# Health check opcional (ajuda no Render)
@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    # Apenas para ambiente local
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
