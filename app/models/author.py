from sqlalchemy.orm import relationship
#import user
from .. import db

from ..models.user import User

from flask_sqlalchemy import SQLAlchemy

from .paper import Paper
"""
class Author(User):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, db.ForeignKey('user.pid'),primary_key=True)
    user = db.relationship('User', back_populates='author')

    papers = db.relationship('Paper', back_populates='author', lazy='dynamic') #query ile döndürülmesi gerekiyor


"""
from sqlalchemy.orm import relationship
#import user
from .. import db


from flask_sqlalchemy import SQLAlchemy

from .paper import Paper
class Author(db.Model):
    __tablename__ = 'authors'

    #id = db.Column(db.Integer, db.ForeignKey('user.pid'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    #user_type = db.Column(db.String(50), nullable=False)

    """__mapper_args__ = {
        'polymorphic_identity': 'author',
    }"""
    # Author'a özgü ilişkiler ve metodlar
    # Relationship with papers as an author
    papers = relationship("Paper", back_populates="author")
