from flask import Blueprint, jsonify, request, session
from panel.models import User, Plan, Order, Invoice
from panel.database import db

storefront_admin_bp = Blueprint('storefront_admin', __name__)

def req():
    return 'user' in session

@storefront_admin_bp.route('/api/storefront/users', methods=['GET'])
def list_users():
    if not req(): return jsonify({'ok': False}), 401
    users = User.query.order_by(User.created_at.desc()).all()
    data = []
    for u in users:
        data.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'created_at': u.created_at.strftime('%Y-%m-%d %H:%M')
        })
    return jsonify({'ok': True, 'users': data})

@storefront_admin_bp.route('/api/storefront/plans', methods=['GET', 'POST'])
def manage_plans():
    if not req(): return jsonify({'ok': False}), 401
    
    if request.method == 'POST':
        data = request.json
        if data.get('id'):
            # Edit
            plan = Plan.query.get(data['id'])
            if plan:
                plan.name = data.get('name', plan.name)
                plan.description = data.get('description', plan.description)
                plan.price = float(data.get('price', plan.price))
                plan.billing_cycle = data.get('billing_cycle', plan.billing_cycle)
                plan.script_type = data.get('script_type', plan.script_type)
        else:
            # Create
            plan = Plan(
                name=data['name'],
                description=data.get('description', ''),
                price=float(data['price']),
                billing_cycle=data.get('billing_cycle', 'monthly'),
                script_type=data.get('script_type', 'smm')
            )
            db.session.add(plan)
            
        db.session.commit()
        return jsonify({'ok': True})
        
    plans = Plan.query.all()
    data = []
    for p in plans:
        data.append({
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'billing_cycle': p.billing_cycle,
            'script_type': p.script_type
        })
    return jsonify({'ok': True, 'plans': data})

@storefront_admin_bp.route('/api/storefront/orders', methods=['GET'])
def list_orders():
    if not req(): return jsonify({'ok': False}), 401
    orders = Order.query.order_by(Order.created_at.desc()).all()
    data = []
    for o in orders:
        data.append({
            'id': o.id,
            'username': o.user.username if o.user else 'Unknown',
            'plan': o.plan.name if o.plan else 'Unknown',
            'domain': o.domain,
            'status': o.status,
            'script_username': o.script_username,
            'script_password': o.script_password,
            'created_at': o.created_at.strftime('%Y-%m-%d %H:%M')
        })
    return jsonify({'ok': True, 'orders': data})

@storefront_admin_bp.route('/api/storefront/plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    if not req(): return jsonify({'ok': False}), 401
    plan = Plan.query.get(plan_id)
    if plan:
        db.session.delete(plan)
        db.session.commit()
    return jsonify({'ok': True})
