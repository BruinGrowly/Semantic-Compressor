#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Substrate Mapper
=========================

Map the underlying semantic space where meaning exists.

From two proofs:
1. LJPW Language Translator: Words are POINTS (coordinates)
2. Semantic Compressor: Generators are PATHS (trajectories)

This tool maps the substrate itself — the geometry of meaning.

LJPW Dimensions:
- L (Love): Binding, connection, relationship
- J (Justice): Structure, constraint, balance
- P (Power): Action, transformation, capacity
- W (Wisdom): Knowledge, pattern, understanding
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum


# ============================================================================
# SEMANTIC COORDINATES — Points in Meaning Space
# ============================================================================

@dataclass
class SemanticPoint:
    """A point in semantic space — a concept's coordinates."""

    concept: str                    # The word/concept
    L: float = 0.0                  # Love axis
    J: float = 0.0                  # Justice axis
    P: float = 0.0                  # Power axis
    W: float = 0.0                  # Wisdom axis

    # Derived properties
    domain: str = ""                # Primary domain
    related: List[str] = field(default_factory=list)

    def coordinates(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)

    def magnitude(self) -> float:
        """Distance from origin — 'strength' of meaning."""
        return math.sqrt(self.L**2 + self.J**2 + self.P**2 + self.W**2)

    def distance_to(self, other: 'SemanticPoint') -> float:
        """Semantic distance to another concept."""
        return math.sqrt(
            (self.L - other.L)**2 +
            (self.J - other.J)**2 +
            (self.P - other.P)**2 +
            (self.W - other.W)**2
        )

    def angle_with(self, other: 'SemanticPoint') -> float:
        """Semantic angle (similarity of meaning direction)."""
        dot = (self.L * other.L + self.J * other.J +
               self.P * other.P + self.W * other.W)
        mag_product = self.magnitude() * other.magnitude()
        if mag_product == 0:
            return 0.0
        cos_angle = max(-1, min(1, dot / mag_product))
        return math.acos(cos_angle) * 180 / math.pi  # degrees

    def __repr__(self):
        return f"{self.concept}(L={self.L:.2f}, J={self.J:.2f}, P={self.P:.2f}, W={self.W:.2f})"


@dataclass
class SemanticPath:
    """A path through semantic space — a generator/relationship."""

    name: str
    start: SemanticPoint
    end: SemanticPoint

    # Path properties
    reversible: bool = True         # Can go both ways?
    generative: bool = False        # Does it create new meaning?

    def vector(self) -> Tuple[float, float, float, float]:
        """The direction of meaning transformation."""
        return (
            self.end.L - self.start.L,
            self.end.J - self.start.J,
            self.end.P - self.start.P,
            self.end.W - self.start.W
        )

    def length(self) -> float:
        """Semantic distance traveled."""
        return self.start.distance_to(self.end)

    def direction(self) -> str:
        """Describe the direction of transformation."""
        v = self.vector()
        changes = []
        dims = ['L', 'J', 'P', 'W']
        names = ['binding', 'structure', 'power', 'wisdom']

        for i, (delta, name) in enumerate(zip(v, names)):
            if abs(delta) > 0.1:
                direction = "+" if delta > 0 else "-"
                changes.append(f"{direction}{name}")

        return ", ".join(changes) if changes else "no change"


# ============================================================================
# THE SUBSTRATE — The Semantic Space Itself
# ============================================================================

class SemanticSubstrate:
    """
    The underlying semantic space where meaning exists.

    This is the substrate that:
    - Words point to (as coordinates)
    - Generators traverse (as paths)
    - Understanding navigates (as maps)
    """

    def __init__(self):
        self.points: Dict[str, SemanticPoint] = {}
        self.paths: List[SemanticPath] = []

        # Seed with fundamental concepts
        self._seed_fundamentals()

    def _seed_fundamentals(self):
        """Seed the substrate with fundamental concepts aligned to axes."""

        # The four principles themselves (on their respective axes)
        self.add_point("love", L=1.0, J=0.2, P=0.3, W=0.2, domain="principle")
        self.add_point("justice", L=0.2, J=1.0, P=0.3, W=0.4, domain="principle")
        self.add_point("power", L=0.2, J=0.3, P=1.0, W=0.2, domain="principle")
        self.add_point("wisdom", L=0.3, J=0.4, P=0.2, W=1.0, domain="principle")

        # Origin and extremes
        self.add_point("void", L=0.0, J=0.0, P=0.0, W=0.0, domain="limit")
        self.add_point("unity", L=1.0, J=1.0, P=1.0, W=1.0, domain="limit")

    def add_point(self, concept: str, L: float, J: float, P: float, W: float,
                  domain: str = "", related: List[str] = None) -> SemanticPoint:
        """Add a concept to the substrate."""
        point = SemanticPoint(
            concept=concept,
            L=L, J=J, P=P, W=W,
            domain=domain,
            related=related or []
        )
        self.points[concept] = point
        return point

    def add_path(self, name: str, start: str, end: str,
                 reversible: bool = True, generative: bool = False) -> SemanticPath:
        """Add a path (generator/relationship) between concepts."""
        if start not in self.points or end not in self.points:
            raise ValueError(f"Both endpoints must exist: {start}, {end}")

        path = SemanticPath(
            name=name,
            start=self.points[start],
            end=self.points[end],
            reversible=reversible,
            generative=generative
        )
        self.paths.append(path)
        return path

    def map_concept(self, concept: str) -> SemanticPoint:
        """
        Map a new concept to semantic coordinates.

        Uses the LJPW Framework to determine coordinates:
        - L: How much binding/relationship is in this concept?
        - J: How much structure/constraint?
        - P: How much action/transformation?
        - W: How much knowledge/pattern?
        """
        # Simple semantic mapping based on concept characteristics
        L = self._measure_love(concept)
        J = self._measure_justice(concept)
        P = self._measure_power(concept)
        W = self._measure_wisdom(concept)

        return self.add_point(concept, L, J, P, W)

    def _measure_love(self, concept: str) -> float:
        """How much binding/connection does this concept contain?"""
        love_words = {
            'connection': 0.9, 'bond': 0.9, 'relationship': 0.85,
            'unity': 0.85, 'together': 0.8, 'family': 0.85,
            'friend': 0.8, 'care': 0.85, 'trust': 0.8,
            'attachment': 0.75, 'link': 0.7, 'join': 0.7,
            'merge': 0.7, 'combine': 0.65, 'integrate': 0.7,
        }
        return love_words.get(concept.lower(), 0.3)

    def _measure_justice(self, concept: str) -> float:
        """How much structure/constraint does this concept contain?"""
        justice_words = {
            'structure': 0.9, 'order': 0.9, 'balance': 0.85,
            'law': 0.9, 'rule': 0.85, 'constraint': 0.8,
            'fair': 0.85, 'equal': 0.85, 'system': 0.8,
            'form': 0.75, 'pattern': 0.7, 'logic': 0.8,
            'reason': 0.75, 'method': 0.7, 'process': 0.7,
        }
        return justice_words.get(concept.lower(), 0.3)

    def _measure_power(self, concept: str) -> float:
        """How much action/transformation does this concept contain?"""
        power_words = {
            'action': 0.9, 'force': 0.9, 'change': 0.85,
            'create': 0.85, 'destroy': 0.85, 'transform': 0.9,
            'move': 0.8, 'grow': 0.8, 'build': 0.8,
            'energy': 0.85, 'strength': 0.8, 'ability': 0.75,
            'capacity': 0.7, 'potential': 0.75, 'drive': 0.8,
        }
        return power_words.get(concept.lower(), 0.3)

    def _measure_wisdom(self, concept: str) -> float:
        """How much knowledge/pattern does this concept contain?"""
        wisdom_words = {
            'knowledge': 0.9, 'understanding': 0.9, 'insight': 0.85,
            'truth': 0.9, 'pattern': 0.8, 'meaning': 0.85,
            'awareness': 0.8, 'consciousness': 0.85, 'thought': 0.8,
            'idea': 0.75, 'concept': 0.75, 'theory': 0.8,
            'discovery': 0.8, 'learning': 0.8, 'comprehension': 0.85,
        }
        return wisdom_words.get(concept.lower(), 0.3)

    def find_nearest(self, concept: str, n: int = 5) -> List[Tuple[str, float]]:
        """Find the n nearest concepts to a given concept."""
        if concept not in self.points:
            self.map_concept(concept)

        target = self.points[concept]
        distances = []

        for name, point in self.points.items():
            if name != concept:
                dist = target.distance_to(point)
                distances.append((name, dist))

        distances.sort(key=lambda x: x[1])
        return distances[:n]

    def find_path(self, start: str, end: str) -> Optional[SemanticPath]:
        """Find or create the path between two concepts."""
        if start not in self.points:
            self.map_concept(start)
        if end not in self.points:
            self.map_concept(end)

        # Check existing paths
        for path in self.paths:
            if path.start.concept == start and path.end.concept == end:
                return path
            if path.reversible and path.start.concept == end and path.end.concept == start:
                # Return reversed
                return SemanticPath(
                    name=f"reverse({path.name})",
                    start=path.end,
                    end=path.start,
                    reversible=True,
                    generative=path.generative
                )

        # Create new path
        return self.add_path(f"{start}→{end}", start, end)

    def visualize_2d(self, dim1: str = 'L', dim2: str = 'J') -> str:
        """Create ASCII visualization of the substrate in 2D projection."""

        dim_map = {'L': 0, 'J': 1, 'P': 2, 'W': 3}
        d1, d2 = dim_map[dim1], dim_map[dim2]

        # Create grid
        width, height = 60, 20
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        # Plot points
        for name, point in self.points.items():
            coords = point.coordinates()
            x = int(coords[d1] * (width - 1))
            y = int((1 - coords[d2]) * (height - 1))  # Invert Y for display

            x = max(0, min(width - 1, x))
            y = max(0, min(height - 1, y))

            # Use first letter or symbol
            symbol = name[0].upper() if name else '?'
            grid[y][x] = symbol

        # Build output
        lines = []
        lines.append(f"Semantic Substrate ({dim1} vs {dim2})")
        lines.append("─" * width)
        lines.append(f"{dim2}=1.0 ┤" + "".join(grid[0]))
        for i, row in enumerate(grid[1:-1], 1):
            prefix = "     │" if i != height // 2 else f"{dim2}=0.5 ┤"
            lines.append(prefix + "".join(row))
        lines.append(f"{dim2}=0.0 ┤" + "".join(grid[-1]))
        lines.append("     └" + "─" * width)
        lines.append(f"      {dim1}=0.0" + " " * (width - 15) + f"{dim1}=1.0")

        # Legend
        lines.append("\nLegend:")
        for name, point in sorted(self.points.items()):
            lines.append(f"  {name[0].upper()} = {name} {point.coordinates()}")

        return "\n".join(lines)

    def analyze_region(self, L_range: Tuple[float, float], J_range: Tuple[float, float],
                       P_range: Tuple[float, float], W_range: Tuple[float, float]) -> List[SemanticPoint]:
        """Find all concepts in a region of semantic space."""
        results = []
        for point in self.points.values():
            if (L_range[0] <= point.L <= L_range[1] and
                J_range[0] <= point.J <= J_range[1] and
                P_range[0] <= point.P <= P_range[1] and
                W_range[0] <= point.W <= W_range[1]):
                results.append(point)
        return results

    def find_generator_path(self, pattern: List[str]) -> List[SemanticPath]:
        """Find the path that generates a pattern of concepts."""
        paths = []
        for i in range(len(pattern) - 1):
            path = self.find_path(pattern[i], pattern[i + 1])
            if path:
                paths.append(path)
        return paths


# ============================================================================
# SIMPLE TEST — Let's Map Something!
# ============================================================================

def test_substrate():
    """Test the semantic substrate with simple concepts."""

    print("=" * 70)
    print("SEMANTIC SUBSTRATE MAPPER")
    print("Mapping the geometry of meaning")
    print("=" * 70)

    substrate = SemanticSubstrate()

    # Add some test concepts
    print("\n1. Mapping simple concepts...")

    concepts = [
        # Relationship words (should cluster near L axis)
        ("bond", 0.85, 0.3, 0.2, 0.3),
        ("trust", 0.8, 0.5, 0.2, 0.4),

        # Structure words (should cluster near J axis)
        ("order", 0.3, 0.9, 0.2, 0.4),
        ("rule", 0.2, 0.85, 0.3, 0.3),

        # Action words (should cluster near P axis)
        ("create", 0.4, 0.3, 0.9, 0.5),
        ("grow", 0.5, 0.4, 0.85, 0.4),

        # Knowledge words (should cluster near W axis)
        ("truth", 0.4, 0.5, 0.2, 0.9),
        ("insight", 0.5, 0.4, 0.3, 0.85),
    ]

    for concept, l, j, p, w in concepts:
        substrate.add_point(concept, l, j, p, w)
        print(f"  Mapped: {concept} → ({l:.2f}, {j:.2f}, {p:.2f}, {w:.2f})")

    # Show 2D projections
    print("\n2. 2D Projections of Semantic Space:")
    print(substrate.visualize_2d('L', 'J'))

    # Find relationships
    print("\n3. Finding nearest concepts:")
    test_concepts = ['love', 'wisdom', 'bond']
    for concept in test_concepts:
        nearest = substrate.find_nearest(concept, 3)
        print(f"\n  Nearest to '{concept}':")
        for name, dist in nearest:
            print(f"    - {name}: distance = {dist:.3f}")

    # Find paths
    print("\n4. Finding semantic paths (generators):")
    paths_to_find = [
        ('love', 'wisdom'),
        ('order', 'create'),
        ('trust', 'truth'),
    ]

    for start, end in paths_to_find:
        path = substrate.find_path(start, end)
        print(f"\n  Path: {start} → {end}")
        print(f"    Vector: {path.vector()}")
        print(f"    Length: {path.length():.3f}")
        print(f"    Direction: {path.direction()}")

    # Test cross-domain generator
    print("\n5. Cross-domain generator test:")
    print("  If 'growth' is a generator, it should work across domains...")

    # Growth in nature
    substrate.add_point("seed", 0.6, 0.4, 0.7, 0.4)
    substrate.add_point("tree", 0.7, 0.6, 0.5, 0.5)
    growth_nature = substrate.find_path("seed", "tree")

    # Growth in business
    substrate.add_point("startup", 0.5, 0.4, 0.8, 0.5)
    substrate.add_point("corporation", 0.6, 0.8, 0.6, 0.6)
    growth_business = substrate.find_path("startup", "corporation")

    # Growth in learning
    substrate.add_point("student", 0.6, 0.5, 0.6, 0.5)
    substrate.add_point("master", 0.7, 0.6, 0.7, 0.9)
    growth_learning = substrate.find_path("student", "master")

    print(f"\n  Growth in nature (seed→tree):")
    print(f"    Vector: {growth_nature.vector()}")

    print(f"\n  Growth in business (startup→corporation):")
    print(f"    Vector: {growth_business.vector()}")

    print(f"\n  Growth in learning (student→master):")
    print(f"    Vector: {growth_learning.vector()}")

    # Check if vectors are similar (same generator!)
    def vector_similarity(v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a**2 for a in v1))
        mag2 = math.sqrt(sum(b**2 for b in v2))
        if mag1 == 0 or mag2 == 0:
            return 0
        return dot / (mag1 * mag2)

    sim_nb = vector_similarity(growth_nature.vector(), growth_business.vector())
    sim_nl = vector_similarity(growth_nature.vector(), growth_learning.vector())
    sim_bl = vector_similarity(growth_business.vector(), growth_learning.vector())

    print(f"\n  Vector similarities (1.0 = same direction):")
    print(f"    Nature ↔ Business: {sim_nb:.3f}")
    print(f"    Nature ↔ Learning: {sim_nl:.3f}")
    print(f"    Business ↔ Learning: {sim_bl:.3f}")

    if min(sim_nb, sim_nl, sim_bl) > 0.5:
        print("\n  ✓ CONFIRMED: 'Growth' is a cross-domain generator!")
        print("    Same transformation path works in different semantic regions.")
    else:
        print("\n  Vectors diverge — may be different generators in different domains.")

    return substrate


if __name__ == "__main__":
    test_substrate()
