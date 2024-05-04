from config import db
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class WishList(db.Model):
    __tablename__ = 'WishList'

    account_id = Column(String(50), ForeignKey('Users.account_id'), nullable=False, primary_key=True)
    product_id = Column(String(50), ForeignKey('Products.product_id'), nullable=False, primary_key=True)

    user = relationship('User', backref=backref('wish_list', uselist=False, cascade='all, delete-orphan', single_parent=True))
    product = relationship('Product', backref='wish_list')

