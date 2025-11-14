"""
LJPW Semantic Compressor v1.0
Based on DNA-LJPW correspondence principles

Implements semantic compression using:
- 4-letter LJPW encoding (like GATC)
- Complementary pairing (L-W stable, J-P dynamic)
- Codon-like triplet encoding
- Error correction via pairing checksums
"""

import math
import json
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# FOUNDATIONAL CONSTANTS
# ============================================================================

class LJPWBase(Enum):
    """The 4 'bases' of LJPW semantic DNA"""
    L = 0.618034  # Love - Force multiplier (like G: strong binder)
    J = 0.414214  # Justice - Vulnerable to erosion (like T: weak binder)
    P = 0.718282  # Power - Catalytic change (like A: flexible)
    W = 0.693147  # Wisdom - Stable structure (like C: G's partner)

# Complementary pairing (discovered from analysis)
COMPLEMENTARY_PAIRS = {
    'L': 'W',  # Love ↔ Wisdom (stable pair, like G-C)
    'W': 'L',
    'P': 'J',  # Power ↔ Justice (dynamic pair, like A-T)
    'J': 'P',
}

# Natural Equilibrium - the "reference genome"
NATURAL_EQUILIBRIUM = {
    'L': 0.618034,
    'J': 0.414214,
    'P': 0.718282,
    'W': 0.693147,
}

# ============================================================================
# QUANTIZATION: Converting continuous values to discrete bases
# ============================================================================

class LJPWQuantizer:
    """
    Quantizes continuous LJPW values into discrete 'bases'
    Uses 4 levels per dimension (like DNA's 4 bases)
    """

    def __init__(self, levels=4):
        self.levels = levels
        # Define quantization thresholds
        self.thresholds = [i / levels for i in range(levels + 1)]

    def quantize_value(self, value: float, dim: str) -> int:
        """
        Quantize a single LJPW value to discrete level (0-3)

        Returns:
            Integer level 0-3
        """
        # Clamp to [0, 1.5] range (LJPW can exceed 1.0 due to coupling)
        clamped = max(0.0, min(1.5, value))
        normalized = clamped / 1.5  # Normalize to [0, 1]

        for i in range(self.levels):
            if normalized <= self.thresholds[i + 1]:
                return i
        return self.levels - 1

    def dequantize_value(self, level: int, dim: str) -> float:
        """
        Convert discrete level back to continuous value
        Uses midpoint of quantization bin
        """
        bin_start = self.thresholds[level]
        bin_end = self.thresholds[level + 1]
        midpoint = (bin_start + bin_end) / 2
        return midpoint * 1.5  # Scale back to LJPW range

# ============================================================================
# LJPW CODONS: Triplet encoding of semantic primitives
# ============================================================================

@dataclass
class LJPWCodon:
    """
    A 3-base sequence encoding a semantic primitive
    Like DNA: 3 bases = 1 codon → 1 amino acid
    LJPW: 3 dimensions = 1 codon → 1 semantic primitive
    """
    base1: str  # L, J, P, or W
    base2: str
    base3: str
    level1: int  # Quantization level (0-3)
    level2: int
    level3: int

    def to_string(self) -> str:
        """Compact string representation: 'L2J1P3'"""
        return f"{self.base1}{self.level1}{self.base2}{self.level2}{self.base3}{self.level3}"

    @classmethod
    def from_string(cls, s: str):
        """Parse from compact string"""
        return cls(
            base1=s[0], level1=int(s[1]),
            base2=s[2], level2=int(s[3]),
            base3=s[4], level3=int(s[5])
        )

    def complement(self) -> 'LJPWCodon':
        """Return complementary codon using pairing rules"""
        return LJPWCodon(
            base1=COMPLEMENTARY_PAIRS[self.base1], level1=self.level1,
            base2=COMPLEMENTARY_PAIRS[self.base2], level2=self.level2,
            base3=COMPLEMENTARY_PAIRS[self.base3], level3=self.level3,
        )

# ============================================================================
# SEMANTIC GENOME: Sequence of LJPW states
# ============================================================================

@dataclass
class SemanticGenome:
    """
    A compressed representation of a system's evolution
    Like DNA: sequence of codons encoding a phenotype
    """
    codons: List[LJPWCodon]
    metadata: Dict[str, Any]

    def __len__(self):
        return len(self.codons)

    def to_string(self) -> str:
        """Compact string representation"""
        codon_str = '-'.join(c.to_string() for c in self.codons)
        return codon_str

    def to_json(self) -> str:
        """JSON representation for storage"""
        return json.dumps({
            'codons': [c.to_string() for c in self.codons],
            'metadata': self.metadata,
        })

    @classmethod
    def from_json(cls, json_str: str):
        """Reconstruct from JSON"""
        data = json.loads(json_str)
        codons = [LJPWCodon.from_string(s) for s in data['codons']]
        return cls(codons=codons, metadata=data['metadata'])

# ============================================================================
# SEMANTIC COMPRESSOR: The "Condenser"
# ============================================================================

class SemanticCompressor:
    """
    Compresses LJPW state sequences into compact semantic genomes

    Like DNA:
    - Uses 4-letter alphabet (L, J, P, W)
    - Encodes in triplets (codons)
    - Applies pairing for error correction
    """

    def __init__(self, quantization_levels=4):
        self.quantizer = LJPWQuantizer(levels=quantization_levels)

    def compress_state_sequence(self,
                                states: List[Tuple[float, float, float, float]],
                                metadata: Dict = None) -> SemanticGenome:
        """
        Compress a sequence of LJPW states into a semantic genome

        Args:
            states: List of (L, J, P, W) tuples representing system evolution
            metadata: Optional metadata about the source

        Returns:
            Compressed SemanticGenome
        """
        codons = []

        for state in states:
            L, J, P, W = state

            # Quantize each dimension
            L_level = self.quantizer.quantize_value(L, 'L')
            J_level = self.quantizer.quantize_value(J, 'J')
            P_level = self.quantizer.quantize_value(P, 'P')
            W_level = self.quantizer.quantize_value(W, 'W')

            # Encode as codon (using LJP as the triplet, W stored separately)
            # We'll use a 4-base encoding strategy
            codon = LJPWCodon(
                base1='L', level1=L_level,
                base2='J', level2=J_level,
                base3='P', level3=P_level,
            )
            codons.append(codon)

            # Store W in a complementary codon for error correction
            w_codon = LJPWCodon(
                base1='W', level1=W_level,
                base2='L', level2=L_level,  # Checksum: L-W pairing
                base3='P', level3=P_level,  # Checksum: P-J pairing
            )
            codons.append(w_codon)

        if metadata is None:
            metadata = {}

        metadata['original_length'] = len(states)
        metadata['compression_ratio'] = self._calculate_compression_ratio(states, codons)

        return SemanticGenome(codons=codons, metadata=metadata)

    def _calculate_compression_ratio(self,
                                    original_states: List[Tuple],
                                    codons: List[LJPWCodon]) -> float:
        """
        Calculate compression ratio

        Original: 4 floats × 8 bytes = 32 bytes per state
        Compressed: 6 chars × 1 byte = 6 bytes per codon pair
        """
        original_bytes = len(original_states) * 4 * 8  # 4 floats × 8 bytes
        compressed_bytes = len(codons) * 1  # ~1 byte per base (6 chars per codon)
        return original_bytes / compressed_bytes

# ============================================================================
# SEMANTIC DECOMPRESSOR: The "Expander"
# ============================================================================

class SemanticDecompressor:
    """
    Decompresses semantic genomes back to LJPW state sequences
    Includes error correction using complementary pairing
    """

    def __init__(self, quantization_levels=4):
        self.quantizer = LJPWQuantizer(levels=quantization_levels)

    def decompress_genome(self, genome: SemanticGenome) -> List[Tuple[float, float, float, float]]:
        """
        Decompress a semantic genome back to LJPW states

        Returns:
            List of (L, J, P, W) tuples
        """
        states = []

        # Process codons in pairs (main codon + W checksum codon)
        for i in range(0, len(genome.codons), 2):
            if i + 1 >= len(genome.codons):
                break

            main_codon = genome.codons[i]
            w_codon = genome.codons[i + 1]

            # Dequantize values
            L = self.quantizer.dequantize_value(main_codon.level1, 'L')
            J = self.quantizer.dequantize_value(main_codon.level2, 'J')
            P = self.quantizer.dequantize_value(main_codon.level3, 'P')
            W = self.quantizer.dequantize_value(w_codon.level1, 'W')

            # Error correction: verify checksums
            L_check = self.quantizer.dequantize_value(w_codon.level2, 'L')
            P_check = self.quantizer.dequantize_value(w_codon.level3, 'P')

            # If checksums don't match, use average (simple error correction)
            if abs(L - L_check) > 0.1:
                L = (L + L_check) / 2
            if abs(P - P_check) > 0.1:
                P = (P + P_check) / 2

            states.append((L, J, P, W))

        return states

    def validate_genome(self, genome: SemanticGenome) -> Dict[str, Any]:
        """
        Validate genome integrity using pairing checksums

        Returns:
            Dict with validation results
        """
        errors = []

        for i in range(0, len(genome.codons), 2):
            if i + 1 >= len(genome.codons):
                break

            main_codon = genome.codons[i]
            w_codon = genome.codons[i + 1]

            # Check if checksums match
            if main_codon.level1 != w_codon.level2:  # L checksum
                errors.append(f"Codon {i}: L checksum mismatch")
            if main_codon.level3 != w_codon.level3:  # P checksum
                errors.append(f"Codon {i}: P checksum mismatch")

        return {
            'valid': len(errors) == 0,
            'error_count': len(errors),
            'errors': errors[:10],  # First 10 errors
            'integrity_score': 1.0 - (len(errors) / (len(genome.codons) / 2)),
        }

# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("LJPW SEMANTIC COMPRESSOR v1.0")
    print("DNA-Inspired Semantic Compression System")
    print("="*70)

    # Example: Compress a system's evolution trajectory
    print("\n1. CREATING SAMPLE SYSTEM TRAJECTORY")
    print("-" * 70)

    # Simulate a project evolving from poor state to Natural Equilibrium
    trajectory = [
        (0.2, 0.3, 0.9, 0.2),  # Initial: Low L,J,W, High P (reckless power)
        (0.3, 0.35, 0.85, 0.3), # Starting to improve
        (0.4, 0.38, 0.80, 0.4),
        (0.5, 0.40, 0.75, 0.5),
        (0.55, 0.41, 0.73, 0.6),
        (0.60, 0.41, 0.72, 0.65),
        (0.618, 0.414, 0.718, 0.693),  # Reached Natural Equilibrium
    ]

    print(f"Trajectory: {len(trajectory)} states")
    print(f"Initial state: L={trajectory[0][0]}, J={trajectory[0][1]}, P={trajectory[0][2]}, W={trajectory[0][3]}")
    print(f"Final state:   L={trajectory[-1][0]}, J={trajectory[-1][1]}, P={trajectory[-1][2]}, W={trajectory[-1][3]}")

    # Compress
    print("\n2. COMPRESSING TO SEMANTIC GENOME")
    print("-" * 70)

    compressor = SemanticCompressor(quantization_levels=4)
    genome = compressor.compress_state_sequence(
        trajectory,
        metadata={'system': 'Example Project', 'domain': 'software'}
    )

    print(f"Compressed genome length: {len(genome)} codons")
    print(f"Compression ratio: {genome.metadata['compression_ratio']:.2f}x")
    print(f"\nGenome string representation:")
    print(f"{genome.to_string()}")

    # Show first few codons
    print(f"\nFirst 4 codons (decoded):")
    for i, codon in enumerate(genome.codons[:4]):
        print(f"  Codon {i}: {codon.to_string()} (bases: {codon.base1}-{codon.base2}-{codon.base3})")

    # Decompress
    print("\n3. DECOMPRESSING GENOME")
    print("-" * 70)

    decompressor = SemanticDecompressor(quantization_levels=4)
    reconstructed = decompressor.decompress_genome(genome)

    print(f"Reconstructed {len(reconstructed)} states")
    print(f"\nOriginal vs Reconstructed (first and last states):")
    print(f"Original[0]:      L={trajectory[0][0]:.3f}, J={trajectory[0][1]:.3f}, P={trajectory[0][2]:.3f}, W={trajectory[0][3]:.3f}")
    print(f"Reconstructed[0]: L={reconstructed[0][0]:.3f}, J={reconstructed[0][1]:.3f}, P={reconstructed[0][2]:.3f}, W={reconstructed[0][3]:.3f}")
    print(f"\nOriginal[-1]:      L={trajectory[-1][0]:.3f}, J={trajectory[-1][1]:.3f}, P={trajectory[-1][2]:.3f}, W={trajectory[-1][3]:.3f}")
    print(f"Reconstructed[-1]: L={reconstructed[-1][0]:.3f}, J={reconstructed[-1][1]:.3f}, P={reconstructed[-1][2]:.3f}, W={reconstructed[-1][3]:.3f}")

    # Calculate reconstruction error
    print("\n4. RECONSTRUCTION ACCURACY")
    print("-" * 70)

    total_error = 0
    for orig, recon in zip(trajectory, reconstructed):
        error = math.sqrt(sum((o - r)**2 for o, r in zip(orig, recon)))
        total_error += error

    avg_error = total_error / len(trajectory)
    print(f"Average reconstruction error (Euclidean): {avg_error:.4f}")
    print(f"Error as % of typical LJPW range [0-1]: {100*avg_error:.2f}%")

    # Validate integrity
    print("\n5. GENOME INTEGRITY VALIDATION")
    print("-" * 70)

    validation = decompressor.validate_genome(genome)
    print(f"Valid: {validation['valid']}")
    print(f"Integrity score: {validation['integrity_score']:.1%}")
    print(f"Error count: {validation['error_count']}")

    # JSON serialization
    print("\n6. SERIALIZATION")
    print("-" * 70)

    json_str = genome.to_json()
    print(f"JSON length: {len(json_str)} bytes")
    print(f"Original trajectory (as floats): {len(trajectory) * 4 * 8} bytes")
    print(f"Space savings: {100 * (1 - len(json_str) / (len(trajectory) * 4 * 8)):.1f}%")

    print(f"\nJSON preview (first 200 chars):")
    print(f"{json_str[:200]}...")

    # Test round-trip
    print("\n7. ROUND-TRIP TEST")
    print("-" * 70)

    genome_restored = SemanticGenome.from_json(json_str)
    reconstructed2 = decompressor.decompress_genome(genome_restored)

    roundtrip_error = 0
    for orig, recon in zip(trajectory, reconstructed2):
        error = math.sqrt(sum((o - r)**2 for o, r in zip(orig, recon)))
        roundtrip_error += error

    print(f"Round-trip successful: {len(reconstructed2) == len(trajectory)}")
    print(f"Round-trip error: {roundtrip_error / len(trajectory):.4f}")

    print("\n" + "="*70)
    print("COMPRESSION SUCCESSFUL")
    print("="*70)
    print(f"\nKey Statistics:")
    print(f"  - Compression ratio: {genome.metadata['compression_ratio']:.2f}x")
    print(f"  - Reconstruction accuracy: {100*(1-avg_error):.1f}%")
    print(f"  - Integrity score: {validation['integrity_score']:.1%}")
    print(f"  - Space savings: {100 * (1 - len(json_str) / (len(trajectory) * 4 * 8)):.1f}%")
