from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="templates")

@app.route("/")   # rota raiz
def home():
    return render_template("index.html")

@app.route("/tutor")
def tutor():
    return render_template("tutor.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
