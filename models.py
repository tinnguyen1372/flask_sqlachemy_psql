from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()
ma = Marshmallow()

# Customer modelling


class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    dob = db.Column(db.String())

    def __init__(self, customer_id, name, dob):
        self.name = name
        self.customer_id = customer_id
        self.dob = dob

    def __repr__(self):
        return f"{self.customer_id}:{self.name}:{self.dob}"

# Order modelling


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer(), db.ForeignKey('customer.customer_id'))
    customer = db.relationship(
        "Customer", backref=backref("customer", uselist=False))
    itemname = db.Column(db.String())
    itemprice = db.Column(db.Integer())
    datetime = db.Column(db.String())

    def __init__(self, customer_id, itemname, itemprice, datetime):
        self.itemname = itemname
        self.customer_id = customer_id
        self.itemprice = itemprice
        self.datetime = datetime

    def __repr__(self):
        return f"{self.customer_id}:{self.itemname}:{self.itemprice}:{self.datetime}"


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True
