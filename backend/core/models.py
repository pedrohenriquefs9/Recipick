from .database import db
from sqlalchemy.sql import func

class ApiCall(db.Model):
    __tablename__ = 'api_call' # Definir o nome da tabela explicitamente é uma boa prática
    
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(200), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    
    # CORREÇÃO: Voltando o nome da coluna para 'response_text'
    response_text = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ApiCall {self.id}>'