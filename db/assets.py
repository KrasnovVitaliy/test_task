import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
import db.base as base


class Assets(base.Base):
    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))

    def __init__(self, name):
        self.name = name

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'name']
        return self.serialize(to_serialize)
