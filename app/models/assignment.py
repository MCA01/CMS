from .. import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)


    paper = relationship("Paper", back_populates="review")
    reviewer = relationship("Reviewer", back_populates="review")
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.paper_id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewers.id'), nullable=False)
    paper = relationship("Paper")
    reviewer = relationship('Reviewer', back_populates='assignments')
    review_status = db.Column(db.Boolean, nullable =True , default = False)


    def __repr__(self):
        return f'<Paper {self.id}, paper id : {self.paper_id}, reviewer id :{self.reviewer_id}>'



