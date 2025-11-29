#!/usr/bin/env python3
"""
Example 3: Compress and Decompress

This example shows:
- How to compress LJPW states into semantic genomes
- How to decompress genomes back to states
- Compression ratios achieved
- Round-trip accuracy

Run:
    python 03_compress_decompress.py
"""

import sys
from pathlib import Path

# Add parent directory to path for src module imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ljpw.ljpw_semantic_compressor import SemanticCompressor, SemanticDecompressor
from src.ljpw.ljpw_standalone import SimpleCodeAnalyzer


def main():
    print("=" * 70)
    print("LJPW Example 3: Compress and Decompress")
    print("=" * 70)
    print()

    # Sample code files to analyze
    code_samples = {
        "v1_initial.py": """
def process(data):
    return [x*2 for x in data]
""",
        "v2_typed.py": '''
def process(data: list) -> list:
    """Process data"""
    return [x*2 for x in data]
''',
        "v3_safe.py": '''
def process(data: list) -> list:
    """Process data with validation"""
    if not data:
        raise ValueError("Empty data")
    try:
        return [x*2 for x in data]
    except Exception as e:
        logging.error(f"Error: {e}")
        raise
''',
    }

    # Analyze each version
    analyzer = SimpleCodeAnalyzer()
    states = []

    print("ANALYZING CODE EVOLUTION:")
    print("-" * 70)

    for name, code in code_samples.items():
        result = analyzer.analyze(code, name)
        ljpw = result["ljpw"]
        state = (ljpw["L"], ljpw["J"], ljpw["P"], ljpw["W"])
        states.append(state)

        print(f"\n{name}:")
        print(f"  L={ljpw['L']:.3f}, J={ljpw['J']:.3f}, P={ljpw['P']:.3f}, W={ljpw['W']:.3f}")
        print(f"  Health: {result['health']*100:.1f}%")

    # Compress the trajectory
    print()
    print("COMPRESSING TRAJECTORY:")
    print("-" * 70)

    compressor = SemanticCompressor()
    genome = compressor.compress_state_sequence(
        states, metadata={"project": "example", "versions": len(states)}
    )

    # Calculate sizes
    original_size = len(str(states).encode("utf-8"))
    compressed_size = len(genome.to_string().encode("utf-8"))
    ratio = original_size / compressed_size

    print(f"\nOriginal size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {ratio:.1f}x")
    print(f"\nCompressed genome:")
    print(f"  {genome.to_string()}")

    # Decompress
    print()
    print("DECOMPRESSING GENOME:")
    print("-" * 70)

    decompressor = SemanticDecompressor()
    reconstructed = decompressor.decompress_genome(genome)

    print(f"\nReconstructed {len(reconstructed)} states")

    # Compare original vs reconstructed
    print()
    print("ACCURACY CHECK:")
    print("-" * 70)

    total_error = 0
    for i, (original, recon) in enumerate(zip(states, reconstructed)):
        error = sum((o - r) ** 2 for o, r in zip(original, recon)) ** 0.5
        total_error += error

        print(f"\nState {i+1}:")
        print(
            f"  Original:      L={original[0]:.3f}, J={original[1]:.3f}, P={original[2]:.3f}, W={original[3]:.3f}"
        )
        print(
            f"  Reconstructed: L={recon[0]:.3f}, J={recon[1]:.3f}, P={recon[2]:.3f}, W={recon[3]:.3f}"
        )
        print(f"  Error: {error:.4f}")

    avg_error = total_error / len(states)
    accuracy = (1 - avg_error) * 100

    print()
    print(f"Average reconstruction error: {avg_error:.4f}")
    print(f"Accuracy: {accuracy:.2f}%")

    # Validate genome integrity
    print()
    print("INTEGRITY VALIDATION:")
    print("-" * 70)

    validation = decompressor.validate_genome(genome)
    print(f"\nGenome valid: {validation['valid']}")
    print(f"Integrity score: {validation['integrity_score']:.1%}")
    print(f"Error count: {validation['error_count']}")

    if validation["valid"]:
        print("\n✓ Genome is intact! All checksums passed.")
    else:
        print(f"\n✗ Genome has {validation['error_count']} checksum errors")

    # Demonstrate token savings
    print()
    print("TOKEN SAVINGS (for AI):")
    print("-" * 70)

    # Estimate tokens (rough: 1 token ≈ 4 chars)
    original_tokens = sum(len(code) for code in code_samples.values()) // 4
    compressed_tokens = len(genome.to_string()) // 4

    print(f"\nSending to AI without compression:")
    print(f"  {original_tokens} tokens (full code)")
    print(f"\nSending to AI with LJPW:")
    print(f"  {compressed_tokens} tokens (genome only)")
    print(f"\nToken reduction: {(1 - compressed_tokens/original_tokens)*100:.1f}%")
    print(f"Savings: {original_tokens - compressed_tokens} tokens")

    # Demonstrate configurable precision
    print()
    print("CONFIGURABLE PRECISION:")
    print("-" * 70)
    print("\nYou can trade genome size for accuracy using quantization levels:")
    print()

    test_state = states[0]  # Use first state for comparison
    precision_levels = [
        (4, "fast"),
        (8, "balanced"),
        (16, "precise"),
        (32, "exact"),
    ]

    print(f"{'Levels':<10} {'Use Case':<12} {'Error':<12} {'Size':<10}")
    print("-" * 70)

    for levels, use_case in precision_levels:
        comp = SemanticCompressor(quantization_levels=levels)
        decomp = SemanticDecompressor(quantization_levels=levels)

        g = comp.compress_state_sequence([test_state])
        recon = decomp.decompress_genome(g)[0]

        error = sum((o - r) ** 2 for o, r in zip(test_state, recon)) ** 0.5
        size = len(g.to_string())

        print(f"{levels:<10} {use_case:<12} {error:<12.4f} {size:<10} bytes")

    print()
    print("Tip: Use LJPWQuantizer.recommend_levels('balanced') for guidance")

    print()
    print("=" * 70)
    print("KEY TAKEAWAYS:")
    print("-" * 70)
    print("1. LJPW compresses code quality to tiny genomes")
    print("2. Configurable precision: 4-64 levels for accuracy vs size trade-off")
    print("3. Enables massive token savings when working with AI")
    print("4. Built-in error correction via complementary pairing")
    print("5. Use recommend_levels() for guidance on precision settings")
    print()
    print("Next: Try running 04_interpret_scores.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
