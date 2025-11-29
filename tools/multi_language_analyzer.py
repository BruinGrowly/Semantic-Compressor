#!/usr/bin/env python3
"""
Multi-Language LJPW Analyzer
=============================

Analyzes code across multiple programming languages and computes LJPW coordinates.

Supports:
- Python
- JavaScript
- TypeScript
- Go (extensible to Rust, Java, C++)

Key Innovation: Language-agnostic semantic analysis

Usage:
    from multi_language_analyzer import analyze_code, compare_implementations

    # Analyze single file
    ljpw = analyze_code('quicksort.py', language='python')

    # Compare cross-language implementations
    results = compare_implementations({
        'python': 'quicksort.py',
        'javascript': 'quicksort.js',
        'go': 'quicksort.go'
    })
"""

import ast
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.ljpw.ljpw_standalone import compute_ljpw_coordinates
except ImportError:
    # Fallback implementation
    pass


@dataclass
class LJPWCoordinates:
    """LJPW coordinates for a code implementation"""

    L: float  # Love (Safety)
    J: float  # Justice (Structure)
    P: float  # Power (Performance)
    W: float  # Wisdom (Design)
    language: str
    file_path: str
    metadata: Dict[str, Any]

    def to_dict(self):
        return {
            "L": self.L,
            "J": self.J,
            "P": self.P,
            "W": self.W,
            "language": self.language,
            "file_path": self.file_path,
            "distance_from_anchor": self.distance_from_anchor(),
            "distance_from_ne": self.distance_from_ne(),
            "divine_perfection": self.divine_perfection(),
            "physical_optimization": self.physical_optimization(),
            "health_score": self.health_score(),
            "metadata": self.metadata,
        }

    def distance_from_anchor(self):
        """Distance from Anchor Point (1,1,1,1)"""
        return math.sqrt(
            (self.L - 1.0) ** 2 + (self.J - 1.0) ** 2 + (self.P - 1.0) ** 2 + (self.W - 1.0) ** 2
        )

    def distance_from_ne(self):
        """Distance from Natural Equilibrium (0.618, 0.414, 0.718, 0.693)"""
        NE = (0.618, 0.414, 0.718, 0.693)
        return math.sqrt(
            (self.L - NE[0]) ** 2
            + (self.J - NE[1]) ** 2
            + (self.P - NE[2]) ** 2
            + (self.W - NE[3]) ** 2
        )

    def divine_perfection(self):
        """Divine perfection percentage (closer to Anchor = higher)"""
        return max(0, 100 * (2 - self.distance_from_anchor()) / 2)

    def physical_optimization(self):
        """Physical optimization percentage (closer to NE = higher)"""
        return max(0, 100 * (2 - self.distance_from_ne()) / 2)

    def health_score(self):
        """Overall code health (balance between divine and physical)"""
        return (self.divine_perfection() + self.physical_optimization()) / 2

    def euclidean_distance(self, other: "LJPWCoordinates") -> float:
        """Compute 4D Euclidean distance to another LJPW coordinate"""
        return math.sqrt(
            (self.L - other.L) ** 2
            + (self.J - other.J) ** 2
            + (self.P - other.P) ** 2
            + (self.W - other.W) ** 2
        )


class PythonAnalyzer:
    """Analyze Python code to extract LJPW coordinates"""

    @staticmethod
    def analyze(code: str, filepath: str = "unknown") -> LJPWCoordinates:
        """Analyze Python code and compute LJPW coordinates"""

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")

        # Initialize dimensions
        L_score = 0.0  # Love (Safety)
        J_score = 0.0  # Justice (Structure)
        P_score = 0.0  # Power (Performance)
        W_score = 0.0  # Wisdom (Design)

        metadata = {
            "lines": len(code.split("\n")),
            "functions": 0,
            "classes": 0,
            "error_handling": 0,
            "complexity": 0,
        }

        # === L (Love/Safety) Analysis ===
        # Error handling, input validation, defensive programming

        error_handlers = 0
        assertions = 0

        for node in ast.walk(tree):
            # Try-except blocks
            if isinstance(node, ast.Try):
                error_handlers += 1
            # Assertions
            if isinstance(node, ast.Assert):
                assertions += 1

        metadata["error_handling"] = error_handlers

        # Base L score
        L_base = 0.3  # Baseline
        L_errors = min(0.4, error_handlers * 0.1)  # Up to +0.4 for error handling
        L_assertions = min(0.2, assertions * 0.05)  # Up to +0.2 for assertions
        L_docstrings = 0.1 if PythonAnalyzer._has_docstrings(tree) else 0.0

        L_score = L_base + L_errors + L_assertions + L_docstrings

        # === J (Justice/Structure) Analysis ===
        # Code organization, modularity, clear structure

        classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
        functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
        imports = sum(
            1 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
        )

        metadata["classes"] = classes
        metadata["functions"] = functions

        J_base = 0.2
        J_classes = min(0.3, classes * 0.1)
        J_functions = min(0.3, functions * 0.05)
        J_imports = min(0.2, imports * 0.02)

        J_score = J_base + J_classes + J_functions + J_imports

        # === P (Power/Performance) Analysis ===
        # Efficiency, optimization, algorithmic cleverness

        loops = 0
        comprehensions = 0
        builtin_usage = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                loops += 1
            if isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
                comprehensions += 1
            # Check for optimized builtins: map, filter, reduce, sum
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ("map", "filter", "sum", "max", "min", "sorted"):
                        builtin_usage += 1

        P_base = 0.4
        P_loops = min(0.2, loops * 0.05)
        P_comprehensions = min(0.2, comprehensions * 0.1)
        P_builtins = min(0.2, builtin_usage * 0.05)

        P_score = P_base + P_loops + P_comprehensions + P_builtins

        # === W (Wisdom/Design) Analysis ===
        # Simplicity, elegance, good naming, readability

        avg_func_length = PythonAnalyzer._avg_function_length(tree)
        good_naming = PythonAnalyzer._has_good_naming(code)
        comments = code.count("#")

        W_base = 0.3
        W_simplicity = 0.3 if avg_func_length < 20 else 0.1  # Short functions
        W_naming = 0.2 if good_naming else 0.0
        W_comments = min(0.2, comments * 0.02)

        W_score = W_base + W_simplicity + W_naming + W_comments

        # Normalize to [0, 1] range
        L_score = min(1.0, max(0.0, L_score))
        J_score = min(1.0, max(0.0, J_score))
        P_score = min(1.0, max(0.0, P_score))
        W_score = min(1.0, max(0.0, W_score))

        return LJPWCoordinates(
            L=L_score,
            J=J_score,
            P=P_score,
            W=W_score,
            language="python",
            file_path=filepath,
            metadata=metadata,
        )

    @staticmethod
    def _has_docstrings(tree):
        """Check if code has docstrings"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node):
                    return True
        return False

    @staticmethod
    def _avg_function_length(tree):
        """Average function length in lines"""
        func_lengths = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
                    length = node.end_lineno - node.lineno
                    func_lengths.append(length)

        if not func_lengths:
            return 0

        return sum(func_lengths) / len(func_lengths)

    @staticmethod
    def _has_good_naming(code):
        """Heuristic for good variable naming (not single-letter)"""
        # Extract variable names
        try:
            tree = ast.parse(code)
        except:
            return False

        var_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                var_names.append(node.id)

        if not var_names:
            return True

        # Good naming: avg length > 3, not mostly single letters
        avg_length = sum(len(name) for name in var_names) / len(var_names)
        single_letter = sum(1 for name in var_names if len(name) == 1)

        return avg_length > 3 and single_letter / len(var_names) < 0.3


class JavaScriptAnalyzer:
    """Analyze JavaScript code to extract LJPW coordinates"""

    @staticmethod
    def analyze(code: str, filepath: str = "unknown") -> LJPWCoordinates:
        """Analyze JavaScript code (regex-based, approximate)"""

        lines = code.split("\n")
        metadata = {
            "lines": len(lines),
            "functions": 0,
            "classes": 0,
            "error_handling": 0,
        }

        # === L (Love/Safety) ===
        try_count = code.count("try")
        catch_count = code.count("catch")
        error_handling = min(try_count, catch_count)  # Match pairs

        L_base = 0.3
        L_errors = min(0.4, error_handling * 0.15)
        L_validation = 0.1 if "typeof" in code or "instanceof" in code else 0.0
        L_strict = 0.1 if "'use strict'" in code or '"use strict"' in code else 0.0

        L_score = L_base + L_errors + L_validation + L_strict

        # === J (Justice/Structure) ===
        class_count = code.count("class ")
        function_count = len(re.findall(r"\bfunction\s+\w+", code))
        arrow_functions = code.count("=>")
        import_count = code.count("import") + code.count("require")

        metadata["functions"] = function_count + arrow_functions
        metadata["classes"] = class_count
        metadata["error_handling"] = error_handling

        J_base = 0.2
        J_classes = min(0.3, class_count * 0.15)
        J_functions = min(0.3, (function_count + arrow_functions) * 0.03)
        J_imports = min(0.2, import_count * 0.03)

        J_score = J_base + J_classes + J_functions + J_imports

        # === P (Power/Performance) ===
        loops = code.count("for") + code.count("while")
        array_methods = (
            code.count(".map(")
            + code.count(".filter(")
            + code.count(".reduce(")
            + code.count(".forEach(")
        )
        async_usage = code.count("async") + code.count("await")

        P_base = 0.4
        P_loops = min(0.2, loops * 0.05)
        P_array = min(0.2, array_methods * 0.08)
        P_async = min(0.2, async_usage * 0.05)

        P_score = P_base + P_loops + P_array + P_async

        # === W (Wisdom/Design) ===
        comments = code.count("//") + code.count("/*")
        const_usage = code.count("const")
        let_usage = code.count("let")
        var_usage = code.count("var")

        # Prefer const > let > var (modern best practice)
        modern_vars = const_usage + let_usage
        legacy_vars = var_usage

        W_base = 0.3
        W_comments = min(0.2, comments * 0.02)
        W_modern = 0.3 if modern_vars > legacy_vars else 0.1
        W_concise = 0.2 if len(lines) < 100 else 0.1

        W_score = W_base + W_comments + W_modern + W_concise

        # Normalize
        L_score = min(1.0, max(0.0, L_score))
        J_score = min(1.0, max(0.0, J_score))
        P_score = min(1.0, max(0.0, P_score))
        W_score = min(1.0, max(0.0, W_score))

        return LJPWCoordinates(
            L=L_score,
            J=J_score,
            P=P_score,
            W=W_score,
            language="javascript",
            file_path=filepath,
            metadata=metadata,
        )


class GoAnalyzer:
    """Analyze Go code to extract LJPW coordinates"""

    @staticmethod
    def analyze(code: str, filepath: str = "unknown") -> LJPWCoordinates:
        """Analyze Go code (regex-based, approximate)"""

        lines = code.split("\n")
        metadata = {
            "lines": len(lines),
            "functions": 0,
            "structs": 0,
            "error_handling": 0,
        }

        # === L (Love/Safety) ===
        # Go: explicit error handling via "if err != nil"
        error_checks = len(re.findall(r"if\s+err\s*!=\s*nil", code))
        panics = code.count("panic(")
        recovers = code.count("recover(")

        metadata["error_handling"] = error_checks

        L_base = 0.4  # Go is inherently safe (type-safe, memory-safe)
        L_errors = min(0.4, error_checks * 0.08)
        L_panic = -0.1 if panics > 0 else 0.0  # Panics reduce safety
        L_recover = 0.1 if recovers > 0 else 0.0

        L_score = L_base + L_errors + L_panic + L_recover

        # === J (Justice/Structure) ===
        structs = len(re.findall(r"\btype\s+\w+\s+struct", code))
        interfaces = len(re.findall(r"\btype\s+\w+\s+interface", code))
        functions = len(re.findall(r"\bfunc\s+(\w+|\(\w+\s+\*?\w+\))", code))
        packages = code.count("package ")

        metadata["structs"] = structs
        metadata["functions"] = functions

        J_base = 0.3  # Go has strong structural conventions
        J_structs = min(0.3, structs * 0.1)
        J_interfaces = min(0.2, interfaces * 0.1)
        J_functions = min(0.2, functions * 0.03)

        J_score = J_base + J_structs + J_interfaces + J_functions

        # === P (Power/Performance) ===
        goroutines = code.count("go ")
        channels = code.count("chan ")
        loops = code.count("for ")
        defers = code.count("defer ")

        P_base = 0.5  # Go is performant by design
        P_concurrent = min(0.3, (goroutines + channels) * 0.1)
        P_loops = min(0.1, loops * 0.02)
        P_defer = min(0.1, defers * 0.05)

        P_score = P_base + P_concurrent + P_loops + P_defer

        # === W (Wisdom/Design) ===
        comments = code.count("//")
        avg_line_length = sum(len(line) for line in lines) / max(len(lines), 1)
        gofmt_compliant = avg_line_length < 100  # Rough heuristic

        W_base = 0.4  # Go encourages simple, readable code
        W_comments = min(0.2, comments * 0.02)
        W_simple = 0.2 if gofmt_compliant else 0.1
        W_concise = 0.2 if len(lines) < 150 else 0.1

        W_score = W_base + W_comments + W_simple + W_concise

        # Normalize
        L_score = min(1.0, max(0.0, L_score))
        J_score = min(1.0, max(0.0, J_score))
        P_score = min(1.0, max(0.0, P_score))
        W_score = min(1.0, max(0.0, W_score))

        return LJPWCoordinates(
            L=L_score,
            J=J_score,
            P=P_score,
            W=W_score,
            language="go",
            file_path=filepath,
            metadata=metadata,
        )


# === Main API ===


def analyze_code(filepath: str, language: str = None) -> LJPWCoordinates:
    """
    Analyze code file and return LJPW coordinates

    Args:
        filepath: Path to code file
        language: Language override (auto-detect if None)

    Returns:
        LJPWCoordinates object
    """

    # Auto-detect language from extension
    if language is None:
        ext = Path(filepath).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
        }
        language = language_map.get(ext, "unknown")

    # Read file
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    # Dispatch to appropriate analyzer
    analyzers = {
        "python": PythonAnalyzer,
        "javascript": JavaScriptAnalyzer,
        "typescript": JavaScriptAnalyzer,  # Treat TS as JS for now
        "go": GoAnalyzer,
    }

    if language not in analyzers:
        raise ValueError(f"Unsupported language: {language}")

    analyzer = analyzers[language]
    return analyzer.analyze(code, filepath)


def compare_implementations(files: Dict[str, str]) -> Dict[str, Any]:
    """
    Compare multiple implementations of the same algorithm across languages

    Args:
        files: Dict mapping language name to filepath
               Example: {'python': 'sort.py', 'javascript': 'sort.js'}

    Returns:
        Dict with comparison results
    """

    results = {}
    coordinates = {}

    # Analyze each file
    for lang, filepath in files.items():
        try:
            ljpw = analyze_code(filepath, language=lang)
            coordinates[lang] = ljpw
            results[lang] = ljpw.to_dict()
        except Exception as e:
            results[lang] = {"error": str(e)}

    # Compute pairwise distances
    languages = list(coordinates.keys())
    distances = {}

    for i, lang1 in enumerate(languages):
        for lang2 in languages[i + 1 :]:
            coord1 = coordinates[lang1]
            coord2 = coordinates[lang2]
            distance = coord1.euclidean_distance(coord2)
            distances[f"{lang1}_vs_{lang2}"] = distance

    # Compute statistics
    if coordinates:
        avg_L = sum(c.L for c in coordinates.values()) / len(coordinates)
        avg_J = sum(c.J for c in coordinates.values()) / len(coordinates)
        avg_P = sum(c.P for c in coordinates.values()) / len(coordinates)
        avg_W = sum(c.W for c in coordinates.values()) / len(coordinates)

        var_L = sum((c.L - avg_L) ** 2 for c in coordinates.values()) / len(coordinates)
        var_J = sum((c.J - avg_J) ** 2 for c in coordinates.values()) / len(coordinates)
        var_P = sum((c.P - avg_P) ** 2 for c in coordinates.values()) / len(coordinates)
        var_W = sum((c.W - avg_W) ** 2 for c in coordinates.values()) / len(coordinates)

        statistics = {
            "mean": {"L": avg_L, "J": avg_J, "P": avg_P, "W": avg_W},
            "variance": {"L": var_L, "J": var_J, "P": var_P, "W": var_W},
            "std_dev": {
                "L": math.sqrt(var_L),
                "J": math.sqrt(var_J),
                "P": math.sqrt(var_P),
                "W": math.sqrt(var_W),
            },
            "cross_language_variance": sum([var_L, var_J, var_P, var_W]) / 4,
        }
    else:
        statistics = {}

    return {
        "implementations": results,
        "pairwise_distances": distances,
        "statistics": statistics,
        "cross_language_invariance_score": 1.0 - statistics.get("cross_language_variance", 1.0),
    }


def batch_analyze(directory: str, languages: List[str] = None) -> List[LJPWCoordinates]:
    """
    Batch analyze all code files in a directory

    Args:
        directory: Path to directory
        languages: Optional list of languages to filter

    Returns:
        List of LJPWCoordinates
    """

    results = []
    dir_path = Path(directory)

    # Extension map
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".go": "go",
    }

    for filepath in dir_path.rglob("*"):
        if filepath.is_file():
            ext = filepath.suffix.lower()
            if ext in ext_map:
                lang = ext_map[ext]
                if languages is None or lang in languages:
                    try:
                        ljpw = analyze_code(str(filepath), language=lang)
                        results.append(ljpw)
                    except Exception as e:
                        print(f"Error analyzing {filepath}: {e}")

    return results


# === CLI ===


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Multi-language LJPW analyzer")
    parser.add_argument("file", help="File to analyze")
    parser.add_argument("-l", "--language", help="Language (auto-detect if not specified)")
    parser.add_argument("-o", "--output", help="Output JSON file")
    parser.add_argument("--compare", nargs="+", help="Compare multiple files")

    args = parser.parse_args()

    if args.compare:
        # Compare mode
        files = {}
        for f in args.compare:
            lang = Path(f).suffix.lstrip(".")
            files[lang] = f

        results = compare_implementations(files)
        print(json.dumps(results, indent=2))

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
    else:
        # Single file mode
        ljpw = analyze_code(args.file, language=args.language)

        print(f"\nLJPW Analysis: {args.file}")
        print(f"Language: {ljpw.language}")
        print(f"\nCoordinates:")
        print(f"  L (Love/Safety):      {ljpw.L:.3f}")
        print(f"  J (Justice/Structure): {ljpw.J:.3f}")
        print(f"  P (Power/Performance): {ljpw.P:.3f}")
        print(f"  W (Wisdom/Design):     {ljpw.W:.3f}")
        print(f"\nMetrics:")
        print(f"  Divine Perfection:     {ljpw.divine_perfection():.1f}%")
        print(f"  Physical Optimization: {ljpw.physical_optimization():.1f}%")
        print(f"  Health Score:          {ljpw.health_score():.1f}%")

        if args.output:
            with open(args.output, "w") as f:
                json.dump(ljpw.to_dict(), f, indent=2)


if __name__ == "__main__":
    main()
