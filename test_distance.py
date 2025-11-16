#!/usr/bin/env python3
"""
Test Suite for Distance Calculation

Tests the semantic distance calculation between files.
"""

import math
import sys
from pathlib import Path

# Import from ljpw_standalone
sys.path.insert(0, str(Path(__file__).parent))
from ljpw_standalone import calculate_distance, calculate_file_distance

# ============================================================================
# TEST SUITE
# ============================================================================

class TestDistance:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def assert_equal(self, actual, expected, test_name, tolerance=0.001):
        """Assert values are equal within tolerance"""
        if abs(actual - expected) < tolerance:
            self.passed += 1
            self.tests.append((test_name, True, f"✓ {test_name}"))
            return True
        else:
            self.failed += 1
            self.tests.append((test_name, False, f"✗ {test_name}: expected {expected}, got {actual}"))
            return False

    def assert_true(self, condition, test_name):
        """Assert condition is true"""
        if condition:
            self.passed += 1
            self.tests.append((test_name, True, f"✓ {test_name}"))
            return True
        else:
            self.failed += 1
            self.tests.append((test_name, False, f"✗ {test_name}: condition failed"))
            return False

    def print_results(self):
        """Print test results"""
        print("\n" + "=" * 70)
        print("DISTANCE CALCULATION TEST RESULTS")
        print("=" * 70)

        for _, passed, msg in self.tests:
            print(msg)

        print("\n" + "=" * 70)
        print(f"Total: {self.passed + self.failed} tests")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print("=" * 70)

        if self.failed == 0:
            print("\n✅ ALL TESTS PASSED")
            return 0
        else:
            print(f"\n❌ {self.failed} TESTS FAILED")
            return 1

def main():
    test = TestDistance()

    # ========================================================================
    # Test 1: Identical Coordinates
    # ========================================================================
    coords1 = (0.8, 0.9, 0.5, 0.7)
    coords2 = (0.8, 0.9, 0.5, 0.7)
    distance = calculate_distance(coords1, coords2)
    test.assert_equal(distance, 0.0, "Identical coordinates should have distance 0")

    # ========================================================================
    # Test 2: Single Dimension Difference
    # ========================================================================
    coords1 = (0.8, 0.9, 0.5, 0.7)
    coords2 = (0.8, 0.9, 1.5, 0.7)  # Only P differs by 1.0
    distance = calculate_distance(coords1, coords2)
    test.assert_equal(distance, 1.0, "Single dimension difference of 1.0")

    # ========================================================================
    # Test 3: Pythagorean Distance
    # ========================================================================
    coords1 = (0, 0, 0, 0)
    coords2 = (1, 1, 0, 0)  # Should be sqrt(2)
    distance = calculate_distance(coords1, coords2)
    test.assert_equal(distance, math.sqrt(2), "Pythagorean distance", tolerance=0.001)

    # ========================================================================
    # Test 4: Triangle Inequality
    # ========================================================================
    coords1 = (0.8, 0.9, 0.5, 0.7)
    coords2 = (0.6, 0.7, 0.8, 0.9)
    coords3 = (0.9, 0.8, 0.6, 0.5)

    d12 = calculate_distance(coords1, coords2)
    d23 = calculate_distance(coords2, coords3)
    d13 = calculate_distance(coords1, coords3)

    # Triangle inequality: d13 <= d12 + d23
    test.assert_true(d13 <= d12 + d23 + 0.001,
                    "Triangle inequality holds")

    # ========================================================================
    # Test 5: Symmetry
    # ========================================================================
    coords1 = (0.8, 0.9, 0.5, 0.7)
    coords2 = (0.6, 0.7, 0.8, 0.9)

    d12 = calculate_distance(coords1, coords2)
    d21 = calculate_distance(coords2, coords1)

    test.assert_equal(d12, d21, "Distance is symmetric")

    # ========================================================================
    # Test 6: Natural Equilibrium to Anchor
    # ========================================================================
    NE = (0.618, 0.414, 0.718, 0.693)
    Anchor = (1.0, 1.0, 1.0, 1.0)

    distance_NE_Anchor = calculate_distance(NE, Anchor)
    # Expected: sqrt((1-0.618)^2 + (1-0.414)^2 + (1-0.718)^2 + (1-0.693)^2)
    #         = sqrt(0.146 + 0.343 + 0.079 + 0.094)
    #         = sqrt(0.662) = 0.814
    test.assert_equal(distance_NE_Anchor, 0.814, "NE to Anchor distance", tolerance=0.01)

    # ========================================================================
    # Test 7: File Distance (Integration Test)
    # ========================================================================
    # Test distance calculation between actual files
    file1 = "ljpw_standalone.py"
    file2 = "test_configurable_quantization.py"

    if Path(file1).exists() and Path(file2).exists():
        result = calculate_file_distance(file1, file2)

        test.assert_true('error' not in result, "File distance calculation succeeds")
        test.assert_true('distance' in result, "Result contains distance")
        test.assert_true('similarity' in result, "Result contains similarity")
        test.assert_true('interpretation' in result, "Result contains interpretation")
        test.assert_true(result['distance'] >= 0, "Distance is non-negative")

        # Check coordinates are tuples of 4 floats
        test.assert_true(len(result['coords1']) == 4, "Coords1 has 4 dimensions")
        test.assert_true(len(result['coords2']) == 4, "Coords2 has 4 dimensions")
    else:
        print(f"\n⚠ Skipping file distance test (files not found)")

    # ========================================================================
    # Test 8: Distance Interpretation Ranges
    # ========================================================================
    # Test that similarity interpretation is correct

    # Very High similarity (< 0.2)
    coords1 = (0.8, 0.9, 0.5, 0.7)
    coords2 = (0.81, 0.91, 0.51, 0.71)
    distance = calculate_distance(coords1, coords2)
    test.assert_true(distance < 0.2, "Very similar coordinates have distance < 0.2")

    # High similarity (0.2 - 0.4)
    coords1 = (0.8, 0.9, 0.5, 0.7)
    coords2 = (0.8, 0.9, 0.7, 0.7)  # P differs by 0.2
    distance = calculate_distance(coords1, coords2)
    test.assert_true(0.19 < distance < 0.4, "Moderately similar coords: 0.2 < d < 0.4")

    # ========================================================================
    # Test 9: Zero Coordinates
    # ========================================================================
    coords1 = (0, 0, 0, 0)
    coords2 = (0, 0, 0, 0)
    distance = calculate_distance(coords1, coords2)
    test.assert_equal(distance, 0.0, "Zero coordinates distance")

    # ========================================================================
    # Test 10: Large Coordinates
    # ========================================================================
    coords1 = (2.0, 2.0, 2.0, 2.0)
    coords2 = (3.0, 3.0, 3.0, 3.0)
    distance = calculate_distance(coords1, coords2)
    # Distance = sqrt(4 * 1^2) = 2.0
    test.assert_equal(distance, 2.0, "Large coordinates distance")

    return test.print_results()

if __name__ == '__main__':
    sys.exit(main())
