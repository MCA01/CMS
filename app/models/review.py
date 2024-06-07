from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from flask_sqlalchemy import SQLAlchemy
from .reviewer import Reviewer



class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(500))
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.paper_id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewers.id'))
    review_result = db.Column(db.String(200),nullable=True)
    paper = relationship("Paper", back_populates="reviews")
    reviewer = relationship("Reviewer", back_populates="reviews")


    def repr(self):
        return f'<Review: {self.id}, {self.score}, {self.comments}, {self.paper_id}, {self.reviewer_id}>'