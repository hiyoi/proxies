from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from config import DB_URI
eng = create_engine(DB_URI)
Base = declarative_base()


class Proxy(Base):
    __tablename__ = 'proxy'
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)

    def __init__(self, addr):
        self.address = addr

    def __repr__(self):
        return "<Proxy %s >" % (self.address)


Base.metadata.create_all(eng)
