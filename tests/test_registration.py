"""Testing Registration Routes"""
from flask import url_for
import pytest

from application.database import User
from application import init_app,db

@pytest.fixture(name="app")
def create_app():
    """create a new test app"""
    new_app = init_app()
    new_app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })

    with new_app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield new_app
        db.session.remove()

@pytest.fixture(name="client")
def create_client(app):
    """initialize a fixture test client for flask unit testing"""
    with app.test_client() as app_client:
        yield app_client


# def test_purify_table(app):
#     """purify the database"""
#     with app.app_context():
#         User.query.delete()
#         db.session.commit()

def test_user_registration_success(client):
    """test registration"""
    response = client.post("/registration", data={
        "email": "steve@steve.com",
        "password": "123",
        "confirm": "123",
    }, follow_redirects=True)

    assert response.request.path == url_for('authentication.dashboard')
    assert response.status_code == 200




def test_user_registration_duplicate_user_fail(client, app):
    """test duplicate registration"""
    with app.app_context():
        user = User.create('steve@steve.com', 'testtest')
        db.session.add(user)# pylint: disable=no-member
        db.session.commit()# pylint: disable=no-member

    # with client:
    response = client.post("/registration", data={
        "email": "steve@steve.com",
        "password": "testtest",
        "confirm": "testtest",
    }, follow_redirects=True)

    assert response.request.path == url_for('authentication.registration')
    assert response.status_code == 200
    assert b"Email already registered." in response.data
