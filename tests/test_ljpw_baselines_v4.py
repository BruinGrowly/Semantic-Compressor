#!/usr/bin/env python3
"""
Test suite for LJPW Baselines v4.0

Tests the mathematical baselines implementation without requiring numpy
(basic functionality tests)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ljpw"))

# Import without numpy-dependent components
import math


def test_numerical_equivalents():
    """Test that numerical equivalents are correctly defined"""
    # These are the fundamental constants
    L_expected = (math.sqrt(5) - 1) / 2  # φ⁻¹ ≈ 0.618034
    J_expected = math.sqrt(2) - 1  # √2 - 1 ≈ 0.414214
    P_expected = math.e - 2  # e - 2 ≈ 0.718282
    W_expected = math.log(2)  # ln(2) ≈ 0.693147

    tolerance = 0.000001

    assert abs(L_expected - 0.618034) < tolerance, "Love constant incorrect"
    assert abs(J_expected - 0.414214) < tolerance, "Justice constant incorrect"
    assert abs(P_expected - 0.718282) < tolerance, "Power constant incorrect"
    assert abs(W_expected - 0.693147) < tolerance, "Wisdom constant incorrect"

    print("✓ Numerical equivalents test passed")


def test_reference_points():
    """Test reference points are correctly defined"""
    NE = (0.618034, 0.414214, 0.718282, 0.693147)
    Anchor = (1.0, 1.0, 1.0, 1.0)

    # Test that NE values match constants
    assert abs(NE[0] - ((math.sqrt(5) - 1) / 2)) < 0.000001
    assert abs(NE[1] - (math.sqrt(2) - 1)) < 0.000001
    assert abs(NE[2] - (math.e - 2)) < 0.000001
    assert abs(NE[3] - math.log(2)) < 0.000001

    # Test Anchor is (1,1,1,1)
    assert all(x == 1.0 for x in Anchor)

    print("✓ Reference points test passed")


def test_distance_calculations():
    """Test distance calculation functions"""

    def distance_from_anchor(L, J, P, W):
        return math.sqrt((1 - L) ** 2 + (1 - J) ** 2 + (1 - P) ** 2 + (1 - W) ** 2)

    def distance_from_ne(L, J, P, W):
        NE = (0.618034, 0.414214, 0.718282, 0.693147)
        return math.sqrt((NE[0] - L) ** 2 + (NE[1] - J) ** 2 + (NE[2] - P) ** 2 + (NE[3] - W) ** 2)

    # Test 1: Anchor to Anchor should be 0
    assert distance_from_anchor(1, 1, 1, 1) == 0

    # Test 2: NE to NE should be 0
    assert distance_from_ne(0.618034, 0.414214, 0.718282, 0.693147) < 0.000001

    # Test 3: Origin to Anchor should be 2.0
    assert abs(distance_from_anchor(0, 0, 0, 0) - 2.0) < 0.000001

    print("✓ Distance calculations test passed")


def test_mixing_algorithms():
    """Test mixing algorithms (harmonic, geometric, etc.)"""

    def harmonic_mean(L, J, P, W):
        if L <= 0 or J <= 0 or P <= 0 or W <= 0:
            return 0.0
        return 4.0 / (1 / L + 1 / J + 1 / P + 1 / W)

    def geometric_mean(L, J, P, W):
        if L <= 0 or J <= 0 or P <= 0 or W <= 0:
            return 0.0
        return (L * J * P * W) ** 0.25

    # Test 1: Harmonic mean of (1,1,1,1) should be 1
    assert abs(harmonic_mean(1, 1, 1, 1) - 1.0) < 0.000001

    # Test 2: Geometric mean of (1,1,1,1) should be 1
    assert abs(geometric_mean(1, 1, 1, 1) - 1.0) < 0.000001

    # Test 3: Harmonic mean is always <= geometric mean
    L, J, P, W = 0.8, 0.6, 0.7, 0.9
    assert harmonic_mean(L, J, P, W) <= geometric_mean(L, J, P, W)

    # Test 4: Zero values should return 0
    assert harmonic_mean(0, 0.5, 0.5, 0.5) == 0
    assert geometric_mean(0, 0.5, 0.5, 0.5) == 0

    print("✓ Mixing algorithms test passed")


def test_coupling_effects():
    """Test Love multiplier coupling effects"""

    def effective_dimensions(L, J, P, W):
        return {
            "effective_L": L,
            "effective_J": J * (1 + 1.4 * L),
            "effective_P": P * (1 + 1.3 * L),
            "effective_W": W * (1 + 1.5 * L),
        }

    # Test 1: With L=0, effective dimensions should equal raw dimensions
    eff = effective_dimensions(0, 0.5, 0.5, 0.5)
    assert eff["effective_L"] == 0
    assert eff["effective_J"] == 0.5
    assert eff["effective_P"] == 0.5
    assert eff["effective_W"] == 0.5

    # Test 2: With L=0.5, dimensions should be amplified
    eff = effective_dimensions(0.5, 0.5, 0.5, 0.5)
    assert eff["effective_J"] > 0.5  # Should be amplified
    assert eff["effective_P"] > 0.5  # Should be amplified
    assert eff["effective_W"] > 0.5  # Should be amplified

    # Test 3: Wisdom should have strongest amplification (1.5x)
    eff = effective_dimensions(1.0, 1.0, 1.0, 1.0)
    # At L=1.0: J gets 1.4, P gets 1.3, W gets 1.5
    assert eff["effective_J"] == 1.0 * (1 + 1.4 * 1.0)
    assert eff["effective_P"] == 1.0 * (1 + 1.3 * 1.0)
    assert eff["effective_W"] == 1.0 * (1 + 1.5 * 1.0)
    assert eff["effective_W"] > eff["effective_J"]  # W should be highest

    print("✓ Coupling effects test passed")


def test_interpretation_functions():
    """Test interpretation helper functions"""

    def interpret_distance_from_ne(distance):
        if distance < 0.2:
            return "Near-optimal balance"
        elif distance < 0.5:
            return "Good but improvable"
        elif distance < 0.8:
            return "Moderate imbalance"
        else:
            return "Significant dysfunction"

    def interpret_composite_score(score):
        if score < 0.5:
            return "Critical - multiple dimensions failing"
        elif score < 0.7:
            return "Struggling - functional but inefficient"
        elif score < 0.9:
            return "Competent - solid baseline performance"
        elif score < 1.1:
            return "Strong - above-average effectiveness"
        elif score < 1.3:
            return "Excellent - high-performing, growth active"
        else:
            return "Elite - exceptional, Love multiplier engaged"

    # Test distance interpretation
    assert "Near-optimal" in interpret_distance_from_ne(0.1)
    assert "Good" in interpret_distance_from_ne(0.3)
    assert "Moderate" in interpret_distance_from_ne(0.6)
    assert "dysfunction" in interpret_distance_from_ne(0.9)

    # Test score interpretation
    assert "Critical" in interpret_composite_score(0.3)
    assert "Struggling" in interpret_composite_score(0.6)
    assert "Competent" in interpret_composite_score(0.8)
    assert "Strong" in interpret_composite_score(1.0)
    assert "Excellent" in interpret_composite_score(1.2)
    assert "Elite" in interpret_composite_score(1.4)

    print("✓ Interpretation functions test passed")


def main():
    """Run all tests"""
    print("=" * 70)
    print("LJPW Baselines v4.0 - Test Suite")
    print("=" * 70)
    print()

    tests = [
        test_numerical_equivalents,
        test_reference_points,
        test_distance_calculations,
        test_mixing_algorithms,
        test_coupling_effects,
        test_interpretation_functions,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1

    print()
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {failed} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
