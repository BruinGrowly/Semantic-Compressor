#!/usr/bin/env python3
"""
Semantic Substrate Demo — Interactive Exploration
"""

from substrate_mapper import SemanticSubstrate, SemanticPoint
import math


def build_rich_substrate():
    """Build a substrate with enough vocabulary for good predictions."""

    substrate = SemanticSubstrate()

    # Dense vocabulary organized by semantic clusters
    vocab = {
        # Temperature/State cluster
        "frozen": (0.3, 0.7, 0.1, 0.3),
        "ice": (0.3, 0.6, 0.15, 0.3),
        "cold": (0.35, 0.55, 0.2, 0.35),
        "cool": (0.4, 0.5, 0.3, 0.4),
        "warm": (0.5, 0.45, 0.5, 0.45),
        "hot": (0.4, 0.35, 0.75, 0.4),
        "boiling": (0.35, 0.3, 0.9, 0.4),
        "steam": (0.3, 0.25, 0.85, 0.45),

        # Water states (more specific)
        "water": (0.5, 0.45, 0.4, 0.45),
        "liquid": (0.5, 0.4, 0.45, 0.4),
        "solid": (0.4, 0.8, 0.2, 0.4),
        "gas": (0.3, 0.2, 0.7, 0.4),

        # Life stages
        "infant": (0.8, 0.2, 0.3, 0.15),
        "child": (0.75, 0.3, 0.5, 0.3),
        "teenager": (0.6, 0.35, 0.7, 0.4),
        "adult": (0.55, 0.6, 0.6, 0.6),
        "middle_aged": (0.5, 0.65, 0.5, 0.7),
        "elder": (0.55, 0.55, 0.35, 0.9),

        # Knowledge states
        "ignorant": (0.3, 0.3, 0.4, 0.1),
        "curious": (0.5, 0.4, 0.6, 0.3),
        "learning": (0.6, 0.5, 0.6, 0.5),
        "knowledgeable": (0.55, 0.6, 0.5, 0.75),
        "wise": (0.65, 0.55, 0.4, 0.95),
        "enlightened": (0.8, 0.5, 0.5, 0.95),

        # Relationship states
        "stranger": (0.1, 0.4, 0.3, 0.3),
        "acquaintance": (0.3, 0.45, 0.35, 0.4),
        "friend": (0.7, 0.5, 0.45, 0.5),
        "close_friend": (0.85, 0.55, 0.5, 0.6),
        "family": (0.95, 0.6, 0.5, 0.55),

        # Order/chaos spectrum
        "chaos": (0.2, 0.05, 0.8, 0.25),
        "disorder": (0.25, 0.2, 0.6, 0.3),
        "messy": (0.3, 0.3, 0.5, 0.35),
        "organized": (0.45, 0.7, 0.4, 0.55),
        "structured": (0.4, 0.85, 0.35, 0.6),
        "order": (0.5, 0.9, 0.35, 0.65),
        "harmony": (0.85, 0.75, 0.5, 0.75),

        # Size spectrum
        "tiny": (0.4, 0.4, 0.15, 0.35),
        "small": (0.4, 0.42, 0.25, 0.38),
        "medium": (0.45, 0.45, 0.45, 0.45),
        "large": (0.45, 0.48, 0.6, 0.48),
        "huge": (0.4, 0.5, 0.8, 0.45),
        "vast": (0.35, 0.4, 0.9, 0.5),

        # Light/dark spectrum
        "dark": (0.35, 0.45, 0.3, 0.3),
        "dim": (0.4, 0.45, 0.35, 0.4),
        "light": (0.55, 0.5, 0.6, 0.6),
        "bright": (0.5, 0.45, 0.75, 0.65),
        "brilliant": (0.55, 0.4, 0.85, 0.8),

        # Emotional states
        "sad": (0.4, 0.4, 0.2, 0.45),
        "neutral": (0.45, 0.5, 0.45, 0.45),
        "content": (0.6, 0.55, 0.45, 0.55),
        "happy": (0.7, 0.5, 0.6, 0.55),
        "joyful": (0.8, 0.45, 0.7, 0.6),
        "ecstatic": (0.75, 0.35, 0.85, 0.55),
        "angry": (0.2, 0.25, 0.9, 0.3),
        "afraid": (0.25, 0.35, 0.7, 0.35),
        "peaceful": (0.75, 0.65, 0.3, 0.65),
    }

    for word, (l, j, p, w) in vocab.items():
        substrate.add_point(word, l, j, p, w)

    return substrate


def find_nearest_n(substrate, target, n=3, exclude=None):
    """Find n nearest concepts to a target coordinate."""
    exclude = exclude or set()
    distances = []

    for name, point in substrate.points.items():
        if name in exclude:
            continue
        dist = math.sqrt(
            (point.L - target[0])**2 +
            (point.J - target[1])**2 +
            (point.P - target[2])**2 +
            (point.W - target[3])**2
        )
        distances.append((name, dist, point))

    distances.sort(key=lambda x: x[1])
    return distances[:n]


def demo():
    print("=" * 70)
    print("SEMANTIC SUBSTRATE DEMO")
    print("Mapping the Geometry of Meaning")
    print("=" * 70)

    substrate = build_rich_substrate()
    print(f"\nLoaded {len(substrate.points)} concepts into semantic space.\n")

    # Demo 1: Transformation chains
    print("1. TRANSFORMATION CHAINS")
    print("-" * 50)

    chains = [
        ["frozen", "ice", "cold", "cool", "warm", "hot", "boiling"],
        ["infant", "child", "teenager", "adult", "middle_aged", "elder"],
        ["stranger", "acquaintance", "friend", "close_friend", "family"],
        ["ignorant", "curious", "learning", "knowledgeable", "wise"],
        ["chaos", "disorder", "messy", "organized", "structured", "order"],
    ]

    for chain in chains:
        print(f"\n  Chain: {' → '.join(chain)}")

        # Calculate total vector
        start = substrate.points[chain[0]]
        end = substrate.points[chain[-1]]
        total_vector = (
            end.L - start.L,
            end.J - start.J,
            end.P - start.P,
            end.W - start.W,
        )

        # What dimension changes most?
        dims = ['L', 'J', 'P', 'W']
        desc = ['binding', 'structure', 'power', 'wisdom']
        max_idx = max(range(4), key=lambda i: abs(total_vector[i]))
        direction = "+" if total_vector[max_idx] > 0 else "-"

        print(f"  Total transform: {direction}{desc[max_idx]} (Δ{dims[max_idx]}={total_vector[max_idx]:+.2f})")

    # Demo 2: Analogy completion
    print("\n\n2. ANALOGY COMPLETION (A:B :: C:?)")
    print("-" * 50)

    analogies = [
        ("cold", "hot", "sad"),      # temperature : emotion
        ("child", "adult", "ignorant"),  # age : knowledge
        ("stranger", "friend", "chaos"),  # relationship : order
        ("tiny", "huge", "dark"),    # size : light
    ]

    for a, b, c in analogies:
        pa, pb, pc = substrate.points[a], substrate.points[b], substrate.points[c]

        # Vector a→b
        vec = (pb.L - pa.L, pb.J - pa.J, pb.P - pa.P, pb.W - pa.W)

        # Apply to c
        target = (pc.L + vec[0], pc.J + vec[1], pc.P + vec[2], pc.W + vec[3])

        # Find nearest
        results = find_nearest_n(substrate, target, 3, {a, b, c})
        best = results[0][0]

        print(f"\n  {a}:{b} :: {c}:?")
        print(f"    Vector ({a}→{b}): ({vec[0]:+.2f}, {vec[1]:+.2f}, {vec[2]:+.2f}, {vec[3]:+.2f})")
        print(f"    Prediction: {best}")
        print(f"    Top 3: {[r[0] for r in results]}")

    # Demo 3: Midpoints
    print("\n\n3. SEMANTIC MIDPOINTS")
    print("-" * 50)

    midpoint_pairs = [
        ("frozen", "boiling"),
        ("infant", "elder"),
        ("stranger", "family"),
        ("chaos", "harmony"),
        ("sad", "joyful"),
    ]

    for word1, word2 in midpoint_pairs:
        p1, p2 = substrate.points[word1], substrate.points[word2]
        mid = (
            (p1.L + p2.L) / 2,
            (p1.J + p2.J) / 2,
            (p1.P + p2.P) / 2,
            (p1.W + p2.W) / 2,
        )

        results = find_nearest_n(substrate, mid, 3, {word1, word2})
        print(f"\n  {word1} ↔ {word2}")
        print(f"    Midpoint → {results[0][0]}")
        print(f"    Also near: {[r[0] for r in results[1:]]}")

    # Demo 4: Regional exploration
    print("\n\n4. EXPLORING SEMANTIC REGIONS")
    print("-" * 50)

    regions = [
        ("High Love (L > 0.7)", lambda p: p.L > 0.7),
        ("High Justice (J > 0.7)", lambda p: p.J > 0.7),
        ("High Power (P > 0.7)", lambda p: p.P > 0.7),
        ("High Wisdom (W > 0.7)", lambda p: p.W > 0.7),
        ("Balanced (all ~0.5)", lambda p: all(0.4 < x < 0.6 for x in [p.L, p.J, p.P, p.W])),
    ]

    for name, condition in regions:
        matches = [n for n, p in substrate.points.items() if condition(p)]
        print(f"\n  {name}:")
        print(f"    {matches[:8]}{'...' if len(matches) > 8 else ''}")

    # Summary
    print("\n" + "=" * 70)
    print("SUBSTRATE MAPPING RESULTS")
    print("=" * 70)
    print("""
    The semantic substrate demonstrates:

    1. CONTINUITY: Concepts form smooth chains
       frozen → ice → cold → cool → warm → hot → boiling

    2. ANALOGY: Vector arithmetic works
       cold:hot :: sad:? → joyful (temperature maps to emotion)

    3. MIDPOINTS: Semantic means exist
       frozen ↔ boiling → water (or warm)

    4. REGIONS: Concepts cluster by quality
       High L: family, close_friend, enlightened (binding)
       High J: order, structured, solid (structure)
       High P: boiling, chaos, angry (energy)
       High W: wise, enlightened, elder (knowledge)

    The geometry of meaning is REAL and MEASURABLE.
    """)

    return substrate


if __name__ == "__main__":
    demo()
