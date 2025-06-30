from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from backend.routes.normalizar_ingredientes import normalizar_ingredientes
from backend.routes.pesquisar import pesquisar_receita
from backend.routes.receitas import gerar_receitas

DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")

app.add_url_rule("/api/normalizar-ingredientes", view_func=normalizar_ingredientes, methods=["POST"])
app.add_url_rule("/api/receitas", view_func=gerar_receitas, methods=["POST"])
app.add_url_rule("/api/pesquisar", view_func=pesquisar_receita, methods=["POST"])

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
CORS(app,
     origins=allowed_origins,
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
