import pytest
from assertpy import assert_that
from Lib.app import app
from Lib.db import db
import Lib.models
import os

@pytest.fixture(scope="session", autouse=True)
def setup(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
    db.drop_all()
    db.create_all()

def test_uses_the_correct_database():
    assert_that(app.config["SQLALCHEMY_DATABASE_URI"]).contains('test.db')

def test_can_retrieve_food_items_for_a_food_stock():
    # Given there are food stock
    food_stock = Lib.models.FoodStock(name='fridge')
    db.session.add(food_stock)
    db.session.commit()

    # and there are three food items
    butter = Lib.models.FoodItem(name='butter', food_stock_id=food_stock.id)
    bread = Lib.models.FoodItem(name='bread', food_stock_id=food_stock.id)
    milk = Lib.models.FoodItem(name='milk', food_stock_id=food_stock.id)
    db.session.add(butter)
    db.session.add(bread)
    db.session.add(milk)

    db.session.commit()

    # When I call the list food items endpoint with a list ID
    response = app.test_client().get('/api/1/food_items/')

    # Then I can see the three food items
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).is_equal_to(
        b'{"food_items":' +
        b'[{"food_stock_id":1,"id":1,"name":"butter"},' + 
        b'{"food_stock_id":1,"id":2,"name":"bread"},' +
        b'{"food_stock_id":1,"id":3,"name":"milk"}],' +
        b'"food_stock_id":"1"}\n'
    )

