# Escola Digital - Sistema de Gerenciamento de Atividades

Este projeto é um sistema de gerenciamento de atividades e usuários para escolas, construído com **Flask** (Python) e integrado com **Supabase** para persistência de dados.

## Funcionalidades Principais

*   **Login de Administrador:** Gerenciamento de licenças de Professores.
*   **Gerenciamento de Professores:** Cadastro, renovação e exclusão de professores (com senha inicial).
*   **Gerenciamento de Alunos:** Cadastro, troca de senha (simulada) e exclusão de alunos por Administradores e Professores.
*   **Criação de Atividades:** Professores podem criar atividades de múltipla escolha, certo/errado e abertas.
*   **Geração de PDF:** Exportação das atividades criadas para PDF.
*   **Neurogame:** Jogo educacional integrado para Alunos e Professores.
*   **Simulador de Atividade:** Ferramenta para simulação de criação de atividades.

## Configuração e Instalação

### 1. Dependências Python

Instale as dependências do Python:

```bash
pip install -r requirements.txt
```

### 2. Configuração do Supabase

Este projeto utiliza o Supabase como banco de dados. Você precisa configurar as seguintes variáveis de ambiente em um arquivo chamado **`.env`** na raiz do projeto:

| Variável | Descrição | Exemplo |
| :--- | :--- | :--- |
| `SUPABASE_URL` | URL da sua instância Supabase. | `https://xyzcompany.supabase.co` |
| `SUPABASE_KEY` | Sua chave `anon` ou `service_role` do Supabase. | `eyJhbGciOiJIUzI1NiI...` |
| `SUPER_ADMIN_EMAIL` | E-mail para o login do Administrador. | `admin@escola.com` |
| `SUPER_ADMIN_SENHA` | Senha para o login do Administrador. | `senha_secreta` |

**Estrutura de Tabelas Necessárias no Supabase:**

Você precisará criar as seguintes tabelas no seu projeto Supabase:

| Tabela | Chave Primária | Colunas Essenciais |
| :--- | :--- | :--- |
| `professores` | `email` | `email`, `expira_em`, `senha_inicial` |
| `alunos` | `email` | `email`, `turma`, `professor` |
| `game_levels` | `key` | `key`, `name`, `entities`, `relations` |

### 3. Execução

Execute o aplicativo usando o Gunicorn (recomendado para produção) ou diretamente com o Flask (para desenvolvimento):

```bash
# Para produção (usando start.sh)
./start.sh

# Para desenvolvimento (direto no Python)
python main.py
```

## Próximos Passos (Manual)

*   **Configuração do Firebase:** O frontend (dashboards) ainda usa o Firebase para autenticação de Professor/Aluno. Você precisará garantir que as variáveis de configuração do Firebase sejam injetadas corretamente nos templates HTML.
*   **Correção do `aluno_dashboard.html`:** O arquivo `aluno_dashboard.html` precisa ter o link para o simulador adicionado manualmente.
*   **Lógica de Senha:** A `senha_inicial` do professor é armazenada em texto puro no Supabase. **Isso é inseguro** e deve ser substituído por um hash (ex: `bcrypt`) em um ambiente de produção.
*   **Lógica de Troca de Senha:** A rota `/api/trocar_senha_aluno` é apenas simulada e deve ser integrada com o Supabase Auth para ser funcional.

"# sysdigital" 
