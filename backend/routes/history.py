from flask import Blueprint, jsonify
from backend.core.models import ApiCall
from backend.core.userModel import User # Importar o modelo User para obter o nome
from backend.core.database import db
from flask_login import login_required, current_user

history_bp = Blueprint('history_bp', __name__)

@history_bp.route('/api/history', methods=['GET'])
@login_required # 1. Garante que o utilizador está logado
def get_history():
    """
    Retorna o histórico de chamadas da API.
    Acesso restrito a utilizadores com a função 'admin'.
    """
    # 2. Verifica se o utilizador logado tem a permissão de 'admin'
    if current_user.role != 'admin':
        # Se não for admin, retorna um erro de acesso proibido
        return jsonify({"error": "Acesso não autorizado. Permissões de administrador são necessárias."}), 403

    # 3. Se for admin, busca todo o histórico, juntando com os dados do utilizador
    # O .join(User) permite-nos aceder aos dados do utilizador associado a cada chamada
    calls = db.session.query(ApiCall, User.name).join(User, ApiCall.user_id == User.id).order_by(ApiCall.created_at.desc()).all()
    
    history_list = []
    for call, user_name in calls:
        history_list.append({
            "id": call.id,
            "prompt": call.prompt,
            "response": call.response,
            "created_at": call.created_at.isoformat(),
            "user_id": call.user_id,
            "user_name": user_name # Adicionamos o nome do utilizador para facilitar a visualização
        })
        
    return jsonify(history_list)