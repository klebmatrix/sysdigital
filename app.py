import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return {
        "cwd": os.getcwd(),
        "files": os.listdir("."),
        "templates_exists": os.path.exists("templates"),
        "templates_files": os.listdir("templates") if os.path.exists("templates") else "NAO EXISTE"
    }
