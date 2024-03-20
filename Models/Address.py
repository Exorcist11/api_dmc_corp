from config import db
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Address(db.Model):
    __tablename__ = 'Address'

    address_id = Column(Integer, autoincrement=True, primary_key=True)
    account_id = Column(String(9), ForeignKey('Users.account_id'), nullable=True)
    full_name = Column(String(100), nullable=True)
    phone_number = Column(String(11), nullable=True)
    province = Column(String(255), nullable=False)
    district = Column(String(255), nullable=False)
    ward = Column(String(255), nullable=False)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())
    is_activated = Column(Boolean, default=True)

    # Relationship


