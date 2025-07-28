from flask import Blueprint, jsonify
from flask_login import login_required, current_user

sessionBp = Blueprint('session', __name__)

# CORREÇÃO: Removido o /api do início
@sessionBp.route('/auth/check_session', methods=['GET'])
@login_required
def check_session():
    return jsonify({
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }), 200