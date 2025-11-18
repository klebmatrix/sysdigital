from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get("SECRET_KEY", "chave_temporaria")

# A rota principal agora serve o jogo (que será o novo index.html)
@app.route('/')
def index():
    # O jogo não precisa de login, ele é a página principal
    return render_template("index.html")

# Rotas de login, dashboard e logout são removidas, pois não há mais autenticação
# O jogo é a aplicação principal.

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

