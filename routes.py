from flask import Blueprint, request, jsonify
from models import db, User, Product, Gift, Order
from notifications import send_notification
import uuid
from datetime import datetime

app = Blueprint('app', __name__)

@app.route('/users', methods=["POST"])
def create_user():
    data = request.json
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    
    user = User(email=email, phone=phone, address=address)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "email": user.email, "phone": user.phone, "address": user.address})

@app.route('/users/<int:user_id>', methods=['DELETE'])
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
    return jsonify({"message": "User updated successfully!"}), 200

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    product = Product(name=name, description=description, price=price)
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product created successfully!"}), 201

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({"id": product.id, "name": product.name, "description": product.description, "price": product.price})

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    product_id = data.get('product_id')
    customer_id = data.get('customer_id')
    quantity = data.get('quantity')
    total_price = data.get('total_price')

    order = Order(product_id=product_id, customer_id=customer_id, quantity=quantity, total_price=total_price)
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Order created successfully!"}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({"id": order.id, "product_id": order.product_id, "customer_id": order.customer_id, "quantity": order.quantity, "total_price": order.total_price, "status": order.status, "placed_at": order.placed_at})

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    order = Order.query.get_or_404(order_id)
    order.status = data.get('status', order.status)

    db.session.commit()
    return jsonify({"message": "Order updated successfully!"}), 200

@app.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status in ['Shipped', 'Delivered']:
        return jsonify({"message": "Order cannot be canceled."}), 400

    order.status = 'Canceled'
    db.session.commit()
    return jsonify({"message": "Order canceled successfully!"}), 200

@app.route('/orders/<int:order_id>/refund', methods=['POST'])
def refund_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != 'Completed':
        return jsonify({"message": "Only completed orders can be refunded."}), 400

    time_elapsed = datetime.now() - order.placed_at
    if time_elapsed > timedaelta(minutes=5):
        return jsonify({"message": "Refund window has expired. Only refunds within 7 minutes are allowed."}), 400
    
    order.status = 'Refunded'
    db.session.commit()
    return jsonify({"message": "Order refunded successfully!"}), 200

@app.route('/gifts/send', methods=['POST'])
def send_gift():
    data = request.json
    sender_email = data.get('sender_email')
    recipient_id = data.get('recipient_id')

    gift = Gift(sender_email=sender_email, recipient_id=recipient_id, unique_id=str(uuid.uuid4()))
    db.session.add(gift)
    db.session.commit()

    # Fetch recipient's email
    recipient = User.query.get_or_404(recipient_id)
    send_notification(recipient.email, gift.unique_id)

    return jsonify({"message": "Gift sent successfully!"}), 200

@app.route('/gifts/<unique_id>/refuse', methods=['POST'])
def refuse_gift(unique_id):
    gift = Gift.query.filter_by(unique_id=unique_id).first_or_404()

    if gift.status != 'Sent':
        return jsonify({"message": "Gift connot be refused."}), 400

    gift.status = 'Rejected'
    db.session.commit()

    return jsonify({"message": "Gift refusal recorded successfully!"}), 200

@app.route('/gifts/<unique_id>', methods=['GET'])
def track_gift(unique_id):
    gift = Gift.query.filter_by(unique_id=unique_id).first_or_404()
    return jsonify({"unique_id": gift.unique_id, "sender_email": gift.sender_email, "recipient_id": gift.recipient_id, "recipient_address": gift.recipient_address, "status": gift.status})

# from flask import Flask, request, rendertemplate, redirect, urlfor
# import yagmail
# import sqlite3

# app = Flask(__name)

# Initialize Yagmail
# yag = yagmail.SMTP('your_email@gmail.com', 'your_password')

# Mock product database (in a real app, this would be a real database or API)
# mock_products = {
#     '123': 'Smartphone',
#     '456': 'Laptop',
#     '789': 'Headphones'
# }

# Setup SQLite database
# def init_db():
#     with sqlite3.connect('gifts.db') as conn:
#         conn.execute('''
#             CREATE TABLE IF NOT EXISTS gifts (
#                 id INTEGER PRIMARY KEY,
#                 product_id TEXT,
#                 recipient_email TEXT,
#                 status TEXT,
#                 address TEXT
#             )
#         ''')
# init_db()

# @app.route('/send_gift', methods=['POST'])
# def send_gift():
#     product_id = request.form['product_id']
#     recipient_email = request.form['recipient_email']

# Store gift in the database
#     with sqlite3.connect('gifts.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute('INSERT INTO gifts (product_id, recipient_email, status) VALUES (?, ?, ?)', 
#                        (product_id, recipient_email, 'pending'))
#         gift_id = cursor.lastrowid

#     # Create gift link
#     gift_link = f'http://localhost:5000/accept_gift/%7Bgift_id%7D'
#     product_name = mock_products.get(product_id, 'Unknown Product')

#     # Send email
#     yag.send(
#         to=recipient_email,
#         subject='You have received a gift!',
#         contents=f'You have received a gift! Product ID: {product_id} ({product_name}). Accept it here: {gift_link}'
#     )
#     return 'Gift sent!'

# @app.route('/accept_gift/<int:gift_id>', methods=['GET', 'POST'])
# def accept_gift(gift_id):
#     if request.method == 'POST':
#         address = request.form['address']

# Update gift status and address
#         with sqlite3.connect('gifts.db') as conn:
#             conn.execute('UPDATE gifts SET status = ?, address = ? WHERE id = ?', 
#                          ('acc
# epted', address, giftid))

#         # Notify sender
#         senderemail = 'youremail@gmail.com'
#         yag.send(
#             to=senderemail,
#             subject='Gift accepted!',
#             contents=f'The recipient has accepted the gift. Address: {address}'
#         )
#         return 'Gift accepted!'

#     # Retrieve gift details
#     with sqlite3.connect('gifts.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute('SELECT product_id FROM gifts WHERE id = ?', (gift_id,))
#         product_id = cursor.fetchone()

#     product_name = mock_products.get(product_id[0], 'Unknown Product') if product_id else 'Unknown Product'

#     return render_template('accept_gift.html', gift_id=gift_id, product_name=product_name)

# @app.route('/deny_gift/<int:gift_id>', methods=['POST'])
# def deny_gift(gift_id):
#     with sqlite3.connect('gifts.db') as conn:
#         conn.execute('UPDATE gifts SET status = ? WHERE id = ?', 
#                      ('denied', gift_id))
#     return 'Gift denied!'

# if __name == '__main':
#     app.run(debug=True)