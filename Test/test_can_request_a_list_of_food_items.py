import pytest
from assertpy import assert_that
from flask_sqlalchemy import SQLAlchemy
from Lib.app import app
import os

# Given there are food items in a list, (Setup the database with 3 Food items)
# When I call the list food items endpoint with a list ID
# Then I want to be able to see the three food items

@pytest.fixture(scope="session", autouse=True)
def setup(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
    db = SQLAlchemy(app)
    db.drop_all()
    db.create_all()

def test_request_root():
    response = app.test_client().get('/')
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).contains(b'Hello, have you saved food today?')
    assert_that(app.config["SQLALCHEMY_DATABASE_URI"]).contains('test.db')
