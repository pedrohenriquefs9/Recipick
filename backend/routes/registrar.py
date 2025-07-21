# No seu arquivo de login/logout ou em um novo Blueprint para registro
from flask import Blueprint, request, jsonify
from backend.core.userModel import User
from backend.core.database import db # <-- Certifique-se de importar 'db' aqui também!
from werkzeug.security import generate_password_hash # <-- Importar para hashing de senha

registerBp = Blueprint('register', __name__)
# ... (imports)

@registerBp.route('/auth/registrar', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Dados incompletos'}), 400

    if User.query.filter_by(name=name).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'Usuário ou e-mail já existe'}), 409 # Conflict

    try:
        # Crie a instância do usuário passando os argumentos nomeados diretamente:
        new_user = User(name=name, email=email) # <-- AGORA ISSO VAI FUNCIONAR CORRETAMENTE!

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'name': new_user.name,
            'email': new_user.email,
            'password': new_user.password_hash
        }), 201
        
    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500