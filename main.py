from flask import Flask, request, jsonify
from supabase import create_client
import os

app = Flask(__name__)

# Configurar Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para pegar usuário por email
def get_user_by_email(email):
    result = supabase.table("users").select("*").eq("email", email).single().execute()
    if result.error:
        return None
    return result.data

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if user["password"] != password:
        return jsonify({"error": "Senha incorreta"}), 401

    if user["role"] != "admin":
        return jsonify({"error": "Acesso negado, não é admin"}), 403

    return jsonify({"message": f"Bem-vindo admin {email}!"}), 200

if __name__ == "__main__":
    main.run(debug=True)
