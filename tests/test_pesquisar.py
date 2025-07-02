import pytest
from flask import Flask
from backend.routes.pesquisar import pesquisarBp

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
    app.register_blueprint(pesquisarBp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_pesquisar_type (client):
    entradaTeste = {
        "nome_receita": "arroz e feijão"
    }
    resposta = client.post("/api/pesquisar", json=entradaTeste)
    respostaJson = resposta.get_json()
    assert isinstance(respostaJson, dict)
    assert isinstance(respostaJson['receita'], str)
    