from flask import request, jsonify, json, Blueprint
from backend.services.gemini import modelo
from backend.core.database import db
from backend.core.models import ApiCall

# Cria um Blueprint para esta rota
normalizarBp = Blueprint("normalizar", __name__)

@normalizarBp.route("/api/normalizar-ingredientes", methods=["POST"])
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
        resposta = modelo.generate_content(prompt)
        lista_str = resposta.text.strip().replace("`", "").replace("json", "").strip()
        lista_normalizada = json.loads(lista_str)

        try:
            new_call = ApiCall(
                endpoint=request.path,
                prompt=prompt,
                response_text=resposta.text
            )
            db.session.add(new_call)
            db.session.commit()
        except Exception as e:
            print(f"Erro ao salvar histórico em /api/normalizar-ingredientes: {e}")

        return jsonify({"ingredientes_normalizados": lista_normalizada})
    except Exception as e:
        print(f"Erro ao normalizar/parsear JSON da IA: {e}")
        return jsonify({"ingredientes_normalizados": ingredientes_brutos})
