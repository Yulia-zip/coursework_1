from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.services.comparsion_engine import ComparisonEngine

router = APIRouter(prefix="/compare", tags=["sql_comparison"])


class SQLCompareRequest(BaseModel):
    query1: str
    query2: str


class MethodResult(BaseModel):
    method_name: str
    are_equivalent: bool
    explanation: str
    details: Dict[str, Any]


class SQLComparisonResult(BaseModel):
    overall_equivalent: bool
    overall_similarity: float
    method_results: List[MethodResult]
    differences: List[str]


@router.post("/")
async def compare_sql_queries(request: SQLCompareRequest):

    try:
        comparator = ComparisonEngine()

        raw_results = comparator.compare_all_methods(request.query1, request.query2)

        method_results = []
        differences = []

        for method_name, result in raw_results.items():
            method_result = {
                "method_name": method_name,
                "are_equivalent": result.get("are_equivalent", False),
                "explanation": result.get("explanation", ""),
                "details": result
            }
            method_results.append(method_result)

            if not result.get("are_equivalent", False):
                differences.append(f"Метод {method_name}: {result.get('explanation', 'запросы не эквивалентны')}")

        overall_equivalent = any(result["are_equivalent"] for result in method_results)

        overall_similarity = calculate_overall_similarity(method_results)

        return {
            "success": True,
            "overall_equivalent": overall_equivalent,
            "overall_similarity": overall_similarity,
            "method_results": method_results,
            "differences": differences
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Ошибка при сравнении: {str(e)}"
        }


def calculate_overall_similarity(method_results: List[Dict]) -> float:
    weights = {"hash": 0.2, "normalized": 0.3, "ast": 0.5}
    total_similarity = 0

    for result in method_results:
        weight = weights.get(result["method_name"], 0.1)
        similarity = 1.0 if result["are_equivalent"] else 0.0
        total_similarity += similarity * weight

    return round(total_similarity, 2)


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SQL Query Comparator"}