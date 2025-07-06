import pytest
from flask import Flask
from backend.routes.normalizar_ingredientes import normalizarBp

class MockModelo:
    @staticmethod
    def generate_content(prompt):
        class Response:
            text = '["feijão", "cebola roxa", "queijo", "sobrecoxa"]'
        return Response()

@pytest.fixture
def client(monkeypatch):
    from backend.services import gemini
    monkeypatch.setattr(gemini, "modelo", MockModelo)

    app = Flask(__name__)
    app.register_blueprint(normalizarBp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.api
def test_normalizar_ingredientes_escritaErrada(client):
    entradaTeste = {
        "ingredientes": ["feijaox", "cebola oxa", "Qeijo", "spbrecoxa"]
    }
    resposta = client.post("/api/normalizar-ingredientes", json=entradaTeste)
    respostaJson = resposta.get_json()
    assert respostaJson == {"ingredientes_normalizados": ["feijão", "cebola roxa", "queijo", "sobrecoxa"]}

@pytest.mark.api
def test_normalizar_ingredientes_invalidos(client, monkeypatch):
    class MockFalha:
        @staticmethod
        def generate_content(prompt):
            class Response:
                text = '["", "", "", ""]'
            return Response()

    from backend.services import gemini
    monkeypatch.setattr(gemini, "modelo", MockFalha)

    entradaTeste = {
        "ingredientes": ["lajflasdk", "asfhdbsajbashkbadjkbdasjk", "lksdksl", "asdfgh"]
    }
    resposta = client.post("/api/normalizar-ingredientes", json=entradaTeste)
    respostaJson = resposta.get_json()
    assert respostaJson == {"ingredientes_normalizados": ["", "", "", ""]}

@pytest.mark.type
def test_normalizar_ingredientes_type(client):
    entradaTeste = {
        "ingredientes": ["feijão", "cebola roxa", "queijo", "sobrecoxa"]
    }
    resposta = client.post("/api/normalizar-ingredientes", json=entradaTeste)
    respostaJson = resposta.get_json()
    for ingrediente in respostaJson['ingredientes_normalizados']:
        assert isinstance(ingrediente, str)

@pytest.mark.type
def test_normalizar_ingredientes_type2(client):
    entradaTeste = {
        "ingredientes": 'arroz  '
    }
    resposta = client.post("/api/normalizar-ingredientes", json=entradaTeste)
    respostaJson = resposta.get_json()
    for ingrediente in respostaJson['ingredientes_normalizados']:
        assert isinstance(ingrediente, str)
