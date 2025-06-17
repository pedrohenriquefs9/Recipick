from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
modelo = genai.GenerativeModel("gemini-1.5-flash")

DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")
CORS(app)

def construir_prompt_com_settings(base_prompt, settings):
    if not settings:
        return base_prompt

    instrucoes_adicionais = []
    portion_map = { 'pequeno': 'uma porção pequena (individual)', 'medio': 'uma porção média (2 pessoas)', 'grande': 'uma porção grande (4+ pessoas)'}
    complexity_map = { 'rapida': 'uma receita rápida e simples (até 30 min)', 'elaborada': 'uma receita mais elaborada e detalhada' }
    
    instrucoes_adicionais.append(f"- A receita deve ser para {portion_map.get(settings.get('portionSize'), 'uma porção média')}.")
    instrucoes_adicionais.append(f"- Deve ser {complexity_map.get(settings.get('complexity'), 'rápida e simples')}.")

    if settings.get('isVegetarian'):
        instrucoes_adicionais.append("- A receita DEVE ser estritamente vegetariana (sem nenhum tipo de carne, incluindo peixes e frutos do mar).")
    
    restrictions = settings.get('restrictions')
    if restrictions and restrictions.strip():
        instrucoes_adicionais.append(f"- A receita NÃO PODE conter os seguintes ingredientes sob nenhuma hipótese: {restrictions.strip()}.")

    # Adiciona as instruções apenas se houver alguma
    if instrucoes_adicionais:
      prompt_final = f"{base_prompt}\n\nLeve em consideração também as seguintes preferências do usuário ao gerar as receitas:\n" + "\n".join(instrucoes_adicionais)
      return prompt_final
    
    return base_prompt

@app.route("/api/normalizar-ingredientes", methods=["POST"])
def normalizar_ingredientes():
    data = request.json
    ingredientes_brutos = data.get("ingredientes", [])
    if not ingredientes_brutos:
        return jsonify({"ingredientes_normalizados": []})
    prompt = f"""
    Sua única tarefa é normalizar e corrigir a seguinte lista de nomes de ingredientes para sua forma mais comum e correta em português do Brasil.
    Regras:
    1. Corrija erros (ex: "feijaox" -> "feijão").
    2. Padronize o nome (ex: "Tomate italiano maduro" -> "tomate").
    3. Se um item não for um ingrediente, retorne uma string vazia "".
    4. Sua resposta deve ser APENAS uma lista JSON de strings.
    Exemplo de Entrada: ["feijaox", "cebola roxa", "Qeijo", "asdfgh"]
    Sua Saída: ["feijão", "cebola roxa", "queijo", ""]
    ---
    Lista: {json.dumps(ingredientes_brutos)}
    """
    try:
        resposta = modelo.generate_content(prompt)
        lista_str = resposta.text.strip().replace("`", "").replace("json", "").strip()
        lista_normalizada = json.loads(lista_str)
        return jsonify({"ingredientes_normalizados": lista_normalizada})
    except Exception as e:
        print(f"Erro ao normalizar ingredientes: {e}")
        return jsonify({"ingredientes_normalizados": ingredientes_brutos})

@app.route("/api/receitas", methods=["POST"])
def gerar_receitas():
    data = request.json
    ingredientes = data.get("ingredientes", "").strip()
    settings = data.get("settings", {})
    
    if not ingredientes:
        return jsonify({"erro": "Nenhum ingrediente informado."}), 400

    style = settings.get('style', 'criativo') # Padrão é 'criativo'

    if style == 'popular':
        prompt_base = f"""Você é um assistente de culinária focado em receitas **populares e clássicas**. Com base nos ingredientes: {ingredientes}.

Tarefa:
- Sugira 3 receitas **conhecidas e tradicionais** que usem esses ingredientes. Foque no que é familiar e amado pelo público.
- Corrija e liste os ingredientes informados.
- Use um modo de preparo claro e direto.
- Sugira 2 ingredientes extras que combinariam bem com os pratos.
- Para cada novo ingrediente, sugira 1 nova receita popular.

Formato obrigatório:
- Use apenas **markdown puro** (sem emojis).
- Separe visualmente apenas com `---`.
"""
    else: # Estilo criativo (padrão)
        prompt_base = f"""Você é um assistente de receitas **criativas e ousadas**. Com base nos ingredientes: {ingredientes}.

Tarefa:
- Sugira 3 receitas **criativas e surpreendentes** usando os ingredientes informados, incentivando combinações inusitadas.
- Corrija e liste os ingredientes informados.
- Use um modo de preparo inspirador.
- Sugira 2 ingredientes extras que elevariam o nível dos pratos.
- Para cada novo ingrediente, sugira 1 nova receita criativa.

Formato obrigatório:
- Use apenas **markdown puro** (sem emojis).
- Separe visualmente apenas com `---`.
"""
    
    prompt_final = construir_prompt_com_settings(prompt_base, settings)
    resposta = modelo.generate_content(prompt_final)
    return jsonify({"receitas": resposta.text})

@app.route("/api/pesquisar", methods=["POST"])
def pesquisar_receita():
    data = request.json
    nome_receita = data.get("nome_receita", "").strip()
    settings = data.get("settings", {})
    
    if not nome_receita:
        return jsonify({"erro": "Nome da receita não informado."}), 400

    prompt_base = f"""Quero a receita de: {nome_receita}. Apresente de forma clara, usando markdown."""
    
    prompt_final = construir_prompt_com_settings(prompt_base, settings)
    resposta = modelo.generate_content(prompt_final)
    return jsonify({"receita": resposta.text})

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)