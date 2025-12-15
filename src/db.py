import os
import psycopg

def get_connection():
    try:
        conn = psycopg.connect(
            host=os.environ.get("DB_HOST"),
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            port=int(os.environ.get("DB_PORT", 5432))
        )
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco:", e)
        return None
