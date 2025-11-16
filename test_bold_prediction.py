#!/usr/bin/env python3
"""
Test Bold Prediction: Beautiful Code Near Natural Equilibrium

Hypothesis: Code that developers consider "beautiful" or "elegant"
should be close to Natural Equilibrium (φ⁻¹, √2-1, e-2, ln(2)).

This tests if LJPW captures aesthetic/quality judgments, not just
arbitrary measurements.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ljpw_standalone import analyze_quick, calculate_distance

# Natural Equilibrium coordinates
NE = (0.618, 0.414, 0.718, 0.693)

# ============================================================================
# BEAUTIFUL CODE EXAMPLES
# ============================================================================

# Example 1: Classic Python - "There should be one obvious way to do it"
beautiful_python = """
def quicksort(arr):
    '''Elegant recursive quicksort implementation.'''
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""

# Example 2: Clean, minimal, purposeful
beautiful_minimal = """
def compose(*functions):
    '''Compose multiple functions into one.'''
    def inner(arg):
        for f in reversed(functions):
            arg = f(arg)
        return arg
    return inner
"""

# Example 3: Well-balanced with safety and elegance
beautiful_balanced = """
def memoize(func):
    '''Simple memoization decorator with clean design.'''
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache_clear = lambda: cache.clear()
    return wrapper
"""

# Example 4: Pythonic and clear
beautiful_pythonic = """
def flatten(nested_list):
    '''Flatten arbitrarily nested list using recursion.'''
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
"""

# ============================================================================
# UGLY/MESSY CODE EXAMPLES (for comparison)
# ============================================================================

ugly_code_1 = """
def x(a):
    b=[]
    for i in range(len(a)):
        if a[i]<a[len(a)//2]:b.append(a[i])
    c=[]
    for i in range(len(a)):
        if a[i]==a[len(a)//2]:c.append(a[i])
    d=[]
    for i in range(len(a)):
        if a[i]>a[len(a)//2]:d.append(a[i])
    return x(b)+c+x(d) if len(a)>1 else a
"""

ugly_code_2 = """
def f(x):
    y=x
    z=0
    while y>0:
        z=z+1
        y=y-1
    return z
"""

# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_beauty_hypothesis():
    print("\n" + "=" * 70)
    print("BOLD PREDICTION TEST: Beautiful Code Near Natural Equilibrium")
    print("=" * 70)

    print("\nHypothesis: Beautiful code should have distance <0.4 from NE")
    print(f"Natural Equilibrium: L={NE[0]:.3f}, J={NE[1]:.3f}, P={NE[2]:.3f}, W={NE[3]:.3f}")

    # Test beautiful code
    print("\n" + "-" * 70)
    print("BEAUTIFUL CODE EXAMPLES")
    print("-" * 70)

    beautiful_examples = [
        ("Quicksort (elegant recursion)", beautiful_python),
        ("Function composition", beautiful_minimal),
        ("Memoization decorator", beautiful_balanced),
        ("Flatten with generators", beautiful_pythonic)
    ]

    beautiful_distances = []

    for name, code in beautiful_examples:
        result = analyze_quick(code)
        coords = (result['ljpw']['L'], result['ljpw']['J'],
                 result['ljpw']['P'], result['ljpw']['W'])

        dist = calculate_distance(coords, NE)
        beautiful_distances.append(dist)

        L_digit = int(round(coords[0] * 10)) % 10
        J_digit = int(round(coords[1] * 10)) % 10
        P_digit = int(round(coords[2] * 10)) % 10
        W_digit = int(round(coords[3] * 10)) % 10
        genome = f"L{L_digit}J{J_digit}P{P_digit}W{W_digit}"

        print(f"\n{name}:")
        print(f"  Genome: {genome}")
        print(f"  Position: L={coords[0]:.2f}, J={coords[1]:.2f}, P={coords[2]:.2f}, W={coords[3]:.2f}")
        print(f"  Distance from NE: {dist:.3f}", end="")

        if dist < 0.4:
            print("  ✓ CLOSE (prediction confirmed)")
        elif dist < 0.6:
            print("  ≈ MODERATE")
        else:
            print("  ✗ FAR (prediction challenged)")

    # Test ugly code
    print("\n" + "-" * 70)
    print("UGLY CODE EXAMPLES (for comparison)")
    print("-" * 70)

    ugly_examples = [
        ("Ugly quicksort (no spacing)", ugly_code_1),
        ("Ugly counter (inefficient)", ugly_code_2)
    ]

    ugly_distances = []

    for name, code in ugly_examples:
        result = analyze_quick(code)
        coords = (result['ljpw']['L'], result['ljpw']['J'],
                 result['ljpw']['P'], result['ljpw']['W'])

        dist = calculate_distance(coords, NE)
        ugly_distances.append(dist)

        L_digit = int(round(coords[0] * 10)) % 10
        J_digit = int(round(coords[1] * 10)) % 10
        P_digit = int(round(coords[2] * 10)) % 10
        W_digit = int(round(coords[3] * 10)) % 10
        genome = f"L{L_digit}J{J_digit}P{P_digit}W{W_digit}"

        print(f"\n{name}:")
        print(f"  Genome: {genome}")
        print(f"  Position: L={coords[0]:.2f}, J={coords[1]:.2f}, P={coords[2]:.2f}, W={coords[3]:.2f}")
        print(f"  Distance from NE: {dist:.3f}", end="")

        if dist < 0.4:
            print("  ✓ CLOSE")
        elif dist < 0.6:
            print("  ≈ MODERATE")
        else:
            print("  ✗ FAR (as expected)")

    # Analysis
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)

    avg_beautiful = sum(beautiful_distances) / len(beautiful_distances)
    avg_ugly = sum(ugly_distances) / len(ugly_distances)

    print(f"\nAverage distance from NE:")
    print(f"  Beautiful code: {avg_beautiful:.3f}")
    print(f"  Ugly code:      {avg_ugly:.3f}")
    print(f"  Difference:     {avg_ugly - avg_beautiful:.3f}")

    if avg_beautiful < avg_ugly:
        print(f"\n✓ PREDICTION CONFIRMED!")
        print(f"  Beautiful code IS closer to Natural Equilibrium")
    else:
        print(f"\n✗ PREDICTION CHALLENGED")
        print(f"  Beautiful code is NOT closer to Natural Equilibrium")

    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)

    print("""
If beautiful code clusters near Natural Equilibrium, this suggests:

1. LJPW captures aesthetic/quality judgments (not just syntax)
2. Natural Equilibrium represents an objective "good code" attractor
3. Beauty in code is NOT subjective—it's geometric proximity to NE
4. The constants (φ⁻¹, √2-1, e-2, ln(2)) define optimal balance

This would be strong evidence that LJPW captures something
fundamental about code quality, not just arbitrary measurements.
    """)
    print("=" * 70 + "\n")

if __name__ == '__main__':
    test_beauty_hypothesis()
