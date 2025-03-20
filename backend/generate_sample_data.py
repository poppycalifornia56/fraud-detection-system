import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
import models

def generate_sample_data(db: Session):
    # Create departments
    departments = [
        "Finance", "Procurement", "Operations", 
        "IT", "HR", "Legal", "Sales", "Marketing"
    ]
    
    for dept_name in departments:
        db_dept = models.Department(name=dept_name)
        db.add(db_dept)
    
    db.commit()
    
    # Create vendors
    for i in range(1, 21):  # 20 vendors
        risk_profile = random.random() * 0.3  # Most vendors are low risk
        
        # Make a few high-risk vendors
        if i <= 3:
            risk_profile = 0.7 + (random.random() * 0.3)  # High risk
        
        db_vendor = models.Vendor(
            name=f"Vendor {i}",
            registration_number=f"REG-{100000+i}",
            risk_profile=risk_profile
        )
        db.add(db_vendor)
    
    db.commit()
    
    # Create regular transactions
    for i in range(1, 201):  # 200 regular transactions
        dept_id = random.randint(1, len(departments))
        vendor_id = random.randint(1, 20)
        amount = random.uniform(1000, 50000)
        days_ago = random.randint(1, 90)
        
        transaction_date = datetime.now() - timedelta(days=days_ago)
        
        db_transaction = models.Transaction(
            transaction_date=transaction_date,
            amount=amount,
            vendor_id=vendor_id,
            department_id=dept_id,
            description=f"Regular transaction {i}"
        )
        db.add(db_transaction)
    
    # Create anomalous transactions
    for i in range(1, 21):  # 20 anomalous transactions
        dept_id = random.randint(1, len(departments))
        
        # Use high-risk vendors for some anomalies
        if i <= 10:
            vendor_id = random.randint(1, 3)  # High-risk vendors
        else:
            vendor_id = random.randint(4, 20)
        
        # Anomalous high amount
        amount = random.uniform(80000, 150000)
        days_ago = random.randint(1, 30)
        
        transaction_date = datetime.now() - timedelta(days=days_ago)
        
        db_transaction = models.Transaction(
            transaction_date=transaction_date,
            amount=amount,
            vendor_id=vendor_id,
            department_id=dept_id,
            description=f"Potentially anomalous transaction {i}",
            is_flagged=True,
            risk_score=random.uniform(0.7, 0.95)
        )
        db.add(db_transaction)
  

        # Create alert for this transaction
        alert = models.Alert(
            transaction_id=200 + i,  # IDs start after regular transactions
            severity=int(db_transaction.risk_score * 5),
            description=f"Unusually high amount transaction detected"
        )
        db.add(alert)
    
    db.commit()
    print("Sample data generated successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        generate_sample_data(db)
    finally:
        db.close()