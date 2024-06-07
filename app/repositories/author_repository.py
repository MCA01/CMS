from app import db
from ..models.author import Author



class AuthorRepository:
    @staticmethod
    def add_author(user, email, password):
        author = Author(id=user.pid, user_name=user.user_name, email=email, password=password)
        db.session.add(author)
        db.session.commit()

    def get_author_by_authorid(author_id):
        return Author.query.filter_by(id=author_id).first()
