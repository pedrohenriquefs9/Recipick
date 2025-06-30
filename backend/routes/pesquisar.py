from flask import Flask, app, jsonify, request
from flask_cors import CORS
from backend.services.gemini import modelo
from backend.utils.promptConfig import construir_prompt_com_settings
import os

DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")
CORS(app)

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
