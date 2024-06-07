from app import db

from ..models.paper import Paper
class PaperRepository:
    @staticmethod
    def get_paper_by_paper_id(paper_id):
        return Paper.query.filter_by(paper_id=paper_id).first()

    @staticmethod
    def get_papers_by_author_id(author_id):
        papers = Paper.query.filter_by(author_id=author_id).all()

        return papers

    @staticmethod
    def add_paper(author_id, title, topic, keywords, file_name):
        new_paper = Paper(author_id=author_id, title=title, topic=topic, keywords=keywords, file_name=file_name)

        db.session.add(new_paper)
        db.session.flush()

        if new_paper in db.session():
            return True, new_paper.paper_id
        else:
            return False

    @staticmethod
    def commit_paper():
        db.session.commit()

    @staticmethod
    def rollback_paper():
        db.session.rollback()