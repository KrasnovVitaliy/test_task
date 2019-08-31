import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
import db.base as base


class AssetsPrices(base.Base):
    __tablename__ = 'rates_prices'
    id = Column(Integer, primary_key=True)
    rate = Column(Integer, ForeignKey("rates.id"))
    timestamp = Column(Integer())
    value = Column(Integer())

    def __init__(self, rate, value, timestamp):
        self.rate = rate
        self.value = value
        self.timestamp = timestamp

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'rate', 'timestamp', 'value']
        return self.serialize(to_serialize)
