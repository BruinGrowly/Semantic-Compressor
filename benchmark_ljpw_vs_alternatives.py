#!/usr/bin/env python3
"""
Benchmark: LJPW vs Alternative Semantic Similarity Measures
==============================================================

Compares LJPW against traditional code similarity/quality metrics:
1. Cyclomatic Complexity (McCabe)
2. Lines of Code (LOC)
3. Levenshtein Distance (string similarity)
4. AST Edit Distance (structural similarity)
5. Halstead Metrics

Test Cases:
- Semantic equivalence (should be similar)
- Syntactic variation (should be different for most, same for LJPW)
- Quality degradation (should detect smells)
- Cross-language equivalence (only LJPW should handle this)
"""

import sys
from pathlib import Path
import math
import re

sys.path.insert(0, str(Path(__file__).parent))
from ljpw_standalone import analyze_quick, calculate_distance

# =============================================================================
# ALTERNATIVE METRICS IMPLEMENTATIONS
# =============================================================================

def calculate_cyclomatic_complexity(code):
    """Calculate McCabe cyclomatic complexity (simple approximation)"""
    decision_points = len(re.findall(r'\b(if|elif|else|for|while|and|or|except|case)\b', code))
    return decision_points + 1


def calculate_loc(code):
    """Calculate lines of code (non-empty, non-comment)"""
    lines = code.split('\n')
    loc = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('//'):
            loc += 1
    return loc


def levenshtein_distance(s1, s2):
    """Calculate Levenshtein distance between two strings"""
    # Normalize whitespace for fairer comparison
    s1 = ' '.join(s1.split())
    s2 = ' '.join(s2.split())

    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer than s2
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def normalized_levenshtein(s1, s2):
    """Normalized Levenshtein distance (0 = identical, 1 = completely different)"""
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return distance / max_len if max_len > 0 else 0


def simple_ast_features(code):
    """Extract simple AST-like features"""
    features = {
        'functions': len(re.findall(r'\b(def|function|func)\b', code)),
        'classes': len(re.findall(r'\bclass\b', code)),
        'loops': len(re.findall(r'\b(for|while)\b', code)),
        'conditionals': len(re.findall(r'\bif\b', code)),
        'returns': len(re.findall(r'\breturn\b', code)),
        'variables': len(re.findall(r'[a-z_][a-z0-9_]*\s*=', code, re.I)),
    }
    return features


def ast_feature_distance(code1, code2):
    """Calculate distance between AST features (simple structural similarity)"""
    f1 = simple_ast_features(code1)
    f2 = simple_ast_features(code2)

    # Euclidean distance of feature vectors
    distance_sq = sum((f1.get(k, 0) - f2.get(k, 0)) ** 2 for k in set(f1.keys()) | set(f2.keys()))
    return math.sqrt(distance_sq)


def halstead_metrics(code):
    """Calculate Halstead complexity metrics (simplified)"""
    # Operators and operands (simplified)
    operators = re.findall(r'[+\-*/%=<>!&|^~]|[\(\)\[\]\{\}]|\b(if|else|for|while|return|def|class)\b', code)
    operands = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b|\b\d+\b', code)

    n1 = len(set(operators))  # Unique operators
    n2 = len(set(operands))   # Unique operands
    N1 = len(operators)       # Total operators
    N2 = len(operands)        # Total operands

    if n1 == 0 or n2 == 0:
        return {'vocabulary': 0, 'length': 0, 'volume': 0}

    vocabulary = n1 + n2
    length = N1 + N2
    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0

    return {
        'vocabulary': vocabulary,
        'length': length,
        'volume': volume
    }


# =============================================================================
# TEST CASES
# =============================================================================

# Test 1: Semantic Equivalence (different syntax, same meaning)
semantic_equiv_tests = [
    ("Python list comprehension", """
result = [x * 2 for x in range(10)]
"""),
    ("Python traditional loop", """
result = []
for x in range(10):
    result.append(x * 2)
"""),
]

# Test 2: Syntactic Variation (same meaning, different style)
syntactic_variation_tests = [
    ("Compact style", """
def add(a,b):return a+b
"""),
    ("Expanded style", """
def add(a, b):
    result = a + b
    return result
"""),
]

# Test 3: Cross-Language Equivalence (only LJPW should detect)
cross_language_tests = [
    ("Python", """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""),
    ("JavaScript", """
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
"""),
]

# Test 4: Quality Degradation (adding code smell)
quality_degradation_tests = [
    ("Clean code", """
def calculate_total(items):
    return sum(item.price for item in items)
"""),
    ("Code smell (god function)", """
def calculate_total(items):
    total = 0
    for item in items:
        if item:
            if hasattr(item, 'price'):
                if item.price is not None:
                    if item.price > 0:
                        total = total + item.price
    return total
"""),
]


# =============================================================================
# BENCHMARK EXECUTION
# =============================================================================

def ljpw_distance(code1, code2):
    """Calculate LJPW semantic distance"""
    r1 = analyze_quick(code1)
    r2 = analyze_quick(code2)

    coords1 = (r1['ljpw']['L'], r1['ljpw']['J'], r1['ljpw']['P'], r1['ljpw']['W'])
    coords2 = (r2['ljpw']['L'], r2['ljpw']['J'], r2['ljpw']['P'], r2['ljpw']['W'])

    return calculate_distance(coords1, coords2)


def benchmark_test_case(name, code1, code2, expected_similar=True):
    """Run all metrics on a test case"""
    print(f"\n{'─' * 70}")
    print(f"Test: {name}")
    print(f"Expected: {'Similar' if expected_similar else 'Different'}")
    print('─' * 70)

    # LJPW
    ljpw_dist = ljpw_distance(code1, code2)

    # Traditional metrics
    cyclo1 = calculate_cyclomatic_complexity(code1)
    cyclo2 = calculate_cyclomatic_complexity(code2)
    cyclo_diff = abs(cyclo1 - cyclo2)

    loc1 = calculate_loc(code1)
    loc2 = calculate_loc(code2)
    loc_diff = abs(loc1 - loc2)

    lev_dist = normalized_levenshtein(code1, code2)

    ast_dist = ast_feature_distance(code1, code2)

    hal1 = halstead_metrics(code1)
    hal2 = halstead_metrics(code2)
    hal_volume_diff = abs(hal1['volume'] - hal2['volume'])

    # Display results
    print(f"\nLJPW Distance:          {ljpw_dist:.3f} {'✓ Correct' if (ljpw_dist < 0.2) == expected_similar else '✗ Wrong'}")
    print(f"Cyclomatic Diff:        {cyclo_diff} {'✓ Correct' if (cyclo_diff < 2) == expected_similar else '✗ Wrong'}")
    print(f"LOC Diff:               {loc_diff} {'✓ Correct' if (loc_diff < 3) == expected_similar else '✗ Wrong'}")
    print(f"Levenshtein (norm):     {lev_dist:.3f} {'✓ Correct' if (lev_dist < 0.3) == expected_similar else '✗ Wrong'}")
    print(f"AST Feature Distance:   {ast_dist:.3f} {'✓ Correct' if (ast_dist < 2.0) == expected_similar else '✗ Wrong'}")
    print(f"Halstead Volume Diff:   {hal_volume_diff:.1f} {'✓ Correct' if (hal_volume_diff < 20) == expected_similar else '✗ Wrong'}")

    # Score each metric
    scores = {
        'LJPW': 1 if (ljpw_dist < 0.2) == expected_similar else 0,
        'Cyclomatic': 1 if (cyclo_diff < 2) == expected_similar else 0,
        'LOC': 1 if (loc_diff < 3) == expected_similar else 0,
        'Levenshtein': 1 if (lev_dist < 0.3) == expected_similar else 0,
        'AST': 1 if (ast_dist < 2.0) == expected_similar else 0,
        'Halstead': 1 if (hal_volume_diff < 20) == expected_similar else 0,
    }

    return scores


def main():
    """Run benchmark comparing LJPW vs alternatives"""
    print("=" * 70)
    print("BENCHMARK: LJPW vs Alternative Semantic Similarity Measures")
    print("=" * 70)
    print()
    print("Comparing:")
    print("  1. LJPW (4D semantic coordinates)")
    print("  2. Cyclomatic Complexity (McCabe)")
    print("  3. Lines of Code (LOC)")
    print("  4. Levenshtein Distance (string similarity)")
    print("  5. AST Feature Distance (structural similarity)")
    print("  6. Halstead Metrics (complexity)")
    print()

    all_scores = {
        'LJPW': 0,
        'Cyclomatic': 0,
        'LOC': 0,
        'Levenshtein': 0,
        'AST': 0,
        'Halstead': 0,
    }

    total_tests = 0

    # Test 1: Semantic Equivalence
    print("\n" + "=" * 70)
    print("TEST CATEGORY 1: SEMANTIC EQUIVALENCE")
    print("=" * 70)
    print("Different syntax, same meaning → should be similar")

    code1, code2 = semantic_equiv_tests[0][1], semantic_equiv_tests[1][1]
    scores = benchmark_test_case("List comprehension vs Loop", code1, code2, expected_similar=True)
    for metric, score in scores.items():
        all_scores[metric] += score
    total_tests += 1

    # Test 2: Syntactic Variation
    print("\n" + "=" * 70)
    print("TEST CATEGORY 2: SYNTACTIC VARIATION")
    print("=" * 70)
    print("Same meaning, different style → should be similar")

    code1, code2 = syntactic_variation_tests[0][1], syntactic_variation_tests[1][1]
    scores = benchmark_test_case("Compact vs Expanded", code1, code2, expected_similar=True)
    for metric, score in scores.items():
        all_scores[metric] += score
    total_tests += 1

    # Test 3: Cross-Language
    print("\n" + "=" * 70)
    print("TEST CATEGORY 3: CROSS-LANGUAGE EQUIVALENCE")
    print("=" * 70)
    print("Same algorithm, different language → should be similar (LJPW only)")

    code1, code2 = cross_language_tests[0][1], cross_language_tests[1][1]
    scores = benchmark_test_case("Python vs JavaScript", code1, code2, expected_similar=True)
    for metric, score in scores.items():
        all_scores[metric] += score
    total_tests += 1

    # Test 4: Quality Degradation
    print("\n" + "=" * 70)
    print("TEST CATEGORY 4: QUALITY DEGRADATION")
    print("=" * 70)
    print("Clean vs code smell → should be different")

    code1, code2 = quality_degradation_tests[0][1], quality_degradation_tests[1][1]
    scores = benchmark_test_case("Clean vs God Function", code1, code2, expected_similar=False)
    for metric, score in scores.items():
        all_scores[metric] += score
    total_tests += 1

    # Final Results
    print("\n" + "=" * 70)
    print("BENCHMARK RESULTS")
    print("=" * 70)
    print()
    print(f"{'Metric':<20} {'Score':<10} {'Accuracy'}")
    print("─" * 70)

    sorted_metrics = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)

    for metric, score in sorted_metrics:
        accuracy = (score / total_tests) * 100
        bar = '█' * int(accuracy / 5)
        print(f"{metric:<20} {score}/{total_tests:<9} {accuracy:>5.1f}% {bar}")

    print()
    winner = sorted_metrics[0][0]
    print(f"{'🏆 WINNER: ' + winner if winner == 'LJPW' else '⚠ WINNER: ' + winner}")
    print()

    if all_scores['LJPW'] == total_tests:
        print("✓ LJPW correctly classified ALL test cases!")
    elif all_scores['LJPW'] >= total_tests * 0.75:
        print("✓ LJPW performed well (>75% accuracy)")
    else:
        print("⚠ LJPW needs improvement")

    print()
    print("Key Insight:")
    print("  LJPW should excel at cross-language equivalence,")
    print("  which traditional metrics cannot detect.")
    print()


if __name__ == "__main__":
    main()
