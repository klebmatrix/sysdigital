from db import get_connection

def verificar_admin(email, senha):
    """Verifica se é o admin usando variáveis de ambiente."""
    from os import environ
    ADMIN_EMAIL = environ.get("ADMIN_EMAIL")
    ADMIN_PASS = environ.get("ADMIN_PASSWORD")
    return email == ADMIN_EMAIL and senha == ADMIN_PASS

def verificar_professor(email, senha):
    """Verifica se é professor no banco."""
    conn = get_connection()
    if not conn:
        return False
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM professores WHERE email=%s AND senha_inicial=%s",
            (email, senha)
        )
        return cur.fetchone() is not None

def verificar_aluno(email, senha):
    """Verifica se é aluno no banco."""
    conn = get_connection()
    if not conn:
        return False
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM alunos WHERE email=%s AND senha_inicial=%s",
            (email, senha)
        )
        return cur.fetchone() is not None
