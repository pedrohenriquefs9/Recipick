from flask import jsonify, request, Blueprint
import json
import traceback
import re
from backend.services.gemini import modelo, generation_config
from backend.services.image_search import buscar_imagem_receita
from backend.utils.promptConfig import construir_prompt_com_settings
from backend.core.database import db
from backend.core.models import ApiCall
from flask_login import login_required, current_user

receitaBp = Blueprint("receita", __name__)
refinarReceitaBp = Blueprint("refinar_receita", __name__)


def adicionar_imagens_as_receitas(receitas_obj):
    if 'receitas' in receitas_obj and isinstance(receitas_obj.get('receitas'), list):
        for receita in receitas_obj['receitas']:
            if 'titulo' in receita:
                imagem_url = buscar_imagem_receita(receita['titulo'])
                receita['imagemUrl'] = imagem_url
    return receitas_obj


@receitaBp.route("/receitas", methods=["POST"])
@login_required
def gerar_receitas():
    data = request.json or {}
    ingredientes = data.get("ingredientes", "").strip()
    settings = data.get("settings", {})
    resposta_texto = "" # Inicializa para o bloco finally

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
        
        json_match = re.search(r'\{[\s\S]*\}', resposta_texto)
        if not json_match:
            raise ValueError("A resposta da IA não continha um bloco JSON válido.")
        
        json_string = json_match.group(0)
        dados_receitas = json.loads(json_string)

        if 'receitas' not in dados_receitas or not isinstance(dados_receitas['receitas'], list) or not dados_receitas['receitas']:
            raise ValueError("A IA não retornou uma lista de receitas válida.")
        
        dados_receitas_com_imagens = adicionar_imagens_as_receitas(dados_receitas)
        return jsonify(dados_receitas_com_imagens)

    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERRO ao processar JSON da IA: {e}")
        return jsonify({"erro": f"Ocorreu um erro ao processar a resposta da IA: {str(e)}"}), 500
    finally:
        if current_user.is_authenticated:
            new_call = ApiCall(endpoint=request.path, prompt=prompt_final, response_text=resposta_texto, user_id=current_user.id)
            db.session.add(new_call)
            db.session.commit()

# --- FUNÇÃO DE REFINAR CORRIGIDA E COMPLETA ---
@refinarReceitaBp.route("/refinar-receitas", methods=["POST"])
@login_required
def refinar_receitas():
    data = request.json
    historico = data.get("historico", [])
    ingredientes_atuais = data.get("ingredientes", [])
    resposta_texto = "" # Inicializa para o bloco finally

    if not historico:
        return jsonify({"erro": "O histórico de mensagens não foi informado."}), 400

    # LÓGICA DE PROMPT ORIGINAL RESTAURADA
    prompt_conversation = []
    for message in historico:
        if message.get('type') == 'recipe-carousel':
            prompt_conversation.append(f"**Assistant:** [Exibi uma lista de receitas]")
        else:
            prompt_conversation.append(f"**{message['role'].capitalize()}:** {message['content']}")

    historico_formatado = "\n".join(prompt_conversation)
    
    schema_exemplo = """
    {{
      "receitas": [ {{ "titulo": "string", "inspiracao": "string", ... }} ]
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
    try:
        resposta_ia = modelo.generate_content(prompt_refinamento, generation_config=generation_config)
        resposta_texto = resposta_ia.text.strip()

        json_match = re.search(r'\{[\s\S]*\}', resposta_texto)
        if not json_match:
            raise ValueError("A resposta da IA para o refinamento não continha um bloco JSON válido.")
        
        json_string = json_match.group(0)
        dados_json = json.loads(json_string)

        if 'receitas' in dados_json:
            dados_json = adicionar_imagens_as_receitas(dados_json)
        
        return jsonify(dados_json)

    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERRO ao processar JSON da IA em refinar-receitas: {e}")
        return jsonify({"erro": f"Ocorreu um erro ao processar a resposta da IA: {str(e)}"}), 500
    finally:
        if current_user.is_authenticated:
            new_call = ApiCall(endpoint=request.path, prompt=prompt_refinamento, response_text=resposta_texto, user_id=current_user.id)
            db.session.add(new_call)
            db.session.commit()