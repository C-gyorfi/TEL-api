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
    response = app.test_client().delete('/api/food_item/1')
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).contains(b'{"errorCode":"NOT_FOUND","message":"Food item not found"}\n')

def test_can_delete_a_food_item():
    # Given there are food stock with an item
    food_stock = Lib.models.FoodStock(name='fridge')
    db.session.add(food_stock)
    db.session.commit()

    butter = Lib.models.FoodItem(name='butter', expiry_date=datetime.datetime(2020, 5, 17), food_stock_id=food_stock.id)
    db.session.add(butter)
    db.session.commit()

    # When I call the delete endpoint with the id
    response = app.test_client().delete('/api/food_item/1')

    # Then I can see the food item deleted
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).contains(b'{"message":"Successfully deleted the following item: butter"}\n')
    assert_that(Lib.models.FoodItem.query.all()).is_empty()

