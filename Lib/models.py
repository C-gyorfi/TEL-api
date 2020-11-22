from .db import db, mm

class FoodStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    expiry_date=db.Column(db.Date)
    food_stock_id = db.Column(db.Integer, db.ForeignKey("food_stock.id"))
    food_stock = db.relationship("FoodStock", backref="food_items")

class FoodStockSchema(mm.Schema):
  class Meta:
    fields = ('id', 'name')

class FoodItemSchema(mm.Schema):
  class Meta:
    fields = ('id', 'name', 'expiry_date', 'food_stock_id')

food_stock_schema = FoodStockSchema()
food_stocks_schema = FoodStockSchema(many=True)

food_item_schema = FoodItemSchema()
food_items_schema = FoodItemSchema(many=True)
