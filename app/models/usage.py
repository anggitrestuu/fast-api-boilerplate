from sqlalchemy import (
    Column, ForeignKey, Integer, Text, String, 
    Boolean, DateTime, BigInteger, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
from app.models.base import BaseModel

class UsageEvent(BaseModel):
    __tablename__ = "usage_events"

    account_id = Column(UUID(as_uuid=True), ForeignKey("credit_accounts.id"), nullable=False)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=False)
    request_id = Column(UUID(as_uuid=True), unique=True)

    input_tokens = Column(Integer, nullable=False, default=0)
    output_tokens = Column(Integer, nullable=False, default=0)
    credits_consumed = Column(Numeric, nullable=False)
    credit_transaction_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("credit_transactions.id")
    )

    success = Column(Boolean, nullable=False, default=True)
    error_code = Column(String)
    error_message = Column(Text)

    ip_address = Column(String)
    user_agent = Column(String)
    
    requested_at = Column(DateTime(timezone=True), nullable=False)
    processed_at = Column(DateTime(timezone=True))

    transaction = sa.orm.relationship("CreditTransaction")

class UsageEventMetadata(BaseModel):
    __tablename__ = "usage_event_metadata"

    usage_event_id = Column(UUID(as_uuid=True), ForeignKey("usage_events.id"), nullable=False)
    metadata_type = Column(String, nullable=False)  # 'request' or 'response'
    key = Column(String, nullable=False)
    value = Column(Text)

    usage_event = sa.orm.relationship("UsageEvent", backref="metadata")

class UsageAggregateDaily(BaseModel):
    __tablename__ = "usage_aggregates_daily"

    account_id = Column(UUID(as_uuid=True), ForeignKey("credit_accounts.id"), nullable=False)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=False)
    date = Column(sa.Date, nullable=False)

    total_input_tokens = Column(BigInteger, nullable=False, default=0)
    total_output_tokens = Column(BigInteger, nullable=False, default=0)
    total_input_credits = Column(Numeric, nullable=False, default=0)
    total_output_credits = Column(Numeric, nullable=False, default=0)
    total_credits_consumed = Column(Numeric, nullable=False, default=0)

    total_requests = Column(Integer, nullable=False, default=0)
    successful_requests = Column(Integer, nullable=False, default=0)
    failed_requests = Column(Integer, nullable=False, default=0)

    avg_processing_time_ms = Column(Integer)
    p95_processing_time_ms = Column(Integer)
    max_processing_time_ms = Column(Integer)

class UsageQuota(BaseModel):
    __tablename__ = "usage_quotas"

    account_id = Column(UUID(as_uuid=True), ForeignKey("credit_accounts.id"), nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=False)
    
    max_daily_credits = Column(Numeric)
    max_daily_requests = Column(Integer)
    max_requests_per_minute = Column(Integer)
    max_tokens_per_request = Column(Integer)

    account = sa.orm.relationship("CreditAccount", backref="quotas")
    model = sa.orm.relationship("AIModel", backref="quotas")