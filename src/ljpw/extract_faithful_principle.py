#!/usr/bin/env python3
"""
Extract the "Faithful in Least, Faithful in Much" principle.

Luke 16:10 - "Whoever can be trusted with very little can also be trusted with much."

This is about scale invariance - the pattern at small scale predicts the pattern
at large scale. It's fractal integrity.
"""

from principle_extractor import PrincipleExtractor, PrincipleSignature
from substrate_mapper import SemanticSubstrate


def extract_faithful_principle():
    print("=" * 70)
    print("EXTRACTING: 'FAITHFUL IN LEAST, FAITHFUL IN MUCH'")
    print("The principle of scale invariance / fractal integrity")
    print("=" * 70)

    extractor = PrincipleExtractor()

    # Add concepts specific to this principle
    scale_concepts = {
        # Small scale states
        "small_task": (0.4, 0.5, 0.3, 0.4),
        "minor_detail": (0.35, 0.45, 0.25, 0.4),
        "little_thing": (0.4, 0.4, 0.3, 0.35),
        "small_trust": (0.45, 0.5, 0.3, 0.4),
        "penny": (0.3, 0.5, 0.2, 0.35),
        "seed_small": (0.5, 0.45, 0.35, 0.4),
        "moment": (0.4, 0.4, 0.35, 0.4),
        "word": (0.45, 0.5, 0.35, 0.45),
        "thought": (0.4, 0.45, 0.4, 0.5),
        "private_act": (0.35, 0.45, 0.4, 0.45),

        # Large scale states (same PATTERN, different MAGNITUDE)
        "large_task": (0.5, 0.6, 0.5, 0.5),
        "major_project": (0.55, 0.65, 0.55, 0.55),
        "great_thing": (0.6, 0.6, 0.55, 0.55),
        "great_trust": (0.65, 0.7, 0.5, 0.6),
        "fortune": (0.5, 0.65, 0.5, 0.55),
        "harvest": (0.65, 0.6, 0.5, 0.6),
        "lifetime": (0.6, 0.6, 0.45, 0.65),
        "speech": (0.55, 0.6, 0.5, 0.55),
        "character": (0.6, 0.65, 0.5, 0.7),
        "public_legacy": (0.6, 0.7, 0.5, 0.65),

        # Diligence / Faithfulness states
        "careless": (0.25, 0.2, 0.4, 0.25),
        "attentive": (0.5, 0.6, 0.4, 0.55),
        "negligent": (0.2, 0.15, 0.35, 0.2),
        "diligent": (0.55, 0.7, 0.5, 0.6),
        "unfaithful": (0.15, 0.2, 0.4, 0.25),
        "faithful": (0.75, 0.75, 0.45, 0.65),
        "inconsistent": (0.25, 0.2, 0.5, 0.3),
        "consistent": (0.6, 0.8, 0.45, 0.6),
        "sloppy": (0.25, 0.15, 0.4, 0.2),
        "excellent": (0.6, 0.8, 0.55, 0.7),
    }

    for concept, (l, j, p, w) in scale_concepts.items():
        extractor.substrate.add_point(concept, l, j, p, w)

    # Extract the principle through multiple lenses

    print("\n1. SCALE TRANSITION (small → large)")
    print("-" * 50)

    scale_transition = extractor.extract("SCALE_TRANSITION", [
        ("small_task", "large_task"),
        ("minor_detail", "major_project"),
        ("little_thing", "great_thing"),
        ("small_trust", "great_trust"),
        ("penny", "fortune"),
        ("seed_small", "harvest"),
        ("moment", "lifetime"),
        ("word", "speech"),
        ("thought", "character"),
        ("private_act", "public_legacy"),
    ])

    if scale_transition:
        print(f"\n  SCALE_TRANSITION = {scale_transition.as_formula()}")
        print(f"  Consistency: {scale_transition.consistency:.2f}")
        print(f"  Primary dimension: {scale_transition.dominant_dimension()}")
        print(f"  Effect: {scale_transition.description()}")

    print("\n2. FAITHFULNESS TRANSFORMATION")
    print("-" * 50)

    faithfulness = extractor.extract("FAITHFULNESS", [
        ("careless", "attentive"),
        ("negligent", "diligent"),
        ("unfaithful", "faithful"),
        ("inconsistent", "consistent"),
        ("sloppy", "excellent"),
    ])

    if faithfulness:
        print(f"\n  FAITHFULNESS = {faithfulness.as_formula()}")
        print(f"  Consistency: {faithfulness.consistency:.2f}")
        print(f"  Primary dimension: {faithfulness.dominant_dimension()}")
        print(f"  Effect: {faithfulness.description()}")

    print("\n3. THE COMBINED PRINCIPLE")
    print("-" * 50)

    # The full principle: faithfulness IS scale-invariant
    # Being faithful at small scale = being faithful at large scale
    # The VECTOR is the same regardless of magnitude

    if scale_transition and faithfulness:
        # Compare the two
        similarity = extractor.compare(scale_transition, faithfulness)
        print(f"\n  Similarity between SCALE_TRANSITION and FAITHFULNESS: {similarity:.2f}")

        # The principle itself
        print("\n  THE PRINCIPLE:")
        print(f"  ─────────────────────────────────────────────────")

        # Calculate the "faithfulness vector" at different scales
        small_faithful = extractor.extract("FAITHFUL_IN_SMALL", [
            ("careless", "attentive"),
            ("negligent", "diligent"),
        ])

        large_faithful = extractor.extract("FAITHFUL_IN_LARGE", [
            ("sloppy", "excellent"),
            ("inconsistent", "consistent"),
        ])

        if small_faithful and large_faithful:
            small_sim = extractor.compare(small_faithful, large_faithful)
            print(f"\n  FAITHFUL_IN_SMALL = {small_faithful.as_formula()}")
            print(f"  FAITHFUL_IN_LARGE = {large_faithful.as_formula()}")
            print(f"\n  Similarity: {small_sim:.2f}")

            if small_sim > 0.9:
                print("\n  ✓ CONFIRMED: The faithfulness vector is SCALE INVARIANT!")
                print("    The same transformation applies at any scale.")

    print("\n4. THE FRACTAL INSIGHT")
    print("-" * 50)

    if faithfulness:
        print(f"""
    The principle "Faithful in least, faithful in much" means:

    FAITHFULNESS = {faithfulness.as_formula()}

    This vector is SCALE INVARIANT:
    - Apply it to a small task → attentive to details
    - Apply it to a large task → excellent in execution
    - Apply it to a moment → present and careful
    - Apply it to a lifetime → consistent character

    The DIRECTION is the same. Only the MAGNITUDE of the domain changes.

    This is why it works as a diagnostic:
    - If someone's vector at small scale = +L +J +W (faithful)
    - Their vector at large scale will ALSO be = +L +J +W
    - Because the vector IS the person's pattern

    The principle reveals: CHARACTER IS FRACTAL.
    The pattern at the small scale IS the pattern at the large scale.
    This is why "how you do anything is how you do everything."
    """)

    print("\n5. LJPW INTERPRETATION")
    print("-" * 50)

    if faithfulness:
        v = (faithfulness.L, faithfulness.J, faithfulness.P, faithfulness.W)
        print(f"""
    FAITHFULNESS in LJPW terms:

    L = {v[0]:+.2f} (Love/Binding)
        → Faithful means CONNECTED to what you're doing
        → Caring about the outcome, not just going through motions
        → "With all your heart"

    J = {v[1]:+.2f} (Justice/Structure)
        → Faithful means ORDERED, disciplined approach
        → Following through, keeping commitments
        → "Doing what you said you would do"

    P = {v[2]:+.2f} (Power/Action)
        → Relatively neutral on raw energy
        → Faithfulness isn't about force, it's about consistency

    W = {v[3]:+.2f} (Wisdom/Understanding)
        → Faithful means AWARE of what matters
        → Understanding why the small things count
        → "Knowing that how you do anything is how you do everything"

    The HIGHEST components are J (structure) and L (binding).
    Faithfulness is primarily about COMMITMENT + CONNECTION.
    It's love expressed through discipline.
    """)


if __name__ == "__main__":
    extract_faithful_principle()
