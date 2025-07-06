import pytest
from flask import Response
from backend.app import app
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_receitas_semIngredientes(client):
    response = client.post("/api/receitas", json={})
    assert response.status_code == 400
    assert "erro" in response.get_json()

@patch("backend.routes.receitas.modelo.generate_content")
def test_receitas_entradaNormal(mock_generate_content, client):
    mock_generate_content.return_value.text = """
    {
        "receitas": [
            {
                "titulo": "Arroz com Feijão",
                "tempoDePreparoEmMin": 30,
                "porcoes": 4,
                "ingredientes": [
                    {"nome": "arroz", "quantidade": "1", "unidadeMedida": "xícara"},
                    {"nome": "feijão", "quantidade": "1", "unidadeMedida": "xícara"}
                ],
                "preparo": ["Cozinhe o arroz.", "Cozinhe o feijão.", "Misture."]
            }
        ]
    }
    """
    response = client.post("/api/receitas", json={"ingredientes": "arroz, feijão"})
    data = response.get_json()

    assert response.status_code == 200
    assert "receitas" in data
    assert isinstance(data["receitas"], list)
    assert data["receitas"][0]["titulo"] == "Arroz com Feijão"

@patch("backend.routes.receitas.modelo.generate_content", side_effect=Exception("Erro no modelo"))
def test_receitas_erro500(mock_generate_content, client):
    response = client.post("/api/receitas", json={"ingredientes": "batata"})
    data = response.get_json()

    assert response.status_code == 500
    assert "erro" in data
    assert "Ocorreu um erro" in data["erro"]
