import os
import io
import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from supabase import create_client, Client
from dotenv import load_dotenv

# -----------------------------------------------------------
# CONFIGURAÇÃO GERAL
# -----------------------------------------------------------

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "chave-secreta-padrao")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_SENHA = os.getenv("SUPER_ADMIN_SENHA")

supabase: Client | None = None
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Conexão Supabase estabelecida com sucesso.")
    else:
        print("⚠️ Supabase não configurada. Variáveis de ambiente ausentes.")
except Exception as e:
    print(f"❌ Erro ao conectar ao Supabase: {e}")

# -----------------------------------------------------------
# LOGIN E AUTENTICAÇÃO
# -----------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    if 'user' in session:
        return redirect(url_for('menu'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip().lower()
    senha = request.form.get('password', '').strip()

    if not email or not senha:
        return render_template('login.html', error="E-mail e senha são obrigatórios.")

    # ---- LOGIN DO ADMINISTRADOR ----
    if email == SUPER_ADMIN_EMAIL and senha == SUPER_ADMIN_SENHA:
        session['user'] = {
            "email": email,
            "role": "admin"
        }
        print("👑 Login de administrador bem-sucedido.")
        return redirect(url_for('menu'))

    # ---- LOGIN NORMAL VIA SUPABASE ----
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": senha})
        if response.user:
            session['user'] = {
                "email": email,
                "id": response.user.id,
                "role": "user"
            }
            print(f"✅ Login Supabase bem-sucedido: {email}")
            return redirect(url_for('menu'))
        else:
            return render_template('login.html', error="E-mail ou senha incorretos.")
    except Exception as e:
        print("Erro Supabase:", e)
        return render_template('login.html', error="Erro ao autenticar. Verifique suas credenciais.")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# -----------------------------------------------------------
# ROTAS PROTEGIDAS
# -----------------------------------------------------------

@app.route('/menu')
def menu():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('menu.html', user=session['user'])


@app.route('/simulador_atividade')
def simulador_atividade():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('index.html', user=session['user'])

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
        return jsonify({"success": False, "error": str(e)})

# -----------------------------------------------------------
# RODAR APP
# -----------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
