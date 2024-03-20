from config import db
from sqlalchemy import DateTime, Column, String, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'Users'

    account_id = Column(String(9), ForeignKey('Accounts.account_id'), primary_key=True)
    full_name = Column(String(50), nullable=True)
    phone_number = Column(String(10), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    date_of_birth = Column(DateTime(timezone=True), nullable=False)
    time_register = Column(DateTime(timezone=True), default=func.now())
    time_update = Column(DateTime(timezone=True), default=func.now())
    is_deleted = Column(Boolean, default=False)

    # Relationship
    new = relationship('New', backref='Users', lazy=True)
    address = relationship('Address', backref='Users', lazy=True)
    cart = relationship('Cart', backref='Users', lazy=True, uselist=False)
    orders = relationship('Order', backref='Users', lazy=True)

