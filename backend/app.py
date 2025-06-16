
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
modelo = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__, static_folder="frontend", static_url_path="/")
CORS(app)

@app.route("/api/receitas", methods=["POST"])
def gerar_receitas():
    data = request.json
    ingredientes = data.get("ingredientes", "").strip()
    if not ingredientes:
        return jsonify({"erro": "Nenhum ingrediente informado."}), 400

    prompt = f"""Você é um assistente de receitas criativas. O usuário informou os seguintes ingredientes: {ingredientes}.

Tarefa:
- Corrija erros nos nomes dos ingredientes.
- Liste os ingredientes corrigidos como lista com `-`.
- Sugira 3 receitas criativas usando apenas os ingredientes informados.
  - Use pelo menos 3 frases no modo de preparo, com instruções úteis.
- Sugira 2 ingredientes extras que combinariam bem.
- Para cada novo ingrediente, sugira 1 nova receita.

 Formato obrigatório:
- Use apenas **markdown puro** (sem emojis).
- Não use espaçamentos desnecessários entre blocos.
- Separe visualmente apenas com `---` (linha horizontal simples).

Exemplo de estrutura:

**Ingredientes normalizados:**
- ingrediente 1
- ingrediente 2
---
**Receitas com os ingredientes originais**
**1. Nome da receita**
**Ingredientes:** ...
**Modo de preparo:** ...
---
**Ingredientes adicionais sugeridos:**
- ...
---
**Novas receitas com ingredientes extras**
**1. Nome da nova receita**
**Ingredientes:** ...
**Modo de preparo:** ...
"""

    resposta = modelo.generate_content(prompt)
    return jsonify({"receitas": resposta.text})

@app.route("/api/pesquisar", methods=["POST"])
def pesquisar_receita():
    data = request.json
    nome_receita = data.get("nome_receita", "").strip()
    if not nome_receita:
        return jsonify({"erro": "Nome da receita não informado."}), 400

    prompt = f"""Quero a receita de: {nome_receita}.
Apresente de forma clara, usando markdown sem emojis.

**Nome da Receita**
**Ingredientes:**
- item
**Modo de preparo:**
- passo 1
"""

    resposta = modelo.generate_content(prompt)
    return jsonify({"receita": resposta.text})

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
