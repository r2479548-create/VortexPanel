from panel.database import db
from panel.models import User, Order, Plan
from app import app
import datetime

with app.app_context():
    # Ensure there is a plan
    plan = Plan.query.first()
    if not plan:
        plan = Plan(name="IND-EX24", description="6 x 4.0GHz (High-End) • 24 GB RAM • 700 GB NVME • 1Gbps Network Speed • Fast", price=2899, billing_cycle="monthly", script_type="vps")
        db.session.add(plan)
        db.session.commit()
        
    # Add dummy user
    user = User.query.filter_by(email="test@example.com").first()
    if not user:
        user = User(username="TestUser", email="test@example.com", password_hash="dummy")
        db.session.add(user)
        db.session.commit()
        
    # Add dummy order
    order = Order.query.first()
    if not order:
        order = Order(user_id=user.id, plan_id=plan.id, domain="vps-test.domainracer.local", status="pending", script_username="root", script_password="fakepassword")
        db.session.add(order)
        db.session.commit()
        
    print("Dummy data added!")
