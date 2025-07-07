from flask import jsonify, request, Blueprint
import json
import traceback
from backend.services.gemini import modelo, generation_config
from backend.utils.promptConfig import construir_prompt_com_settings
from backend.core.database import db
from backend.core.models import ApiCall

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
    resposta = modelo.generate_content(prompt_final)

    try:
        new_call = ApiCall(
            endpoint=request.path,
            prompt=prompt_final,
            response_text=resposta.text
        )
        db.session.add(new_call)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar histórico em /api/pesquisar: {e}")

    return jsonify({"receita": resposta.text})