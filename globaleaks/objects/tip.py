import sha
import random


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

    def __init__(self, fields, comments, pertinence, expiration_time):
        print "initing."
        self.fields = fields
        self.comments = comments
        self.pertinence = pertinence
        self.expiration_time = expiration_time

    def __repr__(self):
        return "<InternalTip: (%s, %s, %s, %s, %s)" % (self.fields, \
                self.material, self.comments, self.pertinence, \
                self.expiration_time)

class Tip(Base):
    __tablename__ = 'tip'
    id = Column(Integer, primary_key=True)
    internal_id = Column(Integer, ForeignKey('internaltip.id'))
    address = Column(String)
    password = Column(String)

    def __init__(self, internal_id):
        self.internal_id = internal_id
        self.gen_address()

    def gen_address(self):
        # XXX DANGER CHANGE!!
        self.address = sha.sha(''.join(str(random.randint(1,100)) for x in range(1,10))).hexdigest()
        print self.address
        self.password = ""

    def add_comment(self, data):
        pass

class ReceiverTip(Tip):
    total_view_count = Column(Integer, default=0)
    total_download_count = Column(Integer, default=0)
    relative_view_count = Column(Integer, default=0)
    relative_download_count = Column(Integer, default=0)

    __mapper_args__ = {'polymorphic_identity':'tip'}

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

session = Session()

import datetime
Base.metadata.create_all(engine)
#material = StoredFile()
internal_tip = InternalTip({'a':'b','c':'d'}, {'a':1}, 42, datetime.datetime.now())

session.add(internal_tip)
session.commit()

for x in range(1,10):
    recv_tip = ReceiverTip(internal_tip.id)
    session.add(recv_tip)
    internal_tip.children.append(recv_tip)
    session.commit()

tip_addr = recv_tip.address

res = session.query(Tip).filter_by(address=tip_addr).one()
#res = session.query(InternalTip).filter_by(InternalTip.children.address=tip_addr).one()

#res = session.query(InternalTip).options(joinedload('children')).filter_by(address=tip_addr).one()
internal_tip = session.query(InternalTip).filter_by(id=res.internal_id).one()

print internal_tip
