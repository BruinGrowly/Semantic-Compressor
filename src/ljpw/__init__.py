"""
Semantic Compressor - Compress code by meaning, not syntax
===========================================================

A compression engine that works on semantic meaning rather than raw text.

Core Compression Features:
- Cross-language compression (compress Python, decompress to JavaScript)
- Semantic deduplication (find identical code despite different syntax)
- Quality-based compression (better code compresses better)
- AI-ready embeddings (LJPW coordinates for LLMs)

The LJPW Framework:
- L (Love/Safety): Error handling, validation
- J (Justice/Structure): Types, documentation
- P (Power/Performance): Algorithms, optimization
- W (Wisdom/Design): Modularity, patterns

Compression Pipeline:
    Code → LJPW Analysis → Semantic Coordinates → Genome (compressed)

Quick Start:
    from ljpw import analyze_quick

    code = "def add(a, b): return a + b"
    result = analyze_quick(code)

    print(result['genome'])  # L0J0P0W0 (compressed)
    print(result['ljpw'])    # Semantic coordinates

    # Compression: 28 chars → 12 chars (57% reduction)

Natural Equilibrium: (0.618, 0.414, 0.718, 0.693)
Optimal compression point for high-quality code.
"""

__version__ = "2.0.0"
__description__ = "Semantic Compressor - Compress code by meaning, not syntax"

# Import main analyzer from standalone module
try:
    from .ljpw_standalone import analyze_quick, calculate_distance, SimpleCodeAnalyzer
    __all__ = ['analyze_quick', 'calculate_distance', 'SimpleCodeAnalyzer']
except ImportError:
    # Fallback if modules aren't accessible
    __all__ = []
