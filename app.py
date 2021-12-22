from flask import Flask, render_template, request, jsonify, current_app, Blueprint
import psycopg2
import json
from flask_migrate import Migrate
from models import Order, db, Customer, ma, CustomerSchema, OrderSchema
from datetime import datetime
con = psycopg2.connect(database="customer", user="postgres",
                       password="Ned130702", host="127.0.0.1", port="5432")
cursor = con.cursor()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Ned130702@localhost:5432/customer"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    return app


app = create_app()


# @app.route('/')
# # def index():
# #     render_template("index.html")
@app.route('/customer')
def customers():
    number = request.args.get('number')
    if number == None:
        customer_schema = CustomerSchema()
        customers_schema = CustomerSchema(many=True)
        all_customer = Customer.query.all()
        return jsonify(customer_list=customers_schema.dump(all_customer))
    else:
        cursor.execute(
            'SELECT * FROM customer ORDER BY age(cast(dob as date)) ASC')
        result = cursor.fetchall()
        list = []
        count = 0
        for row in result:
            if count < int(number):
                rs = {'customer_id': row[0],
                      'name': row[1],
                      'dob': row[2],
                      }
                list.append(rs.copy())
                rs.clear()
            count = count + 1
        return jsonify(list)


@app.route('/customer/create')
def form():
    return render_template("form.html")


@app.route('/order')
def detail():
    order_schema = OrderSchema()
    customer_id = request.args.get('customer_id')
    if customer_id == None:
        orders_schema = OrderSchema(many=True)
        all_order = Order.query.all()
        return jsonify(order_list=orders_schema.dump(all_order))
    else:
        cursor.execute(
            'select customer.customer_id, itemname, itemprice,datetime from "order" inner join customer on customer.customer_id = "order".customer_id and customer.customer_id =' + customer_id)
        result = cursor.fetchall()
        list = []
        for row in result:
            rs = {'customer_id': row[0],
                  'itemname': row[1],
                  'itemprice': row[2],
                  'datetime': row[3]
                  }
            list.append(rs.copy())
            rs.clear()
        return jsonify(list)


@app.route('/order/create')
def order_create():
    return render_template("order.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        name = request.form['name']
        dob = request.form['dob']
        new_user = Customer(customer_id=customer_id, name=name, dob=dob)
        db.session.add(new_user)
        db.session.commit()
        return f"Done!!"


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        itemname = request.form['itemname']
        itemprice = request.form['itemprice']
        datetime = request.form['datetime']
        new_order = Order(customer_id=customer_id, itemname=itemname,
                          itemprice=itemprice, datetime=datetime)
        db.session.add(new_order)
        db.session.commit()
        return f"Done!!"


if __name__ == '__main__':
    app.run(debug=True)
