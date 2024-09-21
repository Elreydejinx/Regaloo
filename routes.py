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

@app.route('/gifts/<unique_id>', methods=['GET'])
def track_gift(unique_id):
    gift = Gift.query.filter_by(unique_id=unique_id).first_or_404()
    return jsonify({"unique_id": gift.unique_id, "sender_email": gift.sender_email, "recipient_id": gift.recipient_id, "recipient_address": gift.recipient_address, "status": gift.status})

