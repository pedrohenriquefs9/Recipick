from flask import jsonify, request, Blueprint
import json
import traceback
from backend.services.gemini import modelo, generation_config
from backend.utils.promptConfig import construir_prompt_com_settings
from backend.core.database import db
from backend.core.models import ApiCall

# Cria um Blueprint para esta rota
receitaBp = Blueprint("receita", __name__)
refinarReceitaBp = Blueprint("refinar_receita", __name__)

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
        print(f"Erro ao salvar histórico em /api/receitas: {e}")

    return jsonify({"receitas": resposta.text})

@refinarReceitaBp.route("/api/refinar-receitas", methods=["POST"])
def refinar_receitas():
    data = request.json
    historico = data.get("historico", [])

    if not historico:
        return jsonify({"erro": "O histórico de mensagens não foi informado."}), 400

    # Constrói o histórico para o prompt
    prompt_conversation = []
    for message in historico:
        prompt_conversation.append(f"**{message['role'].capitalize()}:** {message['content']}")

    historico_formatado = "\n".join(prompt_conversation)

    prompt_refinamento = f"""
Você é um assistente de culinária. Continue a conversa com base no histórico abaixo.
Se o usuário pedir algo que não seja relacionado a culinária, recuse educadamente.
Responda de forma útil e criativa, mantendo o contexto da conversa.

**Histórico da Conversa:**
{historico_formatado}

**Sua Resposta:**
"""

    resposta = modelo.generate_content(prompt_refinamento)

    try:
        new_call = ApiCall(
            endpoint=request.path,
            prompt=prompt_refinamento,
            response_text=resposta.text
        )
        db.session.add(new_call)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar histórico em /api/refinar-receitas: {e}")

    return jsonify({"receitas": resposta.text})