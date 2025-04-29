from sqlalchemy import Column, DateTime, func, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from app.db.base import Base
from uuid_extensions import uuid7
from datetime import datetime
from app.core.context import current_user_id, current_tenant_id


class SoftDeleteMixin:
    """Mixin for soft delete functionality"""

    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

    # List of fields that need unique constraint handling
    __unique_fields__ = []  # Override this in your models

    @property
    def soft_delete(self):
        """Method for soft delete"""
        self.deleted_at = func.now()
        # Handle unique fields
        for field_name in self.__unique_fields__:
            current_value = getattr(self, field_name)
            if current_value:
                # Add timestamp to make unique value
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                setattr(self, field_name, f"{current_value}_DELETED_{timestamp}")

    @property
    def is_deleted(self) -> bool:
        """Helper property untuk check status deleted"""
        return self.deleted_at is not None

    @declared_attr
    def __mapper_args__(cls):
        return {"eager_defaults": True, "inherit_condition": cls.deleted_at.is_(None)}


class BaseModel(Base):
    """Base model tanpa tenant"""

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), index=True)
    updated_by = Column(UUID(as_uuid=True))


class SoftDeleteModel(BaseModel, SoftDeleteMixin):
    """Base model dengan soft delete"""

    __abstract__ = True


class TenantModel(BaseModel):
    """Base model dengan tenant"""

    __abstract__ = True
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=True)


class TenantSoftDeleteModel(TenantModel, SoftDeleteMixin):
    """Base model dengan tenant dan soft delete"""

    __abstract__ = True


# Event listeners
@event.listens_for(BaseModel, "before_insert", propagate=True)
def set_created_fields(mapper, connection, target):
    user_id = current_user_id.get()
    if user_id:
        target.created_by = user_id
        target.updated_by = user_id


@event.listens_for(BaseModel, "before_update", propagate=True)
def set_updated_fields(mapper, connection, target):
    user_id = current_user_id.get()
    if user_id:
        target.updated_by = user_id


@event.listens_for(TenantModel, "before_insert", propagate=True)
def set_tenant_field(mapper, connection, target):
    tenant_id = current_tenant_id.get()
    if tenant_id:
        target.tenant_id = tenant_id
