import pytest
from flask import Response
from backend.app import create_app # Importa o app e DIST_FOLDER do seu app.py

app=create_app()
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_receitas_semIngredientes(client):
    response = client.post("/api/receitas", json={})
    assert response.status_code == 400
    assert "erro" in response.get_json()

@patch("backend.routes.receitas.modelo.generate_content", side_effect=Exception("Erro no modelo"))
def test_receitas_erro500(mock_generate_content, client):
    response = client.post("/api/receitas", json={"ingredientes": "batata"})
    data = response.get_json()

    assert response.status_code == 500
    #assert "erro" in data
    #assert "Ocorreu um erro" in data["erro"]
