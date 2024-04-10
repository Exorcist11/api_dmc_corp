from config import db
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Category(db.Model):
    __tablename__ = 'Categories'

    category_id = Column(Integer, autoincrement=True, primary_key=True)
    category_name = Column(String(255), nullable=True)
    path_category = Column(String(255), nullable=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    is_activated = Column(Boolean, default=True)

    # Relationship
    products = relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')
