from backend.utils.promptConfig import construir_prompt_com_settings

def test_prompt_settings_vazio():
    base = "Base prompt"
    result = construir_prompt_com_settings(base, {})
    assert result == base

def test_prompt_com_todas_configuracoes():
    base = "Base prompt"
    settings = {
        "portionSize": "grande",
        "complexity": "elaborada",
        "isVegetarian": True
    }
    result = construir_prompt_com_settings(base, settings)

    assert "uma porção grande (4+ pessoas)" in result
    assert "uma receita mais elaborada" in result
    assert "A receita DEVE ser estritamente vegetariana" in result

def test_prompt_com_restricoes():
    base = "Base prompt"
    settings = {
        "restrictions": "glúten, lactose"
    }
    result = construir_prompt_com_settings(base, settings)
    assert "NÃO PODE conter os seguintes ingredientes: glúten, lactose" in result

