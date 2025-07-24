import pytest
from flask import Flask, jsonify, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin # Apenas UserMixin é necessário para o modelo, LoginManager não é usado diretamente aqui
import bcrypt
import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path para importações.
# Isso é importante se 'backend' não estiver diretamente no PYTHONPATH.
# Assumindo que o arquivo de teste está em 'seu_projeto/tests/'
# e 'backend' está em 'seu_projeto/backend/'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Configuração do Banco de Dados e Modelo de Usuário Mock ---
# Em um cenário real, você importaria sua instância de SQLAlchemy e seu modelo User.
# Para fins de teste, criamos uma versão simplificada aqui, incluindo o campo 'name'.
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    Modelo de Usuário simplificado para testes, incluindo 'name'.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False) # Adicionado campo 'name'
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Define a senha do usuário, aplicando hash com bcrypt."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def get_id(self):
        """Retorna o ID do usuário como string, necessário para Flask-Login (se usado)."""
        return str(self.id)

# --- Seu Blueprint de Registro Original (incluído diretamente para auto-contenção do teste) ---
# Em um aplicativo real, você importaria este blueprint de seu respectivo arquivo.

registerBp = Blueprint('register', __name__)

@registerBp.route('/auth/registrar', methods=['POST'])
def register():
    """
    Rota para registro de novo usuário.
    Recebe nome, email e senha via JSON e tenta criar um novo usuário.
    """
    data = request.get_json()
    # Verifica se data é None (caso o corpo da requisição não seja JSON)
    if data is None:
        return jsonify({'message': 'Requisição deve ser JSON'}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Dados incompletos (nome, email e senha são obrigatórios)'}), 400

    # Verifica se o nome de usuário ou e-mail já existem
    if User.query.filter_by(name=name).first():
        return jsonify({'message': 'Nome de usuário já existe'}), 409 # Conflict
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'E-mail já existe'}), 409 # Conflict

    try:
        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'name': new_user.name,
            'email': new_user.email,
            'message': 'Usuário registrado com sucesso' # Adicionado mensagem de sucesso para clareza
        }), 201

    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
        db.session.rollback() # Garante que a transação seja revertida em caso de erro
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

# --- Fixtures Pytest e Testes ---

@pytest.fixture(scope='module')
def app():
    """
    Fixture que configura uma aplicação Flask para testes.
    Inclui configuração de banco de dados em memória.
    """
    app = Flask(__name__)
    app.config['TESTING'] = True # Ativa o modo de teste.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Banco de dados SQLite em memória.
    app.config['SECRET_KEY'] = 'uma_chave_secreta_para_testes' # Chave secreta (boa prática, mesmo que Flask-Login não seja usado aqui).
    app.config['WTF_CSRF_ENABLED'] = False # Desabilita CSRF para facilitar testes.

    db.init_app(app) # Inicializa SQLAlchemy com a aplicação.

    # Registra o blueprint de registro na aplicação de teste.
    app.register_blueprint(registerBp)

    with app.app_context():
        db.create_all() # Cria todas as tabelas no banco de dados em memória.

    yield app # Fornece a aplicação para os testes.

    with app.app_context():
        db.drop_all() # Limpa o banco de dados após a execução de todos os testes do módulo.

@pytest.fixture(scope='module')
def client(app):
    """
    Fixture que fornece um cliente de teste para fazer requisições HTTP à aplicação.
    """
    return app.test_client()

# --- Testes de Registro ---

@pytest.mark.api
def test_successful_registration(client):
    """
    Testa um registro de usuário bem-sucedido com dados válidos.
    """
    response = client.post('/auth/registrar', json={
        'name': 'novo_usuario',
        'email': 'novo@example.com',
        'password': 'senha_segura'
    })
    assert response.status_code == 201
    assert 'Usuário registrado com sucesso' in response.json['message']
    assert response.json['name'] == 'novo_usuario'
    assert response.json['email'] == 'novo@example.com'

    # Opcional: Verificar se o usuário foi realmente adicionado ao banco de dados
    with client.application.app_context():
        user = User.query.filter_by(email='novo@example.com').first()
        assert user is not None
        assert user.name == 'novo_usuario'
        assert user.check_password('senha_segura')

@pytest.mark.api
def test_registration_incomplete_data_missing_name(client):
    """
    Testa o registro com dados incompletos (nome ausente).
    """
    response = client.post('/auth/registrar', json={
        'email': 'incompleto_nome@example.com',
        'password': 'senha'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

@pytest.mark.api
def test_registration_incomplete_data_missing_email(client):
    """
    Testa o registro com dados incompletos (email ausente).
    """
    response = client.post('/auth/registrar', json={
        'name': 'usuario_sem_email',
        'password': 'senha'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

@pytest.mark.api
def test_registration_incomplete_data_missing_password(client):
    """
    Testa o registro com dados incompletos (senha ausente).
    """
    response = client.post('/auth/registrar', json={
        'name': 'usuario_sem_senha',
        'email': 'sem_senha@example.com'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

@pytest.mark.api
def test_registration_existing_email(client):
    """
    Testa o registro com um email que já existe no banco de dados.
    """
    # Primeiro, registra um usuário
    client.post('/auth/registrar', json={
        'name': 'usuario_existente',
        'email': 'existente@example.com',
        'password': 'senha123'
    })

    # Tenta registrar outro usuário com o mesmo email
    response = client.post('/auth/registrar', json={
        'name': 'outro_usuario',
        'email': 'existente@example.com',
        'password': 'outrasenha'
    })
    assert response.status_code == 409
    assert 'E-mail já existe' in response.json['message']

@pytest.mark.api
def test_registration_existing_name(client):
    """
    Testa o registro com um nome de usuário que já existe no banco de dados.
    """
    # Primeiro, registra um usuário
    client.post('/auth/registrar', json={
        'name': 'nome_existente',
        'email': 'primeiro@example.com',
        'password': 'senha123'
    })

    # Tenta registrar outro usuário com o mesmo nome
    response = client.post('/auth/registrar', json={
        'name': 'nome_existente',
        'email': 'segundo@example.com',
        'password': 'outrasenha'
    })
    assert response.status_code == 409
    assert 'Nome de usuário já existe' in response.json['message']
    
@pytest.mark.api
def test_registration_empty_json(client):
    """
    Testa a requisição de registro com um corpo JSON vazio.
    """
    response = client.post('/auth/registrar', json={})
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

