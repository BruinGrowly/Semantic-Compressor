#!/usr/bin/env python3
"""
AST vs Regex Comparison Test

Compares AST-based and regex-based LJPW analysis on the same files.

Goal: Data-driven decision on which approach to use.
"""

import sys
import time
import random
import math
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'ljpw'))

from ljpw_ast_analyzer import LJPWASTAnalyzer
from ljpw_standalone import analyze_file as regex_analyze_file


def select_test_files(base_path: str, num_files: int = 100) -> List[str]:
    """Select random sample of Python files for testing"""
    all_files = list(Path(base_path).rglob("*.py"))

    if len(all_files) <= num_files:
        return [str(f) for f in all_files]

    # Random sample
    selected = random.sample(all_files, num_files)
    return [str(f) for f in selected]


def calculate_differences(regex_result: Dict[str, float], ast_result: Dict[str, float]) -> Dict[str, Any]:
    """Calculate differences between two LJPW results"""
    dims = ['L', 'J', 'P', 'W']

    # Component-wise differences
    differences = {}
    for dim in dims:
        regex_val = regex_result.get(dim, 0)
        ast_val = ast_result.get(dim, 0)
        diff = abs(regex_val - ast_val)
        rel_diff = (diff / regex_val * 100) if regex_val > 0 else 0
        differences[dim] = {
            'regex': regex_val,
            'ast': ast_val,
            'diff': diff,
            'rel_diff_pct': rel_diff,
        }

    # Euclidean distance
    regex_vec = [regex_result.get(d, 0) for d in dims]
    ast_vec = [ast_result.get(d, 0) for d in dims]
    euclidean_dist = math.sqrt(sum((r - a)**2 for r, a in zip(regex_vec, ast_vec)))

    # Check if strongest/weakest dimensions are preserved
    regex_max = dims[regex_vec.index(max(regex_vec))]
    regex_min = dims[regex_vec.index(min(regex_vec))]
    ast_max = dims[ast_vec.index(max(ast_vec))]
    ast_min = dims[ast_vec.index(min(ast_vec))]

    meaning_preserved = (regex_max == ast_max and regex_min == ast_min)

    return {
        'differences': differences,
        'euclidean_distance': euclidean_dist,
        'regex_strongest': regex_max,
        'regex_weakest': regex_min,
        'ast_strongest': ast_max,
        'ast_weakest': ast_min,
        'meaning_preserved': meaning_preserved,
    }


def run_comparison(test_files: List[str]) -> Dict[str, Any]:
    """Run both analyzers on test files and compare"""

    print(f"{'='*70}")
    print(f"AST vs REGEX COMPARISON TEST")
    print(f"{'='*70}")
    print(f"\nTesting on {len(test_files)} files")
    print()

    # Initialize AST analyzer
    ast_analyzer = LJPWASTAnalyzer()

    # Run regex-based analyzer
    print("Running regex-based analyzer...")
    regex_start = time.time()
    regex_results = []

    for file_path in test_files:
        try:
            result = regex_analyze_file(file_path)
            regex_results.append({
                'file': file_path,
                'L': result.get('ljpw', {}).get('L', 0),
                'J': result.get('ljpw', {}).get('J', 0),
                'P': result.get('ljpw', {}).get('P', 0),
                'W': result.get('ljpw', {}).get('W', 0),
            })
        except Exception as e:
            print(f"Regex error on {file_path}: {e}")
            regex_results.append({
                'file': file_path,
                'L': 0.618, 'J': 0.414, 'P': 0.718, 'W': 0.693,
                'error': str(e)
            })

    regex_time = time.time() - regex_start
    regex_speed = len(test_files) / regex_time

    print(f"✓ Regex analysis complete: {regex_time:.2f}s ({regex_speed:.0f} files/sec)")

    # Run AST-based analyzer
    print("\nRunning AST-based analyzer...")
    ast_start = time.time()
    ast_results = []

    for file_path in test_files:
        try:
            result = ast_analyzer.analyze_file(file_path)
            ast_results.append({
                'file': file_path,
                'L': result.get('L', 0),
                'J': result.get('J', 0),
                'P': result.get('P', 0),
                'W': result.get('W', 0),
            })
        except Exception as e:
            print(f"AST error on {file_path}: {e}")
            ast_results.append({
                'file': file_path,
                'L': 0.618, 'J': 0.414, 'P': 0.718, 'W': 0.693,
                'error': str(e)
            })

    ast_time = time.time() - ast_start
    ast_speed = len(test_files) / ast_time

    print(f"✓ AST analysis complete: {ast_time:.2f}s ({ast_speed:.0f} files/sec)")

    # Compare results
    print(f"\n{'='*70}")
    print("COMPARING RESULTS")
    print(f"{'='*70}\n")

    comparisons = []
    for regex_res, ast_res in zip(regex_results, ast_results):
        comp = calculate_differences(regex_res, ast_res)
        comp['file'] = regex_res['file']
        comparisons.append(comp)

    # Overall statistics
    avg_euclidean = sum(c['euclidean_distance'] for c in comparisons) / len(comparisons)
    meaning_preserved_count = sum(1 for c in comparisons if c['meaning_preserved'])
    meaning_preserved_pct = meaning_preserved_count / len(comparisons) * 100

    # Average differences per dimension
    avg_diffs = {}
    for dim in ['L', 'J', 'P', 'W']:
        avg_diff = sum(c['differences'][dim]['diff'] for c in comparisons) / len(comparisons)
        avg_rel_diff = sum(c['differences'][dim]['rel_diff_pct'] for c in comparisons) / len(comparisons)
        avg_diffs[dim] = {
            'abs_diff': avg_diff,
            'rel_diff_pct': avg_rel_diff,
        }

    return {
        'test_files': test_files,
        'regex_time': regex_time,
        'regex_speed': regex_speed,
        'ast_time': ast_time,
        'ast_speed': ast_speed,
        'comparisons': comparisons,
        'avg_euclidean_distance': avg_euclidean,
        'meaning_preserved_count': meaning_preserved_count,
        'meaning_preserved_pct': meaning_preserved_pct,
        'avg_diffs': avg_diffs,
    }


def print_detailed_report(results: Dict[str, Any]):
    """Print detailed comparison report"""

    print(f"{'='*70}")
    print("PERFORMANCE COMPARISON")
    print(f"{'='*70}")
    print(f"\nRegex-based analyzer:")
    print(f"  Time: {results['regex_time']:.2f}s")
    print(f"  Speed: {results['regex_speed']:.0f} files/sec")
    print(f"\nAST-based analyzer:")
    print(f"  Time: {results['ast_time']:.2f}s")
    print(f"  Speed: {results['ast_speed']:.0f} files/sec")

    speed_ratio = results['regex_speed'] / results['ast_speed']
    if speed_ratio > 1:
        print(f"\n→ Regex is {speed_ratio:.1f}x FASTER")
    else:
        print(f"\n→ AST is {1/speed_ratio:.1f}x FASTER")

    print(f"\n{'='*70}")
    print("ACCURACY COMPARISON")
    print(f"{'='*70}")
    print(f"\nAverage Euclidean distance: {results['avg_euclidean_distance']:.4f}")
    print(f"Meaning preserved: {results['meaning_preserved_count']}/{len(results['comparisons'])} ({results['meaning_preserved_pct']:.1f}%)")

    print(f"\nAverage differences by dimension:")
    for dim in ['L', 'J', 'P', 'W']:
        diff_data = results['avg_diffs'][dim]
        print(f"  {dim}: {diff_data['abs_diff']:.4f} ({diff_data['rel_diff_pct']:.1f}% relative)")

    # Show examples of biggest differences
    print(f"\n{'='*70}")
    print("FILES WITH BIGGEST DIFFERENCES")
    print(f"{'='*70}")

    top_diffs = sorted(results['comparisons'], key=lambda x: x['euclidean_distance'], reverse=True)[:5]

    for i, comp in enumerate(top_diffs, 1):
        file_name = Path(comp['file']).name
        print(f"\n{i}. {file_name}")
        print(f"   Distance: {comp['euclidean_distance']:.4f}")
        print(f"   Regex: L={comp['differences']['L']['regex']:.2f}, J={comp['differences']['J']['regex']:.2f}, P={comp['differences']['P']['regex']:.2f}, W={comp['differences']['W']['regex']:.2f}")
        print(f"   AST:   L={comp['differences']['L']['ast']:.2f}, J={comp['differences']['J']['ast']:.2f}, P={comp['differences']['P']['ast']:.2f}, W={comp['differences']['W']['ast']:.2f}")
        print(f"   Meaning preserved: {'✓' if comp['meaning_preserved'] else '✗'}")

    print(f"\n{'='*70}")
    print("RECOMMENDATION")
    print(f"{'='*70}\n")

    # Data-driven recommendation
    if results['meaning_preserved_pct'] < 80:
        print("❌ AST approach FAILS meaning preservation test")
        print(f"   Only {results['meaning_preserved_pct']:.1f}% of files preserved strongest/weakest dims")
        print(f"   Threshold: 80%")
        print(f"\n→ RECOMMENDATION: Stick with proven regex-based approach")

    elif results['avg_euclidean_distance'] > 0.2:
        print("⚠️  AST approach has HIGH coordinate differences")
        print(f"   Average distance: {results['avg_euclidean_distance']:.4f}")
        print(f"   Threshold: 0.2")
        print(f"\n→ RECOMMENDATION: Stick with proven regex-based approach")

    elif speed_ratio > 2:
        print("⚠️  AST approach is SIGNIFICANTLY slower")
        print(f"   Regex is {speed_ratio:.1f}x faster")
        print(f"   Threshold: 2x")
        print(f"\n→ RECOMMENDATION: Stick with proven regex-based approach unless accuracy gains are substantial")

    else:
        print("✅ AST approach passes basic tests")
        print(f"   Meaning preserved: {results['meaning_preserved_pct']:.1f}%")
        print(f"   Average distance: {results['avg_euclidean_distance']:.4f}")
        print(f"   Speed ratio: {speed_ratio:.1f}x")
        print(f"\n→ RECOMMENDATION: Consider AST approach for production use")
        print(f"   Note: Still needs validation on full 9,538 file corpus")


def main():
    """Run comparison test"""
    print("="*70)
    print("AST vs REGEX ANALYZER COMPARISON")
    print("="*70)
    print()
    print("This test compares two approaches to LJPW code analysis:")
    print("1. Regex-based (current, proven on 9,538 files)")
    print("2. AST-based (new, unvalidated)")
    print()

    # Use the requests library as test subject (small, manageable)
    test_path = "/tmp/ljpw_validation_test/requests"

    if not Path(test_path).exists():
        print(f"❌ Test path not found: {test_path}")
        print("\nPlease clone requests library first:")
        print("  mkdir -p /tmp/ljpw_validation_test")
        print("  cd /tmp/ljpw_validation_test")
        print("  git clone https://github.com/psf/requests.git")
        return 1

    # Select test files
    print(f"Selecting test files from: {test_path}")
    test_files = select_test_files(test_path, num_files=100)
    print(f"Selected {len(test_files)} files for testing\n")

    # Run comparison
    results = run_comparison(test_files)

    # Print detailed report
    print_detailed_report(results)

    return 0


if __name__ == '__main__':
    exit(main())
