import pytest
import os
from flask import Flask, Blueprint, Response 
from backend.routes.normalizar_ingredientes import normalizarBp
from backend.routes.pesquisar import pesquisarBp
from backend.routes.receitas import receitaBp

import shutil # Importa shutil para remover diretórios
from backend.app import app, DIST_FOLDER # Importa o app e DIST_FOLDER do seu app.py

@pytest.fixture
def client():
    """
    Fixture Pytest para configurar um cliente de teste para a aplicação Flask.
    Isso permite fazer requisições HTTP simuladas para o aplicativo.
    """
    app.config["TESTING"] = True  # Ativa o modo de teste
    
    # Cria uma pasta 'dist' temporária para simular o frontend compilado
    # e um arquivo 'index.html' e um 'static_file.js' dentro dela.
    temp_dist_folder = os.path.join(os.path.dirname(__file__), "temp_dist")
    os.makedirs(temp_dist_folder, exist_ok=True)
    
    with open(os.path.join(temp_dist_folder, "index.html"), "w") as f:
        f.write("<h1>Frontend Index</h1>")
    with open(os.path.join(temp_dist_folder, "static_file.js"), "w") as f:
        f.write("console.log('Static JS');")

    # Temporariamente sobrescreve app.static_folder para apontar para a pasta temporária
    original_static_folder = app.static_folder
    app.static_folder = temp_dist_folder

    with app.test_client() as client:
        yield client
    
    # Limpeza: remove a pasta temporária e restaura a app.static_folder original
    app.static_folder = original_static_folder
    if os.path.exists(temp_dist_folder):
        shutil.rmtree(temp_dist_folder)


def test_app_creation():
    assert isinstance(app, Flask)
    assert app.name == "backend.app"


def test_app_blueprint():
    assert "normalizar" in app.blueprints
    assert "pesquisar" in app.blueprints
    assert "receita" in app.blueprints


def test_app_index(client):
    """Verifica se a rota '/' serve o index.html."""
    response: Response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Frontend Index</h1>" in response.data
    assert response.mimetype == "text/html"


def test_app_static(client):#
    """Verifica se a rota serve arquivos estáticos corretamente."""
    response: Response = client.get("/static_file.js")
    assert response.status_code == 200
    assert b"console.log('Static JS');" in response.data
    assert response.mimetype == "text/javascript"

