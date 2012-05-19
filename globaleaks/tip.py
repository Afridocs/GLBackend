from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InternalTip(Base):
    """
    This is the internal representation of a Tip that has been submitted to the
    GlobaLeaks node.
    It has a one-to-many association with the individual Tips of every receiver
    and whistleblower.
    """
    __tablename__ = 'internaltip'

    id = Column(Integer, primary_key=True)
    children = relationship("Tip", backref='internaltip')

    fields = Column(PickleType)
    material = relationship("MaterialSet")
    comments = Column(PickleType)
    pertinence = Column(Integer)
    expiration_time = Column(Date)

class MaterialSet(Base):
    """
    This represents a material set: a collection of files.
    """
    __tablename__ = 'materialset'
    id = Column(Integer, primary_key=True)
    tip_id = Column(Integer, ForeignKey('internaltip.id'))
    material = relationship("Material", backref='materialset')

    description = Column(String)

class Material(Base):
    """
    Represents a material: a file.
    """
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True)
    material_set_id = Column(Integer, ForeignKey('materialset.id'))

    file_location = Column(String)
    description = Column(String)

class Tip(Base):
    __tablename__ = 'tip'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('internaltip.id'))
    address = Column(String)
    password = Column(String)

    def add_comment(self, data):
        pass

class ReceiverTip(Tip):
    total_view_count = Column(Integer)
    total_download_count = Column(Integer)
    relative_view_count = Column(Integer)
    relative_download_count = Column(Integer)

    def increment_visit(self):
        pass

    def increment_download(self):
        pass

    def delete_tulip(self):
        pass

    def download_material(self, id):
        pass

class WhistleblowerTip(Tip):
    def add_material(self):
        pass

