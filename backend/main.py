# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend import models
from backend import schemas
from backend.database import engine, get_db
from backend.ml_model import predict_anomalies

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Run anomaly detection
    transactions_df = get_recent_transactions(db, 1000)  # Get last 1000 transactions
    anomalies = predict_anomalies(transactions_df)
    
    if db_transaction.id in anomalies:
        db_transaction.is_flagged = True
        db_transaction.risk_score = anomalies[db_transaction.id]
        
        # Create alert
        alert = models.Alert(
            transaction_id=db_transaction.id,
            severity=int(anomalies[db_transaction.id] * 5),  # Convert score to 1-5 scale
            description=f"Anomalous transaction detected with score {anomalies[db_transaction.id]:.2f}"
        )
        db.add(alert)
        db.commit()
    
    return db_transaction

@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions

@app.get("/alerts/", response_model=List[schemas.Alert])
def read_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = db.query(models.Alert).offset(skip).limit(limit).all()
    return alerts