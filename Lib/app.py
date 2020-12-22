from flask import request, jsonify
from Lib.app_factory import app
from Lib.db import db
from Lib.models import FoodItem, food_items_schema, food_item_schema, FoodStock
from datetime import datetime

@app.route('/')
def home():
  return '<h1>To Eat List API 🦑🥒🥢</h1>'

@app.route('/api/<int:food_stock_id>/food_items/')
def list_food_items(food_stock_id: int):
  try:
    food_items = FoodItem.query.filter_by(food_stock_id=food_stock_id).all()
    if not food_items:
      return jsonify(errorCode="NOT_FOUND", message="The requested resource does not exist")
    else:
      return jsonify(food_stock_id="{0}".format(food_stock_id), food_items=food_items_schema.dump(food_items))
  except Exception as e:
    print(e)
    return jsonify(status='Something bad happened')

@app.route('/api/<int:food_stock_id>/food_item/', methods=['POST'])
def add_food_item_to_food_stock(food_stock_id):
  food_stock = FoodStock.query.filter_by(id=food_stock_id).first()
  if food_stock:
    name = request.get_json()['name']
    expiry_date = request.get_json()['expiry_date']
    new_item = FoodItem(name=name, expiry_date=datetime.strptime(expiry_date, '%Y-%m-%d'), food_stock_id=food_stock.id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify(food_item_schema.dump(new_item))
  else:
    return jsonify(errorCode='NOT_FOUND', message='Food stock does not exist')

@app.cli.command('db_create')
def db_create():
  db.create_all()
  print('Database created!')

@app.cli.command('db_drop')
def db_drop():
  db.drop_all()
  print('Database dropped!')

@app.cli.command('db_seed')
def db_seed():
  fridge = FoodStock(name='fridge')
  cupboard = FoodStock(name='cupboard')
  db.session.add(fridge)
  db.session.add(cupboard)
  db.session.commit()

  ketchup = FoodItem(name='ketchup', food_stock_id=fridge.id)
  cheese = FoodItem(name='cheese', food_stock_id=fridge.id)
  milk = FoodItem(name='milk', food_stock_id=fridge.id)
  flour = FoodItem(name='flour', food_stock_id=cupboard.id)
  db.session.add(ketchup)
  db.session.add(cheese)
  db.session.add(milk)
  db.session.add(flour)

  db.session.commit()
  print('Database seeded!')
