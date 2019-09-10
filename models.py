# models.py

__author__ = 'rijumone.choudhuri@decision-tree.com'


import os
import datetime
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf/conf.ini'))

# Setting up SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

Base = declarative_base()

def get_session():
    engine = create_engine(
        'mysql+mysqlconnector://{user}:{pw}@{host}:{port}/{db}'.format(
            user=config['DATABASE']['username'],
            pw=config['DATABASE']['password'],
            host=config['DATABASE']['host'],
            db=config['DATABASE']['database'],
            port=config['DATABASE']['port'],
            ), 
        echo=False
        )
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class Contacts(Base):
    
    __tablename__ = 'woc_contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    is_active = Column(Boolean())
    
    def __repr__(self):
        return "<Contacts(id={id}, name={name}, is_active={is_active})>".format(
            id=self.id,
            name=self.name,
            is_active=self.is_active,
            )

class History(Base):
    
    __tablename__ = 'woc_history'

    id = Column(Integer, primary_key=True)
    status = Column(String())
    contact_id = Column(Integer)
    timestamp = Column(DateTime(), nullable=True)
    
    def __repr__(self):
        return "<History(id={id}, status={status}, contact_id={contact_id}, timestamp={timestamp})>".format(
            id=self.id,
            status=self.status,
            timestamp=self.timestamp,
            contact_id=self.contact_id,
            )


class Waits(Base):
    
    __tablename__ = 'woc_waits'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    value = Column(Integer)
    
    def __repr__(self):
        return "<Waits(id={id}, name={name}, value={value})>".format(
            id=self.id,
            name=self.name,
            value=self.value,
            )

