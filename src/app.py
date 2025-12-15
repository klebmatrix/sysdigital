from flask import Flask, render_template
import os

# Aqui diz explicitamente que os templates estão em src/templates
app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tutor")
def tutor():
    return render_template("tutor.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
