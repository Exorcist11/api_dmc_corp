from config import db
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Seller(db.Model):
    __tablename__ = 'Sellers'

    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    path_seller = Column(String(100), nullable=True)
    nation = Column(String(50), nullable=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())
    is_activated = Column(Boolean, default=True)

    # Relationship
    product = relationship('Product', backref='seller', lazy=True, cascade='all, delete-orphan')
