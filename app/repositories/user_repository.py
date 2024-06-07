from app import db
from ..models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class UserRepository:
    @staticmethod
    def add_user(user_name, email, password, user_type, expertise_topic=None):
        hashed_password = bcrypt.generate_password_hash(password)

        user = User(user_name=user_name, email=email, password=hashed_password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        return user
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter(User.email == email).first()