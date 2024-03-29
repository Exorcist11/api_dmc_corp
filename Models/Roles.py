from config import db
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class Role(db.Model):
    __tablename__ = 'Roles'

    role_id = Column(String(5), primary_key=True)
    role_name = Column(String(20), nullable=True)

    # Relationship
    accounts = relationship('Account', backref='role', lazy=True)
