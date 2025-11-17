#!/usr/bin/env python3
"""
Test script for configurable quantization levels
Tests accuracy, size, and validation for different precision settings
"""

import math
from ljpw_semantic_compressor import (
    SemanticCompressor,
    SemanticDecompressor,
    LJPWQuantizer,
    LJPWCodon,
)

def test_invalid_levels():
    """Test that invalid quantization levels are properly rejected"""
    print("="*70)
    print("TEST 1: Invalid Quantization Levels")
    print("="*70)

    invalid_cases = [
        (3, "Not a power of 2"),
        (5, "Not in VALID_LEVELS"),
        (128, "Too large"),
        ("4", "Wrong type (string)"),
        (4.0, "Wrong type (float)"),
    ]

    passed = 0
    failed = 0

    for level, description in invalid_cases:
        try:
            quantizer = LJPWQuantizer(levels=level)
            print(f"✗ FAIL: {description} - Expected error but got: {quantizer.levels}")
            failed += 1
        except (TypeError, ValueError) as e:
            print(f"✓ PASS: {description} - Correctly rejected with: {type(e).__name__}")
            passed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_recommend_levels():
    """Test the recommend_levels helper"""
    print("\n" + "="*70)
    print("TEST 2: Recommendation System")
    print("="*70)

    test_cases = [
        ('fast', 4),
        ('balanced', 8),
        ('precise', 16),
        ('exact', 32),
    ]

    passed = 0
    for use_case, expected in test_cases:
        result = LJPWQuantizer.recommend_levels(use_case)
        if result == expected:
            print(f"✓ PASS: '{use_case}' → {result} levels")
            passed += 1
        else:
            print(f"✗ FAIL: '{use_case}' → {result}, expected {expected}")

    # Test invalid use case
    try:
        LJPWQuantizer.recommend_levels('invalid')
        print("✗ FAIL: Invalid use case should raise ValueError")
        return False
    except ValueError:
        print("✓ PASS: Invalid use case correctly rejected")
        passed += 1

    print(f"\nResult: {passed}/{len(test_cases)+1} passed")
    return passed == len(test_cases) + 1


def calculate_error(original, reconstructed):
    """Calculate Euclidean distance between states"""
    return math.sqrt(sum((o - r)**2 for o, r in zip(original, reconstructed)))


def test_quantization_accuracy():
    """Test compression accuracy at different quantization levels"""
    print("\n" + "="*70)
    print("TEST 3: Quantization Accuracy vs Levels")
    print("="*70)

    # Test states covering different value ranges
    test_states = [
        (0.1, 0.2, 0.3, 0.1),  # Low values
        (0.5, 0.5, 0.5, 0.5),  # Mid values
        (0.9, 0.8, 0.9, 0.9),  # High values
        (0.618, 0.414, 0.718, 0.693),  # Natural Equilibrium
        (1.2, 0.8, 1.1, 0.7),  # Values exceeding 1.0
    ]

    levels_to_test = [4, 8, 16, 32, 64]

    print(f"\nTesting {len(test_states)} states across {len(levels_to_test)} quantization levels\n")
    print(f"{'Levels':<10} {'Avg Error':<12} {'Max Error':<12} {'Genome Size':<12} {'Status':<10}")
    print("-" * 70)

    results = {}

    for levels in levels_to_test:
        compressor = SemanticCompressor(quantization_levels=levels)
        decompressor = SemanticDecompressor(quantization_levels=levels)

        errors = []

        for state in test_states:
            # Compress and decompress single state
            genome = compressor.compress_state_sequence([state])
            reconstructed = decompressor.decompress_genome(genome)[0]

            error = calculate_error(state, reconstructed)
            errors.append(error)

        avg_error = sum(errors) / len(errors)
        max_error = max(errors)

        # Get genome size
        genome = compressor.compress_state_sequence(test_states)
        genome_size = len(genome.to_string())

        status = "✓ PASS" if avg_error < 0.5 else "✗ FAIL"

        print(f"{levels:<10} {avg_error:<12.4f} {max_error:<12.4f} {genome_size:<12} {status:<10}")

        results[levels] = {
            'avg_error': avg_error,
            'max_error': max_error,
            'genome_size': genome_size,
        }

    # Verify that higher levels = better accuracy
    print("\nAccuracy Improvement Analysis:")
    print("-" * 70)

    prev_error = float('inf')
    monotonic = True

    for levels in levels_to_test:
        current_error = results[levels]['avg_error']
        improvement = ((prev_error - current_error) / prev_error * 100) if prev_error != float('inf') else 0

        if current_error >= prev_error and prev_error != float('inf'):
            monotonic = False
            print(f"{levels} levels: {current_error:.4f} error (✗ WORSE than previous!)")
        else:
            if prev_error != float('inf'):
                print(f"{levels} levels: {current_error:.4f} error ({improvement:.1f}% improvement)")
            else:
                print(f"{levels} levels: {current_error:.4f} error (baseline)")

        prev_error = current_error

    if monotonic:
        print("\n✓ PASS: Accuracy improves monotonically with more levels")
    else:
        print("\n✗ FAIL: Accuracy should improve with more levels")

    return monotonic


def test_round_trip_all_levels():
    """Test round-trip compression at all quantization levels"""
    print("\n" + "="*70)
    print("TEST 4: Round-Trip Integrity (All Levels)")
    print("="*70)

    trajectory = [
        (0.2, 0.3, 0.9, 0.2),
        (0.4, 0.35, 0.8, 0.4),
        (0.618, 0.414, 0.718, 0.693),
    ]

    levels_to_test = [4, 8, 16, 32, 64]
    all_passed = True

    for levels in levels_to_test:
        compressor = SemanticCompressor(quantization_levels=levels)
        decompressor = SemanticDecompressor(quantization_levels=levels)

        # Compress
        genome = compressor.compress_state_sequence(
            trajectory,
            metadata={'test': f'{levels}-level quantization'}
        )

        # Decompress
        reconstructed = decompressor.decompress_genome(genome)

        # Validate
        validation = decompressor.validate_genome(genome)

        # Check integrity
        passed = (
            len(reconstructed) == len(trajectory) and
            validation['valid'] and
            validation['integrity_score'] == 1.0
        )

        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{levels:2} levels: {status} - {len(reconstructed)} states, {validation['integrity_score']:.1%} integrity")

        if not passed:
            all_passed = False

    return all_passed


def test_codon_parsing_edge_cases():
    """Test that codon parsing handles edge cases properly"""
    print("\n" + "="*70)
    print("TEST 5: Codon Parsing Edge Cases")
    print("="*70)

    valid_cases = [
        "L0J0P0",
        "L9J9P9",  # Max single-digit levels
        "W5L3P7",
    ]

    invalid_cases = [
        ("L0J0P", "Too short"),
        ("L0J0P0X", "Too long"),
        ("X0J0P0", "Invalid base"),
        ("L0X0P0", "Invalid base"),
        ("LaJ0P0", "Non-digit level"),
        ("L-1J0P0", "Negative level (but will parse as 'L-')"),
    ]

    passed = 0

    # Test valid cases
    print("Valid cases:")
    for codon_str in valid_cases:
        try:
            codon = LJPWCodon.from_string(codon_str)
            print(f"✓ PASS: '{codon_str}' parsed successfully")
            passed += 1
        except Exception as e:
            print(f"✗ FAIL: '{codon_str}' should be valid, got: {e}")

    # Test invalid cases
    print("\nInvalid cases (should fail):")
    for codon_str, description in invalid_cases:
        try:
            codon = LJPWCodon.from_string(codon_str)
            print(f"✗ FAIL: '{codon_str}' ({description}) should raise error")
        except (ValueError, TypeError) as e:
            print(f"✓ PASS: '{codon_str}' ({description}) correctly rejected")
            passed += 1

    total = len(valid_cases) + len(invalid_cases)
    print(f"\nResult: {passed}/{total} passed")
    return passed == total


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("CONFIGURABLE QUANTIZATION TEST SUITE")
    print("="*70)
    print("\nTesting configurable precision levels in LJPW semantic compression\n")

    tests = [
        ("Invalid Levels Validation", test_invalid_levels),
        ("Recommendation System", test_recommend_levels),
        ("Quantization Accuracy", test_quantization_accuracy),
        ("Round-Trip Integrity", test_round_trip_all_levels),
        ("Codon Parsing Edge Cases", test_codon_parsing_edge_cases),
    ]

    results = []

    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n✗ EXCEPTION in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")

    total = len(results)
    passed_count = sum(1 for _, passed in results if passed)

    print("\n" + "="*70)
    print(f"OVERALL: {passed_count}/{total} test suites passed")
    print("="*70)

    if passed_count == total:
        print("\n✅ ALL TESTS PASSED - Configurable quantization is working correctly!")
        return 0
    else:
        print(f"\n❌ {total - passed_count} test suite(s) failed")
        return 1


if __name__ == '__main__':
    exit(main())
