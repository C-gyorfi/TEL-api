from flask import jsonify
from .app_factory import app
from .db import db
from .models import FoodItem, food_items_schema, FoodStock

@app.route('/')
def home():
  return '<h1>Hello, have you saved food today?:)</h1>'

@app.route('/api/<int:food_stock_id>/food_items/')
def list_food_items(food_stock_id: int):
  food_items = FoodItem.query.all()
  food_items_schema.dump(food_items)
  return jsonify(food_stock_id="{0}".format(food_stock_id), food_items=food_items_schema.dump(food_items))

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
