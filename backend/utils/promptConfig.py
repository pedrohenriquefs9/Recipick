from typing import Dict, Any

def construir_prompt_com_settings(base_prompt: str, settings: Dict[str, Any]) -> str:
    """
    Adiciona instruções de configuração do utilizador a um prompt base da IA.
    """
    if not settings:
        return base_prompt

    instrucoes_adicionais = []
    
    portion_map = { 
        'pequeno': 'uma porção pequena (individual)', 
        'medio': 'uma porção média (2-3 pessoas)', 
        'grande': 'uma porção grande (4+ pessoas)'
    }
    complexity_map = { 
        'rapida': 'uma receita rápida e simples (até 30 min)', 
        'elaborada': 'uma receita mais elaborada e detalhada' 
    }
    diet_map = {
        'vegetarian': "- A receita DEVE ser estritamente vegetariana (sem carne ou peixe).",
        'vegan': "- A receita DEVE ser estritamente vegana (sem nenhum produto de origem animal, incluindo ovos, laticínios e mel)."
    }

    if 'portionSize' in settings and settings['portionSize'] in portion_map:
        instrucoes_adicionais.append(f"- A receita deve ser para {portion_map.get(settings['portionSize'])}.")
    
    if 'complexity' in settings and settings['complexity'] in complexity_map:
        instrucoes_adicionais.append(f"- Deve ser {complexity_map.get(settings['complexity'])}.")

    if 'diet' in settings and settings['diet'] in diet_map:
        instrucoes_adicionais.append(diet_map[settings['diet']])

    if instrucoes_adicionais:
        prompt_final = f"{base_prompt}\n\nLeve em consideração também as seguintes preferências do utilizador:\n" + "\n".join(instrucoes_adicionais)
        return prompt_final

    return base_prompt