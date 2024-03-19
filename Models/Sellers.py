from config import db
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Seller(db.Model):
    __tablename__ = 'Sellers'

    seller_id = Column(String(5), primary_key=True)
    seller_name = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    nation = Column(String(50), nullable=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())
    is_activated = Column(Boolean, default=True)

    # Relationship
    product = relationship('Products', backref='Seller', lazy=True)

