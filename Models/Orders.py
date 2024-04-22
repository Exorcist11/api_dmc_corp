from config import db
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean, Integer, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Order(db.Model):
    __tablename__ = 'Orders'

    order_id = Column(String(50), primary_key=True)
    account_id = Column(String(50), ForeignKey('Users.account_id'), nullable=False)
    status = Column(String(10), default="pending")
    payment = Column(String(10), nullable=False)
    note = Column(String(200), nullable=True)
    address_id = Column(Integer, ForeignKey('Address.address_id'))
    total = Column(Float, nullable=False, default=0)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())

    # Relationship
    address = relationship('Address', uselist=False, backref='order', lazy=True)
    products = relationship('Product', backref='order', secondary='Order_Product', lazy=True)


class OrderProduct(db.Model):
    __tablename__ = 'Order_Product'

    order_id = Column(String(50), ForeignKey('Orders.order_id'), primary_key=True)
    product_id = Column(String(50), ForeignKey('Products.product_id'), primary_key=True)
    amount = Column(Integer, nullable=True)
    price = Column(Float, nullable=False)


