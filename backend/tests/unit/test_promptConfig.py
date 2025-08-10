import pytest
from backend.utils.promptConfig import construir_prompt_com_settings  # ajuste o caminho conforme necessário

BASE_PROMPT = "Crie uma receita de massa."

def test_prompt_sem_settings():
    resultado = construir_prompt_com_settings(BASE_PROMPT, {})
    assert resultado == BASE_PROMPT

def test_prompt_com_portion_pequeno():
    settings = {"portionSize": "pequeno"}
    resultado = construir_prompt_com_settings(BASE_PROMPT, settings)
    assert "uma porção pequena (individual)" in resultado

def test_prompt_com_complexidade_rapida():
    settings = {"complexity": "rapida"}
    resultado = construir_prompt_com_settings(BASE_PROMPT, settings)
    assert "uma receita rápida e simples" in resultado

def test_prompt_com_dieta_vegan():
    settings = {"diet": "vegan"}
    resultado = construir_prompt_com_settings(BASE_PROMPT, settings)
    assert "estritamente vegana" in resultado
    assert "sem nenhum produto de origem animal" in resultado

def test_prompt_com_todos_os_settings():
    settings = {
        "portionSize": "medio",
        "complexity": "elaborada",
        "diet": "vegetarian"
    }
    resultado = construir_prompt_com_settings(BASE_PROMPT, settings)

    assert "uma porção média" in resultado
    assert "mais elaborada e detalhada" in resultado
    assert "estritamente vegetariana" in resultado

def test_prompt_com_valores_invalidos():
    settings = {
        "portionSize": "gigante",
        "complexity": "dificil",
        "diet": "carnivoro"
    }
    resultado = construir_prompt_com_settings(BASE_PROMPT, settings)
    # Nenhuma instrução adicional deve ser adicionada
    assert resultado == BASE_PROMPT
