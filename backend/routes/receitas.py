from flask import jsonify, request, Blueprint
import json
import traceback
from backend.services.gemini import modelo, generation_config
from backend.utils.promptConfig import construir_prompt_com_settings

# Cria um Blueprint para esta rota
receitaBp = Blueprint("receita", __name__)

@receitaBp.route("/api/receitas", methods=["POST"])
def gerar_receitas():
    data = request.json or {}
    ingredientes = data.get("ingredientes", "").strip()
    settings = data.get("settings", {})

    if not ingredientes:
        return jsonify({"erro": "Nenhum ingrediente informado."}), 400

    style = settings.get('style', 'criativo')
    estilo_desc = "criativas e surpreendentes" if style == 'criativo' else "populares e clássicas"

    prompt_base = f"""
    Sua única tarefa é criar receitas em formato JSON.
    Com base nos ingredientes: **{ingredientes}**.
    Gere um objeto JSON com a chave "receitas", que é uma lista de 3 receitas **{estilo_desc}**.

    O JSON de saída deve seguir exatamente este schema:
    {{
      "receitas": [
        {{
          "titulo": "string",
          "tempoDePreparoEmMin": "integer",
          "porcoes": "integer",
          "ingredientes": [
            {{"nome": "string", "quantidade": "string", "unidadeMedida": "string"}}
          ],
          "preparo": ["string"]
        }}
      ]
    }}
    """

    prompt_final = construir_prompt_com_settings(prompt_base, settings)

    try:
        resposta = modelo.generate_content(prompt_final, generation_config=generation_config)
        dados_receita = json.loads(resposta.text)
        return jsonify(dados_receita)
    except Exception as e:
        print(f"--- ERRO NA ROTA /api/receitas ---\nErro: {e}")
        traceback.print_exc()
        return jsonify({"erro": "Ocorreu um erro ao gerar as receitas. Tente novamente."}), 500
