from sqlalchemy import Column, String, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
from app.models.enums import MetricUnit, ModelMetricType, ModelStatus, ModelType
import sqlalchemy as sa

class AIModel(BaseModel):
    __tablename__ = "ai_models"

    name = Column(String, nullable=False)
    type = Column(SQLEnum(ModelType), nullable=False)
    version = Column(String, nullable=False)
    status = Column(SQLEnum(ModelStatus), nullable=False, default=ModelStatus.ACTIVE)
    description = Column(Text)
    configuration = Column(JSON)

    __table_args__ = (
        sa.UniqueConstraint('name', 'version', name='uq_model_name_version'),
    )

class ModelMetric(BaseModel):
    __tablename__ = "model_metrics"

    model_id = Column(UUID(as_uuid=True), sa.ForeignKey("ai_models.id"), nullable=False)
    metric_type = Column(SQLEnum(ModelMetricType), nullable=False)
    unit_type = Column(SQLEnum(MetricUnit), nullable=False)
    unit_size = Column(sa.Integer, nullable=False, default=1000)
    base_cost = Column(sa.Numeric, nullable=False)
    valid_from = Column(sa.DateTime(timezone=True), nullable=False)
    valid_to = Column(sa.DateTime(timezone=True))
    is_active = Column(sa.Boolean, default=True)

    model = sa.orm.relationship("AIModel", backref="metrics")