import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.core.database import db
from flask_login import LoginManager
from backend.utils.userModel import User

def create_app():
    """
    Cria e configura uma instância da aplicação Flask (Padrão Application Factory).
    """
    DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))
    app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_muito_segura_aqui')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialização das extensões
    db.init_app(app)
    
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login' # Opcional: define a view de login, útil para @login_required

    # Função para recarregar o usuário da sessão
    @login_manager.user_loader
    def load_user(user_id):
        # user_id vem como string, converta para int se seu ID for inteiro
        return User.query.get(int(user_id))
    
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    CORS(app,
         origins=allowed_origins,
         allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         supports_credentials=True)

    # Importação e registro dos Blueprints
    from backend.routes.normalizar_ingredientes import normalizarBp
    from backend.routes.pesquisar import pesquisarBp
    from backend.routes.receitas import receitaBp, refinarReceitaBp # Modificado
    from backend.routes.history import history_bp
    from backend.routes.main import main_bp
    from backend.routes.login import loginBp
    from backend.routes.login import logoutBp
    from backend.routes.registrar import registerBp

    app.register_blueprint(normalizarBp)
    app.register_blueprint(registerBp, url_prefix='/api')
    app.register_blueprint(loginBp, url_prefix='/api')
    app.register_blueprint(logoutBp, url_prefix='/api')
    app.register_blueprint(pesquisarBp)
    app.register_blueprint(receitaBp)
    app.register_blueprint(refinarReceitaBp) # Adicionado
    app.register_blueprint(history_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        print("Criando tabelas do banco de dados...")
        # Cria as tabelas do banco de dados se não existirem
        db.create_all()

    # Hooks de Requisição
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add('Access-Control-Allow-Headers', "*")
            response.headers.add('Access-Control-Allow-Methods', "*")
            return response

    return app


# --- Inicialização do Servidor ---
if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)