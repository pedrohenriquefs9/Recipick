from flask import Blueprint, request, jsonify
from backend.utils.userModel import User
from flask_login import login_user, logout_user, login_required

# Cria um Blueprint para a rota de login
loginBp = Blueprint('login', __name__)
logoutBp = Blueprint('logout', __name__)

@loginBp.route('/api/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # login_user() registra o usuário na sessão do Flask-Login
        login_user(user)
        return jsonify({'message': 'Login realizado com sucesso', 'username': user.username}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401

@logoutBp.route('/api/logout', methods=['POST'])
@login_required # Garante que apenas usuários logados podem fazer logout
def logout():
    logout_user() # Faz o logout do usuário da sessão
    return jsonify({'message': 'Logout realizado com sucesso'}), 200