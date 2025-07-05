import pytest
from flask import Flask
from backend.routes.pesquisar import pesquisarBp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(pesquisarBp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client