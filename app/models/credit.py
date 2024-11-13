from sqlalchemy import (
    Column, ForeignKey, Numeric, String,
    Boolean, DateTime
)
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
from app.models.base import BaseModel
from app.models.enums import AccountStatus, TransactionType, TransactionStatus, PurchaseStatus
from sqlalchemy.dialects.postgresql import JSONB
from app.models.currency import Currency

class CreditAccount(BaseModel):
    __tablename__ = "credit_accounts"

    org_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    balance = Column(Numeric, nullable=False, default=0)
    status = Column(sa.Enum(AccountStatus), nullable=False, default=AccountStatus.ACTIVE)
    deleted_at = Column(DateTime(timezone=True))

    __table_args__ = (
        # Ensure either org_id or user_id is set, but not both
        sa.CheckConstraint(
            '(org_id IS NOT NULL AND user_id IS NULL) OR (org_id IS NULL AND user_id IS NOT NULL)',
            name='valid_owner_check'
        ),
    )

class CreditTransaction(BaseModel):
    __tablename__ = "credit_transactions"

    account_id = Column(UUID(as_uuid=True), ForeignKey("credit_accounts.id"), nullable=False)
    amount = Column(Numeric, nullable=False)
    balance_after = Column(Numeric, nullable=False)
    type = Column(sa.Enum(TransactionType), nullable=False)
    status = Column(
        sa.Enum(TransactionStatus), 
        nullable=False, 
        default=TransactionStatus.PENDING
    )
    reference_type = Column(String, nullable=False)
    reference_id = Column(UUID(as_uuid=True), nullable=False)
    meta_data = Column(JSONB)

    account = sa.orm.relationship("CreditAccount", backref="transactions")

class CreditPackage(BaseModel):
    __tablename__ = "credit_packages"

    name = Column(String, nullable=False)
    credits_amount = Column(Numeric, nullable=False)
    price_amount = Column(Numeric, nullable=False)
    price_currency = Column(String, ForeignKey("currencies.code"), nullable=False)
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True))

class CreditPurchase(BaseModel):
    __tablename__ = "credit_purchases"

    account_id = Column(UUID(as_uuid=True), ForeignKey("credit_accounts.id"), nullable=False)
    package_id = Column(UUID(as_uuid=True), ForeignKey("credit_packages.id"), nullable=False)
    credits_amount = Column(Numeric, nullable=False)
    price_amount = Column(Numeric, nullable=False)
    price_currency = Column(String, ForeignKey("currencies.code"), nullable=False)
    payment_method = Column(String)
    payment_reference = Column(String)
    status = Column(sa.Enum(PurchaseStatus), nullable=False, default=PurchaseStatus.PENDING)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("credit_transactions.id"))

    account = sa.orm.relationship("CreditAccount", backref="purchases")
    package = sa.orm.relationship("CreditPackage")
    transaction = sa.orm.relationship("CreditTransaction")
    currency = sa.orm.relationship("Currency")