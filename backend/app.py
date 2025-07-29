import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Recipe, Favorite
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# --- ALTERAÇÃO ADICIONADA AQUI ---
# Configura o cookie de sessão para funcionar em domínios diferentes (cross-site)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
# ------------------------------------

# Configuração do banco de dados e CORS
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///history.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
CORS(app, origins=allowed_origins, supports_credentials=True)

db.init_app(app)

# Rotas da aplicação (sem alterações)
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({"message": "Logged in successfully", "user": {"id": user.id, "username": user.username}}), 200
    
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/auth/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'No active session'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    return jsonify({'message': 'Session is active', 'user': {'id': user.id, 'username': user.username}}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    recipes = Recipe.query.all()
    return jsonify([{'id': r.id, 'title': r.title, 'ingredients': r.ingredients, 'instructions': r.instructions} for r in recipes]), 200

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': f.id, 'recipe_id': f.recipe_id} for f in favorites]), 200

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    recipe_id = data.get('recipe_id')

    if not recipe_id:
        return jsonify({"message": "Recipe ID is required"}), 400

    favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite added"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)