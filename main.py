import os
import io
import datetime # Adicionado para uso no admin_dashboard
from flask import Flask, request, redirect, url_for, render_template_string, session, jsonify, send_file
# Imports para ReportLab (PDF generation)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# =====================================================================
# 1. Configuração da Aplicação e Credenciais
# =====================================================================

# Lê a chave secreta do ambiente Render.
SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_de_fallback_insegura_nao_use')
if SECRET_KEY == 'chave_de_fallback_insegura_nao_use':
    # Este print aparece nos logs do Render
    print("ALERTA CRÍTICO: SECRET_KEY NÃO CONFIGURADA NO RENDER. Usando fallback.")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Credenciais Lidas do Render
ADMIN_EMAIL_RENDER = os.environ.get('SUPER_ADMIN_EMAIL')
ADMIN_SENHA_RENDER = os.environ.get('SUPER_ADMIN_SENHA')
ADMIN_ROLE_RENDER = 'Administrador' # Função esperada

# MOCK DATABASE para rotas de API (Em um sistema real, seria o Firestore/Firebase Admin SDK)
alunos_db = {
    "aluno.teste@escola.com": {'turma': '5A', 'professor': 'professor.ativo@escola.com', 'senha': '123'},
}

# =====================================================================
# 2. Rota de Debug (APENAS PARA VERIFICAR VARIÁVEIS DE AMBIENTE)
# =====================================================================

@app.route('/debug_credenciais_critico')
def debug_env():
    # NUNCA DEIXE ESTA ROTA EM PRODUÇÃO! Use apenas para depurar.
    if ADMIN_EMAIL_RENDER is None or ADMIN_SENHA_RENDER is None:
        return """
            <h1>FALHA CRÍTICA: Variáveis de ambiente ausentes!</h1>
            <p>O Render NÃO está lendo SUPER_ADMIN_EMAIL ou SUPER_ADMIN_SENHA.</p>
            <p>Verifique o Render Dashboard: As chaves DEVEM estar lá e serem idênticas.</p>
            <p>Valor de SUPER_ADMIN_EMAIL: {}</p>
            <p>Valor de SUPER_ADMIN_SENHA: {}</p>
        """.format(ADMIN_EMAIL_RENDER, ADMIN_SENHA_RENDER)
    else:
        return f"""
            <h1>STATUS: VARIÁVEIS LENDO CORRETAMENTE</h1>
            <p>O sistema leu o E-MAIL e a SENHA do Render com sucesso.</p>
            <p>E-mail Lido: {ADMIN_EMAIL_RENDER}</p>
            <p>Senha Lido: {ADMIN_SENHA_RENDER}</p>
        """


# =====================================================================
# 3. Rotas Web (HTML e Lógica)
# =====================================================================

@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        role = session.get('user_role')
        
        if role == ADMIN_ROLE_RENDER:
            return redirect(url_for('admin_dashboard'))
        
        # Fallback para outros roles (Professor/Aluno)
        return render_template_string(f"""
            <style>body{{font-family: sans-serif; background-color: #f0f4f8; padding: 20px;}} .card {{background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}}</style>
            <div class="card">
                <h1>Bem-vindo, {session.get('user_role', 'Usuário')}!</h1>
                <p>Use o link de login correto para acessar seu painel.</p>
                <a href="{url_for('logout')}" style="color: blue;">Sair</a>
            </div>
        """)
    return redirect(url_for('login'))

@app.route('/admin_dashboard')
def admin_dashboard():
    # Verifica se o usuário está logado e é administrador
    if 'logged_in' in session and session['logged_in'] and session.get('user_role') == ADMIN_ROLE_RENDER:
        
        # Simulação de dados de professores (em um sistema real, viria do DB)
        professores_dados = {
            "professor.teste@escola.com": {"expira_em": "2025-12-31"},
            "professor.ativo@escola.com": {"expira_em": "2026-06-30"},
            "professor.expirado@escola.com": {"expira_em": "2024-01-01"},
        }
        
        # Simulação de dados de alunos (em um sistema real, viria do DB)
        alunos_dados = {
            "aluno.teste@escola.com": {"turma": "5A", "professor": "professor.ativo@escola.com"},
            "aluno.novo@escola.com": {"turma": "6B", "professor": "professor.teste@escola.com"},
        }
        
        # Data de hoje para comparação no JS
        hoje = datetime.date.today().isoformat()
        
        # Renderiza o HTML do dashboard do administrador, passando os dados
        try:
            with open('admin_dashboard.html', 'r', encoding='utf-8') as f:
                admin_html = f.read()
                # Substitui as variáveis Jinja2 no HTML
                return render_template_string(admin_html, 
                                              professores_dados=professores_dados, 
                                              alunos_dados=alunos_dados,
                                              hoje=hoje,
                                              PROFESSOR_EMAIL_PADRAO="professor.teste@escola.com")
        except FileNotFoundError:
            return "Erro: O arquivo 'admin_dashboard.html' não foi encontrado no servidor.", 500

    # Se não for admin ou não estiver logado, redireciona para o login
    return redirect(url_for('login'))

# --- Rotas de API (Administrador) ---

@app.route('/api/cadastrar_professor', methods=['POST'])
def cadastrar_professor():
    data = request.get_json()
    email = data.get('email', '').lower()
    senha = data.get('senha')

    # Simulação de retorno de sucesso
    return jsonify({'success': True, 'message': 'Professor cadastrado com sucesso!', 'professor_info': {'expira_em': '2026-12-31'}, 'generated_password': 'nova_senha_gerada'})

@app.route('/api/renovar_professor', methods=['POST'])
def renovar_professor():
    # Simulação de retorno de sucesso
    return jsonify({'success': True, 'message': 'Licença renovada com sucesso!', 'nova_data': '2027-12-31'})

@app.route('/api/trocar_senha_professor', methods=['POST'])
def trocar_senha_professor():
    # Simulação de retorno de sucesso
    return jsonify({'success': True, 'message': 'Senha alterada com sucesso!'})

@app.route('/api/excluir_professor', methods=['POST'])
def excluir_professor():
    # Simulação de retorno de sucesso
    return jsonify({'success': True, 'message': 'Professor excluído com sucesso!'})

# --- Rotas de Gerenciamento de Alunos (Administrador) ---

@app.route('/api/cadastrar_aluno', methods=['POST'])
def cadastrar_aluno():
    data = request.get_json()
    email = data.get('email', '').lower()
    senha = data.get('senha')
    turma = data.get('turma')

    if not email or not turma:
        return jsonify({'success': False, 'message': 'E-mail e Turma são obrigatórios.'}), 400

    generated_password = None
    if not senha:
        import string
        import random
        generated_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        senha = generated_password

    global alunos_db
    if email in alunos_db:
        return jsonify({'success': False, 'message': f'Aluno com e-mail {email} já cadastrado.'}), 409

    alunos_db[email] = {
        'turma': turma,
        'professor': 'admin@escola.com', 
        'senha': senha
    }

    response = {
        'success': True,
        'message': f'Aluno {email} da turma {turma} cadastrado com sucesso!',
        'aluno_info': {'turma': turma, 'professor': 'admin@escola.com'},
        'generated_password': generated_password
    }
    return jsonify(response)

@app.route('/api/trocar_senha_aluno', methods=['POST'])
def trocar_senha_aluno():
    data = request.get_json()
    email = data.get('email', '').lower()
    nova_senha = data.get('nova_senha')

    if not email or not nova_senha:
        return jsonify({'success': False, 'message': 'E-mail e nova senha são obrigatórios.'}), 400

    global alunos_db
    if email not in alunos_db:
        return jsonify({'success': False, 'message': 'Aluno não encontrado.'}), 404

    alunos_db[email]['senha'] = nova_senha

    return jsonify({'success': True, 'message': f'Senha do aluno {email} alterada com sucesso!'})

@app.route('/api/excluir_aluno', methods=['POST'])
def excluir_aluno():
    data = request.get_json()
    email = data.get('email', '').lower()

    if not email:
        return jsonify({'success': False, 'message': 'E-mail é obrigatório.'}), 400

    global alunos_db
    if email not in alunos_db:
        return jsonify({'success': False, 'message': 'Aluno não encontrado.'}), 404

    del alunos_db[email]

    return jsonify({'success': True, 'message': f'Aluno {email} excluído com sucesso!'})

# --- Rotas de Funcionalidades (Professor) ---

@app.route('/api/gerar_pdf_atividade', methods=['POST'])
def gerar_pdf_atividade():
    # Esta rota simula a criação de um PDF a partir dos dados de uma atividade
    data = request.get_json()
    titulo = data.get('titulo', 'Atividade Sem Título')
    turma = data.get('turma', 'Geral')
    instrucoes = data.get('instrucoes', 'Siga as instruções abaixo para completar a atividade.')
    perguntas = data.get('perguntas', [])

    # Cria um buffer de memória para o PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    Story = []

    # 1. Título e Informações da Turma
    Story.append(Paragraph(f"<b>{titulo}</b>", styles['Title']))
    Story.append(Paragraph(f"<b>Turma:</b> {turma}", styles['Heading3']))
    Story.append(Spacer(1, 12))

    # 2. Instruções
    Story.append(Paragraph("<b>Instruções:</b>", styles['Heading3']))
    Story.append(Paragraph(instrucoes, styles['Normal']))
    Story.append(Spacer(1, 24))

    # 3. Perguntas
    Story.append(Paragraph("<b>Perguntas:</b>", styles['Heading2']))
    for i, pergunta in enumerate(perguntas):
        # Título da Pergunta
        Story.append(Paragraph(f"<b>{i+1}. {pergunta['texto']}</b>", styles['Normal']))
        Story.append(Spacer(1, 6))
        
        # Tipo de Pergunta
        if pergunta['tipo'] == 'multipla_escolha':
            for j, opcao in enumerate(pergunta['opcoes']):
                Story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;({chr(97+j)}) {opcao}", styles['Normal']))
            Story.append(Spacer(1, 12))
        elif pergunta['tipo'] == 'dissertativa':
            # Linhas para resposta
            Story.append(Paragraph("_" * 100, styles['Normal']))
            Story.append(Paragraph("_" * 100, styles['Normal']))
            Story.append(Paragraph("_" * 100, styles['Normal']))
            Story.append(Spacer(1, 12))

    # Constrói o PDF
    doc.build(Story)
    
    # Volta para o início do buffer
    buffer.seek(0)
    
    # Retorna o arquivo PDF
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{titulo.replace(' ', '_')}_{turma}_Atividade.pdf",
        mimetype='application/pdf'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email_form = request.form['email'].strip()
        senha_form = request.form['senha'].strip()
        funcao_form = request.form.get('funcao', '').strip()

        if ADMIN_EMAIL_RENDER is None or ADMIN_SENHA_RENDER is None:
            error = 'Erro interno: Credenciais Admin não encontradas no servidor.'
            print("ERRO DE AMBIENTE: SUPER_ADMIN_EMAIL ou SENHA não lidos!")

        elif email_form == ADMIN_EMAIL_RENDER and senha_form == ADMIN_SENHA_RENDER:
            
            if funcao_form != ADMIN_ROLE_RENDER:
                error = f'Função inválida. Tente usar "{ADMIN_ROLE_RENDER}".'
                print(f"FUNÇÃO FALHOU. Form: '{funcao_form}', Esperado: '{ADMIN_ROLE_RENDER}'") 
            else:
                # SUCESSO!
                session['logged_in'] = True
                session['user_email'] = email_form
                session['user_role'] = funcao_form
                return redirect(url_for('admin_dashboard'))
        else:
            # Falha de E-mail ou Senha
            error = 'E-mail, senha ou função inválidos.'

    # Formulário HTML
    return render_template_string(f"""
        <style>
            body{{font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background-color: #f0f4f8;}}
            .container {{background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px;}}
            h2 {{text-align: center; color: #333; margin-bottom: 20px;}}
            input[type="text"], input[type="password"] {{width: 100%; padding: 10px; margin: 8px 0 16px 0; display: inline-block; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box;}}
            button {{background-color: #007bff; color: white; padding: 14px 20px; margin: 8px 0; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px;}}
            button:hover {{opacity: 0.9;}}
            .error {{color: red; text-align: center; margin-bottom: 15px; background: #ffe0e0; padding: 10px; border-radius: 6px;}}
        </style>
        <div class="container">
            <h2>Tela de Login</h2>
            {{% if error %}} <p class="error">{{ error }}</p> {{% endif %}}
            <form method="post">
                <label for="email">E-mail:</label><input type="text" name="email" id="email" required>
                <label for="senha">Senha:</label><input type="password" name="senha" id="senha" required>
                <label for="funcao">Função (Digite "{ADMIN_ROLE_RENDER}"):</label><input type="text" name="funcao" id="funcao" required>
                <button type="submit">Entrar</button>
            </form>
        </div>
    """)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Quando rodando localmente, use 127.0.0.1 ou localhost
    # No Render, o gunicorn vai rodar o 'main:app' e usar a porta dele.
    app.run(host='0.0.0.0', port=5000, debug=True)
