from flask import Blueprint, request, jsonify, redirect, session
import requests
import time
from panel.models import User, Plan, Order, Invoice
from panel.database import db
from panel.utils.provision import provision_smm_panel

zapupi_bp = Blueprint('zapupi', __name__)

ZAPUPI_KEY = 'zapd3ac6edc258246e7655fa384a0f4b605' # You can move this to DB or config later
ZAPUPI_API_URL = 'https://pay.zapupi.com/api/create-order'

@zapupi_bp.route('/checkout/<int:plan_id>', methods=['GET'])
def checkout(plan_id):
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect('/#login')
        
    plan = Plan.query.get(plan_id)
    if not plan:
        return "Plan not found", 404
        
    user = User.query.get(customer_id)
    
    # 1. Create Order in DB
    domain = f"site-{int(time.time())}.bestsmmpanel.eu.cc" # Temporary domain, can be customized
    new_order = Order(user_id=user.id, plan_id=plan.id, domain=domain, status='pending')
    db.session.add(new_order)
    db.session.commit()
    
    # 2. Create Invoice in DB
    new_invoice = Invoice(user_id=user.id, order_id=new_order.id, amount=plan.price, status='unpaid')
    db.session.add(new_invoice)
    db.session.commit()
    
    # 3. Create ZapUPI Order
    payload = {
        "zap_key": ZAPUPI_KEY,
        "order_id": f"INV{new_invoice.id}{int(time.time())}",
        "amount": str(int(plan.price)),
        "remark": f"{plan.name} | UID:{user.id}",
        "webhook_url": "https://panel.bestsmmpanel.eu.cc/webhook/zapupi"
    }
    
    try:
        response = requests.post(ZAPUPI_API_URL, json=payload, timeout=10)
        data = response.json()
        if data.get('status') == 'Success':
            payment_url = data.get('payment_url')
            # Save ZapUPI reference
            new_invoice.gateway_reference = data.get('order_id')
            db.session.commit()
            return redirect(payment_url)
        else:
            return f"ZapUPI Error: {data.get('message', 'Unknown')}", 500
    except Exception as e:
        return f"Payment Gateway Error: {str(e)}", 500

@zapupi_bp.route('/webhook/zapupi', methods=['POST'])
def zapupi_webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400
        
    order_id_str = data.get('order_id') # format: INV-ID-TIMESTAMP
    status = data.get('status')
    
    if status == 'Success' and order_id_str.startswith('INV'):
        # Just use gateway_reference to find invoice
        invoice = Invoice.query.filter_by(gateway_reference=order_id_str).first()
        if invoice and invoice.status != 'paid':
            # Mark invoice as paid
            invoice.status = 'paid'
            
            # Activate Order and Trigger Auto-Provisioning
            order = Order.query.get(invoice.order_id)
            if order:
                order.status = 'active'
                
                # --- AUTO-PROVISIONING LOGIC HERE ---
                username, password = provision_smm_panel(order.domain)
                order.script_username = username
                order.script_password = password
                
            db.session.commit()
            
    return jsonify({"status": "ok"}), 200
