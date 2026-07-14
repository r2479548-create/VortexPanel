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
    
    # Add new Windows RDP plans
    plan1 = Plan(
        name="Windows RDP 8GB",
        price=15.0,
        description="Windows Server 2022 • 8GB RAM • 4vCPU Cores • 100GB NVMe • RDP Access"
    )
    
    plan2 = Plan(
        name="Windows RDP 16GB",
        price=25.0,
        description="Windows Server 2022 • 16GB RAM • 8vCPU Cores • 200GB NVMe • RDP Access"
    )
    
    db.session.add(plan1)
    db.session.add(plan2)
    db.session.commit()
    
    print("Database seeded with VPS plans.")
