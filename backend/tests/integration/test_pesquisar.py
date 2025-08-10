import pytest
from backend.routes.pesquisar import pesquisarBp
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(pesquisarBp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
class MockModelo:
    @staticmethod
    def generate_content(prompt):
        class Response:
            text = '{"nome": "Arroz e Feijão", "ingredientes": ["arroz", "feijão"]}'
        return Response()

@pytest.mark.error
def test_pesquisar_erro(client):
    entrada_erro = {}
    resposta = client.post("/api/receitas", json=entrada_erro)
    assert resposta.status_code == 404
    assert resposta.get_json() == None
