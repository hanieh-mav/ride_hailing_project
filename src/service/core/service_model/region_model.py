from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, NVARCHAR
from sqlalchemy.orm import relationship

from src.service.core.service_model.base import Base


class RegionModel(Base):
    __tablename__ = 'Region'
    __table_args__ = {'schema': 'ride.hailing'}

    id = Column('Id', Integer, primary_key=True)
    place_id = Column('PlaceId', Integer, nullable=False, unique=True)
    name = Column('Name', NVARCHAR(200), nullable=False)
    last_modified_date = Column('LastModifiedDate', DateTime, default=datetime.now(timezone.utc),
                                onupdate=datetime.now(timezone.utc))
    entry_date = Column('EntryDate', DateTime, default=datetime.now(timezone.utc))

    region_request = relationship('RegionRequestModel', back_populates="region")
