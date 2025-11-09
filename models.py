import psycopg2
import os

# Conexão com o banco
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    port=os.environ.get("DB_PORT", 5432)
)
db = conn
cursor = db.cursor()

def verificar_professor(email, senha):
    cursor.execute(
        "SELECT * FROM professores WHERE email=%s AND senha_inicial=%s",
        (email, senha)
    )
    return cursor.fetchone() is not None

def verificar_aluno(email, senha):
    cursor.execute(
        "SELECT * FROM alunos WHERE email=%s AND senha=%s",
        (email, senha)
    )
    return cursor.fetchone() is not None
