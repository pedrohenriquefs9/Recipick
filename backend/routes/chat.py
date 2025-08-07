from flask import Blueprint, jsonify, request
from backend.core.database import db
from backend.core.models import Chat
from flask_login import login_required, current_user

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/chats', methods=['GET'])
@login_required
def get_user_chats():
    user_chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.created_at.desc()).all()
    
    chats_data = []
    for chat in user_chats:
        messages_data = []
        for msg in chat.messages:
            messages_data.append({
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'type': msg.type,
                'created_at': msg.created_at.isoformat()
            })
        
        chats_data.append({
            'id': chat.id,
            'title': chat.title,
            'isFavorite': chat.is_favorite,
            'createdAt': chat.created_at.isoformat(),
            'messages': messages_data,
            'settings': chat.settings,
            'ingredients': chat.messages[0].content.split(', ') if chat.messages and chat.messages[0].role == 'user' else []
        })
        
    return jsonify(chats_data)

@chat_bp.route('/chats/<int:chat_id>/title', methods=['PUT'])
@login_required
def update_chat_title(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403

    data = request.json
    new_title = data.get('title', '').strip()

    if not new_title:
        return jsonify({"error": "O título não pode estar vazio."}), 400

    chat.title = new_title
    db.session.commit()
    return jsonify({"message": "Título atualizado com sucesso.", "newTitle": new_title})

@chat_bp.route('/chats/<int:chat_id>', methods=['PUT'])
@login_required
def update_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403

    data = request.json
    if 'is_favorite' in data:
        chat.is_favorite = bool(data['is_favorite'])
    if 'settings' in data:
        chat.settings = data['settings']
    
    db.session.commit()
    return jsonify({"message": "Chat atualizado com sucesso"}), 200

@chat_bp.route('/chats/<int:chat_id>', methods=['DELETE'])
@login_required
def delete_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403
    
    db.session.delete(chat)
    db.session.commit()
    return jsonify({"message": "Chat removido com sucesso"}), 200