import pytest
from assertpy import assert_that
from Lib.app import app
from Lib.db import db
import Lib.models
import os
import datetime

@pytest.fixture(autouse=True)
def setup(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
    db.drop_all()
    db.create_all()

def test_when_food_stock_does_not_exists():
    response = app.test_client().post('/api/1/food_item/', json={
        'name': 'hot pot', 'expiry_date': '2020-05-18'
    })
    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.data).contains(b'{"errorCode":"NOT_FOUND","message":"Food stock does not exist"}\n')

def test_can_create_a_new_item_in_a_food_stock():
    # Given there are food stock
    food_stock = Lib.models.FoodStock(name='fridge')
    db.session.add(food_stock)
    db.session.commit()

    # When I try to create a new food item
    response = app.test_client().post('/api/1/food_item/', json={
        'name': 'hot pot', 'expiry_date': '2020-05-18'
    })

    # Then I can see my new food items
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).is_equal_to(
        b'{"expiry_date":"2020-05-18","food_stock_id":1,"id":1,"name":"hot pot"}\n'
    )
