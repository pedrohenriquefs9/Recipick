from flask import Blueprint, request, jsonify
from backend.core.userModel import User
from flask_login import login_user, logout_user

loginBp = Blueprint('login', __name__)
logoutBp = Blueprint('logout', __name__)

# A rota de login agora só precisa de aceitar o método POST
@loginBp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado recebido"}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return jsonify({
                "message": "Login bem-sucedido",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            }), 200
        else:
            return jsonify({"message": "Credenciais inválidas"}), 401

    except Exception as e:
        print(f"ERRO EM /login: {e}")
        return jsonify({"error": "Ocorreu um erro interno."}), 500

@logoutBp.route('/auth/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logout bem-sucedido"}), 200