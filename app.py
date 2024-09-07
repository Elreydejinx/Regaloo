from flask import Flask, request, jsonify, redirect, url_for
from flask_mail import Mail, Message
import uuid
from models import create_app, db, User, Product, Gift, Order
from datetime import datetime, timedelta

app = create_app()
mail = Mail(app)

@app.route('/users', methods=["POST"])
def create_user():
    data = request.json
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')

    user = User(email=email, phone=phone, address=address)
    db.session.add(user)
    db.seesion.commit()

    return jsonify({"message": "User created successfully!"}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "email": user.email, "phone": user.phone, "address": user.address})


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get_or_404(user_id)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)

    db.session.commit()
    return jsonify({"message": "User updated succesfully!"}), 200

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    product = Product(name=name, description=description, price=price)
    db.seesion.add(product)
    db.session.commit()

    return jsonify({"message": "Product created successfully!"}), 201

@app.route('/products', methods = ['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in products])


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({"id": product.id, "name": product.name, "description": product.descriptioin, "price": product.price})

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    product_id = data.get('product_id')
    customer_id = data.get('customer_id')
    quantity = data.get('quantity')
    total_price = data.get('total_price')

    order = Order(product_id=product_id, customer_id =Customer_id, quantity=quantity, total_price=total_price, status='Pending')
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Order created successfully!"}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({"id": order.id, "product_id": order.product_id, "customer_id": order.customer_id, "quantity": order.quantity, "total_price": order.total_price, "status": order.status, "place_at": order.placed_at, "expires_at": order.expires_at})

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    order = Order.query.get_or_404(order_id)
    order.status = data.get('status', order.status)

    db.session.commit()
    return jsonify({"message": "Order updated successfully!"}), 200

@app.route('/order/<int:order_id>cancel', methods=['POST'])
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status in ['Shipped', 'Delivered']:
        return jsonify({"message": "Order cannot be canceled."}), 400

    order.status = 'Canceled'
    order.canceled_at = datetime.utcnow()
    return jsonify({"message": "Order canceled successfully!"}), 200

@app.route('/orders/<int:order_id>/refund', methods=['POST'])
def refund_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != 'Completed':
        return jsonify({"message": "Only completed order can be refunded."}), 400
    
    order.status = 'Refunded'
    order.refunded_at = datetime.utcnow()
    return jsonify({"message" "Order refunded successfully!"}), 200


@app.route('/orders/expired', methods=['GET'])
def get_expired_orders():
    now = datetime.utcnow()
    orders = Order.query.filter(Order.expires_at < now, Order.status == 'Pending').all()
    return jsonify([{"id": o.id, "product_id": o.product_id, "customer_id": o.customer_id, "quantity": o.quantity, "total_price": o.total_price, "status": o.status, "expires_at": o.expires_at} for o in orders])


@app.route('/send_gift', methods=['POST'])
def send_gift():
    data = request.json
    sender_email = date.get('sender_email')
    recipient_id = data.get('recipient_id')

    gift = Gift(sender_email=sender_email, recipient_id=recipient_id, unique_id=str(uuid.uuid4()))
    db.session.add(gift)
    db.session.commit()

    # Fetch recipient's email
    recipient = User.query.get_or_404(recipient_id)
    send_notification(recipient.email, gift.unique_id)

    return jsonify({"message": "Gift sent successfully!"}), 200

@app.route('/provide_address/<unique_id>', methods=['GET', 'POST'])
def provide_address(unique_id):
    gift = Gift.query.filter_by(unique_id=unique_id).first_or_404()
    
    if request.method == 'POST':
        address = request.form['address']
        gift.recipient_address = address
        gift.status = 'Address Provided'
        db.session.commit()
        return jsonify({"message": "Address received successfully!"}), 200
    
    return '''
        <form method="post">
            Address: <input type="text" name="address">
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/gifts/<unique_id>', methods=['GET'])
def track_gift(unique_id):
    gift = Gift.query.filter_by(unique_id=unique_id).first_or_404()
    return jsonify({"unique_id": gift.unique_id, "sender_email": gift.sender_email, "recipient_id": gift.recipient_id, "recipient_address": gift.recipient_address, "status": gift.status})

def send_notification(recipient_email, unique_id):
    link = url_for('provide_address', unique_id=unique_id, _external=True)
    msg = Message('You have received a gift!',
                  recipients=[recipient_email],
                  body=f'You have received a gift! Please provide your delivery address by visiting the following link: {link}')
    mail.send(msg)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile(config.py)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


