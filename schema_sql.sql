-- =================================================================================
-- SCRIPT SQL PARA CRIAÇÃO DO SCHEMA DO BANCO DE DADOS (SUPABASE)
--
-- Este script cria as tabelas necessárias para a aplicação "Escola Digital"
-- com base no diagrama fornecido.
-- =================================================================================

-- 1. Tabela: professores
-- Armazena os dados dos professores.
CREATE TABLE professores (
    email text PRIMARY KEY,
    senha_inicial text NOT NULL,
    expira_em date NOT NULL
);

-- 2. Tabela: alunos
-- Armazena os dados dos alunos, com referência ao professor responsável.
CREATE TABLE alunos (
    email text PRIMARY KEY,
    senha text NOT NULL,
    turma text,
    professor_email text REFERENCES professores(email) ON DELETE CASCADE
);

-- 3. Tabela: atividades
-- Armazena as atividades criadas pelos professores.
CREATE TABLE atividades (
    id serial PRIMARY KEY,
    titulo text NOT NULL,
    tipo text,
    gabarito jsonb,
    professor_email text REFERENCES professores(email) ON DELETE CASCADE,
    created_at timestamp with time zone DEFAULT now()
);

-- 4. Tabela: respostas
-- Armazena as respostas dos alunos às atividades.
CREATE TABLE respostas (
    id serial PRIMARY KEY,
    atividade_id integer REFERENCES atividades(id) ON DELETE CASCADE,
    aluno_email text REFERENCES alunos(email) ON DELETE CASCADE,
    resposta jsonb,
    nota numeric,
    enviada_em timestamp with time zone DEFAULT now()
);

-- 5. Tabela: game_levels
-- Armazena a configuração dos níveis do neurogame.
CREATE TABLE game_levels (
    key text PRIMARY KEY,
    name text NOT NULL,
    entities jsonb,
    relations jsonb
);

-- 6. Tabela: admins
-- Armazena os dados dos administradores (usado para login via variáveis de ambiente no Flask)
-- Nota: Esta tabela é mantida para consistência com o código Python, mas o login
-- de administrador é tratado fora do Supabase Auth.
CREATE TABLE admins (
    email text PRIMARY KEY,
    senha text NOT NULL
);

-- 7. Tabela: usuario (e Users)
-- As tabelas 'usuario' e 'Users' no diagrama parecem ser redundantes ou para um sistema de autenticação diferente.
-- Como a aplicação Flask já usa 'admins', 'professores' e 'alunos' para login,
-- estas tabelas não serão criadas para evitar confusão.
-- Se o usuário desejar migrar para o Supabase Auth, a tabela 'auth.users' seria a mais indicada.

-- =================================================================================
-- FIM DO SCRIPT DE CRIAÇÃO DE SCHEMA
-- =================================================================================

