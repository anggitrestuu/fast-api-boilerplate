# app/models/currency.py
from sqlalchemy import UUID, Column, ForeignKey, String, Integer, Boolean, Numeric, DateTime
from app.models.base import BaseModel
import sqlalchemy as sa

class Currency(BaseModel):
    __tablename__ = "currencies"

    code = Column(String(3), primary_key=True)  # Override default UUID id
    name = Column(String, nullable=False)
    symbol = Column(String)
    decimal_places = Column(Integer, nullable=False, default=2)
    is_active = Column(Boolean, nullable=False, default=True)

class CurrentExchangeRate(BaseModel):
    __tablename__ = "current_exchange_rates"

    from_currency = Column(String(3), ForeignKey("currencies.code"), nullable=False)
    to_currency = Column(String(3), ForeignKey("currencies.code"), nullable=False)
    rate = Column(Numeric, nullable=False)
    source = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        sa.UniqueConstraint('from_currency', 'to_currency', name='uq_currency_pair'),
    )

class HistoricalExchangeRate(BaseModel):
    __tablename__ = "historical_exchange_rates"

    current_rate_id = Column(UUID(as_uuid=True), ForeignKey("current_exchange_rates.id"), nullable=False)
    rate = Column(Numeric, nullable=False)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True))

    current_rate = sa.orm.relationship("CurrentExchangeRate", backref="historical_rates")