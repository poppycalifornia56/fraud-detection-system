from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# from backend 
import models
# from backend
import schemas
from database import engine, get_db
from ml_model import predict_anomalies, get_recent_transactions

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transactions/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        # Create the transaction record in the database
        db_transaction = models.Transaction(**transaction.dict())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        # Run anomaly detection
        transactions_df = get_recent_transactions(db, 1000)  # Get last 1000 transactions
        anomalies = predict_anomalies(transactions_df)
        
        # Check if the transaction is anomalous
        if db_transaction.id in anomalies:
            db_transaction.is_flagged = True
            db_transaction.risk_score = anomalies[db_transaction.id]
            
            # Create an alert based on the anomaly
            alert = models.Alert(
                transaction_id=db_transaction.id,
                severity=int(anomalies[db_transaction.id] * 5),  # Convert score to 1-5 scale
                description=f"Anomalous transaction detected with score {anomalies[db_transaction.id]:.2f}"
            )
            db.add(alert)
            db.commit()

        return db_transaction

    except Exception as e:
        db.rollback()  # Rollback in case of any failure
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
        return transactions
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/alerts/", response_model=List[schemas.Alert])
def read_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        alerts = db.query(models.Alert).offset(skip).limit(limit).all()
        return alerts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
