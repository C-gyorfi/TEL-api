from flask import jsonify
from .app_factory import create_app
from .db import db
from .models import FoodItem, food_items_schema

app = create_app

@app.route('/')
def home():
  return '<h1>Hello, have you saved food today?:)</h1>'

@app.route('/api/<int:food_stock_id>/food_items/')
def list_food_items(food_stock_id: int):
  food_items = FoodItem.query.all()
  food_items_schema.dump(food_items)
  return jsonify(food_stock_id="{0}".format(food_stock_id), food_items=food_items_schema.dump(food_items))
