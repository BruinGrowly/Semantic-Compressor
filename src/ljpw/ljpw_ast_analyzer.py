#!/usr/bin/env python3
"""
AST-based Python Code Analyzer for LJPW

This is an EXPERIMENTAL implementation using Abstract Syntax Tree parsing
to analyze Python code structure and calculate LJPW coordinates.

Purpose: Compare against regex-based approach to see which is more accurate.
Status: UNVALIDATED - needs empirical testing
"""

import ast
from typing import Dict, Any, List, Tuple
from pathlib import Path


class ASTPatternCounter:
    """Counts AST patterns in Python code"""

    def __init__(self):
        self.patterns = {
            # L (Love/Safety) patterns
            'try_except': 0,
            'assert_statements': 0,
            'type_checks': 0,
            'validation_checks': 0,
            'raise_exceptions': 0,

            # J (Justice/Structure) patterns
            'class_definitions': 0,
            'function_definitions': 0,
            'type_annotations': 0,
            'docstrings': 0,
            'imports': 0,

            # P (Power/Execution) patterns
            'list_comprehensions': 0,
            'generator_expressions': 0,
            'lambda_functions': 0,
            'async_functions': 0,
            'decorators': 0,

            # W (Wisdom/Design) patterns
            'abstract_methods': 0,
            'property_decorators': 0,
            'context_managers': 0,
            'metaclasses': 0,
            'design_patterns': 0,
        }

        self.total_nodes = 0
        self.total_lines = 0

    def visit(self, node: ast.AST):
        """Visit AST node and count patterns"""
        self.total_nodes += 1

        # L (Safety) patterns
        if isinstance(node, ast.Try):
            self.patterns['try_except'] += 1
        elif isinstance(node, ast.Assert):
            self.patterns['assert_statements'] += 1
        elif isinstance(node, ast.Raise):
            self.patterns['raise_exceptions'] += 1
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ('isinstance', 'issubclass', 'hasattr'):
                    self.patterns['type_checks'] += 1
                elif node.func.id in ('validate', 'check', 'verify'):
                    self.patterns['validation_checks'] += 1

        # J (Structure) patterns
        elif isinstance(node, ast.ClassDef):
            self.patterns['class_definitions'] += 1
            # Check for docstring
            if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
                self.patterns['docstrings'] += 1
        elif isinstance(node, ast.FunctionDef):
            self.patterns['function_definitions'] += 1
            # Check for docstring
            if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
                self.patterns['docstrings'] += 1
            # Check for type annotations
            if node.returns or any(arg.annotation for arg in node.args.args):
                self.patterns['type_annotations'] += 1
            # Check for async
            if isinstance(node, ast.AsyncFunctionDef):
                self.patterns['async_functions'] += 1
            # Check for decorators
            if node.decorator_list:
                self.patterns['decorators'] += len(node.decorator_list)
                # Check for property
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Name) and dec.id == 'property':
                        self.patterns['property_decorators'] += 1
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            self.patterns['imports'] += 1

        # P (Power/Execution) patterns
        elif isinstance(node, ast.ListComp):
            self.patterns['list_comprehensions'] += 1
        elif isinstance(node, ast.GeneratorExp):
            self.patterns['generator_expressions'] += 1
        elif isinstance(node, ast.Lambda):
            self.patterns['lambda_functions'] += 1

        # W (Wisdom/Design) patterns
        elif isinstance(node, ast.With):
            self.patterns['context_managers'] += 1

        # Recursively visit children
        for child in ast.iter_child_nodes(node):
            self.visit(child)


class LJPWASTAnalyzer:
    """AST-based LJPW code analyzer"""

    def __init__(self):
        # Baseline weights for each dimension (tuned via experimentation)
        self.baseline_weights = {
            'L': 0.618,  # φ⁻¹
            'J': 0.414,  # √2-1
            'P': 0.718,  # e-2
            'W': 0.693,  # ln(2)
        }

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file and return LJPW coordinates"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            return self.analyze_code(code)

        except Exception as e:
            # Return baseline on error
            return {
                'L': self.baseline_weights['L'],
                'J': self.baseline_weights['J'],
                'P': self.baseline_weights['P'],
                'W': self.baseline_weights['W'],
                'error': str(e),
            }

    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze Python code string and return LJPW coordinates"""
        try:
            tree = ast.parse(code)
            counter = ASTPatternCounter()
            counter.visit(tree)
            counter.total_lines = len(code.split('\n'))

            # Calculate LJPW coordinates from pattern counts
            ljpw = self._calculate_ljpw(counter)

            return ljpw

        except SyntaxError as e:
            # Invalid Python code - return baseline
            return {
                'L': self.baseline_weights['L'],
                'J': self.baseline_weights['J'],
                'P': self.baseline_weights['P'],
                'W': self.baseline_weights['W'],
                'error': f'SyntaxError: {e}',
            }

    def _calculate_ljpw(self, counter: ASTPatternCounter) -> Dict[str, float]:
        """Calculate LJPW coordinates from pattern counts"""

        # Avoid division by zero
        total = max(counter.total_nodes, 1)

        # L (Love/Safety) - error handling and validation
        l_patterns = (
            counter.patterns['try_except'] * 3.0 +
            counter.patterns['assert_statements'] * 2.0 +
            counter.patterns['type_checks'] * 1.5 +
            counter.patterns['validation_checks'] * 2.0 +
            counter.patterns['raise_exceptions'] * 1.0
        )
        L = self.baseline_weights['L'] + (l_patterns / total) * 0.4

        # J (Justice/Structure) - organization and documentation
        j_patterns = (
            counter.patterns['class_definitions'] * 3.0 +
            counter.patterns['function_definitions'] * 2.0 +
            counter.patterns['type_annotations'] * 2.5 +
            counter.patterns['docstrings'] * 2.0 +
            counter.patterns['imports'] * 0.5
        )
        J = self.baseline_weights['J'] + (j_patterns / total) * 0.6

        # P (Power/Execution) - computational efficiency
        p_patterns = (
            counter.patterns['list_comprehensions'] * 2.0 +
            counter.patterns['generator_expressions'] * 2.5 +
            counter.patterns['lambda_functions'] * 1.5 +
            counter.patterns['async_functions'] * 3.0 +
            counter.patterns['decorators'] * 1.0
        )
        P = self.baseline_weights['P'] + (p_patterns / total) * 0.3

        # W (Wisdom/Design) - architectural patterns
        w_patterns = (
            counter.patterns['abstract_methods'] * 3.0 +
            counter.patterns['property_decorators'] * 2.0 +
            counter.patterns['context_managers'] * 2.5 +
            counter.patterns['metaclasses'] * 3.0
        )
        W = self.baseline_weights['W'] + (w_patterns / total) * 0.4

        # Clamp to [0, 1.5] range (LJPW_MAX_VALUE)
        L = min(max(L, 0.0), 1.5)
        J = min(max(J, 0.0), 1.5)
        P = min(max(P, 0.0), 1.5)
        W = min(max(W, 0.0), 1.5)

        return {
            'L': L,
            'J': J,
            'P': P,
            'W': W,
        }

    def analyze_directory(self, path: str) -> List[Dict[str, Any]]:
        """Analyze all Python files in a directory"""
        results = []

        for py_file in Path(path).rglob("*.py"):
            result = self.analyze_file(str(py_file))
            result['file'] = str(py_file)
            results.append(result)

        return results


if __name__ == '__main__':
    # Quick test
    analyzer = LJPWASTAnalyzer()

    test_code = """
def calculate_sum(a: int, b: int) -> int:
    \"\"\"Calculate sum of two numbers\"\"\"
    try:
        result = a + b
        if not isinstance(result, int):
            raise TypeError("Result must be int")
        return result
    except Exception as e:
        raise ValueError(f"Calculation failed: {e}")
"""

    result = analyzer.analyze_code(test_code)
    print(f"LJPW: L={result['L']:.3f}, J={result['J']:.3f}, P={result['P']:.3f}, W={result['W']:.3f}")
