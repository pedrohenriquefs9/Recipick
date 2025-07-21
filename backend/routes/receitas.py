from flask import jsonify, request, Blueprint
import json
import traceback
import re
from backend.services.gemini import modelo, generation_config
from backend.services.image_search import buscar_imagem_receita
from backend.utils.promptConfig import construir_prompt_com_settings
from backend.core.database import db
from backend.core.models import ApiCall

receitaBp = Blueprint("receita", __name__)
refinarReceitaBp = Blueprint("refinar_receita", __name__)


def adicionar_imagens_as_receitas(receitas_obj):
    """Função auxiliar para iterar e adicionar URLs de imagem a cada receita."""
    if 'receitas' in receitas_obj and isinstance(receitas_obj.get('receitas'), list):
        for receita in receitas_obj['receitas']:
            if 'titulo' in receita:
                imagem_url = buscar_imagem_receita(receita['titulo'])
                receita['imagemUrl'] = imagem_url
    return receitas_obj


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
    Gere um objeto JSON com a chave "receitas". O valor dessa chave DEVE ser uma lista contendo EXATAMENTE 5 sugestões de receitas **{estilo_desc}**.
    O JSON de saída deve seguir exatamente este schema:
    {{
      "receitas": [
        {{
          "titulo": "string",
          "inspiracao": "string (uma frase curta e atrativa sobre a receita)",
          "tempoDePreparoEmMin": "integer",
          "porcoes": "integer",
          "ingredientes": [
            {{"nome": "string", "quantidade": "string", "unidadeMedida": "string"}}
          ],
          "preparo": ["string (uma lista com os passos do modo de preparo. Cada passo deve ser uma frase completa, detalhada e explicativa.)"]
        }}
      ]
    }}
    """
    prompt_final = construir_prompt_com_settings(prompt_base, settings)
    
    try:
        resposta_ia = modelo.generate_content(prompt_final, generation_config=generation_config)
        resposta_texto = resposta_ia.text.strip()
        dados_receitas = json.loads(resposta_texto)

        dados_receitas_com_imagens = adicionar_imagens_as_receitas(dados_receitas)

        try:
            new_call = ApiCall(endpoint=request.path, prompt=prompt_final, response_text=json.dumps(dados_receitas_com_imagens))
            db.session.add(new_call)
            db.session.commit()
        except Exception as e:
            print(f"Erro ao salvar histórico em /api/receitas: {e}")

        return jsonify(dados_receitas_com_imagens)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"erro": f"Ocorreu um erro: {str(e)}"}), 500


@refinarReceitaBp.route("/api/refinar-receitas", methods=["POST"])
def refinar_receitas():
    data = request.json
    historico = data.get("historico", [])
    ingredientes_atuais = data.get("ingredientes", [])

    if not historico:
        return jsonify({"erro": "O histórico de mensagens não foi informado."}), 400

    prompt_conversation = []
    for message in historico:
        if message.get('type') == 'recipe-carousel':
            prompt_conversation.append(f"**Assistant:** [Exibi uma lista de receitas]")
        else:
            prompt_conversation.append(f"**{message['role'].capitalize()}:** {message['content']}")

    historico_formatado = "\n".join(prompt_conversation)
    
    schema_exemplo = """
    {{
      "receitas": [
        {{
          "titulo": "string",
          "inspiracao": "string (uma frase curta e atrativa sobre a receita)",
          "tempoDePreparoEmMin": "integer",
          "porcoes": "integer",
          "ingredientes": [
            {{"nome": "string", "quantidade": "string", "unidadeMedida": "string"}}
          ],
          "preparo": ["string (uma lista com os passos do modo de preparo. Cada passo deve ser uma frase completa, detalhada e explicativa.)"]
        }}
      ]
    }}
    """

    prompt_refinamento = f"""
Você é um assistente de culinária que gerencia uma lista de ingredientes e sugere receitas.
**Ingredientes Atuais:** {json.dumps(ingredientes_atuais)}
**Histórico da Conversa:**
{historico_formatado}
**Sua Tarefa:**
Analise a última mensagem do usuário e responda em JSON.
**Regras:**
1.  **Modificar Ingredientes:** Se o usuário pedir para **adicionar ou remover** ingredientes, sua resposta DEVE conter a chave `"ingredientes_atualizados"` com a lista de ingredientes completa e corrigida.
2.  **Gerar Receitas:** Se o usuário pedir para **gerar novas receitas**, sua resposta DEVE conter a chave `"receitas"` com uma lista de pelo menos 3 receitas baseadas nos ingredientes (seja os atuais ou os recém-modificados). Use este schema: `{schema_exemplo}`.
3.  **Conversa Simples:** Se o usuário estiver apenas conversando (ex: "olá", "obrigado"), responda com a chave `"texto"`. Ex: `{{"texto": "De nada! Posso ajudar com mais alguma coisa?"}}`.
4.  **Respostas Combinadas:** Se o usuário modificar ingredientes e pedir receitas na mesma frase (ex: "tire o queijo e me dê novas ideias"), sua resposta JSON deve conter AMBAS as chaves: `"ingredientes_atualizados"` e `"receitas"`.
**Exemplos:**
-   Usuário: "pode adicionar cebola?" -> `{{"ingredientes_atualizados": ["pão", "ovo", "queijo", "cebola"], "texto": "Cebola adicionada!"}}`
-   Usuário: "não gostei, tire o pão" -> `{{"ingredientes_atualizados": ["ovo", "queijo"], "texto": "Pão removido. Quer que eu gere novas receitas com os ingredientes restantes?"}}`
-   Usuário: "me dê outras ideias com isso" -> `{{"receitas": [...]}}`
-   Usuário: "adicione arroz e gere novas receitas" -> `{{"ingredientes_atualizados": ["pão", "ovo", "queijo", "arroz"], "receitas": [...]}}`
**Sua Resposta (JSON obrigatório):**
"""
    resposta_ia = modelo.generate_content(prompt_refinamento, generation_config=generation_config)

    try:
        new_call = ApiCall(endpoint=request.path, prompt=prompt_refinamento, response_text=resposta_ia.text)
        db.session.add(new_call)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar histórico em /api/refinar-receitas: {e}")

    try:
        json_match = re.search(r'\{[\s\S]*\}', resposta_ia.text)
        if not json_match:
            return jsonify({"texto": resposta_ia.text})

        json_string = json_match.group(0)
        dados_json = json.loads(json_string)

        if 'receitas' in dados_json:
            dados_json_com_imagens = adicionar_imagens_as_receitas(dados_json)
            return jsonify(dados_json_com_imagens)
        
        return jsonify(dados_json)
    except Exception as e:
        print(f"ERRO: Falha ao parsear JSON da IA. Erro: {e}")
        print(f"Resposta da IA: {resposta_ia.text}")
        return jsonify({"texto": "Desculpe, tive um problema para processar sua solicitação. Você poderia tentar de outra forma?"})