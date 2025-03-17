from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import logging

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
