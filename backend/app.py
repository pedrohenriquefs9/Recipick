from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import re
import traceback
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# --- Verificação da Chave de API ---
if not api_key:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi definida. Por favor, crie um arquivo .env e adicione sua chave.")

genai.configure(api_key=api_key)

# Configura o modelo de IA e a configuração para forçar a saída JSON
generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
modelo = genai.GenerativeModel("gemini-1.5-flash")

# Define a pasta de build do frontend para servir os arquivos estáticos
DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")

# Configuração do CORS para permitir requisições do frontend
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
CORS(app,
     origins=allowed_origins,
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

def construir_prompt_com_settings(base_prompt, settings):
    """Adiciona as configurações do usuário ao prompt base."""
    if not settings:
        return base_prompt

    instrucoes_adicionais = []
    portion_map = { 'pequeno': 'uma porção pequena (individual)', 'medio': 'uma porção média (2 pessoas)', 'grande': 'uma porção grande (4+ pessoas)'}
    complexity_map = { 'rapida': 'uma receita rápida e simples (até 30 min)', 'elaborada': 'uma receita mais elaborada e detalhada' }

    instrucoes_adicionais.append(f"- A receita deve ser para {portion_map.get(settings.get('portionSize'), 'uma porção média')}.")
    instrucoes_adicionais.append(f"- Deve ser {complexity_map.get(settings.get('complexity'), 'rápida e simples')}.")

    if settings.get('isVegetarian'):
        instrucoes_adicionais.append("- A receita DEVE ser estritamente vegetariana (sem nenhum tipo de carne, incluindo peixes e frutos do mar).")

    restrictions = settings.get('restrictions')
    if restrictions and restrictions.strip():
        instrucoes_adicionais.append(f"- A receita NÃO PODE conter os seguintes ingredientes sob nenhuma hipótese: {restrictions.strip()}.")

    if instrucoes_adicionais:
      prompt_final = f"{base_prompt}\n\nLeve em consideração também as seguintes preferências do usuário ao gerar as receitas:\n" + "\n".join(instrucoes_adicionais)
      return prompt_final

    return base_prompt

@app.before_request
def handle_preflight():
    """Lida com as requisições OPTIONS (preflight) do CORS."""
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@app.route("/api/normalizar-ingredientes", methods=["POST"])
def normalizar_ingredientes():
    """Normaliza e corrige uma lista de ingredientes usando a IA."""
    data = request.json
    ingredientes_brutos = data.get("ingredientes", [])
    if not ingredientes_brutos:
        return jsonify({"ingredientes_normalizados": []})

    prompt = f"""
    Sua única tarefa é normalizar e corrigir a seguinte lista de nomes de ingredientes para sua forma mais comum e correta em português do Brasil.
    Regras:
    1. Corrija erros (ex: "feijaox" -> "feijão").
    2. Padronize o nome (ex: "Tomate italiano maduro" -> "tomate").
    3. Se um item não for um ingrediente, retorne uma string vazia "".
    4. Sua resposta deve ser APENAS um objeto JSON com a chave "ingredientes_normalizados", que contém uma lista de strings.

    Exemplo de Entrada: ["feijaox", "cebola roxa", "Qeijo", "asdfgh"]
    Sua Saída: {{"ingredientes_normalizados": ["feijão", "cebola roxa", "queijo", ""]}}
    ---
    Lista de ingredientes para normalizar: {json.dumps(ingredientes_brutos)}
    """

    try:
        resposta = modelo.generate_content(prompt, generation_config=generation_config)
        dados_normalizados = json.loads(resposta.text)
        return jsonify(dados_normalizados)
    except Exception as e:
        print("--- ERRO NO BACKEND (normalizar-ingredientes) ---")
        print(f"Erro: {e}")
        traceback.print_exc()
        print("--- FIM DO ERRO ---")
        
        # Se a IA falhar, retorna a lista original para não quebrar o fluxo
        return jsonify({"ingredientes_normalizados": ingredientes_brutos})

@app.route("/api/receitas", methods=["POST"])
def gerar_receitas():
    """Gera uma lista de receitas em formato JSON estruturado."""
    data = request.json
    ingredientes = data.get("ingredientes", "").strip()
    settings = data.get("settings", {})

    if not ingredientes:
        return jsonify({"erro": "Nenhum ingrediente informado."}), 400

    style = settings.get('style', 'criativo')
    estilo_desc = "criativas e surpreendentes" if style == 'criativo' else "populares e clássicas"

    prompt_base = f"""
    Você é um assistente de culinária especialista em gerar dados estruturados.
    Sua única tarefa é criar receitas em formato JSON.

    Com base nos ingredientes informados pelo usuário: **{ingredientes}**.

    **Tarefa:**
    Gere um objeto JSON contendo uma chave "receitas", que é uma lista de 3 receitas **{estilo_desc}**.

    **Estrutura Obrigatória do JSON:**
    O JSON de saída deve seguir exatamente este schema:
    {{
      "receitas": [
        {{
          "titulo": "string",
          "tempoDePreparoEmMin": "integer",
          "porcoes": "integer",
          "ingredientes": [
            {{
              "nome": "string",
              "quantidade": "string",
              "unidadeMedida": "string"
            }}
          ],
          "preparo": ["string"]
        }}
      ]
    }}
    """

    prompt_final = construir_prompt_com_settings(prompt_base, settings)

    try:
        resposta = modelo.generate_content(prompt_final, generation_config=generation_config)
        dados_receita = json.loads(resposta.text)
        return jsonify(dados_receita)
    except Exception as e:
        print("--- ERRO NO BACKEND (gerar_receitas) ---")
        print(f"Erro: {e}")
        traceback.print_exc()
        print("--- FIM DO ERRO ---")
        return jsonify({"erro": "Ocorreu um erro ao gerar as receitas. Tente novamente."}), 500


@app.route("/api/pesquisar", methods=["POST"])
def pesquisar_receita():
    """Busca uma única receita e a retorna em formato JSON estruturado."""
    data = request.json
    nome_receita = data.get("nome_receita", "").strip()
    settings = data.get("settings", {})

    if not nome_receita:
        return jsonify({"erro": "Nome da receita não informado."}), 400

    prompt_base = f"""
    Você é um assistente de culinária especialista em gerar dados estruturados.
    Sua única tarefa é fornecer a receita de "{nome_receita}" em formato JSON.

    **Estrutura Obrigatória do JSON:**
    O JSON de saída deve seguir exatamente este schema para um único objeto de receita:
    {{
      "titulo": "string",
      "tempoDePreparoEmMin": "integer",
      "porcoes": "integer",
      "ingredientes": [
        {{
          "nome": "string",
          "quantidade": "string",
          "unidadeMedida": "string"
        }}
      ],
      "preparo": ["string"]
    }}
    """

    prompt_final = construir_prompt_com_settings(prompt_base, settings)

    try:
        resposta = modelo.generate_content(prompt_final, generation_config=generation_config)
        dados_receita = json.loads(resposta.text)
        return jsonify({"receitas": [dados_receita]})
    except Exception as e:
        print("--- ERRO NO BACKEND (pesquisar_receita) ---")
        print(f"Erro: {e}")
        traceback.print_exc()
        print("--- FIM DO ERRO ---")
        return jsonify({"erro": "Ocorreu um erro ao pesquisar a receita. Tente novamente."}), 500


# Rotas para servir o frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    """Serve os arquivos estáticos do frontend."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
