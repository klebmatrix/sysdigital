import io
import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------------------------------------
# INICIALIZAÇÃO DO APP
# -----------------------------------------------------------

app = Flask(__name__)

# Banco de dados simples em memória
PROFESSORES_DB = {}

# Banco local de níveis do jogo (mock)
GAME_LEVELS = {
    "algebra": {"name": "Álgebra", "relations": ["expressões", "equações"]},
    "geometria": {"name": "Geometria", "relations": ["ângulos", "áreas"]},
    "calculo": {"name": "Cálculo", "relations": ["limites", "derivadas"]}
}

# -----------------------------------------------------------
# FUNÇÃO DE ERRO PADRÃO
# -----------------------------------------------------------

def render_error_debug(e):
    return jsonify({"success": False, "error": str(e)}), 500


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


@app.route('/api/renovar_professor', methods=['POST'])
def renovar_professor():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email or email not in PROFESSORES_DB:
        return jsonify({"success": False, "message": f"Professor {email} não encontrado para renovação."}), 404

    nova_expiracao = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()
    PROFESSORES_DB[email]["expira_em"] = nova_expiracao
    
    return jsonify({
        "success": True, 
        "message": f"Licença de {email} renovada com sucesso. Nova expiração: {nova_expiracao}.",
        "email": email,
        "nova_data": nova_expiracao
    })


@app.route('/api/excluir_professor', methods=['POST'])
def excluir_professor():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email or email not in PROFESSORES_DB:
        return jsonify({"success": False, "message": f"Professor {email} não encontrado para exclusão."}), 404

    del PROFESSORES_DB[email]
    
    return jsonify({
        "success": True, 
        "message": f"Professor {email} e dados associados excluídos com sucesso.",
        "email": email
    })


# -----------------------------------------------------------
# API PARA GERAR PDF DE ATIVIDADE
# -----------------------------------------------------------

@app.route('/api/gerar_pdf_atividade', methods=['POST'])
def gerar_pdf_atividade():
    try:
        data = request.get_json()
        titulo = data.get('titulo', 'Atividade')
        turma = data.get('turma', 'Geral')
        instrucoes = data.get('instrucoes', '')
        perguntas = data.get('perguntas', [])

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [
            Paragraph(f"<b>{titulo}</b>", styles['Title']),
            Paragraph(f"<b>Turma:</b> {turma}", styles['Normal']),
            Paragraph("<b>Instruções:</b>", styles['Heading3']),
            Paragraph(instrucoes, styles['Normal']),
            Spacer(1, 20)
        ]
        for i, p in enumerate(perguntas, 1):
            story.append(Paragraph(f"{i}. {p.get('texto', '')}", styles['Normal']))
        doc.build(story)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"{titulo}.pdf", mimetype='application/pdf')
    except Exception as e:
        return render_error_debug(e)


# -----------------------------------------------------------
# ROTAS DO NEUROGAME (LOCAL)
# -----------------------------------------------------------

@app.route('/menu')
def menu():
    levels_list = [
        {"name": data["name"], "key": key, "count": len(data.get("relations", []))}
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
# ROTA PRINCIPAL
# -----------------------------------------------------------

@app.route('/')
def index():
    return "✅ App Flask rodando corretamente no Render (modo local, sem Supabase)."


# -----------------------------------------------------------
# EXECUTAR APLICAÇÃO
# -----------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
