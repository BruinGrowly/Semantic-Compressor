#!/usr/bin/env python3
"""
Example 1: Analyze a Single File

This example shows the most basic usage of LJPW:
- Analyze a single code file
- Get LJPW scores
- Interpret the results

Run:
    python 01_analyze_single_file.py
"""

import sys
from pathlib import Path

# Add parent directory to path for src module imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ljpw.ljpw_standalone import SimpleCodeAnalyzer, format_result


def main():
    print("=" * 70)
    print("LJPW Example 1: Analyze a Single File")
    print("=" * 70)
    print()

    # Sample code to analyze
    sample_code = '''
def process_data(data):
    """Process some data"""
    result = []
    for item in data:
        result.append(item * 2)
    return result
'''

    print("Sample code:")
    print("-" * 70)
    print(sample_code)
    print("-" * 70)
    print()

    # Create analyzer
    analyzer = SimpleCodeAnalyzer()

    # Analyze the code
    result = analyzer.analyze(sample_code, filename="sample.py")

    # Print formatted results
    print(format_result(result))
    print()

    # Interpret the scores
    print("INTERPRETATION:")
    print("-" * 70)

    ljpw = result["ljpw"]
    health = result["health"] * 100

    print(f"Love (Safety): {ljpw['L']:.2f}")
    if ljpw["L"] < 0.5:
        print("  → LOW: This code has minimal error handling")
        print("  → FIX: Add try/except, input validation, null checks")

    print(f"\nJustice (Structure): {ljpw['J']:.2f}")
    if ljpw["J"] < 0.4:
        print("  → LOW: This code lacks structure")
        print("  → FIX: Add type hints, docstrings, clear interfaces")

    print(f"\nPower (Performance): {ljpw['P']:.2f}")
    if ljpw["P"] < 0.7:
        print("  → MEDIUM: Performance is okay but not optimized")
        print("  → CONSIDER: Better algorithms, caching, async operations")

    print(f"\nWisdom (Design): {ljpw['W']:.2f}")
    if ljpw["W"] < 0.6:
        print("  → LOW: Design could be improved")
        print("  → FIX: Add abstractions, use design patterns, modularize")

    print(f"\nOverall Health: {health:.1f}%")
    if health >= 80:
        print("  → EXCELLENT! Code is well-balanced")
    elif health >= 60:
        print("  → GOOD: Code is functional with room for improvement")
    elif health >= 40:
        print("  → FAIR: Code needs improvement")
    else:
        print("  → NEEDS WORK: Significant issues to address")

    print()
    print("=" * 70)
    print("Next: Try running 02_analyze_directory.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
