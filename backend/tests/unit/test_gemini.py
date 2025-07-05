#import pytest
#import importlib
#from unittest.mock import patch
#
#def test_gemini_apiMissing(monkeypatch):
#    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
#
#    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
#        import importlib
#        import backend.services.gemini
#        importlib.reload(backend.services.gemini)
#
#@patch("backend.services.gemini.genai.GenerativeModel")
#def test_gmeini_config(mock_model, monkeypatch):
#    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
#
#    # Recarrega o módulo para simular importação após setenv
#    import backend.services.gemini
#    importlib.reload(backend.services.gemini)
#
#    # Verifica se a API foi configurada
#    mock_model.assert_called_with("gemini-1.5-flash")