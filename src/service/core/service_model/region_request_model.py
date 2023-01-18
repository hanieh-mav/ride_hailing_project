from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, BigInteger, ForeignKey

from src.service.core.service_model import Base
from src.service.core.service_model.region_model import RegionModel


class RegionRequestModel(Base):
    __tablename__ = 'RegionRequest'
    __table_args__ = {'schema': 'ride.hailing'}

    id = Column('Id', BigInteger, primary_key=True)
    region_id = Column('RegionId', ForeignKey(RegionModel.id))
    entry_date = Column('EntryDate', DateTime, default=datetime.now(timezone.utc))
