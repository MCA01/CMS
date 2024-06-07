from app.models.paper import Paper
from app.models.assignment import Assignment
from app.models.review import Review
from app.models.user import User
from app.models.author import Author
from app.services.review_service import ReviewerService
from app.services.paper_service import AuthorService
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.author_repository import AuthorRepository
from app.repositories.paper_repository import PaperRepository
from io import BytesIO
from unittest.mock import patch


def test_index(client):
    response = client.get("/")
    assert b"<title>CMS</title>" in response.data

def test_registration(client, app):
    response = client.post("/register/", data={"name": "reviewer_test", "email": "test@testemail.com", "password": "test_password", "user_type": "reviewer", "expertise_topic": "Quantum Computing"})

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@testemail.com"

def test_submit_paper(client, app):
    client.post("/register/", data={"name": "author_test", "email": "test@testemail.com", "password": "test_password", "user_type": "author", "expertise_topic": None})
    client.post("/register/", data={"name": "reviewer_test", "email": "test@testemail.com", "password": "test_password", "user_type": "reviewer", "expertise_topic": "Quantum Computing"})

    response = client.post("/file_upload/", data={"title": "test_paper", "topic": "Quantum Computing", "file": (BytesIO(b'My research paper content'), 'test.pdf')}, content_type='multipart/form-data')

    with app.app_context():
        assert Paper.query.count() == 1
        assert Paper.query.first().title == "test_paper"

def test_reviewer_assignment(client, app):
    test_submit_paper(client, app)

    with app.app_context():
        assignment = Assignment.query.first()
        assert assignment.reviewer_id is not None


def test_review(client, app):
    test_reviewer_assignment(client, app)

    paper_id = Paper.query.first().paper_id
    response = client.get(f"/review/{paper_id}")
    assert b"<title>CMS - Review</title>" in response.data

def test_submit_review(client, app):
    test_reviewer_assignment(client, app)

    paper_id = Paper.query.first().paper_id
    response = client.post(f"/review/{paper_id}", data={"result": "acceptance", "score": "10", "comments": "test comment"})

    with app.app_context():
        assert Review.query.count() == 1
        assert Review.query.first().paper_id == paper_id

def test_paper_review_page(client, app):
    test_submit_review(client, app)

    paper_id = Paper.query.first().paper_id
    response = client.get(f"/paper_review_page/{paper_id}")
    assert b"<title>CMS - Review Details</title>" in response.data

def test_get_reviewer_assignments(client, app):
    test_submit_paper(client, app)

    reviewer_id = User.query.filter_by(user_name="reviewer_test").first().pid
    with patch('app.repositories.assignment_repository.AssignmentRepository.get_assignments_by_reviewer') as mock_get_assignments:
        mock_get_assignments.return_value = [Assignment(reviewer_id=reviewer_id, paper_id=1)]  # Mock assignments data

        assignments = ReviewerService.get_reviewer_assignments(reviewer_id)

    assert len(assignments) == 1
    assert assignments[0].reviewer_id == reviewer_id

def test_get_author_papers(client, app):
    test_submit_paper(client, app)

    with app.app_context():
        author = Author.query.filter_by(user_name="author_test").first()
        with patch('app.repositories.author_repository.AuthorRepository.get_author_by_authorid') as mock_get_author:
            mock_get_author.return_value = author

            papers = [Paper()]
            with patch('app.repositories.paper_repository.PaperRepository.get_papers_by_author_id') as mock_get_papers:
                mock_get_papers.return_value = papers

                assignments = [Assignment()]
                with patch('app.repositories.assignment_repository.AssignmentRepository.get_first_assignment_by_paper_id') as mock_get_assignment:
                    mock_get_assignment.return_value = assignments[0]

                    result = AuthorService.get_author_papers(author.id)

    assert result == assignments

def test_author_page_index(client, app):
    client.post("/register/", data={"name": "author_test", "email": "test@testemail.com", "password": "test_password", "user_type": "author", "expertise_topic": None})

    response = client.get("/author_page_index/")
    assert b"<title>CMS - Author Home</title>" in response.data

def test_author_page(client, app):
    client.post("/register/", data={"name": "author_test", "email": "test@testemail.com", "password": "test_password", "user_type": "author", "expertise_topic": None})

    response = client.get("/author_page/")
    assert b"<title>CMS - Author</title>" in response.data

def test_reviewer_page_index(client, app):
    client.post("/register/", data={"name": "reviewer_test", "email": "test@testemail.com", "password": "test_password", "user_type": "reviewer", "expertise_topic": "Quantum Computing"})

    response = client.get("/reviewer_page_index/")
    assert b"<title>CMS - Reviewer Home</title>" in response.data

def test_reviewer_page(client, app):
    client.post("/register/", data={"name": "reviewer_test", "email": "test@testemail.com", "password": "test_password", "user_type": "reviewer", "expertise_topic": "Quantum Computing"})

    response = client.get("/reviewer_page/")
    assert b"<title>CMS - Reviewer</title>" in response.data
