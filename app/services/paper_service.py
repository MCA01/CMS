# app/services/paper_service.py

from ..repositories.assignment_repository import AssignmentRepository
from ..repositories.author_repository import AuthorRepository
from ..repositories.paper_repository import PaperRepository

from ..repositories.reviewer_repository import ReviewerRepository

from flask import flash
import random

class AuthorService:
    def assign_reviewer(paper_id):
        specific_paper = PaperRepository.get_paper_by_paper_id(paper_id)
        if specific_paper is None:
            return None,f"No paper found with ID {paper_id}"
        potential_reviewers = ReviewerRepository.get_reviewer_by_expertisetopic_availability(spesific_paper = specific_paper, availability=True)

        if not potential_reviewers:
            return None,"No available reviewers found for the topic: " + specific_paper.topic

        assigned_reviewer = random.choice(potential_reviewers)
        specific_paper.reviewer_id = assigned_reviewer.id

        try:
            is_assignment_added = AssignmentRepository.add_assignment(paper_id=specific_paper.paper_id, reviewer_id=assigned_reviewer.id)
            # Eklemenin gerçekleştirilip gerçekleştirilmediğini kontrol etmek için
        except Exception as e:
            AssignmentRepository.rollback_assignment()
        if is_assignment_added:
            AssignmentRepository.commit_assignment()

        total_assignments_for_that_spesific_reviewer = AssignmentRepository.get_assignments_number_for_each_reviewer(reviewer_id=assigned_reviewer.id)
        if total_assignments_for_that_spesific_reviewer >= 10:
            # 10'dan fazla görev atanmışsa reviewer'ın availability durumunu false yap
            ReviewerRepository.update_reviewer_availability(assigned_reviewer.id)
            #Reviewer.query.filter_by(reviewer_id=assigned_reviewer.id).update({"availability": False})

        ReviewerRepository.refresh_reviewer(assigned_reviewer)
        return assigned_reviewer,f"Reviewer {assigned_reviewer.user_name} successfully assigned to paper '{specific_paper.title}'."



    @staticmethod
    def get_author_papers(author_id):
        author = AuthorRepository.get_author_by_authorid(author_id=author_id)
        if author:
            papers = PaperRepository.get_papers_by_author_id(author.id)
            spesific_assignments = []
            for paper in papers:
                assignment = AssignmentRepository.get_first_assignment_by_paper_id(paper_id = paper.paper_id)
                spesific_assignments.append(assignment)
            return spesific_assignments
            #spesific assignments = assignments tablolarının.all hali gibi olmalı

        return None

    @staticmethod
    def upload_file(author_id, title, topic, file):
        if title == "" or topic == "" or file is None:
            upload_page_is_done = False
        else:
            upload_page_is_done = True
        try:
            is_new_paper_added, new_paper_paper_id = PaperRepository.add_paper(author_id=author_id, title=title, topic=topic,
                                                           keywords=file.read(), file_name=file.filename)
            # Eklemenin gerçekleştirilip gerçekleştirilmediğini kontrol etmek için
        except Exception as e:
            PaperRepository.rollback_paper()
        if is_new_paper_added and upload_page_is_done:
            flash('Paper submitted successfully.', 'success')
            PaperRepository.commit_paper()
            assigned_reviewer, msg = AuthorService.assign_reviewer(new_paper_paper_id)
            if assigned_reviewer is None:
                print(msg, 'error')
            else:
                print(msg, 'success')
        else:
            flash('Paper could not be submitted successfully.', 'danger')
