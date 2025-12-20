import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o cliente Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERRO: Variáveis de ambiente SUPABASE_URL ou SUPABASE_KEY não encontradas.")
    # Em um ambiente de produção, você pode querer levantar uma exceção ou ter um fallback
    supabase: Client = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client():
    """Retorna o cliente Supabase inicializado."""
    return supabase

from supabase import create_client, Client


# Constantes de Tabela
PROFESSORES_TABLE = "professores"
ALUNOS_TABLE = "alunos"
ATIVIDADES_TABLE = "atividades"
RESPOSTAS_TABLE = "respostas"
GAME_LEVELS_TABLE = "game_levels"
ADMINS_TABLE = "admins"

