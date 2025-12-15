from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do .env (se houver)
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # Roda localmente
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
