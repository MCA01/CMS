from .. import db
from app.models.assignment import Assignment
from app.models.review import Review
class ReviewRepository:
    @staticmethod
    def add_review(reviewer_id, paper_id, score, comments, result):
        review = Review(reviewer_id=reviewer_id, paper_id=paper_id, score=score, comments=comments, review_result=result)
        db.session.add(review)
        db.session.flush()

        if review in db.session():
            return True
        else:
            return False


    @staticmethod
    def commit_review():
        db.session.commit()

    @staticmethod
    def rollback_review():
        db.session.rollback()