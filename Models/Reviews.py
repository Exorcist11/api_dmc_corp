from config import db
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Review(db.Model):
    __tablename__ = 'Reviews'

    review_id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100), nullable=True)
    content = Column(String(255), nullable=False)
    rate = Column(Integer, nullable=True)
    order_id = Column(String(9), ForeignKey('Orders.order_id'))
    create_at = Column(DateTime(timezone=True), default=func.now())
    is_deleted = Column(Boolean, default=False)

    # Relationship
    order = relationship('Orders', backref='Reviews', lazy=True, uselist=False)


