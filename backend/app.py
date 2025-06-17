from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Configuração Inicial
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
modelo = genai.GenerativeModel("gemini-1.5-flash")

# Definição de Caminhos
DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")
CORS(app)

def construir_prompt_com_settings(base_prompt, settings):
    if not settings:
        return base_prompt

    instrucoes_adicionais = []
    portion_map = { 'pequeno': 'uma porção pequena (individual)', 'medio': 'uma porção média (2 pessoas)', 'grande': 'uma porção grande (4+ pessoas)'}
    complexity_map = { 'rapida': 'uma receita rápida e simples (até 30 min)', 'elaborada': 'uma receita mais elaborada e detalhada' }
    style_map = { 'popular': 'popular e clássica', 'criativo': 'criativa e inusitada' } # Textos um pouco mais diretos

    instrucoes_adicionais.append(f"- A receita deve ser para {portion_map.get(settings.get('portionSize'), 'uma porção média')}.")
    instrucoes_adicionais.append(f"- Deve ser {complexity_map.get(settings.get('complexity'), 'rápida e simples')}.")
    
    estilo_selecionado = style_map.get(settings.get('style'), 'criativa e inusitada')
    instrucoes_adicionais.append(f"- O estilo da receita DEVE ser: {estilo_selecionado}.")

    if settings.get('isVegetarian'):
        instrucoes_adicionais.append("- A receita DEVE ser estritamente vegetariana (sem nenhum tipo de carne, incluindo peixes e frutos do mar).")
    
    restrictions = settings.get('restrictions')
    if restrictions and restrictions.strip():
        instrucoes_adicionais.append(f"- A receita NÃO PODE conter os seguintes ingredientes sob nenhuma hipótese: {restrictions.strip()}.")

    prompt_final = f"{base_prompt}\n\nLeve em consideração as seguintes preferências do usuário ao gerar as receitas:\n" + "\n".join(instrucoes_adicionais)
    return prompt_final

@app.route("/api/normalizar-ingredientes", methods=["POST"])
def normalizar_ingredientes():
    data = request.json
    ingredientes_brutos = data.get("ingredientes", [])
    if not ingredientes_brutos:
        return jsonify({"ingredientes_normalizados": []})

    prompt = f"""
    Você é um especialista em culinária. Sua única tarefa é normalizar e corrigir a seguinte lista de nomes de ingredientes para sua forma mais comum e correta em português do Brasil.

    Regras:
    1. Corrija erros de digitação e acentuação (ex: "cenora" -> "cenoura", "feijaox" -> "feijão").
    2. Padronize o nome, removendo detalhes excessivos (ex: "Tomate italiano maduro" -> "tomate").
    3. Se um item não for um ingrediente culinário reconhecível, retorne uma string vazia "" no lugar dele.
    4. Sua resposta deve ser APENAS uma lista JSON de strings, sem nenhum texto adicional, markdown ou explicação. A ordem e a quantidade de itens na lista de saída devem ser as mesmas da lista de entrada.

    Exemplo de Entrada: ["feijaox", "cebola roxa", "Qeijo", "asdfgh"]
    Sua Saída: ["feijão", "cebola roxa", "queijo", ""]

    ---
    Lista de ingredientes para normalizar: {json.dumps(ingredientes_brutos)}
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

    prompt_base = f"""Você é um assistente de receitas criativas. O usuário informou os seguintes ingredientes: {ingredientes}.

Tarefa:
- Corrija erros nos nomes dos ingredientes.
- Liste os ingredientes corrigidos como lista com `-`.
- Sugira 3 receitas criativas usando apenas os ingredientes informados.
  - Use pelo menos 3 frases no modo de preparo, com instruções úteis.
- Sugira 2 ingredientes extras que combinariam bem.
- Para cada novo ingrediente, sugira 1 nova receita.

 Formato obrigatório:
- Use apenas **markdown puro** (sem emojis).
- Não use espaçamentos desnecessários entre blocos.
- Separe visualmente apenas com `---` (linha horizontal simples).
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

    prompt_base = f"""Quero a receita de: {nome_receita}.
Apresente de forma clara, usando markdown sem emojis.

**Nome da Receita**
**Ingredientes:**
- item
**Modo de preparo:**
- passo 1
"""

    prompt_final = construir_prompt_com_settings(prompt_base, settings)
    resposta = modelo.generate_content(prompt_final)
    return jsonify({"receita": resposta.text})

# Rotas para servir o frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)