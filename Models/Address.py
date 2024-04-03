from config import db
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.sql import func


class Address(db.Model):
    __tablename__ = 'Address'

    address_id = Column(Integer, autoincrement=True, primary_key=True)
    account_id = Column(String(50), ForeignKey('Users.account_id'), nullable=True)
    full_name = Column(String(100), nullable=True)
    phone_number = Column(String(11), nullable=True)
    province = Column(String(20), nullable=False)
    district = Column(String(20), nullable=False)
    ward = Column(String(20), nullable=False)
    note = Column(String(255), nullable=False)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())
    is_activated = Column(Boolean, default=True)

    # Relationship
