from .database import db
from datetime import datetime

class ApiCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    endpoint = db.Column(db.String(200), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=False)