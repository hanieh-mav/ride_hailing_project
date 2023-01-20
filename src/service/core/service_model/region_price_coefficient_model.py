from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey

from src.service.core.service_model import Base, RegionModel


class RegionPriceCoefficientModel(Base):
    __tablename__ = 'RegionPriceCoefficient'
    __table_args__ = {'schema': 'ride.hailing'}

    id = Column('Id', Integer, primary_key=True)
    region_id = Column('RegionId', ForeignKey(RegionModel.id))
    price_coefficient = Column('PriceCoefficient', Float, nullable=False)
    last_modified_date = Column('LastModifiedDate', DateTime, default=datetime.now(timezone.utc),
                                onupdate=datetime.now(timezone.utc))
    entry_date = Column('EntryDate', DateTime, default=datetime.now(timezone.utc))

