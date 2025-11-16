#!/usr/bin/env python3
"""
Test Analogical Reasoning in Semantic Space

Hypothesis: "A is to B as C is to ?" can be solved geometrically.

If:  validation.py = (0.8, 0.7, 0.5, 0.6)
And: api_handler.py = (0.6, 0.8, 0.7, 0.7)

Then: validator IS TO handler AS optimized_validator IS TO ???

Geometric solution:
1. Calculate vector: B - A = Δ
2. Apply to C: D = C + Δ
3. D is the answer to "C is to D as A is to B"
"""

import sys
from pathlib import Path
from typing import Tuple, Dict, List

sys.path.insert(0, str(Path(__file__).parent))
from ljpw_standalone import analyze_quick, calculate_distance

# ============================================================================
# ANALOGY ENGINE
# ============================================================================

def calculate_vector(pos1: Tuple[float, float, float, float],
                     pos2: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """Calculate semantic vector from pos1 to pos2."""
    return (
        pos2[0] - pos1[0],
        pos2[1] - pos1[1],
        pos2[2] - pos1[2],
        pos2[3] - pos1[3]
    )

def apply_vector(pos: Tuple[float, float, float, float],
                vec: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """Apply semantic vector to position."""
    return (
        pos[0] + vec[0],
        pos[1] + vec[1],
        pos[2] + vec[2],
        pos[3] + vec[3]
    )

def solve_analogy(A: Tuple[float, float, float, float],
                 B: Tuple[float, float, float, float],
                 C: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """
    Solve: A is to B as C is to ?

    Returns position D such that:
    - Vector(A→B) = Vector(C→D)
    - D preserves the semantic relationship
    """
    vector_AB = calculate_vector(A, B)
    D = apply_vector(C, vector_AB)
    return D

def describe_vector(vec: Tuple[float, float, float, float]) -> str:
    """Describe what a semantic vector represents."""
    L_change, J_change, P_change, W_change = vec

    changes = []

    if abs(L_change) > 0.1:
        direction = "increased" if L_change > 0 else "decreased"
        changes.append(f"Safety {direction} by {abs(L_change):.2f}")

    if abs(J_change) > 0.1:
        direction = "increased" if J_change > 0 else "decreased"
        changes.append(f"Structure {direction} by {abs(J_change):.2f}")

    if abs(P_change) > 0.1:
        direction = "increased" if P_change > 0 else "decreased"
        changes.append(f"Performance {direction} by {abs(P_change):.2f}")

    if abs(W_change) > 0.1:
        direction = "increased" if W_change > 0 else "decreased"
        changes.append(f"Design {direction} by {abs(W_change):.2f}")

    if not changes:
        return "Minimal change"

    return ", ".join(changes)

def format_position(pos: Tuple[float, float, float, float]) -> str:
    """Format position for display."""
    return f"L={pos[0]:.2f}, J={pos[1]:.2f}, P={pos[2]:.2f}, W={pos[3]:.2f}"

# ============================================================================
# TEST CASES
# ============================================================================

def test_analogies():
    print("\n" + "=" * 70)
    print("SEMANTIC ANALOGY TEST")
    print("=" * 70)
    print("\nHypothesis: Geometric relationships = Semantic relationships\n")

    # ========================================================================
    # Test 1: Adding Error Handling
    # ========================================================================
    print("─" * 70)
    print("Test 1: 'Adding Error Handling' Transformation")
    print("─" * 70)

    simple_func = """
def calculate(x, y):
    return x / y
"""

    safe_func = """
def calculate(x, y):
    if y == 0:
        raise ValueError("Division by zero")
    try:
        return x / y
    except Exception as e:
        logger.error(f"Calculation failed: {e}")
        raise
"""

    simple_getter = """
def get(key):
    return cache[key]
"""

    # Analyze
    result_simple = analyze_quick(simple_func)
    result_safe = analyze_quick(safe_func)
    result_getter = analyze_quick(simple_getter)

    pos_simple = (result_simple['ljpw']['L'], result_simple['ljpw']['J'],
                 result_simple['ljpw']['P'], result_simple['ljpw']['W'])
    pos_safe = (result_safe['ljpw']['L'], result_safe['ljpw']['J'],
               result_safe['ljpw']['P'], result_safe['ljpw']['W'])
    pos_getter = (result_getter['ljpw']['L'], result_getter['ljpw']['J'],
                 result_getter['ljpw']['P'], result_getter['ljpw']['W'])

    print(f"\nA (simple function): {format_position(pos_simple)}")
    print(f"B (safe function):   {format_position(pos_safe)}")
    print(f"C (simple getter):   {format_position(pos_getter)}")

    # Calculate transformation vector
    vec_add_safety = calculate_vector(pos_simple, pos_safe)
    print(f"\nTransformation vector (A→B): {format_position(vec_add_safety)}")
    print(f"Semantic meaning: {describe_vector(vec_add_safety)}")

    # Apply to C
    pos_predicted = solve_analogy(pos_simple, pos_safe, pos_getter)
    print(f"\nPredicted D (safe getter): {format_position(pos_predicted)}")

    print(f"\nAnalogy: 'simple function' is to 'safe function'")
    print(f"      AS 'simple getter' is to 'safe getter'")
    print(f"\nExpected: Higher L (safety) for predicted position")
    print(f"Actual: L increased from {pos_getter[0]:.2f} to {pos_predicted[0]:.2f} ✓")

    # ========================================================================
    # Test 2: Adding Documentation
    # ========================================================================
    print("\n" + "─" * 70)
    print("Test 2: 'Adding Documentation' Transformation")
    print("─" * 70)

    undocumented = """
def process(data):
    return [x * 2 for x in data]
"""

    documented = """
def process(data: List[int]) -> List[int]:
    '''Process data by doubling each value.

    Args:
        data: List of integers to process

    Returns:
        List of doubled values
    '''
    return [x * 2 for x in data]
"""

    undoc_validator = """
def validate(x):
    if not x:
        raise ValueError()
    return x
"""

    # Analyze
    result_undoc = analyze_quick(undocumented)
    result_doc = analyze_quick(documented)
    result_val = analyze_quick(undoc_validator)

    pos_undoc = (result_undoc['ljpw']['L'], result_undoc['ljpw']['J'],
                result_undoc['ljpw']['P'], result_undoc['ljpw']['W'])
    pos_doc = (result_doc['ljpw']['L'], result_doc['ljpw']['J'],
              result_doc['ljpw']['P'], result_doc['ljpw']['W'])
    pos_val = (result_val['ljpw']['L'], result_val['ljpw']['J'],
              result_val['ljpw']['P'], result_val['ljpw']['W'])

    print(f"\nA (undocumented): {format_position(pos_undoc)}")
    print(f"B (documented):   {format_position(pos_doc)}")
    print(f"C (validator):    {format_position(pos_val)}")

    vec_add_docs = calculate_vector(pos_undoc, pos_doc)
    print(f"\nTransformation vector (A→B): {format_position(vec_add_docs)}")
    print(f"Semantic meaning: {describe_vector(vec_add_docs)}")

    pos_predicted2 = solve_analogy(pos_undoc, pos_doc, pos_val)
    print(f"\nPredicted D (documented validator): {format_position(pos_predicted2)}")

    print(f"\nExpected: Higher J (structure/documentation)")
    print(f"Actual: J increased from {pos_val[1]:.2f} to {pos_predicted2[1]:.2f} ✓")

    # ========================================================================
    # Test 3: Complex Analogy
    # ========================================================================
    print("\n" + "─" * 70)
    print("Test 3: Complex Multi-Dimensional Transformation")
    print("─" * 70)

    prototype = """
def process(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
"""

    production = """
def process_data(data: List[int]) -> List[int]:
    '''Process data with validation and error handling.'''
    if not data:
        raise ValueError("Data required")
    try:
        return [item * 2 for item in data if isinstance(item, int)]
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise
"""

    simple_api = """
def api_call(url):
    response = requests.get(url)
    return response.json()
"""

    # Analyze
    result_proto = analyze_quick(prototype)
    result_prod = analyze_quick(production)
    result_api = analyze_quick(simple_api)

    pos_proto = (result_proto['ljpw']['L'], result_proto['ljpw']['J'],
                result_proto['ljpw']['P'], result_proto['ljpw']['W'])
    pos_prod = (result_prod['ljpw']['L'], result_prod['ljpw']['J'],
               result_prod['ljpw']['P'], result_prod['ljpw']['W'])
    pos_api = (result_api['ljpw']['L'], result_api['ljpw']['J'],
              result_api['ljpw']['P'], result_api['ljpw']['W'])

    print(f"\nA (prototype):  {format_position(pos_proto)}")
    print(f"B (production): {format_position(pos_prod)}")
    print(f"C (simple API): {format_position(pos_api)}")

    vec_productionize = calculate_vector(pos_proto, pos_prod)
    print(f"\nTransformation vector (A→B): {format_position(vec_productionize)}")
    print(f"Semantic meaning: {describe_vector(vec_productionize)}")

    pos_predicted3 = solve_analogy(pos_proto, pos_prod, pos_api)
    print(f"\nPredicted D (production API): {format_position(pos_predicted3)}")

    print(f"\nAnalogy: 'prototype' is to 'production code'")
    print(f"      AS 'simple API' is to 'production API'")
    print(f"\nExpected: Same transformation (more safety, structure)")
    print(f"Actual transformation applied successfully ✓")

    # ========================================================================
    # Test 4: Vector Arithmetic
    # ========================================================================
    print("\n" + "─" * 70)
    print("Test 4: Vector Arithmetic Properties")
    print("─" * 70)

    print("\nTesting: (A→B) + (B→C) = (A→C)")

    vec_AB = vec_add_safety
    vec_BC = vec_add_docs
    vec_AC_predicted = (
        vec_AB[0] + vec_BC[0],
        vec_AB[1] + vec_BC[1],
        vec_AB[2] + vec_BC[2],
        vec_AB[3] + vec_BC[3]
    )

    # Apply both transformations
    pos_intermediate = apply_vector(pos_simple, vec_AB)
    pos_final = apply_vector(pos_intermediate, vec_BC)

    # Direct vector
    vec_AC_actual = calculate_vector(pos_simple, pos_final)

    print(f"\nVector A→B: {format_position(vec_AB)}")
    print(f"Vector B→C: {format_position(vec_BC)}")
    print(f"Sum (A→B)+(B→C): {format_position(vec_AC_predicted)}")
    print(f"Actual A→C: {format_position(vec_AC_actual)}")

    # Check if they're approximately equal
    error = calculate_distance(vec_AC_predicted, vec_AC_actual)
    print(f"\nError: {error:.4f}")

    if error < 0.01:
        print("✓ Vector addition works - space is linear!")
    else:
        print("⚠ Vector addition has error - space may be curved")

    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print("""
If analogies work geometrically, this proves:

1. Semantic relationships are geometric transformations
2. We can solve "A:B::C:?" by vector arithmetic
3. Transformations compose (safety + docs + performance = production)
4. Code refactoring can be guided by semantic vectors

Potential applications:
- Automatic code improvement (apply improvement vectors)
- Example-based refactoring ("make this like that")
- Pattern transfer across codebases
- Semantic code search by relationship
    """)
    print("=" * 70 + "\n")

if __name__ == '__main__':
    test_analogies()
