from flask import jsonify, request, Blueprint
from backend.services.gemini import modelo
from backend.utils.promptConfig import construir_prompt_com_settings
from backend.core.database import db
from backend.core.models import ApiCall

pesquisarBp = Blueprint("pesquisar", __name__)

@pesquisarBp.route("/api/pesquisar", methods=["POST"])
def pesquisar_receita():
    data = request.json
    nome_receita = data.get("nome_receita", "").strip()
    settings = data.get("settings", {})

    if not nome_receita:
        return jsonify({"erro": "Nome da receita não informado."}), 400

    prompt_base = f"""Quero a receita de: {nome_receita}. Apresente de forma clara, usando markdown."""

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