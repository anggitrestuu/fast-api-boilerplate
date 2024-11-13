from sqlalchemy import Column, ForeignKey, Numeric, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
from app.models.enums import TokenType
import sqlalchemy as sa

class CurrentUsageRate(BaseModel):
    __tablename__ = "current_usage_rates"

    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=False)
    token_type = Column(SQLEnum(TokenType), nullable=False)
    credits_per_1k_tokens = Column(Numeric, nullable=False)
    min_tokens = Column(Integer, default=1)
    is_rounded_up = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    model = sa.orm.relationship("AIModel", backref="usage_rates")

class HistoricalUsageRate(BaseModel):
    __tablename__ = "historical_usage_rates"

    current_rate_id = Column(UUID(as_uuid=True), ForeignKey("current_usage_rates.id"), nullable=False)
    credits_per_1k_tokens = Column(Numeric, nullable=False)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True))

    current_rate = sa.orm.relationship("CurrentUsageRate", backref="historical_rates")