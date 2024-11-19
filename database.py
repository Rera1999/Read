from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///bot_data.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    language = Column(String)
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
