import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host="db.uinktmdpesynvrxhgvht.supabase.co",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="SUA_SERVICE_ROLE_KEY",
    cursor_factory=RealDictCursor
)
cur = conn.cursor()
cur.execute("SELECT * FROM public.admin WHERE email=%s AND senha=crypt(%s, senha)", 
            ('admin@exemplo.com', 'SuaSenhaSegura123'))
user = cur.fetchone()
print(user)
cur.close()
conn.close()







