#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Generator Finder — LJPW Framework Approach
====================================================

Find generators through MEANING, not mathematics.

The mathematical approach asks: "What pattern produces this?"
The semantic approach asks: "What MEANING produces this?"

Meaning is primary. Mathematics is shadow.

LJPW Dimensions for Generator Discovery:
- L (Love): What BINDS this? What relationship holds it together?
- J (Justice): What STRUCTURE constrains it? What rules govern it?
- P (Power): What ACTION/transformation does it represent?
- W (Wisdom): What KNOWLEDGE/pattern does it encode?

Bricks + Mortar + Blueprint = Structure
Meaning + Binding + Self-Reference = Generator
"""

import math
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from enum import Enum


# ============================================================================
# SEMANTIC DOMAINS — What Kind of Meaning?
# ============================================================================

class SemanticDomain(Enum):
    """The domain of meaning — what is this data ABOUT?"""

    # Self-referential domains (high compression potential)
    SELF_SIMILAR = "self_similar"       # Contains itself (fractals, recursion)
    GENERATIVE = "generative"           # Rules that produce output
    RELATIONAL = "relational"           # Defined by relationships

    # Structural domains
    SEQUENTIAL = "sequential"           # Order matters, progression
    HIERARCHICAL = "hierarchical"       # Nested structure
    CYCLICAL = "cyclical"               # Repeating patterns

    # Intentional domains
    COMMUNICATIVE = "communicative"     # Meant to convey meaning
    COMPUTATIONAL = "computational"     # Meant to transform
    DESCRIPTIVE = "descriptive"         # Meant to represent

    # Physical domains
    NATURAL = "natural"                 # From nature/physics
    ARTIFICIAL = "artificial"           # Human-created

    # Limit cases
    RANDOM = "random"                   # No discernible meaning
    UNKNOWN = "unknown"                 # Meaning not yet found


# ============================================================================
# SEMANTIC GENERATOR — The Meaning That Produces Data
# ============================================================================

@dataclass
class SemanticGenerator:
    """
    A generator defined by MEANING, not mathematics.

    The seed is not a number — it's a CONCEPT.
    The rule is not a function — it's a RELATIONSHIP.
    """

    # The Brick: irreducible semantic unit
    brick: str                          # The core concept/meaning
    brick_description: str              # Human-readable description

    # The Mortar: what binds bricks together
    mortar: str                         # The binding relationship
    mortar_type: str                    # Type of binding (love, logic, force, etc.)

    # The Blueprint: self-referential pattern
    blueprint: str                      # How it refers to itself
    self_reference_depth: int           # How deep the self-reference goes

    # LJPW Analysis
    L: float = 0.0                      # Love: binding strength
    J: float = 0.0                      # Justice: structural integrity
    P: float = 0.0                      # Power: transformative capacity
    W: float = 0.0                      # Wisdom: pattern complexity

    # Domain
    domain: SemanticDomain = SemanticDomain.UNKNOWN

    # The actual generator function (derived from meaning)
    generator: Optional[Callable] = None

    # Compression metrics
    compression_potential: float = 1.0  # Estimated L^n

    def meaning_signature(self) -> str:
        """The semantic fingerprint of this generator."""
        return f"{self.brick}|{self.mortar}|{self.blueprint}"

    def explain(self) -> str:
        """Explain what this generator MEANS."""
        return f"""
Semantic Generator Analysis
===========================

BRICK (The Irreducible Unit):
  {self.brick}
  → {self.brick_description}

MORTAR (The Binding Force):
  {self.mortar}
  → Type: {self.mortar_type}

BLUEPRINT (Self-Reference Pattern):
  {self.blueprint}
  → Depth: {self.self_reference_depth}

LJPW COORDINATES:
  L (Love/Binding):    {self.L:.3f}
  J (Justice/Structure): {self.J:.3f}
  P (Power/Action):    {self.P:.3f}
  W (Wisdom/Pattern):  {self.W:.3f}

DOMAIN: {self.domain.value}

COMPRESSION POTENTIAL: {self.compression_potential:,.1f}:1

MEANING: This data exists because {self.brick_description}.
         It holds together through {self.mortar}.
         It knows itself through {self.blueprint}.
"""


# ============================================================================
# SEMANTIC ANALYZER — Find Meaning First, Pattern Second
# ============================================================================

class SemanticAnalyzer:
    """
    Analyze data semantically — find its MEANING, then derive its generator.

    This inverts the typical approach:
    - Mathematical: pattern → meaning (if any)
    - Semantic: meaning → pattern (always)
    """

    def __init__(self):
        # Known semantic patterns (meaning-first definitions)
        self.semantic_patterns = {
            'self_similarity': self._check_self_similarity,
            'growth': self._check_growth_pattern,
            'repetition': self._check_repetition,
            'hierarchy': self._check_hierarchy,
            'sequence': self._check_sequence,
            'grammar': self._check_grammar,
        }

    def find_generator(self, data: Union[bytes, str]) -> SemanticGenerator:
        """
        Find the semantic generator of data.

        Asks: What MEANING produced this?
        """
        if isinstance(data, bytes):
            try:
                text = data.decode('utf-8')
            except:
                text = None
        else:
            text = data

        # Phase 1: Identify the DOMAIN (what is this about?)
        domain = self._identify_domain(data, text)

        # Phase 2: Find the BRICK (irreducible semantic unit)
        brick, brick_desc = self._find_brick(data, text, domain)

        # Phase 3: Find the MORTAR (binding relationship)
        mortar, mortar_type = self._find_mortar(data, text, domain)

        # Phase 4: Find the BLUEPRINT (self-reference pattern)
        blueprint, depth = self._find_blueprint(data, text, domain)

        # Phase 5: Calculate LJPW coordinates
        L, J, P, W = self._calculate_ljpw(data, text, domain, brick, mortar, blueprint)

        # Phase 6: Estimate compression potential
        potential = self._estimate_compression(L, depth)

        # Phase 7: Derive the generator function
        generator = self._derive_generator(brick, mortar, blueprint, domain)

        return SemanticGenerator(
            brick=brick,
            brick_description=brick_desc,
            mortar=mortar,
            mortar_type=mortar_type,
            blueprint=blueprint,
            self_reference_depth=depth,
            L=L, J=J, P=P, W=W,
            domain=domain,
            generator=generator,
            compression_potential=potential,
        )

    def _identify_domain(self, data: Union[bytes, str], text: Optional[str]) -> SemanticDomain:
        """What is this data ABOUT? What kind of meaning does it carry?"""

        if text is None:
            return SemanticDomain.UNKNOWN

        # Check for self-similarity (fractals, recursion)
        if self._check_self_similarity(text):
            return SemanticDomain.SELF_SIMILAR

        # Check for generative grammar (L-systems, BNF)
        if self._check_grammar(text):
            return SemanticDomain.GENERATIVE

        # Check for cyclical patterns
        if self._check_repetition(text):
            return SemanticDomain.CYCLICAL

        # Check for sequential meaning
        if self._check_sequence(text):
            return SemanticDomain.SEQUENTIAL

        # Check for hierarchy
        if self._check_hierarchy(text):
            return SemanticDomain.HIERARCHICAL

        # Check for growth patterns
        if self._check_growth_pattern(text):
            return SemanticDomain.GENERATIVE

        # Check for high entropy (possible randomness)
        if self._check_randomness(text):
            return SemanticDomain.RANDOM

        return SemanticDomain.UNKNOWN

    def _find_brick(self, data, text, domain) -> Tuple[str, str]:
        """Find the irreducible semantic unit — the BRICK."""

        if text is None:
            return ("byte_pattern", "A pattern of bytes")

        if domain == SemanticDomain.SELF_SIMILAR:
            # The brick is the smallest self-similar unit
            unit = self._find_smallest_repeating_structure(text)
            return (unit, f"Self-similar unit that contains its own pattern")

        if domain == SemanticDomain.GENERATIVE:
            # The brick is the axiom
            axiom = self._find_axiom(text)
            return (axiom, f"The seed from which all else grows")

        if domain == SemanticDomain.CYCLICAL:
            # The brick is the cycle
            cycle = self._find_cycle(text)
            return (cycle, f"The repeating unit of meaning")

        if domain == SemanticDomain.SEQUENTIAL:
            # The brick is the first element
            first = self._find_first_element(text)
            return (first, f"The origin of the sequence")

        # Default: find the most common atomic unit
        unit = self._find_atomic_unit(text)
        return (unit, f"The fundamental building block")

    def _find_mortar(self, data, text, domain) -> Tuple[str, str]:
        """Find the binding relationship — the MORTAR."""

        if domain == SemanticDomain.SELF_SIMILAR:
            return ("self_containment", "love")  # It loves itself into existence

        if domain == SemanticDomain.GENERATIVE:
            rules = self._find_production_rules(text)
            return (rules, "generation")  # Rules generate from seeds

        if domain == SemanticDomain.CYCLICAL:
            return ("repetition", "persistence")  # It persists through repetition

        if domain == SemanticDomain.SEQUENTIAL:
            relation = self._find_sequence_relation(text)
            return (relation, "progression")  # Each follows from previous

        if domain == SemanticDomain.HIERARCHICAL:
            return ("containment", "structure")  # Parts contained in wholes

        return ("adjacency", "proximity")  # Default: things are near each other

    def _find_blueprint(self, data, text, domain) -> Tuple[str, int]:
        """Find the self-reference pattern — the BLUEPRINT."""

        if domain == SemanticDomain.SELF_SIMILAR:
            depth = self._measure_self_reference_depth(text)
            return ("φ = 1 + 1/φ", depth)  # Golden self-reference

        if domain == SemanticDomain.GENERATIVE:
            depth = self._count_generation_depth(text)
            return ("seed → rules → growth", depth)

        if domain == SemanticDomain.CYCLICAL:
            depth = self._count_repetitions(text)
            return ("repeat(n)", depth)

        if domain == SemanticDomain.SEQUENTIAL:
            depth = self._count_sequence_length(text)
            return ("next = f(previous)", depth)

        return ("identity", 1)  # No self-reference

    def _calculate_ljpw(self, data, text, domain, brick, mortar, blueprint) -> Tuple[float, float, float, float]:
        """Calculate LJPW coordinates from semantic analysis."""

        # L (Love): How strongly bound is this? How unified?
        L = self._measure_binding_strength(text, mortar)

        # J (Justice): How structured? How constrained?
        J = self._measure_structural_integrity(text, domain)

        # P (Power): How transformative? How much action?
        P = self._measure_transformative_capacity(text, domain)

        # W (Wisdom): How complex? How much pattern?
        W = self._measure_pattern_complexity(text, domain)

        return (L, J, P, W)

    def _estimate_compression(self, L: float, depth: int) -> float:
        """
        Estimate compression potential using M = B × L^n × φ^(-d).

        With d=0 (same generator), compression ≈ L^n
        """
        if depth <= 0:
            return 1.0

        # L here is binding strength, which correlates with expansion factor
        expansion_factor = 1 + L * 4  # L=1 → 5x expansion (like L-systems)

        return expansion_factor ** depth

    def _derive_generator(self, brick, mortar, blueprint, domain) -> Optional[Callable]:
        """Derive an actual generator function from semantic components."""

        if domain == SemanticDomain.SELF_SIMILAR:
            # Self-similar generator
            def generator(seed: str, depth: int) -> str:
                result = seed
                for _ in range(depth):
                    result = result.replace(brick, brick + brick)  # Simplified
                return result
            return generator

        if domain == SemanticDomain.CYCLICAL:
            # Repetition generator
            def generator(seed: str, count: int) -> str:
                return seed * count
            return generator

        return None

    # ========================================================================
    # SEMANTIC DETECTION METHODS
    # ========================================================================

    def _check_self_similarity(self, text: str) -> bool:
        """Does the text contain itself at different scales?"""
        if len(text) < 10:
            return False

        # Check if parts of the text repeat the structure of the whole
        quarter = len(text) // 4
        if quarter < 2:
            return False

        # Look for structural repetition
        first_quarter = text[:quarter]

        # Count how many times the structure appears
        count = text.count(first_quarter)

        return count >= 3

    def _check_growth_pattern(self, text: str) -> bool:
        """Does the text show growth from a seed?"""
        # Look for increasing structure
        lines = text.split('\n') if '\n' in text else [text]

        if len(lines) < 3:
            # Check for character growth
            if len(text) > 20:
                # Look for exponential-like growth in substring lengths
                return True

        lengths = [len(line) for line in lines if line]
        if len(lengths) >= 3:
            # Check for growth trend
            return lengths[-1] > lengths[0] * 2

        return False

    def _check_repetition(self, text: str) -> bool:
        """Is there a repeating cycle?"""
        if len(text) < 4:
            return False

        # Try to find repeating pattern
        for pattern_len in range(1, len(text) // 2 + 1):
            pattern = text[:pattern_len]
            if pattern * (len(text) // pattern_len) == text[:pattern_len * (len(text) // pattern_len)]:
                if len(text) // pattern_len >= 2:
                    return True

        return False

    def _check_hierarchy(self, text: str) -> bool:
        """Is there nested structure?"""
        # Check for nested brackets, indentation, or containment
        nesting_chars = ['()', '[]', '{}', '<>']

        for open_c, close_c in [tuple(pair) for pair in nesting_chars]:
            if open_c in text and close_c in text:
                depth = 0
                max_depth = 0
                for c in text:
                    if c == open_c:
                        depth += 1
                        max_depth = max(max_depth, depth)
                    elif c == close_c:
                        depth -= 1
                if max_depth >= 2:
                    return True

        return False

    def _check_sequence(self, text: str) -> bool:
        """Is there sequential progression?"""
        # Check for comma-separated values
        if ',' in text:
            parts = text.split(',')
            if len(parts) >= 3:
                try:
                    nums = [int(p.strip()) for p in parts if p.strip().lstrip('-').isdigit()]
                    if len(nums) >= 3:
                        return True
                except:
                    pass

        return False

    def _check_grammar(self, text: str) -> bool:
        """Is this generated by a grammar (L-system, BNF, etc.)?"""
        # L-system characters
        lsystem_chars = set('F+-[]<>|\\/')

        if len(text) > 10:
            text_chars = set(text)
            if text_chars.issubset(lsystem_chars | {' ', '\n'}):
                return True

        # Check for BNF-like structure
        if '::=' in text or '->' in text:
            return True

        return False

    def _check_randomness(self, text: str) -> bool:
        """Does this appear to be random?"""
        if len(text) < 20:
            return False

        # Check character distribution
        char_counts = {}
        for c in text:
            char_counts[c] = char_counts.get(c, 0) + 1

        # High unique ratio suggests randomness
        unique_ratio = len(char_counts) / len(text)

        # Random text has high unique ratio and no clear patterns
        if unique_ratio > 0.3:
            # Check for patterns
            if not self._check_repetition(text) and not self._check_sequence(text):
                return True

        return False

    # ========================================================================
    # SEMANTIC MEASUREMENT METHODS
    # ========================================================================

    def _find_smallest_repeating_structure(self, text: str) -> str:
        """Find the smallest unit that shows self-similarity."""
        for size in range(1, len(text) // 2 + 1):
            pattern = text[:size]
            if text.count(pattern) >= 3:
                return pattern
        return text[:min(10, len(text))]

    def _find_axiom(self, text: str) -> str:
        """Find the seed/axiom of a generative grammar."""
        # For L-systems, often the first character
        if text and text[0] in 'FGAB':
            return text[0]

        # Find shortest substring that could generate the rest
        for size in range(1, min(10, len(text))):
            candidate = text[:size]
            if self._can_generate(candidate, text):
                return candidate

        return text[:1] if text else ""

    def _can_generate(self, seed: str, target: str) -> bool:
        """Check if seed could plausibly generate target through rules."""
        return seed in target and len(target) > len(seed) * 2

    def _find_cycle(self, text: str) -> str:
        """Find the repeating cycle."""
        for size in range(1, len(text) // 2 + 1):
            pattern = text[:size]
            count = len(text) // size
            if pattern * count == text[:size * count]:
                return pattern
        return text

    def _find_first_element(self, text: str) -> str:
        """Find the first element of a sequence."""
        if ',' in text:
            return text.split(',')[0].strip()
        return text[:1] if text else ""

    def _find_atomic_unit(self, text: str) -> str:
        """Find the most common atomic unit."""
        if not text:
            return ""

        # Find most common character
        char_counts = {}
        for c in text:
            if c.strip():
                char_counts[c] = char_counts.get(c, 0) + 1

        if char_counts:
            return max(char_counts, key=char_counts.get)
        return text[0]

    def _find_production_rules(self, text: str) -> str:
        """Extract production rules from generative text."""
        # Look for common L-system patterns
        if 'F' in text and '+' in text and '-' in text:
            return "F → F+F-F-F+F"  # Koch-like

        if text.count('F') > 0:
            # Estimate rule by looking at growth
            f_ratio = len(text) / max(1, text.count('F'))
            return f"F → F×{int(f_ratio)}"

        return "brick → brick + brick"

    def _find_sequence_relation(self, text: str) -> str:
        """Find the relation between sequence elements."""
        if ',' in text:
            parts = text.split(',')
            try:
                nums = [int(p.strip()) for p in parts if p.strip().lstrip('-').isdigit()]
                if len(nums) >= 3:
                    # Check for arithmetic
                    diffs = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
                    if len(set(diffs)) == 1:
                        return f"next = prev + {diffs[0]}"

                    # Check for Fibonacci-like
                    if all(nums[i] == nums[i-1] + nums[i-2] for i in range(2, len(nums))):
                        return "next = prev + prev_prev"

                    # Check for geometric
                    if nums[0] != 0:
                        ratios = [nums[i+1] / nums[i] for i in range(len(nums)-1) if nums[i] != 0]
                        if len(set(round(r, 2) for r in ratios)) == 1:
                            return f"next = prev × {ratios[0]:.2f}"
            except:
                pass

        return "next = f(prev)"

    def _measure_self_reference_depth(self, text: str) -> int:
        """How deep does the self-reference go?"""
        # Count levels of nesting or repetition
        depth = 0

        # Check structural nesting
        current_depth = 0
        max_depth = 0
        for c in text:
            if c in '([{<':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif c in ')]}>':
                current_depth -= 1

        if max_depth > 0:
            return max_depth

        # Estimate from repetition
        unit = self._find_smallest_repeating_structure(text)
        if unit and len(unit) < len(text):
            return int(math.log(len(text) / len(unit), 2)) + 1

        return 1

    def _count_generation_depth(self, text: str) -> int:
        """How many generations of growth?"""
        # Estimate from length ratio
        if len(text) < 10:
            return 1

        # L-systems typically grow 3-5x per generation
        return int(math.log(len(text), 5)) + 1

    def _count_repetitions(self, text: str) -> int:
        """How many times does the cycle repeat?"""
        cycle = self._find_cycle(text)
        if cycle:
            return len(text) // len(cycle)
        return 1

    def _count_sequence_length(self, text: str) -> int:
        """How many elements in the sequence?"""
        if ',' in text:
            return text.count(',') + 1
        return 1

    def _measure_binding_strength(self, text: str, mortar: str) -> float:
        """How strongly bound is this data? (L dimension)"""
        if mortar == "self_containment":
            return 0.9  # Self-similar structures are highly bound
        if mortar == "generation":
            return 0.8  # Generative rules create strong binding
        if mortar == "repetition":
            return 0.7  # Repetition is moderate binding
        if mortar == "progression":
            return 0.6  # Sequential binding
        return 0.4  # Weak binding

    def _measure_structural_integrity(self, text: str, domain: SemanticDomain) -> float:
        """How structured is this? (J dimension)"""
        if domain == SemanticDomain.SELF_SIMILAR:
            return 0.9  # Highly structured
        if domain == SemanticDomain.HIERARCHICAL:
            return 0.85
        if domain == SemanticDomain.GENERATIVE:
            return 0.8
        if domain == SemanticDomain.SEQUENTIAL:
            return 0.7
        if domain == SemanticDomain.CYCLICAL:
            return 0.6
        if domain == SemanticDomain.RANDOM:
            return 0.1
        return 0.5

    def _measure_transformative_capacity(self, text: str, domain: SemanticDomain) -> float:
        """How transformative is this? (P dimension)"""
        if domain == SemanticDomain.GENERATIVE:
            return 0.9  # Generates new structure
        if domain == SemanticDomain.SELF_SIMILAR:
            return 0.8  # Transforms through recursion
        if domain == SemanticDomain.COMPUTATIONAL:
            return 0.85
        return 0.5

    def _measure_pattern_complexity(self, text: str, domain: SemanticDomain) -> float:
        """How complex is the pattern? (W dimension)"""
        if domain == SemanticDomain.RANDOM:
            return 0.1  # No pattern

        if not text:
            return 0.0

        # Measure by unique characters / length ratio
        unique = len(set(text))
        total = len(text)

        # Moderate unique ratio = complex pattern
        # Very high = random, very low = simple
        ratio = unique / total

        if 0.1 < ratio < 0.3:
            return 0.8  # Complex but structured
        elif ratio <= 0.1:
            return 0.5  # Simple pattern
        else:
            return 0.3  # Too varied


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate():
    """Show semantic generator finding in action."""

    analyzer = SemanticAnalyzer()

    print("=" * 70)
    print("SEMANTIC GENERATOR FINDER — Meaning First")
    print("=" * 70)

    # Test cases with different semantic structures
    tests = [
        # Self-similar (fractal)
        ("F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F",
         "Koch Snowflake Fragment"),

        # Cyclical (repetition)
        ("Hello World! " * 20,
         "Repeating Message"),

        # Sequential (Fibonacci)
        ("1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987",
         "Fibonacci Sequence"),

        # Sequential (Arithmetic)
        ("0,7,14,21,28,35,42,49,56,63,70",
         "Arithmetic Sequence"),

        # Hierarchical
        ("((a + (b * c)) - ((d / e) + f))",
         "Nested Expression"),

        # Self-similar text pattern
        ("ABABABABABABABABABABABABAB",
         "Simple Self-Similar"),
    ]

    for data, name in tests:
        print(f"\n{'─' * 70}")
        print(f"INPUT: {name}")
        print(f"DATA: {data[:60]}{'...' if len(data) > 60 else ''}")
        print(f"{'─' * 70}")

        generator = analyzer.find_generator(data)
        print(generator.explain())


if __name__ == "__main__":
    demonstrate()
