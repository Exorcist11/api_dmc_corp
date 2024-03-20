from config import db
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class Role(db.Model):
    __tablename__ = 'Roles'

    role_id = Column(String(5), primary_key=True)
    role_name = Column(String(20), nullable=False)
    description = Column(String(200), nullable=False)

    # Relationship
    accounts = relationship('Account', backref='Roles', lazy=True)
