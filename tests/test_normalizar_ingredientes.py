import pytest
from flask import Flask
from backend.routes.normalizar_ingredientes import normalizarBp

### Mock da função modelo.generate_content
##class MockModelo:
##    @staticmethod
##    def generate_content(prompt):
##        class Response:
##            text = '["feijão", "cebola roxa", "queijo", ""]'
##        return Response()
##
### Substitui o modelo pelo mock no teste
##import backend.services.gemini as gemini_module
##gemini_module.modelo = MockModelo()

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(normalizarBp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_normalizar_ingredientes_escritaErrada(client):
    entradaTeste = {
        "ingredientes": ["feijaox", "cebola oxa", "Qeijo", "spbrecoxa"]
    }
    resposta = client.post("/api/normalizar-ingredientes", json=entradaTeste)
    respostaJson = resposta.get_json()
    assert respostaJson == {"ingredientes_normalizados": ["feijão", "cebola roxa", "queijo", "sobrecoxa"]}
    
def test_normalizar_ingredientes_invalidos(client):
    entradaTeste = {
        "ingredientes": ["lajflasdk", "asfhdbsajbashkbadjkbdasjk", "lksdksl", "asdfgh"]
    }
    resposta = client.post("/api/normalizar-ingredientes", json=entradaTeste)
    respostaJson = resposta.get_json()
    assert respostaJson == {"ingredientes_normalizados": ["", "", "", ""]}

def test_normalizar_ingredientes_type (client):
    entradaTeste = {
        "ingredientes": ["feijão", "cebola roxa", "queijo", "sobrecoxa"]
    }
    resposta = client.post("/api/normalizar-ingredientes", json=entradaTeste)
    respostaJson = resposta.get_json()
    for ingredientes in respostaJson['ingredientes_normalizados']:
        assert isinstance(ingredientes, str)
    
def test_normalizar_ingredientes_type2 (client):
    entradaTeste = {
        "ingredientes": 'arroz  '
    }
    resposta = client.post("/api/normalizar-ingredientes", json=entradaTeste)
    respostaJson = resposta.get_json()
    for ingredientes in respostaJson['ingredientes_normalizados']:
        assert isinstance(ingredientes, str)
    