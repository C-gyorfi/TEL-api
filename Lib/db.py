from .app_factory import create_app
app = create_app

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
mm = Marshmallow(app)
