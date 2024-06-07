from ..repositories.user_repository import UserRepository, bcrypt
from ..repositories.reviewer_repository import ReviewerRepository
from ..repositories.author_repository import AuthorRepository

class UserService:
    @staticmethod
    def register_user(user_name, email, password, user_type, expertise_topic=None):
        user = UserRepository.add_user(user_name, email, password, user_type, expertise_topic=None)

        if user_type == "reviewer":
            ReviewerRepository.add_reviewer(user, email, password, expertise_topic,True)

        elif user_type == "author":
            AuthorRepository.add_author(user, email, password)

        user = UserRepository.get_user_by_email(email)

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None


    @staticmethod
    def sign_in_user(email, password):
        user = UserRepository.get_user_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None