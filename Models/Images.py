from config import db
from sqlalchemy import Column, String, Integer


class Image(db.Model):
    __tablename__ = 'Images'

    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String(255), nullable=True)
    content_type = Column(String(255), nullable=False)
    product_id = Column(String(50), nullable=True)
    account_id = Column(String(50), nullable=True)


