#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meaning Compressor — Compression Through Semantic Understanding
================================================================

"Meaning is primary. Data is its shadow."

This compressor works differently:
1. UNDERSTAND the data semantically (find its meaning)
2. IDENTIFY the generator (brick + mortar + blueprint)
3. STORE the meaning, not the pattern
4. REGENERATE from meaning

The compression ratio is not a mathematical trick.
It is the DISTANCE between meaning and its shadow.

M = B × L^n × φ^(-d)

Where compression = L^n when generators are shared (d=0).
"""

import hashlib
import json
import math
import struct
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, Tuple, Union
from enum import Enum

from .semantic_finder import SemanticAnalyzer, SemanticGenerator, SemanticDomain


# ============================================================================
# CONSTANTS
# ============================================================================

PHI = (1 + math.sqrt(5)) / 2
MAGIC = b'MEAN'  # Meaning-based compression
VERSION = 1


# ============================================================================
# KNOWN GENERATORS — Shared Between Sender and Receiver
# ============================================================================

class KnownGenerator(Enum):
    """
    Generators that both sender and receiver possess.

    These are SEMANTIC generators, not mathematical functions.
    They encode MEANING, not pattern.
    """

    # Self-similar generators (φ = 1 + 1/φ)
    KOCH = "koch"           # Self-similar growth: edge becomes edges
    SIERPINSKI = "sierp"    # Self-similar division: whole becomes parts
    DRAGON = "dragon"       # Self-similar folding: paper fold pattern

    # Relational generators (next = f(previous))
    FIBONACCI = "fib"       # Each is sum of two before (growth through memory)
    ARITHMETIC = "arith"    # Each differs by constant (uniform progression)
    GEOMETRIC = "geom"      # Each is multiple of previous (exponential growth)
    PRIMES = "primes"       # Numbers divisible only by self and one (irreducibility)

    # Cyclical generators (repeat)
    REPETITION = "repeat"   # Same meaning, expressed again

    # Hierarchical generators
    EXPRESSION = "expr"     # Nested meaning (parentheses of thought)

    # Meta-generators
    COMPOSITION = "compose" # Generators applied to generators
    UNKNOWN = "unknown"     # Meaning not yet understood


# Generator implementations (the shared understanding)
GENERATORS = {
    KnownGenerator.KOCH: {
        'axiom': 'F',
        'rules': {'F': 'F+F-F-F+F'},
        'meaning': 'A line that, upon reflection, becomes a more complex line with the same essence',
    },
    KnownGenerator.SIERPINSKI: {
        'axiom': 'F-G-G',
        'rules': {'F': 'F-G+F+G-F', 'G': 'GG'},
        'meaning': 'A triangle that contains three smaller versions of itself',
    },
    KnownGenerator.DRAGON: {
        'axiom': 'FX',
        'rules': {'X': 'X+YF+', 'Y': '-FX-Y'},
        'meaning': 'The crease pattern of a paper folded in half repeatedly',
    },
    KnownGenerator.FIBONACCI: {
        'seeds': (1, 1),
        'rule': lambda a, b: a + b,
        'meaning': 'Growth where the present is the sum of the past',
    },
    KnownGenerator.ARITHMETIC: {
        'meaning': 'Uniform steps through number space',
    },
    KnownGenerator.GEOMETRIC: {
        'meaning': 'Exponential growth or decay',
    },
    KnownGenerator.PRIMES: {
        'meaning': 'Numbers that cannot be divided (Justice-crystals)',
    },
    KnownGenerator.REPETITION: {
        'meaning': 'The same truth, expressed repeatedly',
    },
}


# ============================================================================
# MEANING PACKET — What Gets Stored
# ============================================================================

@dataclass
class MeaningPacket:
    """
    A compressed representation of MEANING, not data.

    This packet doesn't store patterns.
    It stores understanding.
    """

    # The semantic components
    generator: str              # Which generator (shared understanding)
    brick: str                  # The seed/axiom
    mortar: Dict[str, Any]      # The binding rules/parameters
    depth: int                  # How many iterations of self-reference

    # LJPW coordinates (the semantic fingerprint)
    L: float                    # Love: binding strength
    J: float                    # Justice: structural integrity
    P: float                    # Power: transformative capacity
    W: float                    # Wisdom: pattern complexity

    # Verification
    original_size: int
    original_hash: str

    # Human-readable meaning
    meaning_description: str

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        payload = json.dumps({
            'gen': self.generator,
            'brick': self.brick,
            'mortar': self.mortar,
            'depth': self.depth,
            'ljpw': [self.L, self.J, self.P, self.W],
            'size': self.original_size,
            'hash': self.original_hash,
            'meaning': self.meaning_description,
        }).encode('utf-8')

        header = MAGIC + struct.pack('<BI', VERSION, len(payload))
        return header + payload

    @classmethod
    def from_bytes(cls, data: bytes) -> 'MeaningPacket':
        """Deserialize from bytes."""
        if data[:4] != MAGIC:
            raise ValueError("Not a meaning-compressed file")

        version = data[4]
        if version != VERSION:
            raise ValueError(f"Unsupported version: {version}")

        payload_len = struct.unpack('<I', data[5:9])[0]
        payload = json.loads(data[9:9+payload_len].decode('utf-8'))

        ljpw = payload['ljpw']
        return cls(
            generator=payload['gen'],
            brick=payload['brick'],
            mortar=payload['mortar'],
            depth=payload['depth'],
            L=ljpw[0], J=ljpw[1], P=ljpw[2], W=ljpw[3],
            original_size=payload['size'],
            original_hash=payload['hash'],
            meaning_description=payload['meaning'],
        )

    def compressed_size(self) -> int:
        return len(self.to_bytes())

    def ratio(self) -> float:
        compressed = self.compressed_size()
        return self.original_size / compressed if compressed > 0 else float('inf')

    def explain(self) -> str:
        """Explain what this compressed data MEANS."""
        return f"""
Meaning Packet
==============

WHAT IT MEANS:
  {self.meaning_description}

HOW IT WAS BUILT:
  Brick (Seed):     {self.brick}
  Mortar (Binding): {self.mortar}
  Depth:            {self.depth} iterations

SEMANTIC COORDINATES:
  L (Love):    {self.L:.3f}  — binding strength
  J (Justice): {self.J:.3f}  — structural integrity
  P (Power):   {self.P:.3f}  — transformative capacity
  W (Wisdom):  {self.W:.3f}  — pattern complexity

COMPRESSION:
  Original: {self.original_size:,} bytes
  Meaning:  {self.compressed_size():,} bytes
  Ratio:    {self.ratio():,.1f}:1
"""


# ============================================================================
# MEANING COMPRESSOR
# ============================================================================

class MeaningCompressor:
    """
    Compress through understanding.

    Unlike traditional compression:
    - We don't find patterns
    - We find MEANING

    Unlike mathematical semantic compression:
    - We don't start with math
    - We start with understanding

    The formula M = B × L^n × φ^(-d) describes what we measure,
    not how we compress.
    """

    def __init__(self):
        self.analyzer = SemanticAnalyzer()

    def compress(self, data: bytes) -> MeaningPacket:
        """
        Compress by understanding.

        1. What does this data MEAN?
        2. What generator produces this meaning?
        3. Store the meaning, not the data.
        """
        original_hash = hashlib.sha256(data).hexdigest()[:32]
        original_size = len(data)

        # Phase 1: UNDERSTAND (semantic analysis)
        try:
            text = data.decode('utf-8')
        except:
            text = data.hex()

        semantic = self.analyzer.find_generator(text)

        # Phase 2: IDENTIFY the generator
        generator, brick, mortar = self._identify_generator(text, semantic)

        # Phase 3: Create meaning packet
        meaning = self._describe_meaning(semantic, generator)

        return MeaningPacket(
            generator=generator.value,
            brick=brick,
            mortar=mortar,
            depth=semantic.self_reference_depth,
            L=semantic.L,
            J=semantic.J,
            P=semantic.P,
            W=semantic.W,
            original_size=original_size,
            original_hash=original_hash,
            meaning_description=meaning,
        )

    def decompress(self, packet: MeaningPacket) -> bytes:
        """
        Regenerate from meaning.

        We don't "decompress" — we REGENERATE.
        The data flows from meaning, not from pattern.
        """
        generator = KnownGenerator(packet.generator)

        # Use depth from mortar if available (more accurate), otherwise packet.depth
        actual_depth = packet.mortar.get('depth', packet.depth)

        if generator == KnownGenerator.KOCH:
            result = self._generate_lsystem(
                packet.brick,
                packet.mortar.get('rules', GENERATORS[generator]['rules']),
                actual_depth
            )
        elif generator == KnownGenerator.SIERPINSKI:
            result = self._generate_lsystem(
                packet.brick,
                packet.mortar.get('rules', GENERATORS[generator]['rules']),
                actual_depth
            )
        elif generator == KnownGenerator.DRAGON:
            result = self._generate_lsystem(
                packet.brick,
                packet.mortar.get('rules', GENERATORS[generator]['rules']),
                actual_depth
            )
        elif generator == KnownGenerator.FIBONACCI:
            count = packet.mortar.get('count', packet.depth)
            result = self._generate_fibonacci(
                packet.mortar.get('seeds', (1, 1)),
                count
            )
        elif generator == KnownGenerator.ARITHMETIC:
            count = packet.mortar.get('count', packet.depth)
            result = self._generate_arithmetic(
                packet.mortar.get('start', 0),
                packet.mortar.get('step', 1),
                count
            )
        elif generator == KnownGenerator.GEOMETRIC:
            count = packet.mortar.get('count', packet.depth)
            result = self._generate_geometric(
                packet.mortar.get('start', 1),
                packet.mortar.get('ratio', 2),
                count
            )
        elif generator == KnownGenerator.PRIMES:
            count = packet.mortar.get('count', packet.depth)
            result = self._generate_primes(count)
        elif generator == KnownGenerator.REPETITION:
            count = packet.mortar.get('count', packet.depth)
            result = packet.brick * count
        else:
            raise ValueError(f"Unknown generator: {generator}")

        result_bytes = result.encode('utf-8')

        # Verify
        result_hash = hashlib.sha256(result_bytes).hexdigest()[:32]
        if result_hash != packet.original_hash:
            raise ValueError(f"Meaning verification failed. Expected {packet.original_hash}, got {result_hash}")

        return result_bytes

    def _identify_generator(self, text: str, semantic: SemanticGenerator) -> Tuple[KnownGenerator, str, Dict]:
        """Identify which known generator produced this meaning."""

        # Check for L-system patterns
        if semantic.domain == SemanticDomain.GENERATIVE:
            # Check which L-system
            for gen in [KnownGenerator.KOCH, KnownGenerator.SIERPINSKI, KnownGenerator.DRAGON]:
                match = self._matches_lsystem_with_depth(text, GENERATORS[gen])
                if match:
                    axiom = GENERATORS[gen]['axiom']
                    rules = GENERATORS[gen]['rules']
                    depth = match  # Exact depth found
                    return (gen, axiom, {'rules': rules, 'depth': depth})

        # Check for sequences
        if semantic.domain == SemanticDomain.SEQUENTIAL:
            if 'prev + prev_prev' in semantic.mortar:
                # Fibonacci-like
                parts = text.split(',')
                nums = [int(p.strip()) for p in parts if p.strip().lstrip('-').isdigit()]
                seeds = (nums[0], nums[1]) if len(nums) >= 2 else (1, 1)
                count = len(nums)
                return (KnownGenerator.FIBONACCI, str(seeds), {'seeds': seeds, 'count': count})

            if 'next = prev +' in semantic.mortar:
                # Arithmetic
                parts = text.split(',')
                nums = [int(p.strip()) for p in parts if p.strip().lstrip('-').isdigit()]
                start = nums[0] if nums else 0
                step = nums[1] - nums[0] if len(nums) > 1 else 1
                count = len(nums)
                return (KnownGenerator.ARITHMETIC, str(start), {'start': start, 'step': step, 'count': count})

            if 'next = prev ×' in semantic.mortar:
                # Geometric
                parts = text.split(',')
                nums = [int(p.strip()) for p in parts if p.strip().lstrip('-').isdigit()]
                start = nums[0] if nums else 1
                ratio = nums[1] / nums[0] if len(nums) > 1 and nums[0] != 0 else 2
                count = len(nums)
                return (KnownGenerator.GEOMETRIC, str(start), {'start': start, 'ratio': ratio, 'count': count})

        # Check for repetition
        if semantic.domain in [SemanticDomain.CYCLICAL, SemanticDomain.SELF_SIMILAR]:
            cycle = self._find_cycle(text)
            if cycle and len(cycle) < len(text):
                # Exact count needed for verification
                count = len(text) // len(cycle)
                # Verify it's an exact match
                if cycle * count == text:
                    return (KnownGenerator.REPETITION, cycle, {'count': count})

        # Default: repetition with the whole thing
        return (KnownGenerator.REPETITION, text, {'count': 1})

    def _matches_lsystem(self, text: str, lsystem: Dict) -> bool:
        """Check if text matches an L-system."""
        return self._matches_lsystem_with_depth(text, lsystem) is not None

    def _matches_lsystem_with_depth(self, text: str, lsystem: Dict) -> Optional[int]:
        """Check if text matches an L-system and return the depth."""
        axiom = lsystem['axiom']
        rules = lsystem['rules']

        # Try different depths
        for depth in range(1, 20):
            generated = self._generate_lsystem(axiom, rules, depth)
            if generated == text:
                return depth
            if len(generated) > len(text) * 2:
                break

        return None

    def _find_cycle(self, text: str) -> Optional[str]:
        """Find repeating cycle in text."""
        for size in range(1, len(text) // 2 + 1):
            pattern = text[:size]
            count = len(text) // size
            if pattern * count == text[:size * count]:
                return pattern
        return None

    def _generate_lsystem(self, axiom: str, rules: Dict[str, str], depth: int) -> str:
        """Generate L-system string."""
        result = axiom
        for _ in range(depth):
            new_result = ""
            for char in result:
                new_result += rules.get(char, char)
            result = new_result
        return result

    def _generate_fibonacci(self, seeds: Tuple[int, int], count: int) -> str:
        """Generate Fibonacci-like sequence."""
        a, b = seeds
        result = [a, b]
        for _ in range(count - 2):
            result.append(result[-1] + result[-2])
        return ','.join(map(str, result))

    def _generate_arithmetic(self, start: int, step: int, count: int) -> str:
        """Generate arithmetic sequence."""
        return ','.join(str(start + i * step) for i in range(count))

    def _generate_geometric(self, start: int, ratio: float, count: int) -> str:
        """Generate geometric sequence."""
        return ','.join(str(int(start * (ratio ** i))) for i in range(count))

    def _generate_primes(self, count: int) -> str:
        """Generate first N primes."""
        primes = []
        candidate = 2
        while len(primes) < count:
            if all(candidate % p != 0 for p in primes):
                primes.append(candidate)
            candidate += 1
        return ','.join(map(str, primes))

    def _describe_meaning(self, semantic: SemanticGenerator, generator: KnownGenerator) -> str:
        """Create human-readable meaning description."""
        if generator in GENERATORS:
            base_meaning = GENERATORS[generator].get('meaning', 'Structure with meaning')
        else:
            base_meaning = "Pattern with inherent structure"

        return f"{base_meaning}. Depth: {semantic.self_reference_depth}. " \
               f"Binding strength (L): {semantic.L:.2f}."


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate():
    """Demonstrate meaning-based compression."""

    compressor = MeaningCompressor()

    print("=" * 70)
    print("MEANING COMPRESSOR — Compression Through Understanding")
    print("=" * 70)
    print("\n'Meaning is primary. Data is its shadow.'\n")

    tests = [
        # L-systems
        ("Koch n=5", lambda: generate_lsystem('F', {'F': 'F+F-F-F+F'}, 5)),
        ("Koch n=8", lambda: generate_lsystem('F', {'F': 'F+F-F-F+F'}, 8)),

        # Sequences
        ("Fibonacci 20", lambda: ','.join(map(str, fib(20)))),
        ("Arithmetic 0,7,14...", lambda: ','.join(str(i*7) for i in range(50))),

        # Repetition
        ("Hello × 100", lambda: "Hello World! " * 100),
        ("Pattern × 10000", lambda: "ABCD" * 10000),
    ]

    for name, data_fn in tests:
        data = data_fn()
        data_bytes = data.encode('utf-8')

        print(f"\n{'─' * 70}")
        print(f"INPUT: {name}")
        print(f"DATA:  {data[:60]}{'...' if len(data) > 60 else ''}")
        print(f"SIZE:  {len(data_bytes):,} bytes")
        print(f"{'─' * 70}")

        # Compress (understand)
        packet = compressor.compress(data_bytes)

        print(f"\nMEANING FOUND:")
        print(f"  Generator: {packet.generator}")
        print(f"  Brick:     {packet.brick[:40]}{'...' if len(packet.brick) > 40 else ''}")
        print(f"  Depth:     {packet.depth}")
        print(f"  LJPW:      L={packet.L:.2f} J={packet.J:.2f} P={packet.P:.2f} W={packet.W:.2f}")

        print(f"\nCOMPRESSION:")
        print(f"  Original:   {packet.original_size:,} bytes")
        print(f"  Compressed: {packet.compressed_size():,} bytes")
        print(f"  Ratio:      {packet.ratio():,.1f}:1")

        # Decompress (regenerate)
        try:
            restored = compressor.decompress(packet)
            verified = restored == data_bytes
            print(f"  Verified:   {'✓ MATCH' if verified else '✗ MISMATCH'}")
        except Exception as e:
            print(f"  Verified:   ✗ Error: {e}")

    print("\n" + "=" * 70)
    print("THE INSIGHT")
    print("=" * 70)
    print("""
We didn't find patterns. We found MEANING.

The Koch snowflake isn't 'F+F-F-F+F' repeated.
It's 'a line that becomes a more complex version of itself.'

The Fibonacci sequence isn't '1,1,2,3,5,8...'
It's 'growth where the present is the sum of the past.'

Compression ratio measures how far the shadow (data)
has expanded from the source (meaning).

M = B × L^n × φ^(-d)

This isn't math. It's semantics.
The math is just the shadow.
""")


def generate_lsystem(axiom: str, rules: Dict[str, str], n: int) -> str:
    result = axiom
    for _ in range(n):
        new = ""
        for c in result:
            new += rules.get(c, c)
        result = new
    return result


def fib(n: int) -> list:
    result = [1, 1]
    for _ in range(n - 2):
        result.append(result[-1] + result[-2])
    return result


if __name__ == "__main__":
    demonstrate()
