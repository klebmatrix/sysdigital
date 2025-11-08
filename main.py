# -----------------------------------------------------------
# main.py — Flask + Supabase + Gerenciamento de Professores + PDF + Neurogame
# -----------------------------------------------------------

import io
import os
import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from supabase import create_client, Client

# -----------------------------------------------------------
# CONFIGURAÇÃO DO APP
# -----------------------------------------------------------

app = Flask(__name__)  # ← ESTA LINHA PRECISA VIR ANTES DAS ROTAS

# Banco temporário em memória (para testes)
PROFESSORES_DB = {}

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
    print("⚠️ Supabase não configurado. Variáveis de ambiente ausentes.")

GAME_LEVELS_TABLE = "game_levels"


# -----------------------------------------------------------
# FUNÇÃO DE ERRO
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
# FUNÇÕES DO NEUROGAME
# -----------------------------------------------------------

def get_game_levels():
    if not supabase:
        return {}
    try:
        response = supabase.table(GAME_LEVELS_TABLE).select("*").execute()
        levels = {item['key']: item for item in response.data}
        return levels
    except Exception as e:
        print("Erro ao carregar níveis do jogo:", e)
        return {}


@app.route('/menu')
def menu():
    levels = get_game_levels()
    levels_list = [
        {"name": data["name"], "key": key, "count": len(data.get("relations", []))}
        for key, data in levels.items()
    ]
    return render_template('menu.html', levels=levels_list)


@app.route('/game/<level_key>')
def game(level_key):
    levels = get_game_levels()
    if level_key not in levels:
        return redirect(url_for('menu'))
    payload = levels[level_key]
    return render_template('game.html', payload=payload)


@app.route('/simulador_atividade')
def simulador_atividade():
    return render_template('index.html')


# -----------------------------------------------------------
# RODAR APP
# -----------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
