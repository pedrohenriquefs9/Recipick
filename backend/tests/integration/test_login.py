import pytest
from flask import Flask, jsonify, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from backend.routes.login import login, logout
import bcrypt
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    Modelo de Usuário simplificado para testes.
    Simula o comportamento do seu User real para autenticação.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def get_id(self):
        return str(self.id)

loginBp = Blueprint('login', __name__)
logoutBp = Blueprint('logout', __name__)

@loginBp.route('/auth/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Login realizado com sucesso', 'email': user.email}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401

@logoutBp.route('/auth/logout', methods=['POST'])
@login_required 
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

# --- Fixtures Pytest e Testes ---

@pytest.fixture(scope='module')
def app():
    """
    Fixture que configura uma aplicação Flask para testes.
    Inclui configuração de banco de dados em memória e Flask-Login.
    """
    app = Flask(__name__)
    app.config['TESTING'] = True # Ativa o modo de teste. <--NECESSARIO
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    app.config['SECRET_KEY'] = 'uma_chave_secreta_para_testes'
    app.config['WTF_CSRF_ENABLED'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app) 
    login_manager.login_view = 'login.login'

    @login_manager.user_loader
    def load_user(user_id):
        """Função de carregamento de usuário para Flask-Login."""
        return User.query.get(int(user_id))

    app.register_blueprint(loginBp)
    app.register_blueprint(logoutBp)

    with app.app_context():
        db.create_all() 
        test_user = User(email='test@example.com')
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()

    yield app 

    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """
    Fixture que fornece um cliente de teste para fazer requisições HTTP à aplicação.
    """
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    """
    Fixture que fornece um runner de linha de comando para testar comandos CLI (se houver).
    Não é estritamente necessário para este código, mas é comum em testes Flask.
    """
    return app.test_cli_runner()

# --- Testes de Login ---

@pytest.mark.api
def test_successful_login(client):
    """
    Testa um login bem-sucedido com credenciais corretas.
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'Login realizado com sucesso' in response.json['message']
    assert 'test@example.com' in response.json['email']

@pytest.mark.api
def test_invalid_credentials_login_wrong_password(client):
    """
    Testa um login com senha incorreta.
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'Credenciais inválidas' in response.json['message']

@pytest.mark.api
def test_invalid_credentials_login_non_existent_user(client):
    """
    Testa um login com um email de usuário que não existe.
    """
    response = client.post('/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'password123'
    })
    assert response.status_code == 401
    assert 'Credenciais inválidas' in response.json['message']

@pytest.mark.api
def test_successful_logout(client): #necessita de alteração futura
    """
    Testa um logout bem-sucedido após um login prévio.
    """
    client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert 'Logout realizado com sucesso' in response.json['message']

@pytest.mark.api
def test_logout_without_login(client):
    """
    Testa a tentativa de logout sem estar logado.
    Espera um redirecionamento para a página de login devido ao @login_required.
    """
    response = client.post('/auth/logout')

    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']

