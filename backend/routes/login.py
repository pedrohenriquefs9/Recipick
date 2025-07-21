from flask import Blueprint, request, jsonify
from backend.core.userModel import User
from flask_login import login_user, logout_user, login_required

loginBp = Blueprint('login', __name__)
logoutBp = Blueprint('logout', __name__)

@loginBp.route('/auth/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Login realizado com sucesso', 'email': user.email}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401

@logoutBp.route('/auth/logout', methods=['POST'])
@login_required # Garante que apenas usuários logados podem fazer logout
def logout():
    logout_user() # Faz o logout do usuário da sessão
    return jsonify({'message': 'Logout realizado com sucesso'}), 200