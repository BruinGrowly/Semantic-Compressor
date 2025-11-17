#!/usr/bin/env python3
"""
Test Suite for Distance Calculation

Tests the semantic distance calculation between files.
"""

import json
import math
import sys
from pathlib import Path

# Import from ljpw_standalone
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'ljpw'))
from ljpw_standalone import (
    calculate_distance,
    calculate_file_distance,
    calculate_batch_distance,
    format_distance_result_json,
    format_batch_distance_result_json
)

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

    # ========================================================================
    # Test 11: JSON Output Format
    # ========================================================================
    if Path(file1).exists() and Path(file2).exists():
        result = calculate_file_distance(file1, file2)
        json_output = format_distance_result_json(result)

        # Parse JSON to verify it's valid
        try:
            parsed = json.loads(json_output)
            test.assert_true('file1' in parsed, "JSON contains file1")
            test.assert_true('file2' in parsed, "JSON contains file2")
            test.assert_true('coordinates' in parsed, "JSON contains coordinates")
            test.assert_true('distance' in parsed, "JSON contains distance")
            test.assert_true('similarity' in parsed, "JSON contains similarity")
        except json.JSONDecodeError:
            test.assert_true(False, "JSON output is valid JSON")
    else:
        print(f"\n⚠ Skipping JSON format test (files not found)")

    # ========================================================================
    # Test 12: Batch Distance Calculation
    # ========================================================================
    # Create a list of test files
    test_files = []
    for filepath in [file1, file2, "test_distance.py"]:
        if Path(filepath).exists():
            test_files.append(filepath)

    if len(test_files) >= 3:
        batch_result = calculate_batch_distance(test_files)

        test.assert_true('error' not in batch_result, "Batch calculation succeeds")
        test.assert_true('files' in batch_result, "Batch result contains files")
        test.assert_true('distance_matrix' in batch_result, "Batch result contains distance matrix")
        test.assert_true('most_similar' in batch_result, "Batch result contains most_similar")
        test.assert_true('most_different' in batch_result, "Batch result contains most_different")

        # Verify distance matrix dimensions
        n = len(test_files)
        matrix = batch_result['distance_matrix']
        test.assert_true(len(matrix) == n, f"Distance matrix has {n} rows")
        test.assert_true(len(matrix[0]) == n, f"Distance matrix has {n} columns")

        # Verify diagonal is all zeros
        all_zeros = all(matrix[i][i] == 0.0 for i in range(n))
        test.assert_true(all_zeros, "Distance matrix diagonal is all zeros")

        # Verify symmetry
        symmetric = all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n))
        test.assert_true(symmetric, "Distance matrix is symmetric")
    else:
        print(f"\n⚠ Skipping batch distance test (need at least 3 files)")

    # ========================================================================
    # Test 13: Batch JSON Output Format
    # ========================================================================
    if len(test_files) >= 3:
        batch_result = calculate_batch_distance(test_files)
        json_output = format_batch_distance_result_json(batch_result)

        # Parse JSON to verify it's valid
        try:
            parsed = json.loads(json_output)
            test.assert_true('files' in parsed, "Batch JSON contains files")
            test.assert_true('coordinates' in parsed, "Batch JSON contains coordinates")
            test.assert_true('distance_matrix' in parsed, "Batch JSON contains distance_matrix")
            test.assert_true('most_similar' in parsed, "Batch JSON contains most_similar")
            test.assert_true('most_different' in parsed, "Batch JSON contains most_different")
        except json.JSONDecodeError:
            test.assert_true(False, "Batch JSON output is valid JSON")
    else:
        print(f"\n⚠ Skipping batch JSON format test (need at least 3 files)")

    # ========================================================================
    # Test 14: Most Similar/Different Detection
    # ========================================================================
    if len(test_files) >= 3:
        batch_result = calculate_batch_distance(test_files)

        most_sim = batch_result['most_similar']
        most_diff = batch_result['most_different']

        test.assert_true(most_sim is not None, "Most similar pair found")
        test.assert_true(most_diff is not None, "Most different pair found")

        # Most similar should have smaller distance than most different
        if most_sim and most_diff:
            test.assert_true(most_sim[2] <= most_diff[2],
                           "Most similar distance <= most different distance")
    else:
        print(f"\n⚠ Skipping most similar/different test (need at least 3 files)")

    # ========================================================================
    # Test 15: Batch Error Handling (< 2 files)
    # ========================================================================
    batch_result = calculate_batch_distance(["single_file.py"])
    test.assert_true('error' in batch_result, "Batch with <2 files returns error")

    return test.print_results()

if __name__ == '__main__':
    sys.exit(main())
