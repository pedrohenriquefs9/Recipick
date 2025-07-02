from typing import Dict, Any

def construir_prompt_com_settings(base_prompt: str, settings: Dict[str, Any]) -> str:
    """
    Adiciona instruções de configuração do usuário a um prompt base da IA.
    O estilo da receita é tratado diretamente na rota para definir a "persona" da IA.
    """
    if not settings:
        return base_prompt

    instrucoes_adicionais = []
    portion_map = { 'pequeno': 'uma porção pequena (individual)', 'medio': 'uma porção média (2 pessoas)', 'grande': 'uma porção grande (4+ pessoas)'}
    complexity_map = { 'rapida': 'uma receita rápida e simples (até 30 min)', 'elaborada': 'uma receita mais elaborada e detalhada' }

    instrucoes_adicionais.append(f"- A receita deve ser para {portion_map.get(settings.get('portionSize'), 'uma porção média')}.")
    instrucoes_adicionais.append(f"- Deve ser {complexity_map.get(settings.get('complexity'), 'rápida e simples')}.")

    if settings.get('isVegetarian'):
        instrucoes_adicionais.append("- A receita DEVE ser estritamente vegetariana.")

    restrictions = settings.get('restrictions')
    if restrictions and restrictions.strip():
        instrucoes_adicionais.append(f"- A receita NÃO PODE conter os seguintes ingredientes: {restrictions.strip()}.")

    if instrucoes_adicionais:
        prompt_final = f"{base_prompt}\n\nLeve em consideração também as seguintes preferências do usuário:\n" + "\n".join(instrucoes_adicionais)
        return prompt_final

    return base_prompt
