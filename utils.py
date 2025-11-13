import os
from supabase_client import get_supabase_client
from supabase_client import PROFESSORES_TABLE, ALUNOS_TABLE

supabase = get_supabase_client()

def verificar_professor(email, senha):
    """Verifica se é professor no Supabase."""
    if not supabase:
        return False
    try:
        response = supabase.table(PROFESSORES_TABLE).select("*").eq("email", email).eq("senha_inicial", senha).execute()
        return response.data and len(response.data) > 0
    except Exception as e:
        print(f"Erro ao verificar professor: {e}")
        return False

def verificar_aluno(email, senha):
    """Verifica se é aluno no Supabase."""
    if not supabase:
        return False
    try:
        response = supabase.table(ALUNOS_TABLE).select("*").eq("email", email).eq("senha", senha).execute()
        return response.data and len(response.data) > 0
    except Exception as e:
        print(f"Erro ao verificar aluno: {e}")
        return False

