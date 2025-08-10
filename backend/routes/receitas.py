from flask import jsonify, request, Blueprint
import json
import re
import concurrent.futures
from backend.services.gemini import modelo, generation_config
from backend.services.image_search import buscar_imagem_receita
from backend.utils.promptConfig import construir_prompt_com_settings
from backend.core.database import db
from backend.core.models import Chat, Message
from flask_login import login_required, current_user

receitaBp = Blueprint("receita", __name__)
refinarReceitaBp = Blueprint("refinar_receita", __name__)

@receitaBp.route("/buscar-imagem", methods=["POST"])
@login_required
def buscar_imagem_endpoint():
    data = request.json or {}
    titulo = data.get("titulo")
    if not titulo:
        return jsonify({"error": "Nenhum título fornecido."}), 400
    
    image_url = buscar_imagem_receita(titulo)
    
    if image_url:
        return jsonify({"imageUrl": image_url})
    else:
        return jsonify({"error": "Imagem não encontrada."}), 404

def validar_receitas_da_ia(dados_receitas):
    if 'receitas' not in dados_receitas or not isinstance(dados_receitas['receitas'], list):
        raise ValueError("A IA não retornou uma lista de receitas válida.")
    for receita in dados_receitas['receitas']:
        required_keys = ['titulo', 'ingredientes', 'preparo']
        if not isinstance(receita, dict) or not all(k in receita for k in required_keys):
            raise ValueError("A IA retornou uma receita com formato inválido.")
    return dados_receitas

@receitaBp.route("/receitas", methods=["POST"])
@login_required
def gerar_receitas():
    data = request.json or {}
    chat_id_str = data.get("chatId")
    ingredientes = data.get("ingredientes", "").strip()
    settings = data.get("settings", {})
    user_message_data = data.get("userMessage")

    if not ingredientes or not user_message_data:
        return jsonify({"erro": "Dados insuficientes para gerar receita."}), 400

    chat = Chat.query.get(chat_id_str) if chat_id_str and not str(chat_id_str).startswith('local-') else None
    
    if not chat:
        titulo_chat_inicial = user_message_data['content'][:50] if user_message_data else "Novo Pedido"
        chat = Chat(user_id=current_user.id, title=titulo_chat_inicial, settings=settings)
        db.session.add(chat)
        db.session.flush()

    user_message = Message(chat_id=chat.id, role=user_message_data['role'], content=user_message_data['content'], type=user_message_data['type'])
    db.session.add(user_message)
    
    style = settings.get('style', 'criativo')
    estilo_desc = "criativas e surpreendentes" if style == 'criativo' else "populares e clássicas"
    
    prompt_base = f"""
    Sua tarefa é gerar uma resposta JSON com uma lista de receitas com base nos ingredientes: **{ingredientes}**.
    O JSON de saída deve ter UMA chave no nível raiz: "receitas".
    O valor de "receitas" deve ser uma lista de EXATAMENTE 5 sugestões de receitas {estilo_desc}.
    Cada objeto na lista "receitas" DEVE seguir este schema:
    {{
        "titulo": "string",
        "inspiracao": "string",
        "tempoDePreparoEmMin": "integer",
        "porcoes": "integer",
        "ingredientes": [{{ "nome": "string", "quantidade": "string", "unidadeMedida": "string" }}],
        "preparo": ["string"]
    }}
    """
    prompt_final = construir_prompt_com_settings(prompt_base, settings)
    
    try:
        resposta_ia = modelo.generate_content(prompt_final, generation_config=generation_config)
        resposta_texto = resposta_ia.text.strip()
        json_match = re.search(r'\{[\s\S]*\}', resposta_texto)
        if not json_match: raise ValueError("A resposta da IA não continha um bloco JSON válido.")
        
        dados_receitas = json.loads(json_match.group(0))
        dados_receitas_validados = validar_receitas_da_ia(dados_receitas)
        
        if str(chat_id_str).startswith('local-'):
            titulo_chat = dados_receitas_validados['receitas'][0]['titulo'] if dados_receitas_validados['receitas'] else chat.title
            chat.title = titulo_chat
            
        assistant_message = Message(chat_id=chat.id, role='assistant', content=json.dumps(dados_receitas_validados['receitas']), type='recipe-carousel')
        db.session.add(assistant_message)
        db.session.commit()

        return jsonify({
            "chatId": chat.id,
            "chatTitle": chat.title,
            "assistantMessage": {
                "id": assistant_message.id,
                "role": 'assistant',
                "content": assistant_message.content,
                "type": 'recipe-carousel'
            }
        })
    except Exception as e:
        db.session.rollback()
        print(f"ERRO ao processar e salvar receita: {e}")
        return jsonify({"erro": f"Ocorreu um erro interno: {str(e)}"}), 500

@refinarReceitaBp.route("/refinar-receitas", methods=["POST"])
@login_required
def refinar_receitas():
    data = request.json
    chat_id = data.get("chatId")
    historico = data.get("historico", [])
    ingredientes_atuais = data.get("ingredientes", [])
    user_message_data = data.get("userMessage")

    if not all([chat_id, historico, user_message_data]):
        return jsonify({"erro": "Dados insuficientes para refinar a receita."}), 400

    chat = Chat.query.get(chat_id)
    if not chat or chat.user_id != current_user.id:
        return jsonify({"erro": "Chat não encontrado ou não autorizado."}), 404
        
    user_message = Message(chat_id=chat.id, role=user_message_data['role'], content=user_message_data['content'], type=user_message_data['type'])
    db.session.add(user_message)

    prompt_conversation = [f"**{ 'model' if msg['role'] == 'assistant' else 'user' }:** {'[O assistente exibiu uma lista de receitas]' if msg.get('type') == 'recipe-carousel' else msg['content']}" for msg in historico]
    historico_formatado = "\n".join(prompt_conversation)
    
    schema_exemplo = """
    {{
      "titulo": "string",
      "inspiracao": "string", "tempoDePreparoEmMin": "integer",
      "porcoes": "integer", "ingredientes": [{{ "nome": "string", "quantidade": "string", "unidadeMedida": "string" }}],
      "preparo": ["string"]
    }}
    """

    prompt_refinamento = f"""
    Sua tarefa é analisar a última mensagem do usuário e decidir a ação correta, respondendo em JSON.
    **Ingredientes Atuais:** {json.dumps(ingredientes_atuais)}
    **Histórico da Conversa:**
{historico_formatado}
    
    **Regras de Decisão:**
    1.  Se o usuário pedir para **adicionar/remover ingredientes**, sua resposta DEVE conter a chave `"ingredientes_atualizados"`.
    2.  Se o usuário pedir por **novas receitas**, sua resposta DEVE conter a chave `"receitas"`.
        - A lista de receitas DEVE ter **pelo menos 3 sugestões**.
        - Cada objeto na lista DEVE seguir este schema: `{schema_exemplo}`.
    3.  Se a mensagem for uma **conversa simples** (ex: "gostei"), responda APENAS com a chave `"texto"`.
    4.  Se o usuário fizer as duas coisas (ex: "adicione tomate e gere novas receitas"), inclua ambas as chaves.
    5.  **IMPORTANTE:** O JSON final DEVE ser sintaticamente perfeito.

    **Sua Resposta (APENAS JSON VÁLIDO):**
    """
    
    resposta_texto = ""
    try:
        resposta_ia = modelo.generate_content(prompt_refinamento, generation_config=generation_config)
        resposta_texto = resposta_ia.text.strip()
        json_match = re.search(r'\{[\s\S]*\}', resposta_texto)
        if not json_match: raise ValueError("A resposta da IA para o refinamento não continha JSON.")
        
        json_string = json_match.group(0)
        dados_json = json.loads(json_string)

        if 'texto' in dados_json:
            assistant_text = Message(chat_id=chat.id, role='assistant', content=dados_json['texto'], type='text')
            db.session.add(assistant_text)
        
        if 'receitas' in dados_json:
            assistant_recipes = Message(chat_id=chat.id, role='assistant', content=json.dumps(dados_json['receitas']), type='recipe-carousel')
            db.session.add(assistant_recipes)
            
        db.session.commit()
        return jsonify(dados_json)
    except Exception as e:
        db.session.rollback()
        print(f"ERRO ao processar e salvar refinamento: {e}")
        print("--- RESPOSTA DA IA QUE CAUSOU O ERRO ---")
        print(resposta_texto)
        print("------------------------------------")
        return jsonify({"erro": f"Ocorreu um erro interno: {str(e)}"}), 500