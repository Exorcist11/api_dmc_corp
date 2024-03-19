from config import db
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class CategoryProduct(db.Model):
    __tablename__ = 'Category_Product'

    category_id = Column(String(5), ForeignKey('Categories.category_id'), primary_key=True)
    product_id = Column(String(5), ForeignKey('Products.product_id'), primary_key=True)


class Category(db.Model):
    __tablename__ = 'Categories'

    category_id = Column(String(5), primary_key=True)
    category_name = Column(String(255), nullable=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    is_activated = Column(Boolean, default=True)

    # Relationship
    products = relationship('Products', secondary='Category_Product', lazy=True, backref='Category')
