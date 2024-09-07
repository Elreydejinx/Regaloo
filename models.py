from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config
from datetime import datetime, timedelta


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    address = db.Column(db.String(250), nullable=True)
    gifts = db.relationship('Gift', backref='recipient', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='product', lazy=True)


class Gift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String(120), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_address = db.Column(db.String(250), nullable=True)
    unique_id = db.Column(db.String(36), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=3))
    refunded_at = db.Column(db.DateTime, nullable=True)
    canceled_at = db.Column(db.DateTime, nullable=True)
