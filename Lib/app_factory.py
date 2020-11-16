from flask import Flask
import os

create_app = Flask(__name__)

create_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
create_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
