from flask import Blueprint, request, jsonify, session
from panel.models import User, Plan, Order, Invoice
from panel.database import db
import hashlib
import time

storefront_bp = Blueprint('storefront', __name__)

@storefront_bp.route('/api/store/plans', methods=['GET'])
def get_plans():
    plans = Plan.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'description': p.description} for p in plans])

@storefront_bp.route('/api/store/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Registration successful'})

@storefront_bp.route('/api/store/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
        
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user.password_hash != password_hash:
        return jsonify({'error': 'Invalid credentials'}), 401
        
    session['customer_id'] = user.id
    return jsonify({'success': True, 'message': 'Logged in successfully'})

@storefront_bp.route('/api/store/me', methods=['GET'])
def me():
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({'loggedIn': False})
    
    user = User.query.get(customer_id)
    if not user:
        return jsonify({'loggedIn': False})
        
    orders = Order.query.filter_by(user_id=user.id).all()
    order_data = []
    for o in orders:
        order_data.append({
            'id': o.id,
            'plan': o.plan.name,
            'domain': o.domain,
            'status': o.status,
            'username': o.script_username,
            'password': o.script_password
        })
        
    return jsonify({
        'loggedIn': True,
        'user': {'email': user.email, 'username': user.username},
        'orders': order_data
    })

@storefront_bp.route('/api/store/logout', methods=['POST'])
def logout():
    session.pop('customer_id', None)
@storefront_bp.route('/api/store/buy', methods=['POST'])
def buy():
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'Not logged in'}), 401
        
    data = request.json
    plan_id = data.get('plan_id')
    domain = data.get('domain', f'vps-{int(time.time())}.local')
    payment_method = data.get('payment_method') # ETH, BTC, or Monero
    
    plan = Plan.query.get(plan_id)
    if not plan:
        return jsonify({'error': 'Plan not found'}), 404
        
    # Create the Order
    new_order = Order(
        user_id=customer_id,
        plan_id=plan.id,
        domain=domain,
        status='pending' # Awaiting crypto confirmation
    )
    db.session.add(new_order)
    db.session.commit() # commit to get order id
    
    # Create the Invoice
    new_invoice = Invoice(
        user_id=customer_id,
        order_id=new_order.id,
        amount=plan.price,
        status='pending',
        gateway_reference=f'Crypto: {payment_method}'
    )
    db.session.add(new_invoice)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Order placed successfully. Please complete the crypto payment.', 'order_id': new_order.id})

