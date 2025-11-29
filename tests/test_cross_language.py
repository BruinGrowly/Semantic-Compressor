#!/usr/bin/env python3
"""
Test Cross-Language Genome Consistency

Hypothesis: The same semantic meaning in different languages
should produce identical (or very similar) genomes.

This tests whether LJPW captures language-independent meaning.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ljpw"))
from ljpw_standalone import analyze_quick, calculate_distance

# ============================================================================
# TEST CASES: Same Semantic Meaning, Different Languages
# ============================================================================

# Test 1: Simple addition function
python_add = """
def add(a, b):
    return a + b
"""

javascript_add = """
function add(a, b) {
    return a + b;
}
"""

rust_add = """
fn add(a: i32, b: i32) -> i32 {
    a + b
}
"""

cpp_add = """
int add(int a, int b) {
    return a + b;
}
"""

go_add = """
func add(a int, b int) int {
    return a + b
}
"""

ruby_add = """
def add(a, b)
  a + b
end
"""

swift_add = """
func add(_ a: Int, _ b: Int) -> Int {
    return a + b
}
"""

kotlin_add = """
fun add(a: Int, b: Int): Int {
    return a + b
}
"""

# Test 2: Input validation
python_validate = """
def validate(data):
    if not data:
        raise ValueError("Required")
    if not isinstance(data, dict):
        raise TypeError("Must be dict")
    return data
"""

javascript_validate = """
function validate(data) {
    if (!data) {
        throw new Error("Required");
    }
    if (typeof data !== 'object') {
        throw new TypeError("Must be object");
    }
    return data;
}
"""

typescript_validate = """
function validate(data: any): object {
    if (!data) {
        throw new Error("Required");
    }
    if (typeof data !== 'object') {
        throw new TypeError("Must be object");
    }
    return data;
}
"""

# Test 3: Class with methods
python_class = """
class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, x):
        self.result += x
        return self.result
"""

javascript_class = """
class Calculator {
    constructor() {
        this.result = 0;
    }

    add(x) {
        this.result += x;
        return this.result;
    }
}
"""

java_class = """
public class Calculator {
    private int result = 0;

    public int add(int x) {
        result += x;
        return result;
    }
}
"""

# ============================================================================
# RUN TESTS
# ============================================================================


def test_cross_language():
    print("\n" + "=" * 70)
    print("CROSS-LANGUAGE SEMANTIC CONSISTENCY TEST")
    print("=" * 70)
    print("\nHypothesis: Same meaning → Similar genome (regardless of language)")
    print()

    test_cases = [
        (
            "Simple Addition",
            [
                ("Python", python_add),
                ("JavaScript", javascript_add),
                ("Rust", rust_add),
                ("C++", cpp_add),
                ("Go", go_add),
                ("Ruby", ruby_add),
                ("Swift", swift_add),
                ("Kotlin", kotlin_add),
            ],
        ),
        (
            "Input Validation",
            [
                ("Python", python_validate),
                ("JavaScript", javascript_validate),
                ("TypeScript", typescript_validate),
            ],
        ),
        (
            "Class/OOP",
            [("Python", python_class), ("JavaScript", javascript_class), ("Java", java_class)],
        ),
    ]

    for test_name, cases in test_cases:
        print(f"\n{'─' * 70}")
        print(f"Test: {test_name}")
        print("─" * 70)

        results = []
        for lang, code in cases:
            result = analyze_quick(code)
            results.append((lang, result))

            L = result["ljpw"]["L"]
            J = result["ljpw"]["J"]
            P = result["ljpw"]["P"]
            W = result["ljpw"]["W"]

            # Create genome from coordinates (quantize to 0-9)
            L_digit = int(round(L * 10)) % 10
            J_digit = int(round(J * 10)) % 10
            P_digit = int(round(P * 10)) % 10
            W_digit = int(round(W * 10)) % 10
            genome = f"L{L_digit}J{J_digit}P{P_digit}W{W_digit}"

            print(f"\n{lang}:")
            print(f"  Genome: {genome}")
            print(f"  Coords: L={L:.2f}, J={J:.2f}, P={P:.2f}, W={W:.2f}")

        # Calculate pairwise distances
        print(f"\nPairwise Semantic Distances:")
        n = len(results)
        for i in range(n):
            for j in range(i + 1, n):
                lang1, r1 = results[i]
                lang2, r2 = results[j]

                coords1 = (r1["ljpw"]["L"], r1["ljpw"]["J"], r1["ljpw"]["P"], r1["ljpw"]["W"])
                coords2 = (r2["ljpw"]["L"], r2["ljpw"]["J"], r2["ljpw"]["P"], r2["ljpw"]["W"])

                distance = calculate_distance(coords1, coords2)

                print(f"  {lang1} ↔ {lang2}: {distance:.3f}", end="")

                if distance < 0.3:
                    print("  ✓ Very similar (hypothesis confirmed)")
                elif distance < 0.6:
                    print("  ≈ Moderately similar")
                else:
                    print("  ✗ Different (hypothesis challenged)")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print(
        """
If distances are consistently low (<0.3), this provides evidence that:

1. LJPW captures language-independent semantic meaning
2. Syntax is merely the surface rendering of deeper 4D position
3. The framework operates at a fundamental level beyond code structure

This would support the "Medium" or "Deep" interpretation in
SEMANTIC_COMPRESSION_DEEP_MECHANICS.md
    """
    )
    print("=" * 70 + "\n")


if __name__ == "__main__":
    test_cross_language()
