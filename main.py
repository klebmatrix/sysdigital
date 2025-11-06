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

    # Simula o cadastro com expiração em 1 ano
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
    """Exibe o menu de seleção de níveis do jogo."""
    global GAME_LEVELS
    GAME_LEVELS = get_game_levels()
    
    levels_list = [
        {"name": data["name"], "key": key, "count": len(data["relations"])}
        for key, data in GAME_LEVELS.items()
    ]
    return render_template('menu.html', levels=levels_list)


@app.route('/game/<level_key>')
def game(level_key):
    """Exibe a tela do jogo para o nível selecionado."""
    if level_key not in GAME_LEVELS:
        return redirect(url_for('menu'))

    payload = GAME_LEVELS[level_key]
    return render_template('game.html', payload=payload)


@app.route('/simulador_atividade')
def simulador_atividade():
    """Exibe o simulador de atividade (index.html)."""
    return render_template('index.html')


# -----------------------------------------------------------
# RODAR APP
# -----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
