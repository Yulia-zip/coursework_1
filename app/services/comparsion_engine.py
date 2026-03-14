import hashlib

from app.services.ast_comparator import ASTNormalizer
from app.services.normalize import SQL_Normalize

class ComparisonEngine:

    def __init__(self):
        self.normalizer=SQL_Normalize()

    def compare(self,query1: str, query2: str, method: str = "auto") -> dict:
        if method=="hash":
            return self.compare_hash(query1,query2)
        elif method=="normalized":
            return self.compare_normalized(query1,query2)
        elif method=="ast":
            return self.compare_ast(query1,query2)
        elif method=="auto":
            return self.compare_auto(query1,query2)
        else:
            raise ValueError(f"Неизвестный метод сравнения:{method}")


    def compare_all_methods(self,query1: str, query2: str)->dict:
        return {
            "hash": self.compare_hash(query1, query2),
            "normalized": self.compare_normalized(query1, query2),
            "ast": self.compare_ast(query1, query2)
        }

    def compare_hash(self,query1: str, query2: str)->dict:
        hash1=hashlib.sha256(query1.encode()).hexdigest()
        hash2=hashlib.sha256(query2.encode()).hexdigest()
        are_equivalence=hash1==hash2

        return {
            "method": "hash",
            "are_equivalent": are_equivalence,
            "hash1": hash1[:16] + "...",  # Сокращенный для показа
            "hash2": hash2[:16] + "...",
            "explanation": "Сравнение хешей исходных запросов (быстро, но ненадежно)"
        }

    def compare_normalized(self, q1: str, q2: str) -> dict:
        norm1 = self.normalizer.normalize(q1)
        norm2 = self.normalizer.normalize(q2)
        are_equivalent = norm1 == norm2

        return {
            "method": "normalized",
            "are_equivalent": are_equivalent,
            "normalized1": norm1,
            "normalized2": norm2,
            "explanation": "Сравнение после нормализации (регистр, пробелы)"
        }

    def compare_ast(self, q1: str, q2: str) -> dict:
        """Метод 3: AST сравнение с использованием sqlglot"""
        try:
            # Используем ваш ASTNormalizer
            ast_normalizer = ASTNormalizer()

            # Нормализуем оба запроса через AST
            ast1 = ast_normalizer.normalize(q1)
            ast2 = ast_normalizer.normalize(q2)

            # Сравниваем строковые представления нормализованных AST
            are_equivalent = str(ast1) == str(ast2)

            return {
                "method": "ast",
                "are_equivalent": are_equivalent,
                "ast1": str(ast1),
                "ast2": str(ast2),
                "explanation": "Сравнение абстрактных синтаксических деревьев (игнорирует порядок условий WHERE, JOIN)",
                "details": {
                    "ast_size1": len(list(ast1.walk())) if hasattr(ast1, 'walk') else 0,
                    "ast_size2": len(list(ast2.walk())) if hasattr(ast2, 'walk') else 0,
                    "normalization_applied": "Коммутативность AND/OR, сортировка условий"
                }
            }
        except Exception as e:
            return {
                "method": "ast",
                "are_equivalent": False,
                "error": str(e),
                "explanation": "Ошибка при AST анализе",
                "ast1": "",
                "ast2": ""
            }

    def compare_auto(self, q1: str, q2: str) -> dict:
        """Умное сравнение: быстрая проверка → точная"""
        # Сначала быстрая проверка хешем
        hash_result = self.compare_hash(q1, q2)
        if hash_result["are_equivalent"]:
            return hash_result

        # Если хеши разные, используем нормализацию
        normalized_result = self.compare_normalized(q1, q2)
        return normalized_result