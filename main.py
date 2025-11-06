import os
import datetime
import string
import random
import io
import traceback
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------------------------------------
# SIMULAÇÃO DE BANCO DE DADOS
# -----------------------------------------------------------

PROFESSORES_DB = {
    "professor.teste@escola.com": {"expira_em": "2025-12-31"},
    "professor.ativo@escola.com": {"expira_em": "2026-06-30"},
    "professor.expirado@escola.com": {"expira_em": "2024-01-01"},
}

ALUNOS_DB = {
    "aluno.teste@escola.com": {"turma": "5A", "professor": "professor.ativo@escola.com"},
    "aluno.novo@escola.com": {"turma": "6B", "professor": "professor.teste@escola.com"},
    "aluno.excluir@escola.com": {"turma": "9C", "professor": "professor.ativo@escola.com"},
}

# -----------------------------------------------------------
# CONFIGURAÇÃO DO APP
# -----------------------------------------------------------

SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_fallback_insegura')
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = SECRET_KEY

ADMIN_EMAIL_RENDER = os.environ.get('SUPER_ADMIN_EMAIL')
ADMIN_SENHA_RENDER = os.environ.get('SUPER_ADMIN_SENHA')
ADMIN_ROLE_RENDER = 'Administrador'

# -----------------------------------------------------------
# FUNÇÃO DE DEBUG PARA ERROS
# -----------------------------------------------------------

def render_error_debug(e):
    """Renderiza uma página com o traceback completo."""
    tb = traceback.format_exc()
    return f"""
    <h1>Erro Interno do Servidor (500)</h1>
    <h3>{str(e)}</h3>
    <pre>{tb}</pre>
    """, 500

# -----------------------------------------------------------
# ROTAS PRINCIPAIS
# -----------------------------------------------------------

@app.route('/')
def home():
    try:
        if 'logged_in' in session and session['logged_in']:
            role = session.get('user_role')
            if role == ADMIN_ROLE_RENDER:
                return redirect(url_for('admin_dashboard'))
            return render_template('mensagem_generica.html', role=role)
        return redirect(url_for('login'))
    except Exception as e:
        return render_error_debug(e)

@app.route('/admin_dashboard')
def admin_dashboard():
    try:
        if 'logged_in' in session and session['logged_in'] and session.get('user_role') == ADMIN_ROLE_RENDER:
            hoje = datetime.date.today().isoformat()
            return render_template('admin_dashboard.html',
                                   professores_dados=PROFESSORES_DB,
                                   alunos_dados=ALUNOS_DB,
                                   hoje=hoje,
                                   PROFESSOR_EMAIL_PADRAO="professor.teste@escola.com")
        return redirect(url_for('login'))
    except Exception as e:
        return render_error_debug(e)

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        error = None
        if request.method == 'POST':
            email_raw = request.form.get('email')
            senha_raw = request.form.get('senha')
            funcao_raw = request.form.get('funcao')

            if not email_raw or not senha_raw:
                error = 'E-mail e senha são obrigatórios.'
            else:
                email_form = email_raw.strip()
                senha_form = senha_raw.strip()
                funcao_form = funcao_raw.strip() if funcao_raw else ''
                
                if ADMIN_EMAIL_RENDER is None or ADMIN_SENHA_RENDER is None:
                    error = 'Erro interno: Credenciais Admin não encontradas no servidor.'
                elif email_form == ADMIN_EMAIL_RENDER and senha_form == ADMIN_SENHA_RENDER:
                    if funcao_form != ADMIN_ROLE_RENDER:
                        error = f'Função inválida. Use "{ADMIN_ROLE_RENDER}".'
                    else:
                        session['logged_in'] = True
                        session['user_email'] = email_form
                        session['user_role'] = funcao_form
                        return redirect(url_for('admin_dashboard'))
                else:
                    error = 'E-mail, senha ou função inválidos.'

        return render_template('login_uni.html',
                               error=error,
                               ADMIN_ROLE_RENDER=ADMIN_ROLE_RENDER,
                               debug_env_url=url_for('debug_env'))
    except Exception as e:
        return render_error_debug(e)

@app.route('/debug_credenciais_critico')
def debug_env():
    """ROTA REINSERIDA: Para verificar se as variáveis de ambiente críticas estão sendo lidas."""
    try:
        if ADMIN_EMAIL_RENDER is None or ADMIN_SENHA_RENDER is None:
            return "<h1>FALHA CRÍTICA:</h1><p>Variáveis não lidas no ambiente Render.</p>"
        else:
            return f"<h1>OK:</h1><p>SUPER_ADMIN_EMAIL={ADMIN_EMAIL_RENDER}</p>"
    except Exception as e:
        return render_error_debug(e)

@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('login'))
    except Exception as e:
        return render_error_debug(e)

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
	
	    # Simula o cadastro com expiração em 1 ano e armazena a senha inicial
	    nova_expiracao = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()
	    # ATENÇÃO: Em um sistema real, a senha NUNCA deve ser armazenada em texto puro.
	    # Aqui, estamos simulando o armazenamento para fins de demonstração.
	    PROFESSORES_DB[email] = {
	        "expira_em": nova_expiracao,
	        "senha_inicial": senha_inicial # Armazena a senha inicial
	    }
	    
	    return jsonify({
	        "success": True, 
	        "message": f"Professor {email} cadastrado com sucesso. Expira em {nova_expiracao}. Senha inicial: {senha_inicial}",
	        "email": email,
	        "professor_info": PROFESSORES_DB[email]
	    })

@app.route('/api/renovar_professor', methods=['POST'])
def renovar_professor():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email or email not in PROFESSORES_DB:
        return jsonify({"success": False, "message": f"Professor {email} não encontrado para renovação."}), 404

    # Simula a renovação por mais 1 ano a partir de hoje
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

    # Simula a exclusão do DB
    del PROFESSORES_DB[email]
    
    return jsonify({
        "success": True, 
        "message": f"Professor {email} e dados associados excluídos com sucesso.",
        "email": email
    })

# -----------------------------------------------------------
# EXEMPLO DE API (PDF)
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
        story = [Paragraph(f"<b>{titulo}</b>", styles['Title']),
                 Paragraph(f"<b>Turma:</b> {turma}", styles['Normal']),
                 Paragraph("<b>Instruções:</b>", styles['Heading3']),
                 Paragraph(instrucoes, styles['Normal']),
                 Spacer(1, 20)]
        for i, p in enumerate(perguntas, 1):
            story.append(Paragraph(f"{i}. {p.get('texto', '')}", styles['Normal']))
        doc.build(story)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"{titulo}.pdf", mimetype='application/pdf')
    except Exception as e:
        return render_error_debug(e)

	# -----------------------------------------------------------
	# ROTAS DO NEUROGAME
	# -----------------------------------------------------------
	
# Carrega os níveis do jogo do Supabase
		def get_game_levels():
		    if not supabase:
		        return {}
		    
		    response = supabase.table(GAME_LEVELS_TABLE).select("*").execute()
		    
		    # Converte a lista de dicionários em um dicionário com 'key' como chave
		    levels = {item['key']: item for item in response.data}
		    return levels
		
		GAME_LEVELS = get_game_levels() # Carrega os níveis na inicialização do app
	
@app.route('/menu')
		def menu():
		    """Exibe o menu de seleção de níveis do jogo."""
		    # Recarrega os níveis para garantir que estão atualizados
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