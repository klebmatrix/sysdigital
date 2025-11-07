from flask import Flask, render_template
from flask_cors import CORS
from backend.database import db
from backend.routes.admin import admin_bp
from backend.routes.professor import professor_bp
from backend.routes.aluno import aluno_bp
from flask_login import LoginManager
from models import Admin, Professor, Aluno

# Inicializa o app Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-supersegura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escoladigital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
db.init_app(app)
CORS(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Registrar Blueprints
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(professor_bp, url_prefix="/professor")
app.register_blueprint(aluno_bp, url_prefix="/aluno")

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    # Tenta encontrar o usuário em qualquer tipo de conta
    user = Admin.query.get(user_id)
    if not user:
        user = Professor.query.get(user_id)
    if not user:
        user = Aluno.query.get(user_id)
    return user

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')

# Criar o banco e as tabelas ao iniciar a aplicação
with app.app_context():
    db.create_all()

# Executar o app localmente
if __name__ == "__main__":
    app.run(debug=True)
