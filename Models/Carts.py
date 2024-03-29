from config import db
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Cart(db.Model):
    __tablename__ = 'Carts'

    cart_id = Column(String(9), primary_key=True)
    account_id = Column(String(50), ForeignKey('Users.account_id'))
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())

    # Relationship
    user = relationship('User', backref='Carts', uselist=False, lazy=True)
    products = relationship('Product', backref='Carts', secondary='Cart_Product', lazy=True)


class CartProducts(db.Model):
    __tablename__ = 'Cart_Product'

    cart_id = Column(String(9), ForeignKey('Carts.cart_id'), primary_key=True)
    product_id = Column(String(9), ForeignKey('Products.product_id'), primary_key=True)
    amount = Column(Integer, nullable=True, default=0)
    price = Column(Float, nullable=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())




