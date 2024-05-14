from config import db
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Review(db.Model):
    __tablename__ = 'Reviews'

    review_id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100), nullable=True)
    content = Column(String(255), nullable=True)
    rate = Column(Integer, nullable=False)
    name = Column(String(255), nullable=True)
    order_id = Column(String(50), ForeignKey('Orders.order_id'))
    product_id = Column(String(50), ForeignKey('Products.product_id'))
    account_id = Column(String(50), ForeignKey('Users.account_id'))
    create_at = Column(DateTime(timezone=True), default=func.now())
    is_deleted = Column(Boolean, default=False)

    # Relationship
    order = relationship('Order', backref='rating', lazy=True, uselist=False)
    user = relationship('User', backref='rating', lazy=True, uselist=False)
    product = relationship('Product', backref='rating', lazy=True, uselist=False)


