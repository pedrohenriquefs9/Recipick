import requests
import os
from backend.services.gemini import modelo

# Cache para armazenar URLs de imagens e evitar buscas repetidas.
_IMAGE_CACHE = {}

# Lista de categorias disponíveis na Foodish API
CATEGORIAS_FOODISH = ["biryani", "burger", "butter-chicken", "dessert", "dosa", "idly", "pasta", "pizza", "rice", "samosa"]

def _mapear_receita_para_categoria(titulo_receita: str) -> str:
    """
    Usa o Gemini Pro para mapear o título de uma receita para a categoria mais relevante da Foodish API.
    """
    prompt = f"""
    Sua única tarefa é classificar o título da receita a seguir em uma das categorias disponíveis.
    As categorias são: {", ".join(CATEGORIAS_FOODISH)}.

    Analise o título e retorne APENAS o nome exato da categoria mais apropriada.
    Se nenhuma categoria parecer adequada, retorne "burger" como um padrão seguro.

    Exemplo de entrada: "Lasanha à Bolonhesa"
    Exemplo de saída: pasta

    Exemplo de entrada: "Cheesecake de Morango"
    Exemplo de saída: dessert

    Título da receita: "{titulo_receita}"
    """
    try:
        resposta_ia = modelo.generate_content(prompt)
        categoria = resposta_ia.text.strip().lower()
        # Garante que a resposta da IA seja uma das categorias válidas
        return categoria if categoria in CATEGORIAS_FOODISH else "burger"
    except Exception as e:
        print(f"ERRO ao mapear categoria com IA para '{titulo_receita}': {e}")
        return "burger" # Retorna um padrão em caso de erro

def buscar_imagem_receita(titulo_receita: str):
    """
    Busca uma imagem de receita na Foodish API, mapeando o título para uma categoria relevante.
    """
    if not titulo_receita or not isinstance(titulo_receita, str):
        return None

    # Usa o título como chave do cache para evitar reprocessamento
    if titulo_receita in _IMAGE_CACHE:
        return _IMAGE_CACHE[titulo_receita]

    print(f"Mapeando categoria para a receita: '{titulo_receita}'")
    categoria = _mapear_receita_para_categoria(titulo_receita)
    print(f"-> Categoria definida pela IA: '{categoria}'")

    url_api = f"https://foodish-api.com/api/images/{categoria}/"

    try:
        response = requests.get(url_api, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        imagem_url = data.get("image")
        
        if imagem_url:
            print(f"-> Sucesso! Imagem encontrada para '{titulo_receita}'")
            _IMAGE_CACHE[titulo_receita] = imagem_url
            return imagem_url
        else:
            raise ValueError("A resposta da API Foodish não continha uma URL de imagem.")

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Erro na chamada da API Foodish para categoria '{categoria}': {e}")
        _IMAGE_CACHE[titulo_receita] = None
        return None