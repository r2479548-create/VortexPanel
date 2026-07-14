from flask import Blueprint, request, jsonify, session
from panel.models import User, Plan, Order, Invoice
from panel.database import db
import hashlib
import time
import requests
import uuid

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
    
    plan = Plan.query.get(plan_id)
    if not plan:
        return jsonify({'error': 'Plan not found'}), 404
        
    # Unique order ID for ZapUPI
    unique_order_id = f"ORD{int(time.time())}{uuid.uuid4().hex[:6]}"
    
    # Calculate amount in INR
    amount_inr = str(int(plan.price * 83))

    # We need the base URL for the webhook
    # For local development, this will be localhost or local IP, which won't be reachable from ZapUPI
    # The user should configure this later if deploying publicly.
    host = request.host_url.rstrip('/')
    webhook_url = f"{host}/api/store/webhook/zapupi"
    
    zap_key = "zapd3ac6edc258246e7655fa384a0f4b605"
    
    try:
        resp = requests.post("https://pay.zapupi.com/api/create-order", json={
            "zap_key": zap_key,
            "order_id": unique_order_id,
            "amount": amount_inr,
            "remark": f"Plan {plan.name} | User {customer_id}",
            "webhook_url": webhook_url
        }, timeout=15)
        zap_data = resp.json()
        
        if zap_data.get('status') == 'success' or 'payment_url' in zap_data:
            payment_url = zap_data.get('payment_url')
            if not payment_url and 'data' in zap_data:
                 payment_url = zap_data['data'].get('payment_url')
                 
            if payment_url:
                # Create the Order as pending
                new_order = Order(
                    user_id=customer_id,
                    plan_id=plan.id,
                    domain=domain,
                    status='pending_payment' # Awaiting ZapUPI confirmation
                )
                db.session.add(new_order)
                db.session.commit()
                
                # Create the Invoice linking ZapUPI order ID
                new_invoice = Invoice(
                    user_id=customer_id,
                    order_id=new_order.id,
                    amount=plan.price,
                    status='pending',
                    gateway_reference=f"ZapUPI: {unique_order_id}"
                )
                db.session.add(new_invoice)
                db.session.commit()
                
                return jsonify({'success': True, 'payment_url': payment_url, 'order_id': new_order.id})
                
        return jsonify({'error': 'ZapUPI Gateway Error: ' + str(zap_data)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@storefront_bp.route('/api/store/webhook/zapupi', methods=['POST'])
def zapupi_webhook():
    data = request.json
    if not data:
        return jsonify({"status": "ok"}), 200
        
    status = data.get('status')
    order_id = data.get('order_id') # This is the unique ORD-xxx string
    
    if status == 'Success' and order_id:
        # Find the invoice with this gateway reference
        invoice = Invoice.query.filter_by(gateway_reference=f"ZapUPI: {order_id}").first()
        if invoice and invoice.status != 'paid':
            invoice.status = 'paid'
            
            # Update order
            order = Order.query.get(invoice.order_id)
            if order:
                order.status = 'active'
                # Generate a dummy Windows RDP build
                from panel.utils.provision import provision_vps
                provision_vps(order)
                
            db.session.commit()
            
    return jsonify({"status": "ok"}), 200

