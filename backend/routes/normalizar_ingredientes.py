from flask import request, jsonify, json, Blueprint
from backend.services.gemini import modelo, generation_config
from backend.core.database import db
from backend.core.models import ApiCall

normalizarBp = Blueprint("normalizar", __name__)

# CORREÇÃO: Removido o prefixo /api/. O endereço agora é relativo ao blueprint.
@normalizarBp.route("/normalizar-ingredientes", methods=["POST"])
def normalizar_ingredientes():
    data = request.json or {}
    ingredientes_brutos = data.get("ingredientes", [])
    if not ingredientes_brutos:
        return jsonify({"ingredientes_normalizados": []})

    prompt = f"""
    Sua única tarefa é normalizar e corrigir a seguinte lista de nomes de ingredientes para sua forma mais comum e correta em português do Brasil.
    Regras:
    1. Corrija erros (ex: "feijaox" -> "feijão").
    2. Padronize o nome (ex: "Tomate italiano maduro" -> "tomate").
    3. Se um item não for um ingrediente, retorne uma string vazia "".
    4. Sua resposta deve ser APENAS um objeto JSON com a chave "ingredientes_normalizados", contendo uma lista de strings.

    Exemplo de Entrada: ["feijaox", "cebola roxa", "Qeijo", "asdfgh"]
    Sua Saída: {{"ingredientes_normalizados": ["feijão", "cebola roxa", "queijo", ""]}}
    ---
    Lista de ingredientes para normalizar: {json.dumps(ingredientes_brutos)}
    """

    try:
        resposta = modelo.generate_content(prompt, generation_config=generation_config)
        resposta_texto = resposta.text.strip()
        dados_normalizados = json.loads(resposta_texto)

        # A lógica para salvar no histórico deve ser adicionada aqui se necessário
        # Ex: new_call = ApiCall(...)
        #     db.session.add(new_call)
        #     db.session.commit()

        return jsonify(dados_normalizados)
        
    except Exception as e:
        print(f"Erro ao normalizar/parsear JSON da IA: {e}")
        return jsonify({"ingredientes_normalizados": ingredientes_brutos})