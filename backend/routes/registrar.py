from flask import Blueprint, request, jsonify
from backend.core.database import db
from backend.core.userModel import User
import bcrypt # bcrypt é mais seguro, vamos mantê-lo

registerBp = Blueprint('register', __name__)

@registerBp.route('/auth/registrar', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado recebido"}), 400

        name = data.get('name') # Adicionando o campo nome
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return jsonify({"error": "Nome, email e senha são obrigatórios"}), 400

        if User.query.filter((User.email == email) | (User.name == name)).first():
            return jsonify({"error": "Utilizador com este email ou nome já existe"}), 409

        # Cria a instância do utilizador
        new_user = User(name=name, email=email)
        # Define a senha usando o método do modelo, que irá hashear e atribuir a password_hash
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Utilizador registado com sucesso!"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"ERRO EM /register: {e}")
        return jsonify({"error": "Ocorreu um erro interno ao registar o utilizador."}), 500