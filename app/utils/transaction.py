# app/utils/transaction.py
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import APIError

def transaction_handler():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the service instance (self) and find its db session
            service_instance = args[0]
            db: AsyncSession = service_instance.db
            
            try:
                result = await func(*args, **kwargs)
                await db.commit()
                return result
            except Exception as e:
                await db.rollback()
                raise e
        return wrapper
    return decorator