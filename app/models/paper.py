from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from flask_sqlalchemy import SQLAlchemy



class Paper(db.Model):
    __tablename__ = 'papers'

    paper_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    abstract = db.Column(db.Text, nullable=True)
    title = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(100), nullable=False)

    keywords = db.Column(db.String(255))
    file_name = db.Column(db.String(255), nullable=False)
    #status = db.Column(db.String(50))
    #original_paper_file_name = db.Column(db.String(255))
    #content_type = db.Column(db.String(50))
    #last_modified = db.Column(db.String(50))

    # Relationship with author

    author = relationship("Author", back_populates="papers")


    from .review import Review
    # Relationship with reviews
    #reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewers.id'))
    reviews = relationship("Review", back_populates="paper")
    assignments = relationship("Assignment", back_populates="paper")

    def __repr__(self):
        return f'<Paper {self.paper_id},{self.author_id}, {self.abstract},{self.title},{self.topic},{self.keywords},{self.file_name},>'
