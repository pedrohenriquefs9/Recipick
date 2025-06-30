from flask import Flask, app, jsonify, request
from flask_cors import CORS
import os
from backend.services.gemini import modelo
from backend.utils.promptConfig import construir_prompt_com_settings

DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")
CORS(app)

@app.route("/api/receitas", methods=["POST"])
def gerar_receitas():
    data = request.json
    ingredientes = data.get("ingredientes", "").strip()
    settings = data.get("settings", {})

    if not ingredientes:
        return jsonify({"erro": "Nenhum ingrediente informado."}), 400

    style = settings.get('style', 'criativo')

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