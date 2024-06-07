import pytest

from app import create_app, db

@pytest.fixture()
def db_var():
    return 'sqlite:///testdatabase.db'

@pytest.fixture()
def app(db_var):
    app = create_app(db_var)

    with app.app_context():
        db.create_all()

        print("CREATING DATABASE")
        yield app

        db.drop_all()



@pytest.fixture()
def client(app):
    return app.test_client()
