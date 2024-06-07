from .. import db
from app.models.assignment import Assignment
from app.models.review import Review
from app.models.assignment import Assignment
from ..models.paper import Paper
from ..repositories.paper_repository import PaperRepository


class AssignmentRepository:
    @staticmethod
    def get_assignments_by_reviewer(reviewer_id):
        return Assignment.query.filter_by(reviewer_id=reviewer_id).all()


    def get_first_assignment_by_paper_id(paper_id):
        return Assignment.query.filter_by(paper_id = paper_id).first()

    def get_assignments_number_for_each_reviewer(reviewer_id):
        return Assignment.query.filter_by(reviewer_id=reviewer_id).count()


    @staticmethod
    def update_assignment_review_status(paper_id, review_status):
        Assignment.query.filter_by(paper_id=paper_id).update({"review_status": review_status})
        db.session.commit()

    def add_assignment(paper_id, reviewer_id):
        new_assignment = Assignment(paper_id=paper_id, reviewer_id=reviewer_id)
        db.session.add(new_assignment)
        db.session.flush()
        if new_assignment in db.session():
            return True
        else:
            return False

    @staticmethod
    def commit_assignment():
        db.session.commit()

    @staticmethod
    def rollback_assignment():
        db.session.rollback()


