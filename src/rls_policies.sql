-- =================================================================================
-- SCRIPT SQL PARA CONFIGURAÇÃO DE ROW LEVEL SECURITY (RLS) NO SUPABASE
--
-- Este script deve ser executado no SQL Editor do Supabase.
-- Ele habilita o RLS nas tabelas e cria as políticas de acesso para
-- garantir que Professores e Alunos vejam apenas os dados relevantes.
--
-- Variáveis de Contexto:
-- - auth.jwt() -> 'email': Usado para identificar o usuário logado (Professor/Aluno).
-- =================================================================================

-- 1. Habilitar RLS nas tabelas
ALTER TABLE alunos ENABLE ROW LEVEL SECURITY;
ALTER TABLE professores ENABLE ROW LEVEL SECURITY;
ALTER TABLE atividades ENABLE ROW LEVEL SECURITY;
ALTER TABLE respostas ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_levels ENABLE ROW LEVEL SECURITY;

-- 2. Políticas para a tabela 'alunos'
-- Professor pode ver os alunos que ele gerencia
CREATE POLICY "Professores podem ver seus alunos"
ON alunos FOR SELECT
USING (professor_email = current_setting('request.jwt.claims', true)::json->>'email');

-- Aluno só pode ver seu próprio registro
CREATE POLICY "Alunos podem ver seu próprio registro"
ON alunos FOR SELECT
USING (email = current_setting('request.jwt.claims', true)::json->>'email');

-- Aluno pode inserir seu próprio registro (se necessário)
CREATE POLICY "Alunos podem inserir seu próprio registro"
ON alunos FOR INSERT
WITH CHECK (email = current_setting('request.jwt.claims', true)::json->>'email');

-- 3. Políticas para a tabela 'professores'
-- Professores podem ver apenas seu próprio registro (para fins de perfil)
CREATE POLICY "Professores podem ver seu próprio registro"
ON professores FOR SELECT
USING (email = current_setting('request.jwt.claims', true)::json->>'email');

-- 4. Políticas para a tabela 'atividades'
-- Aluno pode ver atividades criadas pelo seu professor
CREATE POLICY "Alunos podem ver atividades de seu professor"
ON atividades FOR SELECT
USING (professor_email IN (SELECT professor_email FROM alunos WHERE email = current_setting('request.jwt.claims', true)::json->>'email'));

-- Professor pode ver e gerenciar suas próprias atividades
CREATE POLICY "Professores podem gerenciar suas atividades"
ON atividades FOR ALL
USING (professor_email = current_setting('request.jwt.claims', true)::json->>'email')
WITH CHECK (professor_email = current_setting('request.jwt.claims', true)::json->>'email');

-- 5. Políticas para a tabela 'respostas'
-- Aluno pode ver e inserir suas próprias respostas
CREATE POLICY "Alunos podem gerenciar suas respostas"
ON respostas FOR ALL
USING (aluno_email = current_setting('request.jwt.claims', true)::json->>'email')
WITH CHECK (aluno_email = current_setting('request.jwt.claims', true)::json->>'email');

-- Professor pode ver as respostas de seus alunos
CREATE POLICY "Professores podem ver respostas de seus alunos"
ON respostas FOR SELECT
USING (aluno_email IN (SELECT email FROM alunos WHERE professor_email = current_setting('request.jwt.claims', true)::json->>'email'));

-- 6. Políticas para a tabela 'game_levels'
-- Todos podem ler os níveis do jogo (público)
CREATE POLICY "Todos podem ler os níveis do jogo"
ON game_levels FOR SELECT
USING (true);

-- =================================================================================
-- NOTA IMPORTANTE:
-- O Supabase usa a função 'auth.jwt()' para obter o payload do token JWT.
-- O campo 'email' é acessado via 'current_setting('request.jwt.claims', true)::json->>'email''.
-- Para que isso funcione, o token JWT que sua aplicação Flask gera/usa
-- DEVE conter o campo 'email' com o e-mail do usuário logado.
-- =================================================================================

