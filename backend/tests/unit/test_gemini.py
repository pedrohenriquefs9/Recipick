import os
import pytest
import google.generativeai as genai
from backend.services import gemini


def test_gemini_keyPresente():
    assert "GEMINI_API_KEY" in os.environ, "GEMINI_API_KEY não está definida no ambiente."


def test_gemini_modelo():
    assert isinstance(gemini.modelo, genai.GenerativeModel)
    assert gemini.modelo.model_name == "models/gemini-1.5-pro"


def test_gemini_responseJson():
    config = gemini.generation_config
    assert config.response_mime_type == "application/json"


def test_genai_foi_configurado(monkeypatch):
    called = {}

    def fake_configure(api_key):
        called["api_key"] = api_key

    monkeypatch.setattr(genai, "configure", fake_configure)

    '''
    reload usado para que o genai.configure seja executado na versão fake_configure
    '''
    import importlib
    import backend.services.gemini as gemini_reload
    importlib.reload(gemini_reload)

    assert called.get("api_key") == os.environ.get("GEMINI_API_KEY")
