import pytest
from flask import Flask, jsonify

# Importação do blueprint. Esta é a importação correta para o teste.
from backend.routes.normalizar_ingredientes import normalizarBp

# --- SETUP DO MOCK ---
# Estas classes de mock são uma ótima forma de simular o comportamento da API externa
# sem ter que fazer uma chamada de rede real. Isto torna os testes rápidos e fiáveis.

class FakeResponse:
    """Uma classe de mock para simular o objeto de resposta do modelo."""
    def __init__(self, text):
        self.text = text

class FakeModelo:
    """Uma classe de mock para simular o comportamento do modelo da IA."""
    def __init__(self, text_to_return):
        self.text_to_return = text_to_return

    def generate_content(self, prompt, generation_config=None):
        """Simula a chamada ao modelo, devolvendo o texto pré-definido."""
        return FakeResponse(self.text_to_return)

# --- FIXTURES PARA O APP DE TESTE ---
# Estas fixtures são o coração do teu ficheiro de teste. Elas preparam o ambiente para cada teste.

@pytest.fixture
def app(monkeypatch):
    """
    Fixture que cria a aplicação Flask para os testes.

    É aqui que fazes a parte mais importante: substituis o modelo real da IA
    por uma versão "fake" usando o monkeypatch. Isto isola o teu teste,
    garantindo que não dependes de serviços externos.
    """
    app = Flask(__name__)
    app.register_blueprint(normalizarBp)

    # AQUI ESTÁ A CORREÇÃO. Importamos o módulo `normalizar_ingredientes`
    # em vez de `normalizar`, que não existe.
    from backend.routes import normalizar_ingredientes
    monkeypatch.setattr(normalizar_ingredientes, "modelo", FakeModelo(
        '{"ingredientes_normalizados": ["feijão", "cebola roxa", "queijo", ""]}'
    ))

    return app

@pytest.fixture
def client(app):
    """
    Fixture que cria um cliente de teste para fazer requisições.
    O Pytest usa a fixture 'app' para configurar este cliente.
    """
    return app.test_client()

# --- TESTES ---
# A tua suite de testes é sólida e cobre casos importantes.

def test_normalizacao_ingredientes(client):
    """
    Teste que verifica o cenário de sucesso.
    1. Envia um payload com ingredientes mal escritos.
    2. Verifica se o status code é 200.
    3. Verifica se a resposta JSON contém a chave esperada.
    4. Verifica se a lista de ingredientes normalizados é a esperada,
       incluindo o queijo (corrigido) e a string vazia (removido).
    """
    payload = {
        "ingredientes": ["feijaox", "cebola roxa", "Qeijo", "asdfgh"]
    }
    response = client.post("/normalizar-ingredientes", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert "ingredientes_normalizados" in data
    assert data["ingredientes_normalizados"] == ["feijão", "cebola roxa", "queijo", ""]

def test_lista_vazia(client):
    """
    Teste de caso de limite. Verifica se a API lida corretamente com uma lista vazia.
    """
    payload = {
        "ingredientes": []
    }
    response = client.post("/normalizar-ingredientes", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["ingredientes_normalizados"] == []

def test_erro_json_da_ia(monkeypatch, client):
    """
    Teste para um cenário de falha.
    1. Simula uma resposta não JSON do modelo da IA.
    2. Verifica se a API retorna os ingredientes originais, conforme o esperado.
       Isto é um excelente teste para garantir a resiliência da tua aplicação.
    """
    # AQUI ESTÁ A CORREÇÃO. Importamos o módulo correto para o monkeypatch.
    from backend.routes import normalizar_ingredientes

    class ModeloComErro:
        def generate_content(self, prompt, generation_config=None):
            return FakeResponse("isso não é um json válido")

    # Substitui temporariamente o modelo com erro usando monkeypatch
    monkeypatch.setattr(normalizar_ingredientes, "modelo", ModeloComErro())

    payload = {"ingredientes": ["cebola", "tomate"]}
    response = client.post("/normalizar-ingredientes", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["ingredientes_normalizados"] == ["cebola", "tomate"]
