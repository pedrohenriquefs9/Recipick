# backend/utils/userModel.py

from backend.core.database import db # Assumindo que 'db' está aqui
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # Se estiver usando Flask-Login

class User(db.Model, UserMixin): # Certifique-se de herdar de db.Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Para armazenar a senha hash

    def set_password(self, password):
        """Hasheia a senha e armazena o hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

    # Necessário para Flask-Login
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.name}>'