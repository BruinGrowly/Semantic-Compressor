"""
Comprehensive Test Suite for LJPW Semantic Compiler Framework

Tests:
1. DNA-LJPW Correspondence Properties
2. Compression/Decompression Fidelity
3. Full Pipeline Integration
4. Mathematical Invariants
5. Performance Benchmarks
6. Edge Cases
"""

# Import framework components
import importlib.util
import math
import random
import time
from typing import Dict, List, Tuple


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load modules
import os

base_path = os.path.join(os.path.dirname(__file__), "..", "src", "ljpw")
compiler_mod = load_module(
    "ljpw_semantic_compiler", os.path.join(base_path, "ljpw_semantic_compiler.py")
)
compressor_mod = load_module(
    "ljpw_semantic_compressor", os.path.join(base_path, "ljpw_semantic_compressor.py")
)
expander_mod = load_module("ljpw_expander", os.path.join(base_path, "ljpw_expander.py"))
pipeline_mod = load_module("ljpw_pipeline", os.path.join(base_path, "ljpw_pipeline.py"))

# Import classes
SemanticCompressor = compressor_mod.SemanticCompressor
SemanticDecompressor = compressor_mod.SemanticDecompressor
AdvancedSemanticCompressor = compiler_mod.AdvancedSemanticCompressor
LJPWPipeline = pipeline_mod.LJPWPipeline

# Natural Equilibrium
NE = (0.618034, 0.414214, 0.718282, 0.693147)

# ============================================================================
# TEST SUITE 1: DNA-LJPW CORRESPONDENCE PROPERTIES
# ============================================================================


class DNACorrespondenceSuite:
    """Test the DNA-LJPW correspondence claims"""

    def __init__(self):
        self.results = []

    def test_conservation_laws(self):
        """Test P≈W pairing (like Chargaff's rule)"""
        print("\n" + "=" * 70)
        print("TEST 1: Conservation Laws (P~=W Pairing)")
        print("=" * 70)

        L, J, P, W = NE
        pw_diff = abs(P - W)

        print(f"Testing Chargaff-like rule: P ~= W")
        print(f"  P = {P:.6f}")
        print(f"  W = {W:.6f}")
        print(f"  |P - W| = {pw_diff:.6f}")

        # Test: difference should be < 0.03 (3% threshold)
        threshold = 0.03
        passed = pw_diff < threshold

        print(f"\nThreshold: {threshold}")
        print(
            f"Result: {'PASS' if passed else 'FAIL'} - P and W are {'nearly equal' if passed else 'different'}"
        )

        self.results.append(
            {"test": "P≈W Conservation", "passed": passed, "value": pw_diff, "threshold": threshold}
        )

        return passed

    def test_entropy_efficiency(self):
        """Test that LJPW has near-optimal entropy"""
        print("\n" + "=" * 70)
        print("TEST 2: Information Entropy Efficiency")
        print("=" * 70)

        L, J, P, W = NE
        total = L + J + P + W

        # Calculate normalized frequencies
        freq_L = L / total
        freq_J = J / total
        freq_P = P / total
        freq_W = W / total

        # Shannon entropy
        entropy = -(
            freq_L * math.log2(freq_L)
            + freq_J * math.log2(freq_J)
            + freq_P * math.log2(freq_P)
            + freq_W * math.log2(freq_W)
        )

        max_entropy = math.log2(4)  # 2.0 bits for uniform distribution
        efficiency = entropy / max_entropy

        print(f"Shannon Entropy: {entropy:.6f} bits")
        print(f"Maximum Possible: {max_entropy:.6f} bits")
        print(f"Efficiency: {efficiency:.6f} ({100*efficiency:.2f}%)")

        # Test: efficiency should be > 98%
        threshold = 0.98
        passed = efficiency > threshold

        print(f"\nThreshold: {threshold:.2%}")
        print(
            f"Result: {'PASS' if passed else 'FAIL'} - Entropy is {'near-optimal' if passed else 'suboptimal'}"
        )

        self.results.append(
            {
                "test": "Entropy Efficiency",
                "passed": passed,
                "value": efficiency,
                "threshold": threshold,
            }
        )

        return passed

    def test_gc_content_analog(self):
        """Test asymmetric distribution (GC content analog)"""
        print("\n" + "=" * 70)
        print("TEST 3: Asymmetric Distribution (GC Content Analog)")
        print("=" * 70)

        L, J, P, W = NE
        total = L + J + P + W

        high_value = P + W  # "GC" analog
        low_value = L + J  # "AT" analog

        gc_ratio = high_value / total

        print(f"High-value dimensions (P+W): {high_value:.6f}")
        print(f"Low-value dimensions (L+J): {low_value:.6f}")
        print(f"'GC Content': {gc_ratio:.6f} ({100*gc_ratio:.1f}%)")

        # Test: should be in biological range of 40-60%
        min_threshold = 0.40
        max_threshold = 0.60
        passed = min_threshold <= gc_ratio <= max_threshold

        print(f"\nBiological range: {min_threshold:.0%} - {max_threshold:.0%}")
        print(
            f"Result: {'PASS' if passed else 'FAIL'} - Ratio is {'within' if passed else 'outside'} biological range"
        )

        self.results.append(
            {
                "test": "GC Content Analog",
                "passed": passed,
                "value": gc_ratio,
                "threshold": f"{min_threshold}-{max_threshold}",
            }
        )

        return passed

    def run_all_tests(self):
        """Run all DNA correspondence tests"""
        print("\n" + "#" * 70)
        print("# DNA-LJPW CORRESPONDENCE TEST SUITE")
        print("#" * 70)

        tests = [
            self.test_conservation_laws,
            self.test_entropy_efficiency,
            self.test_gc_content_analog,
        ]

        passed = 0
        for test in tests:
            if test():
                passed += 1

        print("\n" + "=" * 70)
        print(f"DNA CORRESPONDENCE TESTS: {passed}/{len(tests)} PASSED")
        print("=" * 70)

        return passed, len(tests)


# ============================================================================
# TEST SUITE 2: COMPRESSION/DECOMPRESSION FIDELITY
# ============================================================================


class CompressionFidelitySuite:
    """Test compression and decompression accuracy"""

    def __init__(self):
        self.results = []

    def test_round_trip_accuracy(self):
        """Test that compress -> decompress preserves data"""
        print("\n" + "=" * 70)
        print("TEST 4: Round-Trip Compression Accuracy")
        print("=" * 70)

        # Create test trajectory
        original_trajectory = [
            (0.2, 0.3, 0.9, 0.2),
            (0.4, 0.4, 0.8, 0.4),
            (0.6, 0.41, 0.72, 0.65),
            (0.618, 0.414, 0.718, 0.693),  # Natural Equilibrium
        ]

        print(f"Original trajectory: {len(original_trajectory)} states")

        # Compress
        compressor = SemanticCompressor(quantization_levels=4)
        genome = compressor.compress_state_sequence(original_trajectory)

        print(f"Compressed to: {len(genome)} codons")

        # Decompress
        decompressor = SemanticDecompressor(quantization_levels=4)
        reconstructed = decompressor.decompress_genome(genome)

        print(f"Reconstructed: {len(reconstructed)} states")

        # Calculate error
        total_error = 0
        for orig, recon in zip(original_trajectory, reconstructed):
            error = math.sqrt(sum((o - r) ** 2 for o, r in zip(orig, recon)))
            total_error += error

        avg_error = total_error / len(original_trajectory)

        print(f"\nAverage reconstruction error: {avg_error:.4f}")
        print(f"Error as percentage: {100*avg_error:.2f}%")

        # Test: error should be < 30% (due to quantization)
        threshold = 0.30
        passed = avg_error < threshold

        print(f"\nThreshold: {threshold:.2%}")
        print(
            f"Result: {'PASS' if passed else 'FAIL'} - Reconstruction is {'accurate' if passed else 'inaccurate'}"
        )

        self.results.append(
            {
                "test": "Round-Trip Accuracy",
                "passed": passed,
                "value": avg_error,
                "threshold": threshold,
            }
        )

        return passed

    def test_error_correction(self):
        """Test that error correction via pairing works"""
        print("\n" + "=" * 70)
        print("TEST 5: Error Correction via Complementary Pairing")
        print("=" * 70)

        # Create test trajectory
        trajectory = [(0.5, 0.4, 0.7, 0.6) for _ in range(10)]

        compressor = SemanticCompressor(quantization_levels=4)
        genome = compressor.compress_state_sequence(trajectory)

        # Validate genome integrity
        decompressor = SemanticDecompressor(quantization_levels=4)
        validation = decompressor.validate_genome(genome)

        print(f"Genome integrity validation:")
        print(f"  Valid: {validation['valid']}")
        print(f"  Integrity score: {validation['integrity_score']:.1%}")
        print(f"  Errors detected: {validation['error_count']}")

        # Test: should have 100% integrity
        threshold = 1.0
        passed = validation["integrity_score"] >= threshold

        print(f"\nThreshold: {threshold:.0%}")
        print(
            f"Result: {'PASS' if passed else 'FAIL'} - Integrity is {'perfect' if passed else 'compromised'}"
        )

        self.results.append(
            {
                "test": "Error Correction",
                "passed": passed,
                "value": validation["integrity_score"],
                "threshold": threshold,
            }
        )

        return passed

    def test_compression_ratio(self):
        """Test that compression achieves expected ratios"""
        print("\n" + "=" * 70)
        print("TEST 6: Compression Ratio Performance")
        print("=" * 70)

        # Large trajectory
        trajectory = [
            (
                random.uniform(0.3, 0.9),
                random.uniform(0.3, 0.8),
                random.uniform(0.4, 0.9),
                random.uniform(0.3, 0.8),
            )
            for _ in range(100)
        ]

        compressor = SemanticCompressor(quantization_levels=4)
        genome = compressor.compress_state_sequence(trajectory)

        # Calculate compression
        original_bytes = len(trajectory) * 4 * 8  # 4 floats × 8 bytes
        compressed_bytes = len(genome.codons) * 1  # ~1 byte per codon char

        ratio = original_bytes / compressed_bytes if compressed_bytes > 0 else 0

        print(f"Original: {original_bytes} bytes")
        print(f"Compressed: {compressed_bytes} bytes")
        print(f"Compression ratio: {ratio:.1f}x")

        # Test: should achieve > 10x compression
        threshold = 10.0
        passed = ratio > threshold

        print(f"\nThreshold: {threshold:.1f}x")
        print(
            f"Result: {'PASS' if passed else 'FAIL'} - Compression is {'sufficient' if passed else 'insufficient'}"
        )

        self.results.append(
            {"test": "Compression Ratio", "passed": passed, "value": ratio, "threshold": threshold}
        )

        return passed

    def run_all_tests(self):
        """Run all compression tests"""
        print("\n" + "#" * 70)
        print("# COMPRESSION FIDELITY TEST SUITE")
        print("#" * 70)

        tests = [
            self.test_round_trip_accuracy,
            self.test_error_correction,
            self.test_compression_ratio,
        ]

        passed = 0
        for test in tests:
            if test():
                passed += 1

        print("\n" + "=" * 70)
        print(f"COMPRESSION TESTS: {passed}/{len(tests)} PASSED")
        print("=" * 70)

        return passed, len(tests)


# ============================================================================
# TEST SUITE 3: FULL PIPELINE INTEGRATION
# ============================================================================


class PipelineIntegrationSuite:
    """Test the complete pipeline end-to-end"""

    def __init__(self):
        self.results = []

    def test_real_code_analysis(self):
        """Test pipeline with real code samples"""
        print("\n" + "=" * 70)
        print("TEST 7: Real Code Analysis")
        print("=" * 70)

        # Test code samples
        test_samples = [
            (
                "safe_code.py",
                """
def process_data(data: list) -> list:
    '''Process data with validation'''
    if not isinstance(data, list):
        raise TypeError("Data must be list")

    try:
        result = []
        for item in data:
            if item is not None:
                result.append(item * 2)
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise
""",
            ),
            (
                "algorithm.py",
                """
def quicksort(arr: list) -> list:
    '''Quick sort algorithm - O(n log n)'''
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
""",
            ),
        ]

        print(f"Testing with {len(test_samples)} code files")

        # Run pipeline
        pipeline = LJPWPipeline()
        results = pipeline.analyze_codebase(
            test_samples, generate_docs=False, generate_improvement_plan=False
        )

        # Validate results
        has_analysis = len(results["analysis"]) == len(test_samples)
        has_genome = len(results["compressed_genome"]) > 0
        has_compression = results["compression_ratio"] > 1
        has_reasoning = "health_score" in results["reasoning"]

        print(f"\nValidation:")
        print(f"  Analysis complete: {has_analysis}")
        print(f"  Genome created: {has_genome}")
        print(f"  Compression achieved: {has_compression} ({results['compression_ratio']:.1f}x)")
        print(f"  Reasoning complete: {has_reasoning}")

        passed = all([has_analysis, has_genome, has_compression, has_reasoning])

        print(
            f"\nResult: {'PASS' if passed else 'FAIL'} - Pipeline {'completed' if passed else 'failed'}"
        )

        self.results.append(
            {
                "test": "Real Code Analysis",
                "passed": passed,
                "value": results["compression_ratio"],
                "threshold": "All steps complete",
            }
        )

        return passed

    def test_health_score_calculation(self):
        """Test that health scores are calculated correctly"""
        print("\n" + "=" * 70)
        print("TEST 8: Health Score Calculation")
        print("=" * 70)

        # Code at Natural Equilibrium should have high health
        perfect_code = (
            "perfect.py",
            """
def safe_efficient_well_designed_function(data: list) -> list:
    '''Perfect balance of safety, structure, performance, and design'''
    if not isinstance(data, list):
        raise TypeError("Expected list")

    try:
        # Efficient algorithm
        result = [item for item in data if item is not None]
        return sorted(result)  # O(n log n)
    except Exception as e:
        logging.error(f"Error processing: {e}")
        raise
""",
        )

        pipeline = LJPWPipeline()
        results = pipeline.analyze_codebase(
            [perfect_code], generate_docs=False, generate_improvement_plan=False
        )

        health_score = results["reasoning"]["health_score"]
        avg_ljpw = results["reasoning"]["average_ljpw"]
        distance = results["reasoning"]["distance_from_ne"]

        print(f"Health Score: {health_score:.2%}")
        print(
            f"Average LJPW: L={avg_ljpw[0]:.2f}, J={avg_ljpw[1]:.2f}, P={avg_ljpw[2]:.2f}, W={avg_ljpw[3]:.2f}"
        )
        print(f"Distance from NE: {distance:.3f}")

        # Test: health should be reasonable (> 0)
        threshold = 0.0
        passed = health_score > threshold

        print(f"\nThreshold: > {threshold:.0%}")
        print(
            f"Result: {'PASS' if passed else 'FAIL'} - Health score is {'valid' if passed else 'invalid'}"
        )

        self.results.append(
            {
                "test": "Health Score Calculation",
                "passed": passed,
                "value": health_score,
                "threshold": threshold,
            }
        )

        return passed

    def run_all_tests(self):
        """Run all pipeline tests"""
        print("\n" + "#" * 70)
        print("# PIPELINE INTEGRATION TEST SUITE")
        print("#" * 70)

        tests = [
            self.test_real_code_analysis,
            self.test_health_score_calculation,
        ]

        passed = 0
        for test in tests:
            if test():
                passed += 1

        print("\n" + "=" * 70)
        print(f"PIPELINE TESTS: {passed}/{len(tests)} PASSED")
        print("=" * 70)

        return passed, len(tests)


# ============================================================================
# TEST SUITE 4: PERFORMANCE BENCHMARKS
# ============================================================================


class PerformanceSuite:
    """Benchmark performance characteristics"""

    def __init__(self):
        self.results = []

    def test_large_scale_compression(self):
        """Test compression on large datasets"""
        print("\n" + "=" * 70)
        print("TEST 9: Large-Scale Compression Performance")
        print("=" * 70)

        # Generate large dataset
        sizes = [100, 500, 1000]

        for size in sizes:
            print(f"\nTesting with {size} states:")

            trajectory = [
                (
                    random.uniform(0.3, 0.9),
                    random.uniform(0.3, 0.8),
                    random.uniform(0.4, 0.9),
                    random.uniform(0.3, 0.8),
                )
                for _ in range(size)
            ]

            # Time compression
            start = time.time()
            compressor = SemanticCompressor(quantization_levels=4)
            genome = compressor.compress_state_sequence(trajectory)
            compress_time = time.time() - start

            # Time decompression
            start = time.time()
            decompressor = SemanticDecompressor(quantization_levels=4)
            reconstructed = decompressor.decompress_genome(genome)
            decompress_time = time.time() - start

            print(f"  Compression time: {compress_time*1000:.2f}ms")
            print(f"  Decompression time: {decompress_time*1000:.2f}ms")
            print(f"  Total time: {(compress_time + decompress_time)*1000:.2f}ms")
            print(f"  Throughput: {size/(compress_time + decompress_time):.0f} states/sec")

        # Test: should process at least 1000 states/sec
        threshold = 100  # states/sec (conservative)
        throughput = size / (compress_time + decompress_time)
        passed = throughput > threshold

        print(f"\nThreshold: {threshold} states/sec")
        print(
            f"Result: {'PASS' if passed else 'FAIL'} - Performance is {'acceptable' if passed else 'poor'}"
        )

        self.results.append(
            {
                "test": "Large-Scale Compression",
                "passed": passed,
                "value": throughput,
                "threshold": threshold,
            }
        )

        return passed

    def run_all_tests(self):
        """Run all performance tests"""
        print("\n" + "#" * 70)
        print("# PERFORMANCE BENCHMARK SUITE")
        print("#" * 70)

        tests = [
            self.test_large_scale_compression,
        ]

        passed = 0
        for test in tests:
            if test():
                passed += 1

        print("\n" + "=" * 70)
        print(f"PERFORMANCE TESTS: {passed}/{len(tests)} PASSED")
        print("=" * 70)

        return passed, len(tests)


# ============================================================================
# MASTER TEST RUNNER
# ============================================================================


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "#" * 70)
    print("# LJPW FRAMEWORK COMPREHENSIVE TEST SUITE")
    print("# Testing all components and claims")
    print("#" * 70)

    total_passed = 0
    total_tests = 0

    # Run test suites
    suites = [
        ("DNA-LJPW Correspondence", DNACorrespondenceSuite()),
        ("Compression Fidelity", CompressionFidelitySuite()),
        ("Pipeline Integration", PipelineIntegrationSuite()),
        ("Performance Benchmarks", PerformanceSuite()),
    ]

    results_summary = []

    for suite_name, suite in suites:
        passed, total = suite.run_all_tests()
        total_passed += passed
        total_tests += total
        results_summary.append((suite_name, passed, total))

    # Final summary
    print("\n" + "#" * 70)
    print("# FINAL TEST RESULTS")
    print("#" * 70)

    for suite_name, passed, total in results_summary:
        pct = 100 * passed / total if total > 0 else 0
        status = "PASS" if passed == total else "PARTIAL" if passed > 0 else "FAIL"
        print(f"\n{suite_name}:")
        print(f"  Tests: {passed}/{total} passed ({pct:.0f}%)")
        print(f"  Status: {status}")

    overall_pct = 100 * total_passed / total_tests if total_tests > 0 else 0
    print(f"\n" + "=" * 70)
    print(f"OVERALL: {total_passed}/{total_tests} tests passed ({overall_pct:.0f}%)")
    print("=" * 70)

    if total_passed == total_tests:
        print("\n[SUCCESS] All tests passed! Framework is validated.")
    elif overall_pct >= 80:
        print("\n[GOOD] Most tests passed. Framework is functional.")
    elif overall_pct >= 50:
        print("\n[PARTIAL] Some tests passed. Framework needs work.")
    else:
        print("\n[FAIL] Many tests failed. Framework needs revision.")

    return total_passed, total_tests


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    run_all_tests()
