from flask import Blueprint, request, jsonify
from backend.core.database import db
from backend.core.userModel import User
import re

registerBp = Blueprint('register', __name__)

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@registerBp.route('/auth/registrar', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado recebido"}), 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return jsonify({"error": "Nome, email e senha são obrigatórios"}), 400

        if not re.match(EMAIL_REGEX, email):
            return jsonify({"error": "Formato de e-mail inválido."}), 400

        if not (6 <= len(password) <= 14):
            return jsonify({"error": "A senha deve ter entre 6 e 14 caracteres."}), 400

        if User.query.filter((User.email == email) | (User.name == name)).first():
            return jsonify({"error": "Utilizador com este email ou nome já existe"}), 409

        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Utilizador registado com sucesso!"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"ERRO EM /register: {e}")
        return jsonify({"error": "Ocorreu um erro interno ao registar o utilizador."}), 500