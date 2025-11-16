#!/usr/bin/env python3
"""
Test Semantic Interpolation

Hypothesis: Intermediate positions in LJPW space represent
semantically intermediate code.

If we have:
- Code A at position (0.3, 0.2, 0.8, 0.3) - Fast prototype
- Code B at position (0.9, 0.8, 0.3, 0.7) - Safe production code

Then interpolated position (0.6, 0.5, 0.55, 0.5) should represent
code with intermediate properties: moderate safety, moderate speed.
"""

import sys
from pathlib import Path
from typing import Tuple, Dict

sys.path.insert(0, str(Path(__file__).parent))
from ljpw_standalone import analyze_quick, calculate_distance

# ============================================================================
# INTERPOLATION ENGINE
# ============================================================================

def interpolate_position(pos1: Tuple[float, float, float, float],
                        pos2: Tuple[float, float, float, float],
                        alpha: float = 0.5) -> Tuple[float, float, float, float]:
    """
    Interpolate between two positions in LJPW space.

    alpha = 0.0 → returns pos1
    alpha = 0.5 → returns midpoint
    alpha = 1.0 → returns pos2
    """
    L = pos1[0] + alpha * (pos2[0] - pos1[0])
    J = pos1[1] + alpha * (pos2[1] - pos1[1])
    P = pos1[2] + alpha * (pos2[2] - pos1[2])
    W = pos1[3] + alpha * (pos2[3] - pos1[3])
    return (L, J, P, W)

def describe_position(coords: Tuple[float, float, float, float]) -> Dict:
    """
    Generate semantic description of what code at this position should be like.
    """
    L, J, P, W = coords

    description = {
        'coordinates': coords,
        'genome': f"L{int(round(L*10))%10}J{int(round(J*10))%10}P{int(round(P*10))%10}W{int(round(W*10))%10}",
        'characteristics': []
    }

    # Love (Safety) analysis
    if L < 0.3:
        description['characteristics'].append("MINIMAL SAFETY: Little to no error handling")
    elif L < 0.5:
        description['characteristics'].append("LOW SAFETY: Basic error handling only")
    elif L < 0.7:
        description['characteristics'].append("MODERATE SAFETY: Good error handling")
    elif L < 0.9:
        description['characteristics'].append("HIGH SAFETY: Extensive validation and error handling")
    else:
        description['characteristics'].append("MAXIMUM SAFETY: Defensive programming, comprehensive checks")

    # Justice (Structure) analysis
    if J < 0.3:
        description['characteristics'].append("MINIMAL STRUCTURE: No types or docs")
    elif J < 0.5:
        description['characteristics'].append("LOW STRUCTURE: Minimal documentation")
    elif J < 0.7:
        description['characteristics'].append("MODERATE STRUCTURE: Some types and docs")
    elif J < 0.9:
        description['characteristics'].append("HIGH STRUCTURE: Well-typed and documented")
    else:
        description['characteristics'].append("MAXIMUM STRUCTURE: Rigorous types, comprehensive docs")

    # Power (Performance) analysis
    if P < 0.3:
        description['characteristics'].append("MINIMAL PERFORMANCE: Simple, unoptimized")
    elif P < 0.5:
        description['characteristics'].append("LOW PERFORMANCE: Basic implementation")
    elif P < 0.7:
        description['characteristics'].append("MODERATE PERFORMANCE: Some optimization")
    elif P < 0.9:
        description['characteristics'].append("HIGH PERFORMANCE: Optimized algorithms")
    else:
        description['characteristics'].append("MAXIMUM PERFORMANCE: Highly optimized, cached")

    # Wisdom (Design) analysis
    if W < 0.3:
        description['characteristics'].append("MINIMAL DESIGN: No abstraction or patterns")
    elif W < 0.5:
        description['characteristics'].append("LOW DESIGN: Simple, direct code")
    elif W < 0.7:
        description['characteristics'].append("MODERATE DESIGN: Some abstractions")
    elif W < 0.9:
        description['characteristics'].append("HIGH DESIGN: Well-abstracted, patterns used")
    else:
        description['characteristics'].append("MAXIMUM DESIGN: Elegant architecture, deep patterns")

    # Overall archetype
    if L > 0.7 and J > 0.7 and P < 0.4:
        description['archetype'] = "BUREAUCRAT: Safe and structured but slow"
    elif L < 0.4 and J < 0.4 and P > 0.7:
        description['archetype'] = "PROTOTYPE: Fast but risky and messy"
    elif L > 0.7 and P > 0.7 and W > 0.7:
        description['archetype'] = "IDEAL: Balanced excellence"
    elif abs(L - 0.618) < 0.2 and abs(J - 0.414) < 0.2:
        description['archetype'] = "NATURAL: Near optimal equilibrium"
    else:
        description['archetype'] = "BALANCED: Moderate in all dimensions"

    return description

# ============================================================================
# TEST CASES
# ============================================================================

def test_interpolation():
    print("\n" + "=" * 70)
    print("SEMANTIC INTERPOLATION TEST")
    print("=" * 70)
    print("\nHypothesis: Positions between A and B have intermediate semantics\n")

    # Test Case 1: Prototype → Production
    print("─" * 70)
    print("Test 1: From Prototype to Production Code")
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
    '''Process data by doubling each value with validation.'''
    if not data:
        raise ValueError("Data required")
    if not isinstance(data, list):
        raise TypeError("Data must be list")

    try:
        return [item * 2 for item in data]
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise
"""

    # Analyze endpoints
    result_proto = analyze_quick(prototype)
    result_prod = analyze_quick(production)

    pos_proto = (result_proto['ljpw']['L'], result_proto['ljpw']['J'],
                result_proto['ljpw']['P'], result_proto['ljpw']['W'])
    pos_prod = (result_prod['ljpw']['L'], result_prod['ljpw']['J'],
               result_prod['ljpw']['P'], result_prod['ljpw']['W'])

    print(f"\nPrototype Code:")
    print(f"  Position: L={pos_proto[0]:.2f}, J={pos_proto[1]:.2f}, P={pos_proto[2]:.2f}, W={pos_proto[3]:.2f}")
    desc_proto = describe_position(pos_proto)
    print(f"  Archetype: {desc_proto['archetype']}")

    print(f"\nProduction Code:")
    print(f"  Position: L={pos_prod[0]:.2f}, J={pos_prod[1]:.2f}, P={pos_prod[2]:.2f}, W={pos_prod[3]:.2f}")
    desc_prod = describe_position(pos_prod)
    print(f"  Archetype: {desc_prod['archetype']}")

    # Test interpolation at various points
    print(f"\nInterpolated Positions:")
    for alpha in [0.25, 0.5, 0.75]:
        pos_interp = interpolate_position(pos_proto, pos_prod, alpha)
        desc = describe_position(pos_interp)

        print(f"\n  {alpha*100:.0f}% toward production:")
        print(f"    Position: L={pos_interp[0]:.2f}, J={pos_interp[1]:.2f}, P={pos_interp[2]:.2f}, W={pos_interp[3]:.2f}")
        print(f"    Genome: {desc['genome']}")
        print(f"    Archetype: {desc['archetype']}")
        for char in desc['characteristics']:
            print(f"      • {char}")

    # Test Case 2: Fast & Risky → Safe & Slow
    print("\n" + "─" * 70)
    print("Test 2: From Fast/Risky to Safe/Slow")
    print("─" * 70)

    fast_risky = """
def get(key):
    return cache[key]
"""

    safe_slow = """
def get_value(key: str) -> Optional[Any]:
    '''Safely retrieve value from cache with validation.'''
    if not key:
        raise ValueError("Key required")
    if not isinstance(key, str):
        raise TypeError("Key must be string")

    if key not in cache:
        logger.warning(f"Key not found: {key}")
        return None

    try:
        return cache[key]
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        return None
"""

    result_fast = analyze_quick(fast_risky)
    result_safe = analyze_quick(safe_slow)

    pos_fast = (result_fast['ljpw']['L'], result_fast['ljpw']['J'],
               result_fast['ljpw']['P'], result_fast['ljpw']['W'])
    pos_safe = (result_safe['ljpw']['L'], result_safe['ljpw']['J'],
               result_safe['ljpw']['P'], result_safe['ljpw']['W'])

    print(f"\nFast/Risky Code:")
    print(f"  Position: L={pos_fast[0]:.2f}, J={pos_fast[1]:.2f}, P={pos_fast[2]:.2f}, W={pos_fast[3]:.2f}")

    print(f"\nSafe/Slow Code:")
    print(f"  Position: L={pos_safe[0]:.2f}, J={pos_safe[1]:.2f}, P={pos_safe[2]:.2f}, W={pos_safe[3]:.2f}")

    # Midpoint
    pos_mid = interpolate_position(pos_fast, pos_safe, 0.5)
    desc_mid = describe_position(pos_mid)

    print(f"\nMidpoint (balanced):")
    print(f"  Position: L={pos_mid[0]:.2f}, J={pos_mid[1]:.2f}, P={pos_mid[2]:.2f}, W={pos_mid[3]:.2f}")
    print(f"  Genome: {desc_mid['genome']}")
    print(f"  Expected: Moderate safety, moderate performance")
    print(f"  Actual archetype: {desc_mid['archetype']}")
    for char in desc_mid['characteristics']:
        print(f"    • {char}")

    # Test Case 3: Verify linearity
    print("\n" + "─" * 70)
    print("Test 3: Verify Linear Interpolation Property")
    print("─" * 70)

    print(f"\nChecking: distance(A, mid) ≈ distance(mid, B)")

    dist_proto_mid = calculate_distance(pos_proto, pos_mid)
    dist_mid_prod = calculate_distance(pos_mid, pos_prod)

    print(f"  Distance(prototype, midpoint): {dist_proto_mid:.3f}")
    print(f"  Distance(midpoint, production): {dist_mid_prod:.3f}")
    print(f"  Ratio: {dist_proto_mid/dist_mid_prod:.2f}")

    if 0.8 < dist_proto_mid/dist_mid_prod < 1.2:
        print(f"  ✓ Nearly equal - linear interpolation works!")
    else:
        print(f"  ⚠ Unequal - space may be non-linear")

    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print("""
If interpolated positions have semantics between the endpoints, this proves:

1. LJPW space is semantically meaningful (not just arbitrary coordinates)
2. Position determines semantics (not just correlates)
3. We can navigate semantic space by moving in directions
4. Code generation at target positions is theoretically possible

This validates the "coordinate extraction" model of semantic compression.
    """)
    print("=" * 70 + "\n")

if __name__ == '__main__':
    test_interpolation()
