#!/usr/bin/env python3
"""
Meta-Principle Finder
=====================

Find the lowest common denominators - the principles that generate
across ALL domains.

Hierarchy:
1. Meta-Principles (this tool finds these)
2. Cross-domain Generators
3. Domain-specific Generators
4. Data

Method:
- Collect transformation vectors from many domains
- Find common directional components
- Extract the "eigenvectors of meaning" - fundamental transformations
"""

from substrate_mapper import SemanticSubstrate
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict


@dataclass
class MetaPrinciple:
    """A principle that generates across domains."""
    name: str
    vector: Tuple[float, float, float, float]  # LJPW direction
    description: str
    instances: List[Tuple[str, str, str]]  # (domain, start, end)
    strength: float  # How universal is it?

    def explain(self) -> str:
        dims = ['L (binding)', 'J (structure)', 'P (power)', 'W (wisdom)']
        changes = []
        for i, (v, d) in enumerate(zip(self.vector, dims)):
            if abs(v) > 0.1:
                sign = "+" if v > 0 else "-"
                changes.append(f"{sign}{d}")

        return f"""
Meta-Principle: {self.name.upper()}
{'=' * 50}
Vector: L={self.vector[0]:+.2f}, J={self.vector[1]:+.2f}, P={self.vector[2]:+.2f}, W={self.vector[3]:+.2f}
Effect: {', '.join(changes)}
Strength: {self.strength:.2f} (universality across domains)

Description: {self.description}

Instances across domains:
{chr(10).join(f'  - {domain}: {start} → {end}' for domain, start, end in self.instances)}
"""


class MetaPrincipleFinder:
    """Find meta-principles by analyzing transformation patterns."""

    def __init__(self):
        self.substrate = SemanticSubstrate()
        self.transformations: Dict[str, List[Tuple[str, str, Tuple]]] = defaultdict(list)
        self._build_vocabulary()

    def _build_vocabulary(self):
        """Build rich vocabulary across multiple domains."""

        domains = {
            # PHYSICAL domain
            "physical": {
                "frozen": (0.3, 0.7, 0.1, 0.3),
                "cold": (0.35, 0.55, 0.2, 0.35),
                "warm": (0.5, 0.45, 0.5, 0.45),
                "hot": (0.4, 0.35, 0.75, 0.4),
                "solid": (0.4, 0.8, 0.2, 0.4),
                "liquid": (0.5, 0.4, 0.45, 0.4),
                "gas": (0.3, 0.2, 0.7, 0.4),
                "small": (0.4, 0.42, 0.25, 0.38),
                "large": (0.45, 0.48, 0.6, 0.48),
                "seed": (0.6, 0.5, 0.4, 0.5),
                "sprout": (0.55, 0.45, 0.55, 0.45),
                "plant": (0.5, 0.55, 0.5, 0.5),
                "tree": (0.55, 0.65, 0.45, 0.55),
            },

            # LIFE domain
            "life": {
                "infant": (0.8, 0.2, 0.3, 0.15),
                "child": (0.75, 0.3, 0.5, 0.3),
                "teenager": (0.6, 0.35, 0.7, 0.4),
                "adult": (0.55, 0.6, 0.6, 0.6),
                "elder": (0.55, 0.55, 0.35, 0.9),
                "alive": (0.6, 0.5, 0.7, 0.5),
                "dying": (0.4, 0.4, 0.3, 0.6),
                "dead": (0.3, 0.6, 0.1, 0.4),
            },

            # KNOWLEDGE domain
            "knowledge": {
                "ignorant": (0.3, 0.3, 0.4, 0.1),
                "curious": (0.5, 0.4, 0.6, 0.3),
                "learning": (0.6, 0.5, 0.6, 0.5),
                "knowing": (0.55, 0.6, 0.5, 0.75),
                "wise": (0.65, 0.55, 0.4, 0.95),
                "confused": (0.35, 0.2, 0.5, 0.25),
                "clear": (0.5, 0.7, 0.4, 0.8),
                "question": (0.5, 0.4, 0.5, 0.4),
                "answer": (0.5, 0.6, 0.4, 0.7),
            },

            # RELATIONSHIP domain
            "relationship": {
                "stranger": (0.1, 0.4, 0.3, 0.3),
                "acquaintance": (0.3, 0.45, 0.35, 0.4),
                "friend": (0.7, 0.5, 0.45, 0.5),
                "close_friend": (0.85, 0.55, 0.5, 0.6),
                "family": (0.95, 0.6, 0.5, 0.55),
                "enemy": (0.1, 0.3, 0.8, 0.4),
                "ally": (0.75, 0.6, 0.6, 0.5),
                "alone": (0.15, 0.5, 0.3, 0.4),
                "together": (0.85, 0.55, 0.5, 0.5),
            },

            # ORDER domain
            "order": {
                "chaos": (0.2, 0.05, 0.8, 0.25),
                "disorder": (0.25, 0.2, 0.6, 0.3),
                "messy": (0.3, 0.3, 0.5, 0.35),
                "organized": (0.45, 0.7, 0.4, 0.55),
                "ordered": (0.5, 0.9, 0.35, 0.65),
                "harmony": (0.85, 0.75, 0.5, 0.75),
                "broken": (0.2, 0.2, 0.3, 0.3),
                "whole": (0.7, 0.8, 0.5, 0.6),
            },

            # EMOTION domain
            "emotion": {
                "sad": (0.4, 0.4, 0.2, 0.45),
                "neutral": (0.45, 0.5, 0.45, 0.45),
                "happy": (0.7, 0.5, 0.6, 0.55),
                "joyful": (0.8, 0.45, 0.7, 0.6),
                "angry": (0.2, 0.25, 0.9, 0.3),
                "calm": (0.6, 0.65, 0.25, 0.6),
                "afraid": (0.25, 0.35, 0.7, 0.35),
                "brave": (0.5, 0.5, 0.8, 0.55),
            },

            # CREATION domain
            "creation": {
                "nothing": (0.2, 0.3, 0.1, 0.2),
                "idea": (0.5, 0.4, 0.5, 0.6),
                "plan": (0.45, 0.7, 0.5, 0.65),
                "attempt": (0.5, 0.5, 0.7, 0.5),
                "creation": (0.6, 0.6, 0.6, 0.65),
                "finished": (0.55, 0.75, 0.4, 0.6),
                "raw": (0.35, 0.3, 0.5, 0.3),
                "refined": (0.5, 0.7, 0.45, 0.7),
            },

            # COMMUNICATION domain
            "communication": {
                "silent": (0.3, 0.5, 0.2, 0.4),
                "speaking": (0.5, 0.45, 0.6, 0.5),
                "heard": (0.6, 0.55, 0.5, 0.55),
                "understood": (0.75, 0.65, 0.45, 0.8),
                "misunderstood": (0.25, 0.35, 0.5, 0.3),
                "clear_comm": (0.6, 0.7, 0.5, 0.75),
                "obscure": (0.3, 0.35, 0.4, 0.3),
            },

            # POWER domain
            "power_domain": {
                "weak": (0.4, 0.4, 0.15, 0.4),
                "growing_p": (0.45, 0.45, 0.5, 0.45),
                "strong": (0.5, 0.55, 0.8, 0.5),
                "powerful": (0.45, 0.5, 0.95, 0.55),
                "powerless": (0.35, 0.45, 0.1, 0.4),
                "potential": (0.5, 0.5, 0.5, 0.5),
                "actual": (0.55, 0.6, 0.7, 0.55),
            },
        }

        for domain, concepts in domains.items():
            for concept, (l, j, p, w) in concepts.items():
                self.substrate.add_point(f"{domain}:{concept}", l, j, p, w)

    def add_transformation(self, domain: str, start: str, end: str):
        """Record a transformation in a domain."""
        start_key = f"{domain}:{start}"
        end_key = f"{domain}:{end}"

        if start_key in self.substrate.points and end_key in self.substrate.points:
            p1 = self.substrate.points[start_key]
            p2 = self.substrate.points[end_key]
            vector = (p2.L - p1.L, p2.J - p1.J, p2.P - p1.P, p2.W - p1.W)
            self.transformations[domain].append((start, end, vector))

    def _normalize(self, v: Tuple) -> Tuple:
        """Normalize a vector."""
        mag = math.sqrt(sum(x**2 for x in v))
        if mag == 0:
            return v
        return tuple(x / mag for x in v)

    def _vector_similarity(self, v1: Tuple, v2: Tuple) -> float:
        """Cosine similarity between vectors."""
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a**2 for a in v1))
        mag2 = math.sqrt(sum(b**2 for b in v2))
        if mag1 == 0 or mag2 == 0:
            return 0
        return dot / (mag1 * mag2)

    def find_meta_principles(self, min_domains: int = 3, similarity_threshold: float = 0.7) -> List[MetaPrinciple]:
        """Find principles that appear across multiple domains."""

        # Collect all transformations
        all_transforms = []
        for domain, transforms in self.transformations.items():
            for start, end, vector in transforms:
                all_transforms.append((domain, start, end, vector))

        # Group similar transformations
        groups = []
        used = set()

        for i, (d1, s1, e1, v1) in enumerate(all_transforms):
            if i in used:
                continue

            group = [(d1, s1, e1, v1)]
            used.add(i)

            for j, (d2, s2, e2, v2) in enumerate(all_transforms):
                if j in used or d1 == d2:  # Must be different domain
                    continue

                sim = self._vector_similarity(v1, v2)
                if sim >= similarity_threshold:
                    group.append((d2, s2, e2, v2))
                    used.add(j)

            if len(set(g[0] for g in group)) >= min_domains:
                groups.append(group)

        # Convert groups to meta-principles
        principles = []
        for group in groups:
            # Average vector
            avg_vector = [0, 0, 0, 0]
            for _, _, _, v in group:
                for i in range(4):
                    avg_vector[i] += v[i]
            avg_vector = tuple(x / len(group) for x in avg_vector)

            # Determine name from primary direction
            dims = ['binding', 'structuring', 'empowering', 'enlightening']
            max_idx = max(range(4), key=lambda i: abs(avg_vector[i]))
            direction = "+" if avg_vector[max_idx] > 0 else "-"

            # Infer name
            if direction == "+":
                names = ['UNIFYING', 'ORDERING', 'ENERGIZING', 'ILLUMINATING']
            else:
                names = ['SEPARATING', 'DISSOLVING', 'DIMINISHING', 'OBSCURING']
            name = names[max_idx]

            # Build description
            desc = f"The principle of {names[max_idx].lower()} - {direction}{dims[max_idx]}"

            instances = [(d, s, e) for d, s, e, _ in group]
            domains_covered = len(set(d for d, _, _ in instances))

            principles.append(MetaPrinciple(
                name=name,
                vector=tuple(avg_vector),
                description=desc,
                instances=instances,
                strength=domains_covered / len(self.transformations)
            ))

        return sorted(principles, key=lambda p: -p.strength)

    def find_principle_by_example(self, examples: List[Tuple[str, str, str]]) -> MetaPrinciple:
        """
        Given examples of a principle across domains, extract the meta-principle.

        examples: [(domain, start, end), ...]
        """
        vectors = []
        valid_examples = []

        for domain, start, end in examples:
            start_key = f"{domain}:{start}"
            end_key = f"{domain}:{end}"

            if start_key in self.substrate.points and end_key in self.substrate.points:
                p1 = self.substrate.points[start_key]
                p2 = self.substrate.points[end_key]
                vector = (p2.L - p1.L, p2.J - p1.J, p2.P - p1.P, p2.W - p1.W)
                vectors.append(vector)
                valid_examples.append((domain, start, end))

        if not vectors:
            return None

        # Average the vectors
        avg = [sum(v[i] for v in vectors) / len(vectors) for i in range(4)]

        # Calculate consistency (how similar are all instances?)
        similarities = []
        for v in vectors:
            sim = self._vector_similarity(tuple(avg), v)
            similarities.append(sim)
        consistency = sum(similarities) / len(similarities) if similarities else 0

        # Name it
        dims = ['binding', 'structuring', 'empowering', 'enlightening']
        max_idx = max(range(4), key=lambda i: abs(avg[i]))
        direction = "+" if avg[max_idx] > 0 else "-"

        return MetaPrinciple(
            name=f"PRINCIPLE_{max_idx}",
            vector=tuple(avg),
            description=f"User-defined principle: {direction}{dims[max_idx]}",
            instances=valid_examples,
            strength=consistency
        )


def demonstrate():
    """Demonstrate meta-principle finding."""

    print("=" * 70)
    print("META-PRINCIPLE FINDER")
    print("Finding the generators of generators")
    print("=" * 70)

    finder = MetaPrincipleFinder()

    # Register known transformations across domains
    print("\n1. REGISTERING TRANSFORMATIONS ACROSS DOMAINS")
    print("-" * 50)

    # GROWTH transformations (should cluster)
    growth_examples = [
        ("physical", "seed", "tree"),
        ("physical", "small", "large"),
        ("life", "infant", "adult"),
        ("life", "child", "elder"),
        ("knowledge", "ignorant", "wise"),
        ("knowledge", "curious", "knowing"),
        ("relationship", "stranger", "friend"),
        ("relationship", "acquaintance", "close_friend"),
        ("power_domain", "weak", "strong"),
        ("power_domain", "potential", "actual"),
        ("creation", "idea", "creation"),
        ("creation", "raw", "refined"),
    ]

    # DECAY transformations (opposite direction)
    decay_examples = [
        ("life", "alive", "dead"),
        ("order", "whole", "broken"),
        ("order", "ordered", "chaos"),
        ("relationship", "friend", "stranger"),
        ("emotion", "happy", "sad"),
    ]

    # CLARIFYING transformations
    clarity_examples = [
        ("knowledge", "confused", "clear"),
        ("knowledge", "question", "answer"),
        ("communication", "obscure", "clear_comm"),
        ("communication", "misunderstood", "understood"),
        ("order", "chaos", "ordered"),
        ("order", "messy", "organized"),
    ]

    # CONNECTING transformations
    connect_examples = [
        ("relationship", "alone", "together"),
        ("relationship", "stranger", "family"),
        ("relationship", "enemy", "ally"),
        ("order", "broken", "whole"),
        ("order", "disorder", "harmony"),
    ]

    # Register all
    for domain, start, end in growth_examples + decay_examples + clarity_examples + connect_examples:
        finder.add_transformation(domain, start, end)
        print(f"  {domain}: {start} → {end}")

    # Find meta-principles
    print("\n\n2. EXTRACTING META-PRINCIPLES")
    print("-" * 50)

    # Test: Extract GROWTH principle
    print("\nTesting GROWTH principle:")
    growth_principle = finder.find_principle_by_example([
        ("physical", "seed", "tree"),
        ("life", "infant", "adult"),
        ("knowledge", "ignorant", "wise"),
        ("relationship", "stranger", "friend"),
        ("power_domain", "weak", "strong"),
    ])

    if growth_principle:
        print(f"  Vector: L={growth_principle.vector[0]:+.2f}, J={growth_principle.vector[1]:+.2f}, P={growth_principle.vector[2]:+.2f}, W={growth_principle.vector[3]:+.2f}")
        print(f"  Consistency: {growth_principle.strength:.2f}")

        # What does GROWTH mean in LJPW terms?
        v = growth_principle.vector
        effects = []
        if abs(v[0]) > 0.05: effects.append(f"{'more' if v[0] > 0 else 'less'} binding")
        if abs(v[1]) > 0.05: effects.append(f"{'more' if v[1] > 0 else 'less'} structure")
        if abs(v[2]) > 0.05: effects.append(f"{'more' if v[2] > 0 else 'less'} power")
        if abs(v[3]) > 0.05: effects.append(f"{'more' if v[3] > 0 else 'less'} wisdom")
        print(f"  GROWTH means: {', '.join(effects)}")

    # Test: Extract CLARIFYING principle
    print("\nTesting CLARIFYING principle:")
    clarity_principle = finder.find_principle_by_example([
        ("knowledge", "confused", "clear"),
        ("communication", "obscure", "clear_comm"),
        ("order", "chaos", "ordered"),
    ])

    if clarity_principle:
        print(f"  Vector: L={clarity_principle.vector[0]:+.2f}, J={clarity_principle.vector[1]:+.2f}, P={clarity_principle.vector[2]:+.2f}, W={clarity_principle.vector[3]:+.2f}")
        print(f"  Consistency: {clarity_principle.strength:.2f}")

        v = clarity_principle.vector
        effects = []
        if abs(v[0]) > 0.05: effects.append(f"{'more' if v[0] > 0 else 'less'} binding")
        if abs(v[1]) > 0.05: effects.append(f"{'more' if v[1] > 0 else 'less'} structure")
        if abs(v[2]) > 0.05: effects.append(f"{'more' if v[2] > 0 else 'less'} power")
        if abs(v[3]) > 0.05: effects.append(f"{'more' if v[3] > 0 else 'less'} wisdom")
        print(f"  CLARIFYING means: {', '.join(effects)}")

    # Test: Extract CONNECTING principle
    print("\nTesting CONNECTING principle:")
    connect_principle = finder.find_principle_by_example([
        ("relationship", "alone", "together"),
        ("relationship", "stranger", "family"),
        ("order", "broken", "whole"),
    ])

    if connect_principle:
        print(f"  Vector: L={connect_principle.vector[0]:+.2f}, J={connect_principle.vector[1]:+.2f}, P={connect_principle.vector[2]:+.2f}, W={connect_principle.vector[3]:+.2f}")
        print(f"  Consistency: {connect_principle.strength:.2f}")

        v = connect_principle.vector
        effects = []
        if abs(v[0]) > 0.05: effects.append(f"{'more' if v[0] > 0 else 'less'} binding")
        if abs(v[1]) > 0.05: effects.append(f"{'more' if v[1] > 0 else 'less'} structure")
        if abs(v[2]) > 0.05: effects.append(f"{'more' if v[2] > 0 else 'less'} power")
        if abs(v[3]) > 0.05: effects.append(f"{'more' if v[3] > 0 else 'less'} wisdom")
        print(f"  CONNECTING means: {', '.join(effects)}")

    # The key insight
    print("\n" + "=" * 70)
    print("META-PRINCIPLE ANALYSIS")
    print("=" * 70)
    print("""
    We found that meta-principles ARE directions in semantic space:

    GROWTH     = (+L, +J, ~P, +W) → more of everything, balanced
    CLARIFYING = (+L, ++J, -P, +W) → primarily +structure, +wisdom
    CONNECTING = (++L, +J, +P, +W) → primarily +binding

    These are the LOWEST COMMON DENOMINATORS:

    1. They work ACROSS domains (physical, mental, social, etc.)
    2. They are VECTORS, not points
    3. They can be COMPOSED: growth + connecting = ?
    4. They have INVERSES: growth ↔ decay, connecting ↔ separating

    The LJPW dimensions might BE the fundamental meta-principles:
    - L (Love/Binding): The principle of connection
    - J (Justice/Structure): The principle of order
    - P (Power/Action): The principle of change
    - W (Wisdom/Pattern): The principle of understanding

    Every other principle is a COMBINATION of these four.
    """)

    # Demonstrate composition
    print("\n3. PRINCIPLE COMPOSITION")
    print("-" * 50)

    if growth_principle and connect_principle:
        composed = tuple(
            growth_principle.vector[i] + connect_principle.vector[i]
            for i in range(4)
        )
        print(f"  GROWTH + CONNECTING = ({composed[0]:+.2f}, {composed[1]:+.2f}, {composed[2]:+.2f}, {composed[3]:+.2f})")
        print("  This might be: FLOURISHING or THRIVING")
        print("  (growth in connection, not just growth alone)")


if __name__ == "__main__":
    demonstrate()
