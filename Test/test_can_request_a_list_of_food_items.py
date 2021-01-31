import pytest
from assertpy import assert_that
from Lib.app import app
from Lib.db import db
import Lib.models
import os
import datetime

pytest.client = app.test_client()

@pytest.fixture(autouse=True)
def setup(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
    db.drop_all()
    db.create_all()
    pytest.client.environ_base['HTTP_AUTHORIZATION'] = "Dummy"

def test_uses_the_correct_database():
    assert_that(app.config["SQLALCHEMY_DATABASE_URI"]).contains('test.db')

def test_when_user_does_not_have_an_authorization_token():
    pytest.client.environ_base['HTTP_AUTHORIZATION'] = ''
    response = pytest.client.get('/api/1/food_items/')

    assert_that(response.status_code).is_equal_to(401)
    assert_that(response.data).contains(b'{"errorCode":"UNAUTHORIZED","message":"Invalid authorization data"}\n')

def test_when_user_has_an_invalid_token():
    pytest.client.environ_base['HTTP_AUTHORIZATION'] = 'invalid'
    response = pytest.client.get('/api/1/food_items/')

    assert_that(response.status_code).is_equal_to(401)
    assert_that(response.data).contains(b'{"errorCode":"UNAUTHORIZED","message":"Invalid authorization data"}\n')

def test_when_requested_resource_does_not_exist():
    response = pytest.client.get('/api/1/food_items/')

    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.data).contains(b'{"errorCode":"NOT_FOUND","message":"The requested resource does not exist"}\n')

def test_can_retrieve_food_items_for_a_food_stock():
    # Given there are food stock
    food_stock = Lib.models.FoodStock(name='fridge')
    db.session.add(food_stock)
    db.session.commit()

    # and there are three food items
    butter = Lib.models.FoodItem(name='butter', expiry_date=datetime.datetime(2020, 5, 17), food_stock_id=food_stock.id)
    bread = Lib.models.FoodItem(name='bread', expiry_date=datetime.datetime(2020, 5, 18), food_stock_id=food_stock.id)
    milk = Lib.models.FoodItem(name='milk', expiry_date=datetime.datetime(2020, 5, 19), food_stock_id=food_stock.id)
    db.session.add(butter)
    db.session.add(bread)
    db.session.add(milk)

    db.session.commit()

    # When I call the list food items endpoint with a list ID
    response = pytest.client.get("/api/% s/food_items/"%(food_stock.id))

    # Then I can see the three food items
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).is_equal_to(
        b'{"food_items":' +
        b'[{"expiry_date":"2020-05-17","food_stock_id":1,"id":1,"name":"butter"},' + 
        b'{"expiry_date":"2020-05-18","food_stock_id":1,"id":2,"name":"bread"},' +
        b'{"expiry_date":"2020-05-19","food_stock_id":1,"id":3,"name":"milk"}],' +
        b'"food_stock_id":"1"}\n'
    )

def test_can_only_return_where_food_stock_id_matches():
    food_stock = Lib.models.FoodStock(name='fridge')
    another_food_stock = Lib.models.FoodStock(name='under the pillow')
    db.session.add(food_stock)
    db.session.add(another_food_stock)
    db.session.commit()

    butter = Lib.models.FoodItem(name='butter', expiry_date=datetime.datetime(2020, 5, 17), food_stock_id=food_stock.id)
    bread = Lib.models.FoodItem(name='bread', expiry_date=datetime.datetime(2020, 5, 17), food_stock_id=another_food_stock.id)
    db.session.add(butter)
    db.session.add(bread)

    db.session.commit()

    response = pytest.client.get("/api/% s/food_items/"%(food_stock.id))

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).is_equal_to(
        b'{"food_items":' +
        b'[{"expiry_date":"2020-05-17","food_stock_id":1,"id":1,"name":"butter"}],' + 
        b'"food_stock_id":"1"}\n'
    )
    assert_that(response.data).does_not_contain(b'bread')

def test_food_items_are_ordered_by_expiry_date():
    food_stock = Lib.models.FoodStock(name='fridge')
    db.session.add(food_stock)
    db.session.commit()

    new_item = Lib.models.FoodItem(name='new egg', expiry_date=datetime.datetime(2020, 5, 18), food_stock_id=food_stock.id)
    old_item = Lib.models.FoodItem(name='old milk', expiry_date=datetime.datetime(2020, 1, 18), food_stock_id=food_stock.id)
    db.session.add(new_item)
    db.session.add(old_item)
    db.session.commit()

    # When I call the list food items endpoint with a list ID
    response = pytest.client.get("/api/% s/food_items/"%(food_stock.id))

    # Then I can see the three food items
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).is_equal_to(
        b'{"food_items":' +
        b'[{"expiry_date":"2020-01-18","food_stock_id":1,"id":2,"name":"old milk"},' + 
        b'{"expiry_date":"2020-05-18","food_stock_id":1,"id":1,"name":"new egg"}],' +
        b'"food_stock_id":"1"}\n'
    )
