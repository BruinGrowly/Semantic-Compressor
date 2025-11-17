"""
LJPW: The Coordinate System of Meaning
=======================================

A universal 4-dimensional semantic framework for analyzing code,
narratives, organizations, and complex adaptive systems.

Core Components:
- ljpw_standalone: Zero-dependency analyzer (recommended entry point)
- ljpw_semantic_compressor: Advanced compression capabilities
- ljpw_ast_analyzer: AST-based analysis
- ljpw_pipeline: End-to-end processing pipeline

Quick Start:
    from ljpw import analyze_quick

    result = analyze_quick("def add(a, b): return a + b")
    print(result['ljpw'])  # {'L': 0.0, 'J': 0.05, 'P': 0.0, 'W': 0.0}

Natural Equilibrium: (0.618, 0.414, 0.718, 0.693)
"""

__version__ = "2.0.0"

# Import main analyzer from standalone module
try:
    from .ljpw_standalone import analyze_quick, calculate_distance, SimpleCodeAnalyzer
    __all__ = ['analyze_quick', 'calculate_distance', 'SimpleCodeAnalyzer']
except ImportError:
    # Fallback if modules aren't accessible
    __all__ = []
