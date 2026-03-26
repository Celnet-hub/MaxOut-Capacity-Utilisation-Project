from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from middleware.config.db import Base 


class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=False) # in production email should be unique
    department = Column(String, nullable=False)
    status = Column(String, nullable=False) # e.g., 'Active', 'Terminated'
    employment_date = Column(Date, nullable=False)
    
    # Relationships
    accounts_managed = relationship("CustomerAccount", foreign_keys='CustomerAccount.account_manager_id', back_populates="account_manager")
    cx_accounts = relationship("CustomerAccount", foreign_keys='CustomerAccount.cx_manager_id', back_populates="cx_manager")

class CustomerAccount(Base):
    __tablename__ = "customer_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, nullable=False, index=True)
    account_status = Column(String, nullable=False) # 'Active', 'Inactive'
    
    # Foreign Keys linking to Employee table
    account_manager_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    cx_manager_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    account_manager = relationship("Employee", foreign_keys=[account_manager_id], back_populates="accounts_managed")
    cx_manager = relationship("Employee", foreign_keys=[cx_manager_id], back_populates="cx_accounts")
    contacts = relationship("Contact", back_populates="account")
    products = relationship("CustomerProduct", back_populates="account")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email_address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    position = Column(String, nullable=True)
    status = Column(String, nullable=False)
    
    account = relationship("CustomerAccount", back_populates="contacts")

class CustomerProduct(Base):
    __tablename__ = "customer_products"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=False)
    cid = Column(String, nullable=False, unique=True) # Circuit ID
    provisioned_bandwidth_mbps = Column(Float, nullable=False)
    burst_capacity_mbps = Column(Float, nullable=False) # Default to 0 if no burst allowed
    pop = Column(String, nullable=False) # Point of Presence
    
    date_provisioned = Column(Date, nullable=False)
    date_decommissioned = Column(Date, nullable=True)
    date_capacity_upgraded = Column(Date, nullable=True)
    date_capacity_downgraded = Column(Date, nullable=True)
    
    account = relationship("CustomerAccount", back_populates="products")
    max_out_events = relationship("MaxOutEvent", back_populates="product")

class MaxOutEvent(Base):
    __tablename__ = "max_out_events"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("customer_products.id"), nullable=False)
    notification_sent = Column(Boolean, default=False, nullable=False)
    
    # UPDATED: timezone=True tells Postgres to handle timezones properly,
    # and the default uses the modern Python datetime approach.
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    product = relationship("CustomerProduct", back_populates="max_out_events")