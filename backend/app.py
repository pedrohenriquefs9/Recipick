import os
from flask import Flask, jsonify
from flask_cors import CORS
from backend.core.database import db
from flask_login import LoginManager
# Importando os modelos para que o SQLAlchemy saiba quais tabelas criar
from backend.core.userModel import User
from backend.core.models import Chat, Message, ApiCall
from dotenv import load_dotenv

load_dotenv()

def create_app():
    DIST_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipick-front/dist"))
    app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")

    # --- Configurações da Aplicação ---
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    CORS(app, origins=allowed_origins, supports_credentials=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///history.db')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma_chave_secreta_muito_segura')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True

    # --- Inicialização de Extensões ---
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify(error="Autenticação necessária."), 401
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # --- Registro de Blueprints (Rotas) ---
    from backend.routes.normalizar_ingredientes import normalizarBp
    from backend.routes.pesquisar import pesquisarBp
    from backend.routes.receitas import receitaBp, refinarReceitaBp
    from backend.routes.history import history_bp
    from backend.routes.main import main_bp
    from backend.routes.login import loginBp, logoutBp
    from backend.routes.registrar import registerBp
    from backend.routes.session import sessionBp
    from backend.routes.chat import chat_bp

    app.register_blueprint(registerBp, url_prefix='/api')
    app.register_blueprint(loginBp, url_prefix='/api')
    app.register_blueprint(logoutBp, url_prefix='/api')
    app.register_blueprint(sessionBp, url_prefix='/api')
    app.register_blueprint(history_bp, url_prefix='/api')
    app.register_blueprint(normalizarBp, url_prefix='/api')
    app.register_blueprint(pesquisarBp, url_prefix='/api')
    app.register_blueprint(receitaBp, url_prefix='/api')
    app.register_blueprint(refinarReceitaBp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(main_bp)

    # --- Criação das Tabelas do Banco de Dados ---
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)