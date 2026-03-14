import ast
import re
from typing import Tuple, List
from ..models.shemas import CodeCompareRequest


class CodeValidator:
    """Валидатор Python кода"""

    MAX_CODE_LENGTH = 10000  # максимальная длина кода в символах
    MAX_AST_NODES = 1000  # максимальное количество узлов в AST

    @staticmethod
    def validate_python_syntax(code: str) -> Tuple[bool, str]:
        """Проверка синтаксиса Python кода"""
        try:
            ast.parse(code)
            return True, "Синтаксис корректен"
        except SyntaxError as e:
            return False, f"Синтаксическая ошибка: {e}"

    @staticmethod
    def validate_code_length(code: str) -> Tuple[bool, str]:
        """Проверка длины кода"""
        if len(code) > CodeValidator.MAX_CODE_LENGTH:
            return False, f"Код слишком длинный. Максимум: {CodeValidator.MAX_CODE_LENGTH} символов"
        return True, "Длина кода в допустимых пределах"

    @staticmethod
    def detect_potential_issues(code: str) -> List[str]:
        """Обнаружение потенциально проблемных конструкций"""
        issues = []

        # Проверка на бесконечные циклы
        if 'while True:' in code or 'while 1:' in code:
            issues.append("Обнаружен потенциально бесконечный цикл")

        # Проверка на опасные импорты (для демонстрации)
        dangerous_imports = ['os.system', 'subprocess.run', 'eval', 'exec']
        for imp in dangerous_imports:
            if imp in code:
                issues.append(f"Обнаружен потенциально опасный вызов: {imp}")

        return issues

    @staticmethod
    def estimate_ast_complexity(code: str) -> Tuple[bool, str, int]:
        """Оценка сложности AST"""
        try:
            tree = ast.parse(code)
            node_count = len(list(ast.walk(tree)))

            if node_count > CodeValidator.MAX_AST_NODES:
                return False, f"AST слишком сложный. Узлов: {node_count}, максимум: {CodeValidator.MAX_AST_NODES}", node_count
            return True, f"Сложность AST допустима. Узлов: {node_count}", node_count
        except SyntaxError:
            return False, "Невозможно оценить сложность из-за синтаксических ошибок", 0

    @classmethod
    def full_validation(cls, code: str) -> Tuple[bool, List[str]]:
        """Полная валидация кода"""
        errors = []
        warnings = []

        # Проверка синтаксиса
        is_valid, syntax_msg = cls.validate_python_syntax(code)
        if not is_valid:
            errors.append(syntax_msg)
        else:
            # Проверка длины
            is_valid, length_msg = cls.validate_code_length(code)
            if not is_valid:
                errors.append(length_msg)

            # Проверка сложности AST
            is_valid, complexity_msg, _ = cls.estimate_ast_complexity(code)
            if not is_valid:
                errors.append(complexity_msg)

            # Поиск потенциальных проблем
            issues = cls.detect_potential_issues(code)
            warnings.extend(issues)

        return len(errors) == 0, errors + warnings


# Создаем экземпляр валидатора для использования
validator = CodeValidator()