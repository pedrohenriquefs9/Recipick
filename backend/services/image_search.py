import requests
import os
import re

# Cache para armazenar URLs de imagens e evitar buscas repetidas.
_IMAGE_CACHE = {}

def _limpar_query(query):
    """
    Remove uma lista extensa de palavras comuns, adjetivos e verbos de modo de preparo 
    para focar nos substantivos principais da receita.
    """
    palavras_a_remover = [
        # Artigos e Preposições
        'à', 'com', 'sem', 'e', 'o', 'a', 'os', 'as', 'de', 'do', 'da', 'dos', 'das', 
        'no', 'na', 'nos', 'nas', 'em', 'um', 'uma', 'uns', 'umas', 'para', 'por',
        
        # Adjetivos e Descrições Comuns
        'simples', 'fácil', 'rápido', 'delicioso', 'especial', 'caseiro', 'caseira', 
        'cremoso', 'cremosa', 'crocante', 'light', 'fit', 'tradicional', 'perfeito',
        'incrível', 'melhor', 'mundo', 'irresistível',
        
        # Verbos de Preparo
        'recheado', 'recheada', 'gratinado', 'gratinada', 'assado', 'assada', 
        'frito', 'frita', 'grelhado', 'grelhada', 'cozido', 'cozida', 'poché',
        
        # Termos Afetivos ou Desnecessários
        'da vovó', 'da tia', 'meu', 'minha',
        
        # Palavras já implícitas na busca
        'receita', 'prato', 'comida'
    ]
    query_limpa = query.lower()
    query_limpa = re.sub(r'[^\w\s]', '', query_limpa)
    
    for frase in ['da vovó', 'da tia']:
        query_limpa = query_limpa.replace(frase, '')

    palavras = [palavra for palavra in query_limpa.split() if palavra not in palavras_a_remover]
    
    return " ".join(palavras)

def _buscar_na_api(query_formatada):
    """Função interna para realizar a chamada à API do Google."""
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

    if not api_key or not search_engine_id:
        print("AVISO: Chaves da API do Google não configuradas.")
        return None

    params = {
        'q': query_formatada,
        'key': api_key,
        'cx': search_engine_id,
        'searchType': 'image',
        'num': 1,
        'imgSize': 'large',
        'safe': 'high'
    }

    try:
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=5)
        response.raise_for_status()
        results = response.json()
        if 'items' in results and len(results['items']) > 0:
            return results['items'][0]['link']
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na chamada da API para query '{query_formatada}': {e}")
        return None

def buscar_imagem_receita(query_original):
    """
    Busca uma imagem de receita com cache e uma estratégia de múltiplas tentativas para máxima eficácia.
    """
    if not query_original or not isinstance(query_original, str):
        return None

    if query_original in _IMAGE_CACHE:
        return _IMAGE_CACHE[query_original]
    
    query_limpa = _limpar_query(query_original)
    palavras_limpas = query_limpa.split()
    palavras_originais = query_original.split()

    # Cria uma lista de possíveis buscas, da mais específica para a mais genérica
    candidatos_de_busca = []
    candidatos_de_busca.append(f'"{query_original}" receita')
    
    if query_limpa:
        candidatos_de_busca.append(f"{query_limpa} prato")
    
    if len(palavras_originais) >= 3:
        candidatos_de_busca.append(" ".join(palavras_originais[:3]))
        
    if len(palavras_limpas) >= 2:
        candidatos_de_busca.append(" ".join(palavras_limpas[:2]))

    if len(palavras_originais) >= 2:
        candidatos_de_busca.append(" ".join(palavras_originais[:2]))
    
    # Remove buscas duplicadas, mantendo a ordem
    queries_unicas = list(dict.fromkeys(candidatos_de_busca))

    # Tenta cada busca da lista até encontrar uma imagem
    for i, query in enumerate(queries_unicas):
        print(f"Busca Nível {i+1} para '{query_original}': Usando query '{query}'")
        imagem_url = _buscar_na_api(query)
        if imagem_url:
            print(f"-> Sucesso na busca Nível {i+1}!")
            _IMAGE_CACHE[query_original] = imagem_url
            return imagem_url

    print(f"Nenhuma imagem encontrada para a query original: '{query_original}'")
    _IMAGE_CACHE[query_original] = None
    return None