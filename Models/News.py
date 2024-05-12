from config import db
from sqlalchemy import String, Column, Text, DateTime, ForeignKey
from sqlalchemy.sql import func


class New(db.Model):
    __tablename__ = 'News'

    new_id = Column(String(5), primary_key=True)
    title_new = Column(String(200), nullable=True)
    image = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    content_html = Column(Text, nullable=False)
    author = Column(String(50), ForeignKey('Users.account_id'), nullable=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at = Column(DateTime(timezone=True), default=func.now())

