from flask import Flask, send_from_directory
from flask.wrappers import Response
from flask_cors import CORS
import os

from backend.routes.normalizar_ingredientes import normalizarBp
from backend.routes.pesquisar import pesquisarBp
from backend.routes.receitas import receitaBp

# Define a pasta onde o frontend compilado (build) está localizado
DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))

# Cria a instância principal da aplicação Flask
app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")

# Configura o CORS para permitir que o frontend se comunique com esta API
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registra os Blueprints na aplicação principal
app.register_blueprint(normalizarBp)
app.register_blueprint(pesquisarBp)
app.register_blueprint(receitaBp)


# --- Rota para Servir o Frontend ---
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path: str) -> Response:
    """
    Serve o arquivo principal do frontend (index.html) ou qualquer outro arquivo estático
    solicitado (como JS, CSS, imagens).
    """
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# --- Inicialização do Servidor ---
if __name__ == "__main__":
    # Este bloco é executado quando você roda 'python -m backend.app'
    app.run(debug=True, port=5000)
