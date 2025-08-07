from .database import db
from .userModel import User
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False, default='Novo Pedido')
    is_favorite = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    settings = db.Column(JSONB, nullable=False, default=lambda: {"diet": "omnivore", "complexity": "rapida", "style": "popular", "portionSize": "pequeno"})
    
    messages = db.relationship('Message', backref='chat', lazy=True, cascade="all, delete-orphan", order_by='Message.created_at')

    def __repr__(self):
        return f'<Chat {self.id}>'

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False, default='text')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Message {self.id} from chat {self.chat_id}>'

class ApiCall(db.Model):
    __tablename__ = 'api_call'
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(200), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ApiCall {self.id}>'