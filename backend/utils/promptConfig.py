def construir_prompt_com_settings(base_prompt, settings):
    if not settings:
        return base_prompt

    instrucoes_adicionais = []
    portion_map = { 'pequeno': 'uma porção pequena (individual)', 'medio': 'uma porção média (2 pessoas)', 'grande': 'uma porção grande (4+ pessoas)'}
    complexity_map = { 'rapida': 'uma receita rápida e simples (até 30 min)', 'elaborada': 'uma receita mais elaborada e detalhada' }
    style_map = { 'popular': 'popular e clássica', 'criativo': 'criativa e inusitada' }

    instrucoes_adicionais.append(f"- A receita deve ser para {portion_map.get(settings.get('portionSize'), 'uma porção média')}.")
    instrucoes_adicionais.append(f"- Deve ser {complexity_map.get(settings.get('complexity'), 'rápida e simples')}.")

    estilo_selecionado = style_map.get(settings.get('style'), 'criativa e inusitada')
    instrucoes_adicionais.append(f"- O estilo da receita DEVE ser: {estilo_selecionado}.")

    if settings.get('isVegetarian'):
        instrucoes_adicionais.append("- A receita DEVE ser estritamente vegetariana (sem nenhum tipo de carne, incluindo peixes e frutos do mar).")

    restrictions = settings.get('restrictions')
    if restrictions and restrictions.strip():
        instrucoes_adicionais.append(f"- A receita NÃO PODE conter os seguintes ingredientes sob nenhuma hipótese: {restrictions.strip()}.")

    if instrucoes_adicionais:
      prompt_final = f"{base_prompt}\n\nLeve em consideração também as seguintes preferências do usuário ao gerar as receitas:\n" + "\n".join(instrucoes_adicionais)
      return prompt_final

    return base_prompt
