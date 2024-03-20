from config import db
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Boolean, Float
from sqlalchemy.sql import func


class Product(db.Model):
    __tablename__ = 'Products'

    product_id = Column(String(5), primary_key=True)
    product_name = Column(String(125), nullable=True)
    seller_id = Column(String(5), ForeignKey('Sellers.seller_id'), nullable=True)
    price = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True, default=1)
    rate = Column(Float, nullable=False, default=0)
    color = Column(String(20), nullable=False)
    material = Column(String(20), nullable=False)
    size = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    waterproof = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())
    is_deleted = Column(Boolean, default=True)

    # Relationship
