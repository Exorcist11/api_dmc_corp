from config import db
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Boolean, Float
from sqlalchemy.sql import func


class Product(db.Model):
    __tablename__ = 'Products'

    product_id = Column(String(50), primary_key=True)
    product_name = Column(String(125), nullable=True)
    path_product = Column(String(255), nullable=True)
    seller_id = Column(Integer, ForeignKey('Sellers.seller_id'), nullable=False)
    category_id = Column(Integer, ForeignKey('Categories.category_id'), nullable=False)
    price = Column(Integer, nullable=False)
    amount = Column(Integer, default=1)
    rate = Column(Float, nullable=True, default=0)
    color = Column(String(20), nullable=True)
    material = Column(String(20), nullable=True)
    size = Column(String(10), nullable=True)
    width = Column(String(10), nullable=True)
    waterproof = Column(String(10), nullable=True)
    description_display = Column(Text, nullable=True)
    description_markdown = Column(Text, nullable=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())
    is_deleted = Column(Boolean, default=True)

    # Relationship
