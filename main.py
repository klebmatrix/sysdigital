import os
import io
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from supabase import create_client, Client
from dotenv import load_dotenv

# -----------------------------------------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------------------------------------

load_dotenv()  # Render já injeta as variáveis de ambiente automaticamente

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave-padrao-secreta")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase conectada com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao conectar Supabase: {e}")
else:
    print("⚠️ Supabase não configurada. Variáveis de ambiente ausentes.")

# Admin do sistema
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL", "")
SUPER_ADMIN_SENHA = os.getenv("SUPER_ADMIN_SENHA", "")

# Banco de professores (simulado em memória)
PROFESSORES_DB = {}

# -----------------------------------------------------------
# ROTA DE LOGIN
# -----------------------------------------------------------

@app.route('/')
def index():
    # Redireciona direto para o login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('password', '').strip()

        # Validação simples do admin
        if email == SUPER_ADMIN_EMAIL.lower() and senha == SUPER_ADMIN_SENHA:
            session['usuario'] = email
            return redirect(url_for('painel'))

        return render_template('login.html', error="Credenciais inválidas.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -----------------------------------------------------------
# ROTA PAINEL (somente logado)
# -----------------------------------------------------------

@app.route('/painel')
def painel():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('painel.html', usuario=session['usuario'])

# -----------------------------------------------------------
# API DE GERENCIAMENTO DE PROFESSORES
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
# GERAR PDF
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
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------------------------------------
# INICIALIZAÇÃO
# -----------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
