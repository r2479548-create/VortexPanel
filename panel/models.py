from datetime import datetime
from panel.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    invoices = db.relationship('Invoice', backref='user', lazy=True)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    billing_cycle = db.Column(db.String(20), default='monthly') # monthly, yearly
    script_type = db.Column(db.String(50), default='smm') # smm, wordpress

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    domain = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, active, suspended, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Store provisioned details
    script_username = db.Column(db.String(80), nullable=True)
    script_password = db.Column(db.String(255), nullable=True)
    
    plan = db.relationship('Plan')

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='unpaid') # unpaid, paid, failed
    gateway_reference = db.Column(db.String(120), nullable=True) # ZapUPI payment ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)
