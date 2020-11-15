import pytest
from assertpy import assert_that
from Lib import app

# Given there are food items in a list, (Setup the database with 3 Food items)
# When I call the list food items endpoint with a list ID
# Then I want to be able to see the three food items

def test_request_root():
    response = app.app.test_client().get('/')
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).contains(b'Hello, have you saved food today?')
