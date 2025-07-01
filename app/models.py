from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
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
    status = Column(String)  # e.g., 'active', 'not_started', 'terminated'
    department = Column(String)
    position = Column(String)
    location = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

class ColumnConfig(Base):
    __tablename__ = 'column_config'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    column_name = Column(String)
    is_visible = Column(Boolean, default=True)
