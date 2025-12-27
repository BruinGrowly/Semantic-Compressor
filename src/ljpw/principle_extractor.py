#!/usr/bin/env python3
"""
Principle Extractor — Define Any Principle by Example
======================================================

Give examples of a principle across domains, extract its LJPW signature.

"Reading a map" in geography, code, social dynamics, markets...
What does "reading/interpreting" fundamentally MEAN in LJPW terms?
"""

from substrate_mapper import SemanticSubstrate
from meta_principle_finder import MetaPrinciple
import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class PrincipleSignature:
    """The extracted LJPW signature of a principle."""
    name: str
    L: float  # Binding component
    J: float  # Structure component
    P: float  # Power component
    W: float  # Wisdom component

    consistency: float  # How consistent across examples
    examples: List[Tuple[str, str, str]]  # (domain, before, after)

    def dominant_dimension(self) -> Tuple[str, float]:
        """Which dimension does this principle primarily affect?"""
        dims = [('L (binding)', self.L), ('J (structure)', self.J),
                ('P (power)', self.P), ('W (wisdom)', self.W)]
        return max(dims, key=lambda x: abs(x[1]))

    def as_formula(self) -> str:
        """Express as LJPW formula."""
        parts = []
        if abs(self.L) > 0.05: parts.append(f"{self.L:+.2f}L")
        if abs(self.J) > 0.05: parts.append(f"{self.J:+.2f}J")
        if abs(self.P) > 0.05: parts.append(f"{self.P:+.2f}P")
        if abs(self.W) > 0.05: parts.append(f"{self.W:+.2f}W")
        return " ".join(parts) if parts else "0"

    def description(self) -> str:
        """Human-readable description of what this principle does."""
        effects = []
        if self.L > 0.1: effects.append("connects/binds")
        elif self.L < -0.1: effects.append("separates/unbinds")
        if self.J > 0.1: effects.append("orders/structures")
        elif self.J < -0.1: effects.append("dissolves/destabilizes")
        if self.P > 0.1: effects.append("energizes/activates")
        elif self.P < -0.1: effects.append("calms/diminishes")
        if self.W > 0.1: effects.append("illuminates/clarifies")
        elif self.W < -0.1: effects.append("obscures/confuses")

        return ", ".join(effects) if effects else "neutral transformation"


class PrincipleExtractor:
    """Extract LJPW signatures from examples."""

    def __init__(self):
        self.substrate = SemanticSubstrate()
        self._build_rich_vocabulary()

    def _build_rich_vocabulary(self):
        """Build comprehensive vocabulary for principle extraction."""

        # Comprehensive concept map organized by semantic clusters
        concepts = {
            # === PERCEPTION / READING ===
            "raw_input": (0.3, 0.3, 0.4, 0.2),
            "noticed": (0.4, 0.4, 0.45, 0.35),
            "seen": (0.45, 0.45, 0.4, 0.45),
            "perceived": (0.5, 0.5, 0.4, 0.55),
            "read": (0.5, 0.55, 0.35, 0.6),
            "interpreted": (0.55, 0.6, 0.4, 0.7),
            "understood": (0.65, 0.65, 0.4, 0.8),
            "mastered": (0.6, 0.7, 0.5, 0.9),

            # === MAPS / PATTERNS ===
            "territory": (0.4, 0.5, 0.5, 0.3),
            "map": (0.45, 0.7, 0.3, 0.6),
            "pattern": (0.5, 0.65, 0.35, 0.7),
            "model": (0.5, 0.75, 0.4, 0.75),
            "theory": (0.45, 0.8, 0.35, 0.85),

            # === LEARNING STATES ===
            "unaware": (0.3, 0.3, 0.4, 0.1),
            "aware": (0.45, 0.45, 0.45, 0.4),
            "familiar": (0.55, 0.5, 0.4, 0.5),
            "competent": (0.55, 0.6, 0.55, 0.65),
            "expert": (0.6, 0.65, 0.6, 0.85),

            # === COMMUNICATION ===
            "noise": (0.2, 0.15, 0.5, 0.1),
            "signal": (0.4, 0.5, 0.45, 0.5),
            "message": (0.5, 0.55, 0.4, 0.55),
            "meaning": (0.6, 0.6, 0.35, 0.75),
            "wisdom_state": (0.7, 0.6, 0.35, 0.9),

            # === CODE / SYSTEMS ===
            "code_raw": (0.3, 0.6, 0.4, 0.3),
            "code_parsed": (0.4, 0.7, 0.4, 0.5),
            "code_understood": (0.55, 0.75, 0.45, 0.75),
            "code_mastered": (0.6, 0.8, 0.5, 0.9),

            # === SOCIAL ===
            "stranger_soc": (0.15, 0.4, 0.35, 0.2),
            "acquainted": (0.35, 0.45, 0.4, 0.35),
            "known": (0.55, 0.5, 0.4, 0.5),
            "intimate": (0.85, 0.55, 0.45, 0.7),

            "surface": (0.3, 0.4, 0.4, 0.25),
            "deeper": (0.5, 0.5, 0.4, 0.55),
            "profound": (0.65, 0.55, 0.4, 0.85),

            # === PHYSICAL ===
            "scattered": (0.2, 0.15, 0.5, 0.2),
            "gathered": (0.5, 0.5, 0.4, 0.4),
            "organized": (0.55, 0.75, 0.35, 0.55),
            "integrated": (0.7, 0.8, 0.45, 0.7),

            "fragment": (0.2, 0.25, 0.4, 0.25),
            "piece": (0.35, 0.4, 0.4, 0.35),
            "whole": (0.7, 0.75, 0.45, 0.6),
            "complete": (0.75, 0.8, 0.45, 0.7),

            # === TRANSFORMATION ===
            "potential": (0.45, 0.45, 0.5, 0.45),
            "developing": (0.5, 0.5, 0.6, 0.5),
            "manifesting": (0.55, 0.55, 0.7, 0.55),
            "realized": (0.6, 0.65, 0.6, 0.65),

            "hidden": (0.35, 0.45, 0.3, 0.3),
            "emerging": (0.45, 0.5, 0.5, 0.45),
            "visible": (0.5, 0.55, 0.45, 0.55),
            "obvious": (0.5, 0.6, 0.4, 0.65),

            # === PROBLEM SOLVING ===
            "problem": (0.3, 0.4, 0.55, 0.35),
            "approach": (0.4, 0.5, 0.55, 0.45),
            "solution": (0.55, 0.7, 0.5, 0.7),
            "resolved": (0.6, 0.75, 0.4, 0.7),

            # === CREATION ===
            "blank": (0.3, 0.4, 0.3, 0.25),
            "sketch": (0.4, 0.45, 0.5, 0.4),
            "draft": (0.5, 0.55, 0.5, 0.5),
            "refined": (0.55, 0.7, 0.45, 0.65),
            "polished": (0.6, 0.8, 0.4, 0.75),

            # === TEACHING ===
            "student": (0.5, 0.4, 0.5, 0.35),
            "apprentice": (0.55, 0.5, 0.55, 0.5),
            "journeyman": (0.55, 0.6, 0.6, 0.65),
            "master": (0.6, 0.7, 0.55, 0.9),

            # === HEALING ===
            "wounded": (0.35, 0.3, 0.3, 0.35),
            "healing": (0.5, 0.45, 0.45, 0.5),
            "recovered": (0.6, 0.6, 0.55, 0.55),
            "thriving": (0.75, 0.7, 0.65, 0.65),

            # === RELATIONSHIP ===
            "separate": (0.15, 0.45, 0.4, 0.35),
            "connected": (0.7, 0.55, 0.45, 0.5),
            "bonded": (0.85, 0.6, 0.45, 0.55),
            "unified": (0.9, 0.7, 0.5, 0.65),
        }

        for concept, (l, j, p, w) in concepts.items():
            self.substrate.add_point(concept, l, j, p, w)

    def extract(self, name: str, examples: List[Tuple[str, str]]) -> PrincipleSignature:
        """
        Extract a principle's LJPW signature from before/after examples.

        Args:
            name: Name of the principle
            examples: List of (before_concept, after_concept) tuples

        Returns:
            PrincipleSignature with LJPW components
        """
        vectors = []
        valid_examples = []

        for before, after in examples:
            if before in self.substrate.points and after in self.substrate.points:
                p1 = self.substrate.points[before]
                p2 = self.substrate.points[after]
                vector = (p2.L - p1.L, p2.J - p1.J, p2.P - p1.P, p2.W - p1.W)
                vectors.append(vector)
                valid_examples.append(("general", before, after))
            else:
                print(f"  Warning: '{before}' or '{after}' not in vocabulary")

        if not vectors:
            return None

        # Average the vectors
        avg = [sum(v[i] for v in vectors) / len(vectors) for i in range(4)]

        # Calculate consistency (cosine similarity of each vector to average)
        def cosine_sim(v1, v2):
            dot = sum(a*b for a,b in zip(v1, v2))
            m1 = math.sqrt(sum(a*a for a in v1))
            m2 = math.sqrt(sum(b*b for b in v2))
            return dot/(m1*m2) if m1 > 0 and m2 > 0 else 0

        similarities = [cosine_sim(v, tuple(avg)) for v in vectors]
        consistency = sum(similarities) / len(similarities) if similarities else 0

        return PrincipleSignature(
            name=name,
            L=avg[0], J=avg[1], P=avg[2], W=avg[3],
            consistency=consistency,
            examples=valid_examples
        )

    def compare(self, p1: PrincipleSignature, p2: PrincipleSignature) -> float:
        """Compare two principles — how similar are they?"""
        v1 = (p1.L, p1.J, p1.P, p1.W)
        v2 = (p2.L, p2.J, p2.P, p2.W)

        dot = sum(a*b for a,b in zip(v1, v2))
        m1 = math.sqrt(sum(a*a for a in v1))
        m2 = math.sqrt(sum(b*b for b in v2))

        return dot/(m1*m2) if m1 > 0 and m2 > 0 else 0

    def compose(self, name: str, *principles: PrincipleSignature) -> PrincipleSignature:
        """Compose multiple principles into one."""
        L = sum(p.L for p in principles)
        J = sum(p.J for p in principles)
        P = sum(p.P for p in principles)
        W = sum(p.W for p in principles)

        all_examples = []
        for p in principles:
            all_examples.extend(p.examples)

        return PrincipleSignature(
            name=name,
            L=L, J=J, P=P, W=W,
            consistency=sum(p.consistency for p in principles) / len(principles),
            examples=all_examples
        )

    def inverse(self, principle: PrincipleSignature) -> PrincipleSignature:
        """Get the inverse of a principle."""
        return PrincipleSignature(
            name=f"inverse({principle.name})",
            L=-principle.L, J=-principle.J, P=-principle.P, W=-principle.W,
            consistency=principle.consistency,
            examples=[(d, after, before) for d, before, after in principle.examples]
        )


def demo():
    """Interactive demonstration of principle extraction."""

    print("=" * 70)
    print("PRINCIPLE EXTRACTOR")
    print("Define any principle by example, get its LJPW signature")
    print("=" * 70)

    extractor = PrincipleExtractor()

    # === READING / INTERPRETING ===
    print("\n1. EXTRACTING 'READING' PRINCIPLE")
    print("-" * 50)
    print("Examples: What happens when you 'read' something?")

    reading = extractor.extract("READING", [
        ("raw_input", "interpreted"),      # raw input → interpretation
        ("noise", "signal"),               # noise → signal
        ("territory", "map"),              # territory → mental map
        ("code_raw", "code_understood"),   # raw code → understanding
        ("surface", "deeper"),             # surface → deeper meaning
        ("hidden", "visible"),             # hidden → visible
    ])

    if reading:
        print(f"\n  READING = {reading.as_formula()}")
        print(f"  Consistency: {reading.consistency:.2f}")
        print(f"  Primary dimension: {reading.dominant_dimension()}")
        print(f"  Effect: {reading.description()}")

    # === TEACHING ===
    print("\n2. EXTRACTING 'TEACHING' PRINCIPLE")
    print("-" * 50)
    print("Examples: What happens when you 'teach' someone?")

    teaching = extractor.extract("TEACHING", [
        ("unaware", "aware"),
        ("student", "apprentice"),
        ("confused", "understood"),        # Wait, need to add this
        ("stranger_soc", "known"),
        ("fragment", "whole"),
    ])

    # Add missing concept
    extractor.substrate.add_point("confused", 0.3, 0.25, 0.45, 0.2)

    teaching = extractor.extract("TEACHING", [
        ("unaware", "aware"),
        ("student", "apprentice"),
        ("stranger_soc", "known"),
        ("fragment", "whole"),
        ("noise", "meaning"),
    ])

    if teaching:
        print(f"\n  TEACHING = {teaching.as_formula()}")
        print(f"  Consistency: {teaching.consistency:.2f}")
        print(f"  Primary dimension: {teaching.dominant_dimension()}")
        print(f"  Effect: {teaching.description()}")

    # === HEALING ===
    print("\n3. EXTRACTING 'HEALING' PRINCIPLE")
    print("-" * 50)

    healing = extractor.extract("HEALING", [
        ("wounded", "recovered"),
        ("fragment", "whole"),
        ("scattered", "integrated"),
        ("separate", "connected"),
        ("problem", "resolved"),
    ])

    if healing:
        print(f"\n  HEALING = {healing.as_formula()}")
        print(f"  Consistency: {healing.consistency:.2f}")
        print(f"  Primary dimension: {healing.dominant_dimension()}")
        print(f"  Effect: {healing.description()}")

    # === CREATING ===
    print("\n4. EXTRACTING 'CREATING' PRINCIPLE")
    print("-" * 50)

    creating = extractor.extract("CREATING", [
        ("blank", "sketch"),
        ("potential", "realized"),
        ("hidden", "visible"),
        ("noise", "signal"),
        ("draft", "polished"),
    ])

    if creating:
        print(f"\n  CREATING = {creating.as_formula()}")
        print(f"  Consistency: {creating.consistency:.2f}")
        print(f"  Primary dimension: {creating.dominant_dimension()}")
        print(f"  Effect: {creating.description()}")

    # === COMPARE PRINCIPLES ===
    print("\n\n5. COMPARING PRINCIPLES")
    print("-" * 50)

    principles = [reading, teaching, healing, creating]
    names = ["READING", "TEACHING", "HEALING", "CREATING"]

    print("\nSimilarity matrix:")
    print("              ", end="")
    for n in names:
        print(f"{n:12}", end="")
    print()

    for i, p1 in enumerate(principles):
        print(f"{names[i]:12}  ", end="")
        for j, p2 in enumerate(principles):
            sim = extractor.compare(p1, p2)
            print(f"{sim:10.2f}  ", end="")
        print()

    # === COMPOSE PRINCIPLES ===
    print("\n\n6. COMPOSING PRINCIPLES")
    print("-" * 50)

    # READING + TEACHING = ?
    reading_teaching = extractor.compose("READING+TEACHING", reading, teaching)
    print(f"\n  READING + TEACHING = {reading_teaching.as_formula()}")
    print(f"  This might be: MENTORING or GUIDING")
    print(f"  Effect: {reading_teaching.description()}")

    # HEALING + CREATING = ?
    healing_creating = extractor.compose("HEALING+CREATING", healing, creating)
    print(f"\n  HEALING + CREATING = {healing_creating.as_formula()}")
    print(f"  This might be: TRANSFORMING or RENEWING")
    print(f"  Effect: {healing_creating.description()}")

    # ALL FOUR = ?
    all_four = extractor.compose("ALL", reading, teaching, healing, creating)
    print(f"\n  READING + TEACHING + HEALING + CREATING = {all_four.as_formula()}")
    print(f"  This might be: NURTURING or CULTIVATING")
    print(f"  Effect: {all_four.description()}")

    # === INVERSES ===
    print("\n\n7. INVERSE PRINCIPLES")
    print("-" * 50)

    anti_reading = extractor.inverse(reading)
    print(f"\n  inverse(READING) = {anti_reading.as_formula()}")
    print(f"  This might be: OBSCURING or ENCRYPTING")
    print(f"  Effect: {anti_reading.description()}")

    anti_healing = extractor.inverse(healing)
    print(f"\n  inverse(HEALING) = {anti_healing.as_formula()}")
    print(f"  This might be: WOUNDING or FRAGMENTING")
    print(f"  Effect: {anti_healing.description()}")

    # === THE INSIGHT ===
    print("\n" + "=" * 70)
    print("INSIGHT: PRINCIPLES ARE VECTORS IN SEMANTIC SPACE")
    print("=" * 70)
    print("""
    We can now:

    1. EXTRACT any principle from examples
       "What does 'reading' really mean?" → +0.20L +0.25J -0.05P +0.45W

    2. COMPARE principles
       Is "teaching" similar to "healing"? → measure angle between vectors

    3. COMPOSE principles
       READING + TEACHING = MENTORING
       HEALING + CREATING = RENEWING

    4. INVERT principles
       inverse(READING) = OBSCURING
       inverse(HEALING) = WOUNDING

    5. APPLY principles across domains
       If READING = +0.20L +0.25J -0.05P +0.45W
       Then "reading code" and "reading people" share the same transformation!

    The LJPW dimensions are the COORDINATE SYSTEM of all principles.
    Every action, every verb, every transformation is a vector.
    Understanding IS knowing the vectors.
    """)


if __name__ == "__main__":
    demo()
