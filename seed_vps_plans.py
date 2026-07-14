import sys
import os

sys.path.append(r'e:\VortexPanel-main\VortexPanel-main')

from app import create_app
from panel.database import db
from panel.models import Plan

app = create_app()

with app.app_context():
    # Clear existing dummy plans if they exist
    Plan.query.delete()
    db.session.commit()
    
    # Add new VPS plans
    plan1 = Plan(
        name="Performance VPS",
        price=25.0,
        description="200GB SSD Space • 16GB RAM • 8vCPU Cores • Unmetered Bandwidth"
    )
    
    plan2 = Plan(
        name="Starter VPS",
        price=8.0,
        description="200GB SSD Space • 2GB RAM • 2vCPU Cores • Unmetered Bandwidth"
    )
    
    db.session.add(plan1)
    db.session.add(plan2)
    db.session.commit()
    
    print("Database seeded with VPS plans.")
