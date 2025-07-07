from flask import jsonify, request, Blueprint
from backend.services.gemini import modelo
from backend.utils.promptConfig import construir_prompt_com_settings
from backend.core.database import db
from backend.core.models import ApiCall

receitaBp = Blueprint("receita", __name__)
refinarReceitaBp = Blueprint("refinar_receita", __name__)

@receitaBp.route("/api/receitas", methods=["POST"])
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