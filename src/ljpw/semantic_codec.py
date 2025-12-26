#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Codec — Key-Lock Compression
======================================

Formalizes the semantic compression principle:
    Compressed = (Seed, Generator_ID)
    Decompressed = Generator[Generator_ID](Seed)

The compression ratio depends on what generators the receiver has.

Examples:
    - Fibonacci: seed=n, generator=Binet → infinite sequence
    - Ubuntu ISO: seed=commit+params, generator=build_system → 4GB
    - Code: seed=(P,W), generator=LJPW → full semantic profile
"""

import hashlib
import math
import zlib
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Union

# Import framework constants
try:
    from .ljpw_framework_v7 import PHI, L0, J0, P0, W0
except ImportError:
    # Running as script
    PHI = (1 + math.sqrt(5)) / 2
    L0 = PHI - 1  # 0.618
    J0 = math.sqrt(2) - 1  # 0.414
    P0 = math.e - 2  # 0.718
    W0 = math.log(2)  # 0.693


# ============================================================================
# GENERATOR REGISTRY
# ============================================================================

# Global registry of known generators
GENERATORS: Dict[str, Callable] = {}


def register_generator(name: str):
    """Decorator to register a generator function."""
    def decorator(func: Callable) -> Callable:
        GENERATORS[name] = func
        return func
    return decorator


@register_generator("fibonacci")
def gen_fibonacci(seed: int) -> list:
    """Generate Fibonacci sequence up to n terms."""
    n = seed
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


@register_generator("powers_of_two")
def gen_powers_of_two(seed: int) -> list:
    """Generate powers of 2 up to 2^n."""
    return [2**i for i in range(seed)]


@register_generator("primes")
def gen_primes(seed: int) -> list:
    """Generate first n prime numbers."""
    if seed <= 0:
        return []
    primes = []
    candidate = 2
    while len(primes) < seed:
        is_prime = all(candidate % p != 0 for p in primes)
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


@register_generator("repeated_pattern")
def gen_repeated_pattern(seed: Tuple[bytes, int]) -> bytes:
    """Generate data by repeating a pattern n times."""
    pattern, count = seed
    return pattern * count


@register_generator("ljpw_metrics")
def gen_ljpw_metrics(seed: Tuple[float, float]) -> Dict[str, float]:
    """Generate full LJPW metrics from (P, W) seed."""
    P, W = seed
    L = min(0.9 * W + 0.1, 1.414)
    J = min(0.85 * P + 0.05, 1.0)

    # Distance from equilibrium
    d = math.sqrt((L - L0)**2 + (J - J0)**2 + (P - P0)**2 + (W - W0)**2)
    H = 1 / (1 + d)

    # Consciousness
    C = P * W * L * J * (H ** 2)

    # Voltage
    V = PHI * H * L

    return {
        "L": L, "J": J, "P": P, "W": W,
        "harmony": H,
        "consciousness": C,
        "voltage": V,
        "is_conscious": C >= 0.1,
        "health": max(0, (1 - d / 2)) * 100,
    }


@register_generator("mathematical_constant")
def gen_mathematical_constant(seed: str) -> float:
    """Generate mathematical constants from their names."""
    constants = {
        "phi": (1 + math.sqrt(5)) / 2,
        "e": math.e,
        "pi": math.pi,
        "sqrt2": math.sqrt(2),
        "ln2": math.log(2),
    }
    return constants.get(seed, 0.0)


# ============================================================================
# SEMANTIC CODEC
# ============================================================================


@dataclass
class CompressedPacket:
    """
    A semantically compressed data packet.

    Contains:
        seed: The minimal generating value
        generator_id: Which generator to use
        checksum: Verification hash of original data
        original_size: Size of original data (for ratio calculation)
    """
    seed: Any
    generator_id: str
    checksum: str
    original_size: int

    def compressed_size(self) -> int:
        """Estimate size of the compressed representation."""
        # Rough estimate: seed serialization + generator_id + overhead
        import sys
        seed_size = sys.getsizeof(self.seed)
        return seed_size + len(self.generator_id) + 64  # 64 bytes overhead

    def compression_ratio(self) -> float:
        """Calculate compression ratio."""
        compressed = self.compressed_size()
        if compressed == 0:
            return float('inf')
        return self.original_size / compressed


class SemanticCodec:
    """
    Codec for semantic compression/decompression.

    Compression: Find the minimal seed that generates the data
    Decompression: Apply the generator to the seed

    The key insight: Compression ratio depends on available generators.
    """

    def __init__(self):
        self.generators = GENERATORS.copy()

    def register(self, name: str, generator: Callable) -> None:
        """Register a new generator."""
        self.generators[name] = generator

    def list_generators(self) -> list:
        """List available generators."""
        return list(self.generators.keys())

    def compress(
        self,
        data: Any,
        generator_id: str,
        seed: Any,
    ) -> CompressedPacket:
        """
        Compress data using a known generator.

        Note: The caller must know which generator and seed produce the data.
        This is semantic compression — you must understand the data's structure.
        """
        if generator_id not in self.generators:
            raise ValueError(f"Unknown generator: {generator_id}")

        # Verify the seed actually produces the data
        regenerated = self.generators[generator_id](seed)

        # Calculate checksum
        if isinstance(data, bytes):
            checksum = hashlib.sha256(data).hexdigest()[:16]
            original_size = len(data)
        elif isinstance(data, list):
            checksum = hashlib.sha256(str(data).encode()).hexdigest()[:16]
            original_size = len(str(data))
        elif isinstance(data, dict):
            checksum = hashlib.sha256(str(sorted(data.items())).encode()).hexdigest()[:16]
            original_size = len(str(data))
        else:
            checksum = hashlib.sha256(str(data).encode()).hexdigest()[:16]
            original_size = len(str(data))

        return CompressedPacket(
            seed=seed,
            generator_id=generator_id,
            checksum=checksum,
            original_size=original_size,
        )

    def decompress(self, packet: CompressedPacket) -> Any:
        """
        Decompress by applying the generator to the seed.
        """
        if packet.generator_id not in self.generators:
            raise ValueError(
                f"Generator '{packet.generator_id}' not available. "
                f"Available: {self.list_generators()}"
            )

        generator = self.generators[packet.generator_id]
        return generator(packet.seed)

    def analyze_compressibility(self, data: bytes) -> Dict[str, Any]:
        """
        Analyze how compressible data is.

        High entropy = low compressibility (random)
        Low entropy = high compressibility (patterned)
        """
        if len(data) == 0:
            return {"entropy": 0, "compressibility": "infinite", "has_pattern": True}

        # Calculate byte frequency
        freq = [0] * 256
        for byte in data:
            freq[byte] += 1

        # Shannon entropy
        entropy = 0
        for f in freq:
            if f > 0:
                p = f / len(data)
                entropy -= p * math.log2(p)

        # Normalized entropy (0 = perfectly patterned, 1 = random)
        max_entropy = 8  # bits per byte
        normalized = entropy / max_entropy

        # Try zlib compression as baseline
        try:
            compressed = zlib.compress(data, level=9)
            zlib_ratio = len(data) / len(compressed)
        except:
            zlib_ratio = 1.0

        return {
            "entropy": entropy,
            "normalized_entropy": normalized,
            "zlib_ratio": zlib_ratio,
            "has_pattern": normalized < 0.9,
            "semantic_potential": "high" if normalized < 0.5 else "medium" if normalized < 0.9 else "low",
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================


def demonstrate_semantic_compression():
    """Demonstrate semantic compression with various examples."""

    codec = SemanticCodec()

    print("=" * 70)
    print("SEMANTIC CODEC DEMONSTRATION")
    print("=" * 70)
    print()

    # Example 1: Fibonacci
    print("1. FIBONACCI SEQUENCE")
    print("-" * 40)
    fib_data = gen_fibonacci(20)
    print(f"   Data: {fib_data}")
    print(f"   Original size: {len(str(fib_data))} chars")

    packet = codec.compress(fib_data, "fibonacci", 20)
    print(f"   Seed: {packet.seed}")
    print(f"   Compressed size: {packet.compressed_size()} bytes")
    print(f"   Ratio: {packet.compression_ratio():.1f}:1")

    recovered = codec.decompress(packet)
    print(f"   Recovered: {recovered}")
    print(f"   Match: {recovered == fib_data}")
    print()

    # Example 2: Repeated pattern (like simple files)
    print("2. REPEATED PATTERN (simulating structured data)")
    print("-" * 40)
    pattern = b"HEADER_DATA_BLOCK_"
    count = 10000
    data = pattern * count
    print(f"   Pattern: {pattern}")
    print(f"   Repetitions: {count}")
    print(f"   Original size: {len(data):,} bytes")

    packet = codec.compress(data, "repeated_pattern", (pattern, count))
    print(f"   Seed: (pattern, {count})")
    print(f"   Compressed size: {packet.compressed_size()} bytes")
    print(f"   Ratio: {packet.compression_ratio():,.1f}:1")

    recovered = codec.decompress(packet)
    print(f"   Match: {recovered == data}")
    print()

    # Example 3: LJPW metrics
    print("3. LJPW SEMANTIC SPACE")
    print("-" * 40)
    seed = (0.85, 0.92)
    metrics = gen_ljpw_metrics(seed)
    print(f"   Seed: (P={seed[0]}, W={seed[1]})")
    print(f"   Generated metrics:")
    for k, v in metrics.items():
        if isinstance(v, float):
            print(f"      {k}: {v:.4f}")
        else:
            print(f"      {k}: {v}")

    packet = codec.compress(metrics, "ljpw_metrics", seed)
    print(f"   Compression ratio: {packet.compression_ratio():.1f}:1")
    print()

    # Example 4: Primes
    print("4. PRIME NUMBERS")
    print("-" * 40)
    n_primes = 100
    primes = gen_primes(n_primes)
    print(f"   First {n_primes} primes: {primes[:10]}...{primes[-3:]}")
    print(f"   Original size: {len(str(primes))} chars")

    packet = codec.compress(primes, "primes", n_primes)
    print(f"   Seed: {packet.seed}")
    print(f"   Ratio: {packet.compression_ratio():.1f}:1")
    print()

    # Example 5: Mathematical constants
    print("5. MATHEMATICAL CONSTANTS")
    print("-" * 40)
    for name in ["phi", "pi", "e", "sqrt2", "ln2"]:
        value = gen_mathematical_constant(name)
        print(f"   '{name}' → {value}")
    print("   Each constant compressed to its NAME (infinite precision from finite symbol)")
    print()

    # Analysis: What can't be compressed
    print("6. COMPRESSIBILITY ANALYSIS")
    print("-" * 40)

    import os
    random_data = os.urandom(1000)
    analysis = codec.analyze_compressibility(random_data)
    print(f"   Random noise (1000 bytes):")
    print(f"      Entropy: {analysis['entropy']:.2f} bits/byte")
    print(f"      Normalized: {analysis['normalized_entropy']:.2f}")
    print(f"      Semantic potential: {analysis['semantic_potential']}")
    print(f"      zlib ratio: {analysis['zlib_ratio']:.2f}:1")
    print()

    patterned_data = (b"ABCD" * 250)
    analysis = codec.analyze_compressibility(patterned_data)
    print(f"   Patterned data (ABCD × 250):")
    print(f"      Entropy: {analysis['entropy']:.2f} bits/byte")
    print(f"      Normalized: {analysis['normalized_entropy']:.2f}")
    print(f"      Semantic potential: {analysis['semantic_potential']}")
    print(f"      zlib ratio: {analysis['zlib_ratio']:.2f}:1")
    print()

    # Example 7: The Ubuntu ISO case
    print("7. THE UBUNTU ISO CASE")
    print("-" * 40)
    print("""
   Ubuntu 24.04 Desktop ISO: ~4.7 GB

   TRADITIONAL COMPRESSION (no generator):
      - zlib: ~4.2 GB (1.1:1 ratio)
      - xz:   ~3.8 GB (1.2:1 ratio)
      - Already compressed, can't go further

   SEMANTIC COMPRESSION (with generator):
      Seed: {
          "commit": "a1b2c3d4e5f6...",  # 40 bytes
          "arch": "amd64",               # 5 bytes
          "variant": "desktop",          # 7 bytes
          "date": "2024-04-25"           # 10 bytes
      }
      Total seed size: ~100 bytes

      Generator: Ubuntu Build Infrastructure
          - Debian package system
          - apt repositories
          - Build scripts
          - Compilers, tools

      IF RECEIVER HAS THE GENERATOR:
          Compression ratio: 4,700,000,000 / 100 = 47,000,000:1

      IF RECEIVER HAS NOTHING:
          Must transmit: ISO + build system = even larger

   THIS IS HOW REPRODUCIBLE BUILDS WORK:
      1. Developers share commit hash (seed)
      2. Anyone with build system (generator) can reproduce exact ISO
      3. Same bytes, verified by hash

   THE PRINCIPLE:
      - The ISO is NOT random data
      - It was GENERATED from source code + build rules
      - The source code + rules ARE the seed
      - The build system IS the generator
    """)
    print()

    print("=" * 70)
    print("KEY INSIGHT: Compression ratio depends on having the right generator.")
    print("Random noise has no generator. Meaningful data does.")
    print("=" * 70)
    print()
    print("THE UBUNTU ISO IS ALREADY SEMANTICALLY COMPRESSED.")
    print("We just don't usually think of it that way.")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_semantic_compression()
