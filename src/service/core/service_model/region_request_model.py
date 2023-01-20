from datetime import datetime, timezone
from src.service.core.service_model.base import Base

from sqlalchemy import Column, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.service.core.service_model import RegionModel


class RegionRequestModel(Base):
    __tablename__ = 'RegionRequest'
    __table_args__ = {'schema': 'ride.hailing'}

    id = Column('Id', BigInteger, primary_key=True)
    region_id = Column('RegionId', ForeignKey(RegionModel.id))
    entry_date = Column('EntryDate', DateTime, default=datetime.now(timezone.utc))

    region = relationship('RegionModel', back_populates="region_request", cascade="all,delete")
