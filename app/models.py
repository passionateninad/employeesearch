from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    status = Column(String)  # 'active', 'not_started', 'terminated'
    department = Column(String)
    position = Column(String)
    location = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
