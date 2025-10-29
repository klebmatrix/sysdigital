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
# ROTAS
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
            email_form = request.form['email'].strip()
            senha_form = request.form['senha'].strip()
            funcao_form = request.form.get('funcao', '').strip()

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
# RODAR APP
# -----------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
