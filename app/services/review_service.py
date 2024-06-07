from flask import flash
from ..repositories.assignment_repository import AssignmentRepository
from ..repositories.review_repository import ReviewRepository



class ReviewerService:
    @staticmethod
    def get_reviewer_assignments(reviewer_id):
        assignments = AssignmentRepository.get_assignments_by_reviewer(reviewer_id)
        return assignments

    class ReviewService:
        @staticmethod
        def submit_review(reviewer_id, paper_id, score, comments, result):
            if score is None or comments == "" or result is None:
                AssignmentRepository.update_assignment_review_status(paper_id, False)
                is_full = False
            else:
                AssignmentRepository.update_assignment_review_status(paper_id, True)
                is_full = True
            try:
                is_added = ReviewRepository.add_review(reviewer_id, paper_id, score, comments, result)
                # Eklemenin gerçekleştirilip gerçekleştirilmediğini kontrol etmek için

            except Exception as e:
                ReviewRepository.rollback_review()

            if is_added and is_full:
                flash('Review submitted successfully.', 'success')
                ReviewRepository.commit_review()
            else:
                flash('Review could not be submitted successfully.', 'danger')