from pydantic import BaseModel, Field
from typing import List, Any, Optional
from enum import Enum

class DifferenceType(str, Enum):
    VARIABLE_RENAMED = "variable_renamed"
    EXPRESSION_CHANGED = "expression_changed"
    FUNCTION_MODIFIED = "function_modified"
    STRUCTURE_CHANGED = "structure_changed"
    COMMENT_ADDED = "comment_added"
    COMMENT_REMOVED = "comment_removed"

class CodeCompareRequest(BaseModel):
    """Схема для запроса сравнения кода"""
    code1: str = Field(..., min_length=1, description="Первый фрагмент кода для сравнения")
    code2: str = Field(..., min_length=1, description="Второй фрагмент кода для сравнения")
    ignore_comments: bool = Field(False, description="Игнорировать комментарии при сравнении")
    ignore_whitespace: bool = Field(False, description="Игнорировать пробелы и переносы строк")

class Difference(BaseModel):
    """Описание одного различия в коде"""
    type: DifferenceType
    description: str
    location: Optional[str] = None
    details: Optional[dict] = None

class ComparisonResult(BaseModel):
    """Результат сравнения двух фрагментов кода"""
    are_identical: bool
    similarity_score: float = Field(..., ge=0, le=1, description="Оценка схожести от 0 до 1")
    total_differences: int
    differences: List[Difference]
    ast_size1: int = Field(..., description="Размер AST первого кода")
    ast_size2: int = Field(..., description="Размер AST второго кода")