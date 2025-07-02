from flask import jsonify, request, Blueprint
import json
import traceback
from backend.services.gemini import modelo, generation_config
from backend.utils.promptConfig import construir_prompt_com_settings

# Cria um Blueprint para esta rota
pesquisarBp = Blueprint("pesquisar", __name__)

@pesquisarBp.route("/api/pesquisar", methods=["POST"])
def pesquisar_receita():
    """
    Busca uma única receita pelo nome e a retorna em formato JSON estruturado.
    """
    data = request.json or {}
    nome_receita = data.get("nome_receita", "").strip()
    settings = data.get("settings", {})

    if not nome_receita:
        return jsonify({"erro": "Nome da receita não informado."}), 400

    prompt_base = f"""
    Sua única tarefa é fornecer a receita de "{nome_receita}" em formato JSON.

    O JSON de saída deve seguir exatamente este schema para um único objeto de receita:
    {{
      "titulo": "string",
      "tempoDePreparoEmMin": "integer",
      "porcoes": "integer",
      "ingredientes": [
        {{"nome": "string", "quantidade": "string", "unidadeMedida": "string"}}
      ],
      "preparo": ["string"]
    }}
    """

    prompt_final = construir_prompt_com_settings(prompt_base, settings)

    try:
        resposta = modelo.generate_content(prompt_final, generation_config=generation_config)
        dados_receita = json.loads(resposta.text)
        # Retorna o objeto dentro de uma lista para manter o mesmo formato da outra rota
        return jsonify({"receitas": [dados_receita]})
    except Exception as e:
        print(f"--- ERRO NA ROTA /api/pesquisar ---\nErro: {e}")
        traceback.print_exc()
        return jsonify({"erro": "Ocorreu um erro ao pesquisar a receita. Tente novamente."}), 500
