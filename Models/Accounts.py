from config import db
from sqlalchemy import String, DateTime, Boolean, Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Account(db.Model):
    __tablename__ = 'Accounts'

    account_id = Column(String(9), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    time_register = Column(DateTime(timezone=True), default=func.now())
    time_update = Column(DateTime(timezone=True), default=func.now())
    role_id = Column(String(5), ForeignKey('Roles.role_id'), nullable=True)
    is_activated = Column(Boolean, default=True)
    id_deleted = Column(Boolean, default=False)

    # Relationship
    user = relationship('User', backref='Accounts', uselist=False, lazy=True)

