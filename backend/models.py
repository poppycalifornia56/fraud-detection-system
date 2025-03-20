from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    description = Column(String)
    is_flagged = Column(Boolean, default=False)
    risk_score = Column(Float, default=0.0)
    
    vendor = relationship("Vendor", back_populates="transactions")
    department = relationship("Department", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, vendor_id={self.vendor_id}, department_id={self.department_id}, is_flagged={self.is_flagged})>"

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    registration_number = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)
    risk_profile = Column(Float, default=0.0)
    
    transactions = relationship("Transaction", back_populates="vendor")

    def __repr__(self):
        return f"<Vendor(id={self.id}, name={self.name}, risk_profile={self.risk_profile})>"

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    transactions = relationship("Transaction", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name})>"

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    creation_date = Column(DateTime, default=datetime.utcnow)
    severity = Column(Integer)  # 1-5 scale
    description = Column(String)
    is_resolved = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Alert(id={self.id}, transaction_id={self.transaction_id}, severity={self.severity}, is_resolved={self.is_resolved})>"
