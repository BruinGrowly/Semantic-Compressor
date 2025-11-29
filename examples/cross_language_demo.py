#!/usr/bin/env python3
"""
Cross-Language LJPW Analysis Demo
==================================

Demonstrates that semantically equivalent code in different languages
maps to similar LJPW coordinates.

This is the CORE THESIS of LJPW veracity.
"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

import json

from multi_language_analyzer import analyze_code, compare_implementations


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"{title:^80}")
    print("=" * 80 + "\n")


def main():
    """Run cross-language analysis demo"""

    print_header("CROSS-LANGUAGE LJPW ANALYSIS DEMO")

    print("Hypothesis: Same algorithm in different languages → Similar LJPW coordinates")
    print("Algorithm: QuickSort (divide-and-conquer sorting)")
    print("Languages: Python, JavaScript, Go")
    print("\n" + "=" * 80)

    # File paths
    base_path = Path(__file__).parent / "cross_language" / "quicksort"
    files = {
        "python": str(base_path / "quicksort.py"),
        "javascript": str(base_path / "quicksort.js"),
        "go": str(base_path / "quicksort.go"),
    }

    # Analyze
    print("\n🔬 Analyzing implementations...")
    results = compare_implementations(files)

    # Display individual results
    print_header("INDIVIDUAL LJPW COORDINATES")

    print(f"{'Language':<15} {'L':<10} {'J':<10} {'P':<10} {'W':<10} {'Health':<10}")
    print("-" * 80)

    for lang, data in results["implementations"].items():
        if "error" not in data:
            print(
                f"{lang.capitalize():<15} "
                f"{data['L']:.3f}      "
                f"{data['J']:.3f}      "
                f"{data['P']:.3f}      "
                f"{data['W']:.3f}      "
                f"{data['health_score']:.1f}%"
            )

    # Display statistics
    print_header("CROSS-LANGUAGE STATISTICS")

    if "statistics" in results and results["statistics"]:
        stats = results["statistics"]

        print("Mean LJPW Coordinates:")
        mean = stats["mean"]
        print(f"  L (Love/Safety):       {mean['L']:.3f}")
        print(f"  J (Justice/Structure): {mean['J']:.3f}")
        print(f"  P (Power/Performance): {mean['P']:.3f}")
        print(f"  W (Wisdom/Design):     {mean['W']:.3f}")

        print("\nStandard Deviation (σ):")
        std = stats["std_dev"]
        print(f"  L: {std['L']:.3f}")
        print(f"  J: {std['J']:.3f}")
        print(f"  P: {std['P']:.3f}")
        print(f"  W: {std['W']:.3f}")
        print(f"  Average σ: {sum(std.values())/4:.3f}")

        print("\nCross-Language Variance:")
        variance = stats["cross_language_variance"]
        print(f"  Total Variance: {variance:.4f}")

        # Invariance score
        invariance = results.get("cross_language_invariance_score", 0)
        print(f"  Invariance Score: {invariance:.2f}")

        if invariance > 0.90:
            print("  ✓ EXCELLENT - Strong semantic invariance!")
        elif invariance > 0.75:
            print("  ✓ GOOD - Clear semantic pattern across languages")
        elif invariance > 0.50:
            print("  ⚠ MODERATE - Some language-specific variation")
        else:
            print("  ✗ WEAK - High language-specific variation")

    # Display pairwise distances
    print_header("PAIRWISE SEMANTIC DISTANCES")

    if "pairwise_distances" in results:
        distances = results["pairwise_distances"]

        print("Euclidean distance in 4D LJPW space:")
        print("(Lower = more semantically similar)\n")

        for pair, distance in sorted(distances.items(), key=lambda x: x[1]):
            lang1, lang2 = pair.split("_vs_")
            status = (
                "✓ SIMILAR"
                if distance < 0.15
                else ("⚠ MODERATE" if distance < 0.30 else "✗ DIFFERENT")
            )
            print(f"  {lang1.capitalize()} ↔ {lang2.capitalize():<15} {distance:.4f}  {status}")

        avg_distance = sum(distances.values()) / len(distances)
        print(f"\n  Average Distance: {avg_distance:.4f}")

        if avg_distance < 0.15:
            print("  ✓ STRONG CROSS-LANGUAGE INVARIANCE")
        elif avg_distance < 0.30:
            print("  ⚠ MODERATE CROSS-LANGUAGE INVARIANCE")
        else:
            print("  ✗ WEAK CROSS-LANGUAGE INVARIANCE")

    # Interpretation
    print_header("INTERPRETATION")

    print(
        """
What This Demonstrates:

1. **Semantic Invariance**: The same algorithm (quicksort) maps to similar
   LJPW coordinates regardless of programming language syntax.

2. **Language-Agnostic Meaning**: LJPW captures the MEANING of code,
   not just syntactic patterns.

3. **Practical Applications**:
   - Cross-language code search (find quicksort in any language)
   - Cross-language quality comparison
   - Language-independent refactoring guidance

4. **Theoretical Implications**:
   - Programming languages are different REPRESENTATIONS of same semantic meaning
   - Semantic space (LJPW) is the "true" coordinate system
   - Syntax is just surface structure, semantics is deep structure

Expected Results:
- Variance σ < 0.10 per dimension (low variability)
- Pairwise distances < 0.20 (semantically similar)
- Invariance score > 0.80 (80%+ of meaning preserved)

If these hold → LJPW captures true semantic invariants ✓
"""
    )

    # Save results
    output_file = Path(__file__).parent.parent / "results" / "cross_language_quicksort.json"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    # Verdict
    print_header("VERDICT")

    if "statistics" in results and results["statistics"]:
        variance = results["statistics"]["cross_language_variance"]
        invariance = results.get("cross_language_invariance_score", 0)

        if invariance > 0.80 and variance < 0.10:
            print("✅ HYPOTHESIS CONFIRMED")
            print("   LJPW demonstrates strong cross-language semantic invariance!")
            print("   Same meaning → Same coordinates (language-independent)")
        elif invariance > 0.60:
            print("⚠️  HYPOTHESIS PARTIALLY CONFIRMED")
            print("   LJPW shows moderate cross-language patterns")
            print("   Further refinement needed")
        else:
            print("❌ HYPOTHESIS NOT CONFIRMED")
            print("   LJPW coordinates vary significantly across languages")
            print("   May not capture language-independent semantics")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
