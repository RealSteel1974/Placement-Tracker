
from sqlalchemy import  Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a new base class for the model
Base = declarative_base()


# Define the PlacementData class as a SQLAlchemy model
class PlacementData(Base):
    __tablename__ = 'placement_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Batch = Column(String(50))
    KaradDac = Column(Integer)
    DAC  = Column(Integer)
    DMC  = Column(Integer)
    DESD = Column(Integer)
    DBDA = Column(Integer)

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))  # Ideally hashed