import pytest
from backend.tests.conftest import client
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

@pytest.mark.type
def test_pesquisar_type (client):
    entradaTeste = {
        "nome_receita": "arroz e feijão"
    }
    resposta = client.post("/api/pesquisar", json=entradaTeste)
    respostaJson = resposta.get_json()
    assert isinstance(respostaJson, dict)
    
@pytest.mark.error
def test_pesquisar_erro (client):
    data = {}
    nome_receita = data.get("nome_receita", "").strip()
    response = client.post("/api/receitas", json=nome_receita)
    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Nome da receita não informado.'}
    