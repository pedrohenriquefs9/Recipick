import pytest
from backend.app import create_app # O caminho de importação foi corrigido
from backend.core.database import db

@pytest.fixture(scope='session')
def app():
    """
    Fixture para criar e configurar a app Flask.
    Usa uma base de dados SQLite em memória para testes.
    """
    # Cria a app com a configuração de teste
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    
    # Cria a base de dados e as tabelas dentro do contexto da app
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Limpa a base de dados após os testes
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='session')
def client(app):
    """
    Fixture para criar um cliente de teste para a app.
    Isto permite fazer requests (GET, POST, etc.) nos testes.
    """
    return app.test_client()
