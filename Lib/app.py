from flask import Flask 

app = Flask(__name__)

@app.route('/')
def home():
  return '<h1>Hello, have you saved food today?</h1>'
