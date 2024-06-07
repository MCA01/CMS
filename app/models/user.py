from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .. import db

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    pid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # Kullanıcı türünü belirten sütun

    #author = db.relationship('Author', back_populates='user', uselist=False)

    def __repr__(self):
        return f'<Person: {self.pid}, {self.user_name}, {self.email}, {self.password}, {self.user_type}>'

    def get_id(self):
        return self.pid