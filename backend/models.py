from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)
    amount = Column(Float)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    description = Column(String)
    is_flagged = Column(Boolean, default=False)
    risk_score = Column(Float, default=0.0)
    
    vendor = relationship("Vendor", back_populates="transactions")
    department = relationship("Department", back_populates="transactions")
    
class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    registration_number = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    risk_profile = Column(Float, default=0.0)
    
    transactions = relationship("Transaction", back_populates="vendor")
    
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    transactions = relationship("Transaction", back_populates="department")
    
class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    severity = Column(Integer)  # 1-5 scale
    description = Column(String)
    is_resolved = Column(Boolean, default=False)