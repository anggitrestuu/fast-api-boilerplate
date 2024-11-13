## Project Structure

```

├── app/
│ ├── **init**.py
│ ├── main.py # FastAPI application initialization
│ ├── api/ # API endpoints
│ │ ├── **init**.py
│ │ ├── v1/ # API version 1
│ │ │ ├── **init**.py
│ │ │ ├── endpoints/ # API route handlers
│ │ │ └── router.py # Router configuration
│ ├── core/ # Core functionality
│ │ ├── **init**.py
│ │ ├── config.py # Configuration settings
│ │ ├── security.py # Security utilities
│ │ ├── exceptions.py # Custom exceptions
│ │ └── repository.py # Base repository class
│ ├── db/ # Database configuration
│ │ ├── **init**.py
│ │ ├── base.py # SQLAlchemy base setup
│ │ └── session.py # Database session management
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic models
│ ├── services/ # Business logic
│ ├── utils/ # Utility functions
│ └── repositories/ # Database queries
├── tests/ # Test files
├── alembic/ # Database migrations
├── docker/ # Docker configuration
├── scripts/ # Utility scripts
├── .env # Environment variables
├── .env.example # Example environment variables
├── requirements.txt # Project dependencies
└── README.md # Project documentation

```

## Core

```python
# app/core/repository.py
from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
from pydantic import BaseModel
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    async def create(self, schema: CreateSchemaType) -> ModelType:
        db_obj = self.model(**schema.model_dump(exclude_unset=True))
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def get(self, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: dict = None
    ) -> tuple[List[ModelType], int]:
        stmt = select(self.model)

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    stmt = stmt.where(getattr(self.model, key) == value)

        total = await self.db.scalar(select(func.count()).select_from(stmt))

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)

        return result.scalars().all(), total

    async def update(
        self,
        *,
        id: Any,
        schema: UpdateSchemaType
    ) -> Optional[ModelType]:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**schema.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.scalar_one_or_none()

    async def delete(self, *, id: Any) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.rowcount > 0
```

## Creating New APIs

### 1. Create Model (`app/models/example.py`)

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class ExampleModel(Base):
    __tablename__ = "example_table"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### 2. Create Schema (`app/schemas/example.py`)

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel, ConfigDict

class BaseSchema(PydanticBaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExampleBase(PydanticBaseModel):
    name: str

class ExampleCreate(PydanticBaseModel):
    pass

class ExampleUpdate(PydanticBaseModel):
    pass

class ExampleResponse(BaseSchema):
    pass
```

### 3. Create Repository (`app/repositories/example.py`)

```python
from app.core.repository import BaseRepository
from app.models.example import ExampleModel
from app.schemas.example import ExampleCreate, ExampleUpdate

class ExampleRepository(BaseRepository[ExampleModel, ExampleCreate, ExampleUpdate]):
    pass
```

### 4. Create Service (`app/services/example.py`)

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.example import ExampleRepository
from app.models.example import ExampleModel
from app.schemas.example import ExampleCreate, ExampleUpdate

class ExampleService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repository = ExampleRepository(ExampleModel, db)

    async def create(self, schema: ExampleCreate):
        return await self.repository.create(schema)

    async def get(self, id: int):
        return await self.repository.get(id)
```

### 5. Create API Endpoint (`app/api/v1/endpoints/example.py`)

```python
from fastapi import APIRouter, Depends
from app.services.example import ExampleService
from app.schemas.example import Example, ExampleCreate
from app.utils.response_handler import success_response

router = APIRouter()

@router.post("/", response_model=Example)
async def create_example(
    schema: ExampleCreate,
    service: ExampleService = Depends()
):
    item = await service.create(schema)
    return success_response(
        data=Example.model_validate(item),
        message="Example created successfully"
    )
```

### 6. Register Router (`app/api/v1/router.py`)

```python
from fastapi import APIRouter
from app.api.v1.endpoints import example

api_router = APIRouter()
api_router.include_router(example.router, prefix="/examples", tags=["examples"])
```
