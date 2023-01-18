from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, Float

from src.service.core.service_model import Base


class RequestThresholdCoefficientModel(Base):
    __tablename__ = 'RequestThresholdCoefficient'
    __table_args__ = {'schema': 'ride.hailing'}

    id = Column('Id', Integer, primary_key=True)
    request_threshold = Column('RequestThreshold', Integer, nullable=False)
    price_coefficient = Column('PriceCoefficient', Float, nullable=False)
    last_modified_date = Column('LastModifiedDate', DateTime, default=datetime.now(timezone.utc),
                                onupdate=datetime.now(timezone.utc))
    entry_date = Column('EntryDate', DateTime, default=datetime.now(timezone.utc))

    def make_dict_data(self):
        return {'id': self.id, 'request_threshold': self.request_threshold, 'price_coefficient': self.price_coefficient}
