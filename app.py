from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import datetime

app = Flask(__name__, template_folder='backend/templates', static_folder='backend/static')
CORS(app)

# -----------------------------------------------------------
# ROTA PRINCIPAL
# -----------------------------------------------------------
@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


# Banco de dados simulado
PROFESSORES_DB = {}
supabase = None
GAME_LEVELS_TABLE = "game_levels"

# -----------------------------------------------------------
# ROTAS DE API DE GERENCIAMENTO DE PROFESSORES
# -----------------------------------------------------------
@app.route('/api/cadastrar_professor', methods=['POST'])
def cadastrar_professor():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    senha_inicial = data.get('senha_inicial', '').strip()
    
    if not email:
        return jsonify({"success": False, "message": "E-mail não fornecido."}), 400

    if not senha_inicial or len(senha_inicial) < 6:
        return jsonify({"success": False, "message": "Senha inicial deve ter no mínimo 6 caracteres."}), 400

    if email in PROFESSORES_DB:
        return jsonify({"success": False, "message": f"Professor {email} já está cadastrado."}), 409

    nova_expiracao = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()
    PROFESSORES_DB[email] = {
        "expira_em": nova_expiracao,
        "senha_inicial": senha_inicial
    }
    
    return jsonify({
        "success": True, 
        "message": f"Professor {email} cadastrado com sucesso. Expira em {nova_expiracao}.",
        "email": email,
        "professor_info": PROFESSORES_DB[email]
    })


# -----------------------------------------------------------
# ROTAS DO NEUROGAME
# -----------------------------------------------------------
def get_game_levels():
    if not supabase:
        return {}
    response = supabase.table(GAME_LEVELS_TABLE).select("*").execute()
    levels = {item['key']: item for item in response.data}
    return levels

GAME_LEVELS = get_game_levels()

@app.route('/menu')
def menu():
    global GAME_LEVELS
    GAME_LEVELS = get_game_levels()
    
    levels_list = [
        {"name": data["name"], "key": key, "count": len(data["relations"])}
        for key, data in GAME_LEVELS.items()
    ]
    return render_template('menu.html', levels=levels_list)


@app.route('/game/<level_key>')
def game(level_key):
    if level_key not in GAME_LEVELS:
        return redirect(url_for('menu'))

    payload = GAME_LEVELS[level_key]
    return render_template('game.html', payload=payload)


@app.route('/simulador_atividade')
def simulador_atividade():
    return render_template('index.html')


# -----------------------------------------------------------
# EXECUÇÃO LOCAL
# -----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
