from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from .. import db
from ..models.user import User

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from .. import db


class Reviewer(db.Model):
    __tablename__ = 'reviewers'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    #user_type = db.Column(db.String(50), nullable=False)
    #id = db.Column(db.Integer, db.ForeignKey('users.pid'), primary_key=True)
    expertise_topic = db.Column(db.String(255),default="QC", nullable=True)
    availability = db.Column(db.Boolean, default=True, nullable=True)
    """__mapper_args__ = {
        'polymorphic_identity': 'reviewer',
    }"""
    # Reviewer'a özgü ilişkiler
    reviews = relationship("Review", back_populates="reviewer")
    assignments = relationship('Assignment', back_populates='reviewer')

    def repr(self):
        return f'<Person: {self.id}, {self.user_name}, {self.email}, {self.password}, {self.expertise_topic}>'
