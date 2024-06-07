from app import db
from ..models.reviewer import Reviewer

class ReviewerRepository:
    @staticmethod
    def add_reviewer(user, email, password, expertise_topic, availability):
        reviewer = Reviewer(id=user.pid, user_name=user.user_name, email=email, password=password,
                            expertise_topic=expertise_topic, availability=availability)
        db.session.add(reviewer)
        db.session.commit()


    def get_reviewer_by_expertisetopic_availability(spesific_paper, availability):
        return Reviewer.query.filter_by(expertise_topic=spesific_paper.topic, availability=availability).all()

    def update_reviewer_availability(assigned_reviewer_id):
        Reviewer.query.filter_by(reviewer_id=assigned_reviewer_id).update({"availability": False})
        db.session.commit()  # Commit all changes including the new assignment

    @staticmethod
    def commit_reviewer():
        db.session.commit()

    @staticmethod
    def rollback_reviewer():
        db.session.rollback()
    def refresh_reviewer(reviewer):
        db.session.refresh(reviewer)


