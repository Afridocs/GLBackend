import sha
import random
from sqlalchemy import Table, Column, Integer
from sqlalchemy import ForeignKey, String, PickleType, Date
from sqlalchemy.orm import relationship, backref, subqueryload, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()

class MaterialSet(Base):
    """
    This represents a material set: a collection of files.
    """
    __tablename__ = 'materialset'
    id = Column(Integer, primary_key=True)
    tip_id = Column(Integer, ForeignKey('internaltip.id'))
    material = relationship("StoredFile", backref='materialset')

    description = Column(String)
    def __init__(self, description):
        self.description = description

class StoredFile(Base):
    """
    Represents a material: a file.
    """
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True)
    material_set_id = Column(Integer, ForeignKey('materialset.id'))

    file_location = Column(String)
    description = Column(String)

    def __init__(self, file_location, description):
        self.file_location = file_location
        self.description = description

