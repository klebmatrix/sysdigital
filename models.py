# Aqui você conecta ao banco de dados real, mas para teste vamos simular

def verificar_professor(email, senha):
    # Substitua pelo seu DB real
    return email == "professor@teste.com" and senha == "123456"

def verificar_aluno(email, senha):
    # Substitua pelo seu DB real
    return email == "aluno@teste.com" and senha == "123456"
