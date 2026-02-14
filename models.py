from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    current_monthly_payment = db.Column(db.Float)
    remaining_balance = db.Column(db.Float)
    property_value = db.Column(db.Float)
    property_zip = db.Column(db.String(10))
    property_county = db.Column(db.String(100))
    property_state = db.Column(db.String(2))
    credit_score = db.Column(db.Integer)
    monthly_income = db.Column(db.Float)
