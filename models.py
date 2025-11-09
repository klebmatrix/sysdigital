import os
import psycopg

# Conexão usando variáveis de ambiente
conn = psycopg.connect(
    host=os.environ.get("DB_HOST"),
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    port=os.environ.get("DB_PORT", 5432)
)
conn.autocommit = True

def verificar_professor(email, senha):
    """Retorna True se o professor existe e a senha confere."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM professores WHERE email=%s AND senha_inicial=%s",
            (email, senha)
        )
        return cur.fetchone() is not None

def verificar_aluno(email, senha):
    """Retorna True se o aluno existe e a senha confere."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM alunos WHERE email=%s AND senha=%s",
            (email, senha)
        )
        return cur.fetchone() is not None
