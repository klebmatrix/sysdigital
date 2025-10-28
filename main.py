import os
import io
import datetime # Adicionado para uso no admin_dashboard
from flask import Flask, request, redirect, url_for, render_template_string, session, jsonify, send_file, render_template
# Imports para ReportLab (PDF generation)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# =====================================================================
# 1. Configuração da Aplicação e Credenciais
# =====================================================================

# Lê a chave secreta do ambiente Render.
SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_de_fallback_insegura_nao_use')
if SECRET_KEY == 'chave_de_fallback_insegura_não_use':
    # Este print aparece nos logs do Render
    print("ALERTA CRÍTICO: SECRET_KEY NÃO CONFIGURADA NO RENDER. Usando fallback.")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
# ====================================================================
# LINHA ADICIONADA: Desabilita o cache de templates do Flask para forçar a atualização
app.config['TEMPLATES_AUTO_RELOAD'] = True
# ====================================================================


# Credenciais Lidas do Render
ADMIN_EMAIL_RENDER = os.environ.get('SUPER_ADMIN_EMAIL')
ADMIN_SENHA_RENDER = os.environ.get('SUPER_ADMIN_SENHA')
ADMIN_ROLE_RENDER = 'Administrador' # Função esperada internamente

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
            # Note: O arquivo 'admin_dashboard.html' deve estar na pasta 'templates' para funcionar corretamente
            return render_template('admin_dashboard.html', 
                                  professores_dados=professores_dados, 
                                  alunos_dados=alunos_dados,
                                  hoje=hoje,
                                  PROFESSOR_EMAIL_PADRAO="professor.teste@escola.com")
        except FileNotFoundError:
            # Fallback caso o admin_dashboard.html não exista
            return render_template_string(f"""
                <style>body{{font-family: sans-serif; background-color: #f0f4f8; padding: 20px;}} .card {{background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}}</style>
                <div class="card">
                    <h1>Dashboard do Administrador (Pendente)</h1>
                    <p>O arquivo 'admin_dashboard.html' precisa ser criado na pasta 'templates' para exibir o painel.</p>
                    <a href="{url_for('logout')}" style="color: blue;">Sair</a>
                </div>
            """)

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
        # ... (código de autenticação omitido por brevidade, mas está correto)
        email_form = request.form['email'].strip()
        password_form = request.form['password'].strip()
        role_form = request.form.get('role', '').strip()

        if ADMIN_EMAIL_RENDER is None or ADMIN_SENHA_RENDER is None:
            error = 'Erro interno: Credenciais Admin não encontradas no servidor.'
            print("ERRO DE AMBIENTE: SUPER_ADMIN_EMAIL ou SENHA não lidos!")

        # Checa as credenciais de ADMIN (E-mail e Senha)
        elif email_form == ADMIN_EMAIL_RENDER and password_form == ADMIN_SENHA_RENDER:
            
            # O campo 'role' no HTML envia o valor 'admin' para a função de Administrador
            if role_form != 'admin':
                error = f'Para o e-mail {ADMIN_EMAIL_RENDER}, a função esperada é Administrador.'
                print(f"FUNÇÃO FALHOU. Form: '{role_form}', Esperado: 'admin'") 
            else:
                # SUCESSO!
                session['logged_in'] = True
                session['user_email'] = email_form
                session['user_role'] = ADMIN_ROLE_RENDER # Mantemos o nome interno 'Administrador'
                return redirect(url_for('admin_dashboard'))
        else:
            # Falha de E-mail, Senha ou se a função (professor/aluno) não for validada aqui (ainda não implementado)
            error = 'E-mail, senha ou função inválidos.'

    # ==== Chamada ao Template com Tratamento de Erro de Arquivo ====
    try:
        return render_template('login.html', error=error)
    except Exception as e:
        # Se falhar, é porque o Render não tem o arquivo 'login.html' na pasta 'templates'
        return render_template_string(f"""
            <div style="font-family: sans-serif; padding: 50px; text-align: center; background-color: #ffcccc; color: #cc0000; border: 5px solid #cc0000;">
                <h1>ERRO CRÍTICO: Arquivo de Login Não Encontrado!</h1>
                <p>O servidor está lendo o `main.py`, mas não consegue encontrar o arquivo <code>templates/login.html</code>.</p>
                <p>Isso é um erro de Deploy.</p>
                <p>Detalhes do Erro: <code>{e}</code></p>
                <p>Solução: Verifique se o arquivo <code>login.html</code> está na pasta <code>templates</code> do seu repositório Git e force o re-deploy.</p>
            </div>
        """, error=error)
    # =============================================================

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Quando rodando localmente, use 127.0.0.1 ou localhost
    # No Render, o gunicorn vai rodar o 'main:app' e usar a porta dele.
    app.run(host='0.0.0.0', port=5000, debug=True)
