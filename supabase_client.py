import os
from supabase import create_client, Client


# Constantes de Tabela
ADMINS_TABLE = "admins"
PROFESSORES_TABLE = "professores"
ALUNOS_TABLE = "alunos"
ATIVIDADES_TABLE = "atividades"
RESPOSTAS_TABLE = "respostas"
GAME_LEVELS_TABLE = "game_levels"

def get_supabase_client() -> Client:
    """Inicializa e retorna o cliente Supabase."""
    try:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            print("Erro: Variáveis de ambiente SUPABASE_URL ou SUPABASE_KEY não encontradas.")
            return None
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        print(f"Erro ao inicializar o cliente Supabase: {e}")
        return None

# O cliente será inicializado no main.py, mas a função está aqui para clareza.
# O main.py deve importar e chamar get_supabase_client()
