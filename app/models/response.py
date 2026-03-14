from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    """Стандартный формат ответа API"""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    """Формат ответа для ошибок"""
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[dict] = None