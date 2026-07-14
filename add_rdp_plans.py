import os
import sys

# Add the project root to python path to import app and db
sys.path.insert(0, r'e:\VortexPanel-main\VortexPanel-main')

from app import app
from panel.database import db
from panel.models import Plan

with app.app_context():
    rdp_plans = [
        {
            'name': 'Windows RDP 8GB',
            'description': '8GB RAM, 4 vCPU, 100GB SSD, Windows Server 2022',
            'price': 15.00,
            'billing_cycle': 'monthly',
            'script_type': 'windows_rdp'
        },
        {
            'name': 'Windows RDP 16GB',
            'description': '16GB RAM, 8 vCPU, 200GB SSD, Windows Server 2022',
            'price': 25.00,
            'billing_cycle': 'monthly',
            'script_type': 'windows_rdp'
        }
    ]

    for p in rdp_plans:
        # Check if plan already exists by name
        existing = Plan.query.filter_by(name=p['name']).first()
        if not existing:
            new_plan = Plan(
                name=p['name'],
                description=p['description'],
                price=p['price'],
                billing_cycle=p['billing_cycle'],
                script_type=p['script_type']
            )
            db.session.add(new_plan)
            print(f"Added {p['name']}")
        else:
            print(f"Plan {p['name']} already exists")
    
    db.session.commit()
    print("Database updated.")
