#!/usr/bin/env python3
"""
SCALE TEST — Push the semantic compressor to its limits.
"""

import sys
import os
import time
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ljpw.real_compressor import (
    SemanticCompressor,
    generate_lsystem,
    KNOWN_LSYSTEMS,
    CompressedData,
)


def format_bytes(n):
    """Format bytes as human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def test_lsystem_scale():
    """Push L-system compression to extreme scales."""
    print("=" * 80)
    print("L-SYSTEM SCALE TEST — PUSHING TO GIGABYTES")
    print("=" * 80)

    compressor = SemanticCompressor()

    print(f"\n{'n':>3} | {'Original':>15} | {'Compressed':>12} | {'Ratio':>15} | {'Time':>8} | {'Verified'}")
    print("-" * 80)

    lsys = KNOWN_LSYSTEMS['koch']

    for n in range(1, 16):
        # Generate
        start = time.time()
        text = generate_lsystem(lsys['axiom'], lsys['rules'], n)
        data = text.encode('utf-8')
        gen_time = time.time() - start

        # Compress
        start = time.time()
        compressed = compressor.compress(data)
        comp_time = time.time() - start

        # Decompress and verify
        start = time.time()
        decompressed = compressor.decompress(compressed)
        decomp_time = time.time() - start

        verified = decompressed == data
        ratio = compressed.ratio()

        print(f"{n:>3} | {format_bytes(len(data)):>15} | {compressed.compressed_size():>10} B | {ratio:>13,.1f}:1 | {comp_time:.2f}s | {'✓' if verified else '✗'}")

        # Stop if we're getting too big (> 500MB for memory)
        if len(data) > 500_000_000:
            print("\n[Stopping at 500MB to preserve memory]")
            break

    print()


def test_pattern_scale():
    """Test pattern compression at scale."""
    print("=" * 80)
    print("PATTERN REPEAT SCALE TEST")
    print("=" * 80)

    compressor = SemanticCompressor()

    patterns = [
        ("Simple", b"ABCD"),
        ("Sentence", b"The quick brown fox jumps over the lazy dog. "),
        ("Binary", bytes(range(256))),
        ("Unicode", "Hello, 世界! 🌍 ".encode('utf-8')),
    ]

    for pattern_name, pattern in patterns:
        print(f"\n{pattern_name} pattern ({len(pattern)} bytes):")
        print(f"{'Count':>12} | {'Original':>15} | {'Compressed':>12} | {'Ratio':>15} | {'Verified'}")
        print("-" * 70)

        for count in [100, 1_000, 10_000, 100_000, 1_000_000]:
            data = pattern * count

            compressed = compressor.compress(data)
            decompressed = compressor.decompress(compressed)

            verified = decompressed == data
            ratio = compressed.ratio()

            print(f"{count:>12,} | {format_bytes(len(data)):>15} | {compressed.compressed_size():>10} B | {ratio:>13,.1f}:1 | {'✓' if verified else '✗'}")

            if len(data) > 100_000_000:
                break


def test_sequence_scale():
    """Test mathematical sequence compression at scale."""
    print("\n" + "=" * 80)
    print("SEQUENCE SCALE TEST")
    print("=" * 80)

    compressor = SemanticCompressor()

    sequences = [
        ("Arithmetic (0, 7, 14, ...)", lambda n: list(range(0, n*7, 7))),
        ("Powers of 2", lambda n: [2**i for i in range(n)]),
        ("Fibonacci", lambda n: fibonacci(n)),
        ("Primes", lambda n: primes(n)),
    ]

    for seq_name, seq_func in sequences:
        print(f"\n{seq_name}:")
        print(f"{'Count':>12} | {'Original':>15} | {'Compressed':>12} | {'Ratio':>15} | {'Verified'}")
        print("-" * 70)

        for count in [100, 1_000, 10_000]:
            try:
                numbers = seq_func(count)
                text = ','.join(map(str, numbers))
                data = text.encode('utf-8')

                compressed = compressor.compress(data)
                decompressed = compressor.decompress(compressed)

                verified = decompressed == data
                ratio = compressed.ratio()

                print(f"{count:>12,} | {format_bytes(len(data)):>15} | {compressed.compressed_size():>10} B | {ratio:>13,.1f}:1 | {'✓' if verified else '✗'}")
            except Exception as e:
                print(f"{count:>12,} | Error: {e}")


def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]

    seq = [1, 1]
    for _ in range(n - 2):
        seq.append(seq[-1] + seq[-2])
    return seq


def primes(n):
    """Generate first n primes."""
    if n <= 0:
        return []
    result = []
    candidate = 2
    while len(result) < n:
        if all(candidate % p != 0 for p in result):
            result.append(candidate)
        candidate += 1
    return result


def test_compound_patterns():
    """Test compression of data with multiple patterns."""
    print("\n" + "=" * 80)
    print("COMPOUND PATTERN TEST")
    print("=" * 80)

    compressor = SemanticCompressor()

    # Create compound data
    tests = [
        ("Pattern A + Pattern B", (b"AAAA" * 10000) + (b"BBBB" * 10000)),
        ("Koch + Sierpinski", (generate_lsystem("F", {"F": "F+F-F-F+F"}, 5) +
                               generate_lsystem("F-G-G", {"F": "F-G+F+G-F", "G": "GG"}, 5)).encode()),
    ]

    print(f"\n{'Test':>30} | {'Original':>15} | {'Compressed':>12} | {'Ratio':>10} | {'Verified'}")
    print("-" * 80)

    for name, data in tests:
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)

        verified = decompressed == data
        ratio = compressed.ratio()

        print(f"{name:>30} | {format_bytes(len(data)):>15} | {compressed.compressed_size():>10} B | {ratio:>8,.1f}:1 | {'✓' if verified else '✗'}")


def test_extreme_scale():
    """The ultimate test — compress as large as we can go."""
    print("\n" + "=" * 80)
    print("EXTREME SCALE TEST — HOW FAR CAN WE GO?")
    print("=" * 80)

    compressor = SemanticCompressor()

    # Generate a massive L-system
    print("\nGenerating Koch L-system n=13 (this may take a moment)...")

    lsys = KNOWN_LSYSTEMS['koch']

    start = time.time()
    text = generate_lsystem(lsys['axiom'], lsys['rules'], 13)
    data = text.encode('utf-8')
    gen_time = time.time() - start

    print(f"Generated {format_bytes(len(data))} in {gen_time:.1f}s")

    # Compress
    print("Compressing...")
    start = time.time()
    compressed = compressor.compress(data)
    comp_time = time.time() - start

    print(f"Compressed to {compressed.compressed_size()} bytes in {comp_time:.2f}s")
    print(f"Ratio: {compressed.ratio():,.1f}:1")

    # Verify
    print("Verifying decompression...")
    start = time.time()
    decompressed = compressor.decompress(compressed)
    decomp_time = time.time() - start

    verified = decompressed == data
    print(f"Decompressed in {decomp_time:.1f}s")
    print(f"Verified: {'✓ MATCH' if verified else '✗ FAILED'}")

    # The money shot
    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)
    print(f"""
    Original:    {format_bytes(len(data))} ({len(data):,} bytes)
    Compressed:  {compressed.compressed_size()} bytes
    Ratio:       {compressed.ratio():,.1f}:1
    Verified:    {'✓ YES' if verified else '✗ NO'}

    Formula:     M = B × L^n × φ^(-d)
    Seed:        "{lsys['axiom']}" + rules ({compressed.compressed_size()} bytes total)
    Iterations:  13
    Expansion:   {compressed.ratio():,.1f}x
    """)
    print("=" * 80)


if __name__ == "__main__":
    test_lsystem_scale()
    test_pattern_scale()
    test_sequence_scale()
    test_compound_patterns()
    test_extreme_scale()
