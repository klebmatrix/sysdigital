import os
import datetime
import io
import traceback
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Importa o cliente Supabase e as constantes das tabelas
from supabase_client import (
    get_supabase_client,
    ADMINS_TABLE,
    PROFESSORES_TABLE,
    ALUNOS_TABLE,
    ATIVIDADES_TABLE,
    RESPOSTAS_TABLE,
    GAME_LEVELS_TABLE
)

# Inicializa o cliente Supabase
supabase = get_supabase_client()

# -----------------------------------------------------------
# CONFIGURAÇÃO DO APP
# -----------------------------------------------------------

SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_fallback_insegura_insegura_para_desenvolvimento')
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = SECRET_KEY

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
# ROTAS PRINCIPAIS E DE AUTENTICAÇÃO
# -----------------------------------------------------------

@app.route('/')
def home():
    try:
        if 'logged_in' in session and session['logged_in']:
            role = session.get('user_role')
            if role == ADMIN_ROLE_RENDER:
                return redirect(url_for('admin'))
            elif role == 'Professor':
                return redirect(url_for('professor'))
            # Adicionar redirecionamento para aluno se houver um dashboard específico
            return render_template('mensagem_generica.html', role=role)
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

            if not email_raw or not senha_raw or not funcao_raw:
                error = 'E-mail, senha e função são obrigatórios.'
            else:
                email_form = email_raw.strip()
                senha_form = senha_raw.strip()
                funcao_form = funcao_raw.strip()
                
                if not supabase:
                    return render_error_debug('Cliente Supabase não inicializado.')
                
                user_data = None
                role = None

                if funcao_form == ADMIN_ROLE_RENDER:
                    response = supabase.table(ADMINS_TABLE).select("*").eq("email", email_form).eq("senha", senha_form).execute()
                    if response.data:
                        user_data = response.data[0]
                        role = ADMIN_ROLE_RENDER
                elif funcao_form == 'Professor':
                    response = supabase.table(PROFESSORES_TABLE).select("*").eq("email", email_form).eq("senha_inicial", senha_form).execute()
                    if response.data:
                        user_data = response.data[0]
                        role = 'Professor'
                # Adicionar lógica para login de aluno aqui se necessário

                if user_data and role:
                    session['logged_in'] = True
                    session['user_email'] = user_data['email']
                    session['user_role'] = role
                    if role == ADMIN_ROLE_RENDER:
                        return redirect(url_for('admin'))
                    elif role == 'Professor':
                        return redirect(url_for('professor'))
                else:
                    error = 'Credenciais ou função inválidas.'

        return render_template('login.html', error=error, ADMIN_ROLE_RENDER=ADMIN_ROLE_RENDER)
    except Exception as e:
        return render_error_debug(e)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -----------------------------------------------------------
# DASHBOARDS
# -----------------------------------------------------------

@app.route('/admin')
def admin():
    if not session.get('logged_in') or session.get('user_role') != ADMIN_ROLE_RENDER:
        return redirect(url_for('login'))
    try:
        professores_data = supabase.table(PROFESSORES_TABLE).select("*").execute().data or []
        alunos_data = supabase.table(ALUNOS_TABLE).select("*").execute().data or []
        return render_template('admin.html', professores_dados=professores_data, alunos_dados=alunos_data)
    except Exception as e:
        return render_error_debug(e)

@app.route('/professor')
def professor():
    if not session.get('logged_in') or session.get('user_role') != 'Professor':
        return redirect(url_for('login'))
    try:
        # Adicionar lógica para carregar dados específicos do professor se necessário
        return render_template('professor.html')
    except Exception as e:
        return render_error_debug(e)

# -----------------------------------------------------------
# ROTAS DE API DE GERENCIAMENTO (CRUD)
# -----------------------------------------------------------

# --- Professores ---
@app.route('/api/cadastrar_professor', methods=['POST'])
def cadastrar_professor():
    if not session.get('logged_in') or session.get('user_role') != ADMIN_ROLE_RENDER:
        return jsonify({"success": False, "message": "Acesso não autorizado."}), 403
    try:
        data = request.get_json()
        email = data.get('email')
        senha_inicial = data.get('senha_inicial')
        expira_em = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()
        
        response = supabase.table(PROFESSORES_TABLE).insert({
            "email": email,
            "senha_inicial": senha_inicial,
            "expira_em": expira_em
        }).execute()

        if response.data:
            return jsonify({"success": True, "message": "Professor cadastrado com sucesso!", "data": response.data[0]})
        return jsonify({"success": False, "message": "Erro ao cadastrar professor."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# --- Alunos ---
@app.route('/api/cadastrar_aluno', methods=['POST'])
def cadastrar_aluno():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Acesso não autorizado."}), 403
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')
        turma = data.get('turma')
        professor_email = session.get('user_email') # Professor logado

        response = supabase.table(ALUNOS_TABLE).insert({
            "email": email,
            "senha": senha,
            "turma": turma,
            "professor_email": professor_email
        }).execute()

        if response.data:
            return jsonify({"success": True, "message": "Aluno cadastrado com sucesso!", "data": response.data[0]})
        return jsonify({"success": False, "message": "Erro ao cadastrar aluno."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# -----------------------------------------------------------
# ROTAS DE API DE ATIVIDADES
# -----------------------------------------------------------

@app.route('/api/atividades', methods=['POST'])
def criar_atividade():
    if not session.get('logged_in') or session.get('user_role') != 'Professor':
        return jsonify({"success": False, "message": "Acesso não autorizado."}), 403
    try:
        data = request.get_json()
        professor_email = session.get('user_email')
        
        response = supabase.table(ATIVIDADES_TABLE).insert({
            "titulo": data.get('titulo'),
            "tipo": data.get('tipo'),
            "gabarito": data.get('gabarito'),
            "professor_email": professor_email
        }).execute()

        if response.data:
            return jsonify({"success": True, "message": "Atividade criada com sucesso!", "data": response.data[0]})
        return jsonify({"success": False, "message": "Erro ao criar atividade."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/atividades/<int:atividade_id>/respostas', methods=['POST'])
def enviar_resposta(atividade_id):
    # Assumindo que o aluno está logado
    if not session.get('logged_in'):
         return jsonify({"success": False, "message": "Acesso não autorizado."}), 403
    try:
        data = request.get_json()
        aluno_email = session.get('user_email') # Simulação, idealmente o aluno teria sua própria sessão

        response = supabase.table(RESPOSTAS_TABLE).insert({
            "atividade_id": atividade_id,
            "aluno_email": aluno_email,
            "resposta": data.get('resposta')
        }).execute()

        if response.data:
            return jsonify({"success": True, "message": "Resposta enviada com sucesso!"})
        return jsonify({"success": False, "message": "Erro ao enviar resposta."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# -----------------------------------------------------------
# ROTAS DO NEUROGAME E SIMULADOR
# -----------------------------------------------------------

@app.route('/menu')
def menu():
    try:
        levels = supabase.table(GAME_LEVELS_TABLE).select("key, name").execute().data or []
        return render_template('menu.html', levels=levels)
    except Exception as e:
        return render_error_debug(e)

@app.route('/game/<level_key>')
def game(level_key):
    try:
        level_data = supabase.table(GAME_LEVELS_TABLE).select("*").eq("key", level_key).single().execute().data
        if not level_data:
            return "Nível não encontrado", 404
        return render_template('game.html', level=level_data)
    except Exception as e:
        return render_error_debug(e)

@app.route('/simulador_atividade')
def simulador_atividade():
    return render_template('index.html')

# -----------------------------------------------------------
# ROTA DE GERAÇÃO DE PDF (Exemplo)
# -----------------------------------------------------------

@app.route('/api/gerar_pdf_atividade', methods=['POST'])
def gerar_pdf_atividade():
    try:
        data = request.get_json()
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Relatório de Atividade", styles['h1']))
        story.append(Spacer(1, 12))

        # Adiciona os dados da atividade ao PDF
        story.append(Paragraph(f"<b>Título:</b> {data.get('titulo', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Instruções:</b> {data.get('instrucoes', 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 12))

        doc.build(story)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='atividade.pdf', mimetype='application/pdf')
    except Exception as e:
        return render_error_debug(e)

# -----------------------------------------------------------
# EXECUÇÃO DO APP
# -----------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

