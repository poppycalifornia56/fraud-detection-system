# backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    transaction_date: Optional[datetime] = None
    amount: float
    vendor_id: int
    department_id: int
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    is_flagged: bool
    risk_score: float
    
    class Config:
        orm_mode = True

class AlertBase(BaseModel):
    transaction_id: int
    severity: int
    description: str

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    creation_date: datetime
    is_resolved: bool
    
    class Config:
        orm_mode = True