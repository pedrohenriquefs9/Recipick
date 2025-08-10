import pytest
from unittest.mock import patch, MagicMock
import json
from flask import Flask
from flask_login import LoginManager, UserMixin
#from backend.routes import receitas

class DummyUser(UserMixin):
    def __init__(self, id=1):
        self.id = id

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

@pytest.fixture(autouse=True)
def mock_login_and_user(monkeypatch):
    """
    Fixture única para garantir a ordem correta de patch e importação.
    1. Aplica o patch no decorador ANTES de o módulo de rotas ser importado.
    2. Importa o módulo de rotas (que agora usará o decorador falso).
    3. Aplica o patch no current_user dentro do módulo já carregado.
    """
    monkeypatch.setattr('flask_login.login_required', lambda f: f)

    from backend.routes import receitas

    monkeypatch.setattr(receitas, 'current_user', DummyUser())

@pytest.fixture
def app():
    from backend.routes import receitas

    app = Flask(__name__)
    
    app.register_blueprint(receitas.receitaBp)
    app.register_blueprint(receitas.refinarReceitaBp)

    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    app.secret_key = "test_secret"

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return DummyUser(user_id)

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('backend.routes.receitas.buscar_imagem_receita')
def test_buscar_imagem_sucesso(mock_buscar_imagem, client):
    mock_buscar_imagem.return_value = "http://image.url/fake.jpg"

    response = client.post('/buscar-imagem', json={"titulo": "bolo"})
    assert response.status_code == 200
    data = response.get_json()
    assert "imageUrl" in data
    assert data["imageUrl"] == "http://image.url/fake.jpg"

def test_buscar_imagem_sem_titulo(client):
    response = client.post('/buscar-imagem', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

@patch('backend.routes.receitas.modelo.generate_content')
@patch('backend.routes.receitas.Chat')
@patch('backend.routes.receitas.db')
def test_gerar_receitas_sucesso(mock_db, mock_chat, mock_generate_content, client):
    mock_generate_content.return_value.text = json.dumps({
        "receitas": [
            {
                "titulo": "Receita 1",
                "inspiracao": "Teste",
                "tempoDePreparoEmMin": 10,
                "porcoes": 2,
                "ingredientes": [{"nome": "ovo", "quantidade": "2", "unidadeMedida": "un"}],
                "preparo": ["Misture tudo."]
            }
        ] * 5
    })
    
    mock_chat.query.get.return_value = None

    mock_chat_instance = MagicMock()
    mock_chat_instance.id = 123 
    mock_chat_instance.title = "Título do Chat"
    mock_chat.return_value = mock_chat_instance

    mock_db.session.add = MagicMock()
    mock_db.session.commit = MagicMock()
    mock_db.session.rollback = MagicMock()

    payload = {
        "ingredientes": "ovo, farinha",
        "userMessage": {"role": "user", "content": "Quero receita", "type": "text"}
    }

    response = client.post('/receitas', json=payload)
    
    assert response.status_code == 200
    data = response.get_json()
    assert "chatId" in data
    assert "assistantMessage" in data
    assert data["assistantMessage"]["type"] == "recipe-carousel"
    assert data["chatId"] == 123


@patch('backend.routes.receitas.Chat')
@patch('backend.routes.receitas.db')
def test_gerar_receitas_dados_insuficientes(mock_db, mock_chat, client):
    payload = {
        "ingredientes": "",
        "userMessage": None
    }
    response = client.post('/receitas', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "erro" in data

@patch('backend.routes.receitas.Chat')
@patch('backend.routes.receitas.db')
@patch('backend.routes.receitas.modelo.generate_content')
def test_refinar_receitas_sucesso(mock_generate_content, mock_db, mock_chat, client):
    resposta_ia = {
        "texto": "Texto de resposta"
    }
    mock_generate_content.return_value.text = json.dumps(resposta_ia)
    mock_chat.query.get.return_value = MagicMock(user_id=1, id=1)
    mock_db.session.add = MagicMock()
    mock_db.session.commit = MagicMock()
    mock_db.session.rollback = MagicMock()

    payload = {
        "chatId": 1,
        "historico": [{"role": "user", "content": "Quero mudar"}],
        "ingredientes": ["ovo"],
        "userMessage": {"role": "user", "content": "Por favor", "type": "text"}
    }

    response = client.post('/refinar-receitas', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "texto" in data

def test_refinar_receitas_dados_insuficientes(client):
    payload = {
        "chatId": None,
        "historico": [],
        "userMessage": None
    }
    response = client.post('/refinar-receitas', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "erro" in data

@patch('backend.routes.receitas.Chat')
def test_refinar_receitas_chat_nao_encontrado(mock_chat, client):
    mock_chat.query.get.return_value = None
    payload = {
        "chatId": 1,
        "historico": [{"role": "user", "content": "Oi"}],
        "ingredientes": ["ovo"],
        "userMessage": {"role": "user", "content": "Oi", "type": "text"}
    }
    response = client.post('/refinar-receitas', json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert "erro" in data
