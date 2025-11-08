from flask import Flask, render_template, request

app = Flask(__name__)

# Ative o modo debug para ver erros detalhados
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            return 'Login bem-sucedido!'
        else:
            return 'Usuário ou senha inválidos.'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
