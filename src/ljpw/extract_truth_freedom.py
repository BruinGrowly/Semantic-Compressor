#!/usr/bin/env python3
"""
Extract the "The Truth Shall Set You Free" principle.

John 8:32 - "And you will know the truth, and the truth will set you free."

This is about how truth leads to liberation.
What IS the relationship between knowing and freedom?
"""

from principle_extractor import PrincipleExtractor, PrincipleSignature
from substrate_mapper import SemanticSubstrate


def extract_truth_freedom():
    print("=" * 70)
    print("EXTRACTING: 'THE TRUTH SHALL SET YOU FREE'")
    print("The principle of truth → liberation")
    print("=" * 70)

    extractor = PrincipleExtractor()

    # Add concepts for truth and freedom
    concepts = {
        # === TRUTH STATES ===
        "lie": (0.15, 0.2, 0.5, 0.1),
        "deception": (0.1, 0.25, 0.55, 0.15),
        "illusion": (0.25, 0.3, 0.4, 0.2),
        "hidden": (0.3, 0.4, 0.35, 0.25),
        "obscured": (0.25, 0.35, 0.4, 0.2),
        "partial_truth": (0.4, 0.5, 0.4, 0.5),
        "honest": (0.6, 0.65, 0.4, 0.65),
        "transparent": (0.65, 0.7, 0.35, 0.7),
        "truth": (0.7, 0.8, 0.4, 0.9),
        "reality": (0.6, 0.85, 0.5, 0.85),

        # === BONDAGE STATES ===
        "enslaved": (0.2, 0.3, 0.2, 0.2),
        "trapped": (0.25, 0.35, 0.25, 0.25),
        "bound": (0.35, 0.4, 0.25, 0.3),
        "constrained": (0.4, 0.5, 0.3, 0.35),
        "limited": (0.4, 0.45, 0.35, 0.4),
        "burdened": (0.35, 0.4, 0.3, 0.35),
        "weighed_down": (0.3, 0.35, 0.25, 0.3),

        # === FREEDOM STATES ===
        "unconstrained": (0.5, 0.5, 0.6, 0.5),
        "released": (0.55, 0.55, 0.55, 0.55),
        "unburdened": (0.6, 0.55, 0.6, 0.55),
        "free": (0.65, 0.6, 0.7, 0.6),
        "liberated": (0.7, 0.65, 0.75, 0.65),
        "sovereign": (0.6, 0.7, 0.8, 0.7),

        # === AWARENESS STATES ===
        "blind": (0.3, 0.35, 0.4, 0.1),
        "ignorant_state": (0.3, 0.3, 0.4, 0.15),
        "confused_state": (0.3, 0.25, 0.45, 0.2),
        "deceived": (0.2, 0.3, 0.4, 0.15),
        "aware_state": (0.5, 0.55, 0.45, 0.6),
        "seeing": (0.55, 0.6, 0.45, 0.7),
        "knowing": (0.6, 0.65, 0.45, 0.8),
        "enlightened_state": (0.75, 0.7, 0.5, 0.95),

        # === SELF STATES ===
        "false_self": (0.2, 0.3, 0.4, 0.2),
        "masked": (0.25, 0.4, 0.45, 0.25),
        "pretending": (0.2, 0.35, 0.5, 0.2),
        "authentic": (0.75, 0.7, 0.55, 0.7),
        "genuine": (0.8, 0.75, 0.5, 0.7),
        "integrated_self": (0.85, 0.8, 0.55, 0.8),

        # === RELATIONSHIP TO TRUTH ===
        "denial": (0.2, 0.25, 0.5, 0.15),
        "avoiding": (0.25, 0.3, 0.45, 0.2),
        "facing": (0.5, 0.55, 0.55, 0.55),
        "accepting": (0.65, 0.65, 0.5, 0.65),
        "embracing": (0.8, 0.7, 0.55, 0.75),
    }

    for concept, (l, j, p, w) in concepts.items():
        extractor.substrate.add_point(concept, l, j, p, w)

    # === EXTRACT TRUTH PRINCIPLE ===
    print("\n1. THE TRUTH TRANSFORMATION")
    print("-" * 50)

    truth_transform = extractor.extract("TRUTH", [
        ("lie", "truth"),
        ("deception", "transparent"),
        ("illusion", "reality"),
        ("hidden", "transparent"),
        ("obscured", "truth"),
        ("partial_truth", "truth"),
    ])

    if truth_transform:
        print(f"\n  TRUTH = {truth_transform.as_formula()}")
        print(f"  Consistency: {truth_transform.consistency:.2f}")
        print(f"  Primary dimension: {truth_transform.dominant_dimension()}")
        print(f"  Effect: {truth_transform.description()}")

    # === EXTRACT FREEDOM PRINCIPLE ===
    print("\n2. THE FREEDOM TRANSFORMATION")
    print("-" * 50)

    freedom_transform = extractor.extract("FREEDOM", [
        ("enslaved", "liberated"),
        ("trapped", "free"),
        ("bound", "released"),
        ("constrained", "unconstrained"),
        ("burdened", "unburdened"),
        ("weighed_down", "free"),
    ])

    if freedom_transform:
        print(f"\n  FREEDOM = {freedom_transform.as_formula()}")
        print(f"  Consistency: {freedom_transform.consistency:.2f}")
        print(f"  Primary dimension: {freedom_transform.dominant_dimension()}")
        print(f"  Effect: {freedom_transform.description()}")

    # === EXTRACT AWARENESS TRANSFORMATION ===
    print("\n3. THE AWARENESS TRANSFORMATION")
    print("-" * 50)

    awareness_transform = extractor.extract("AWARENESS", [
        ("blind", "seeing"),
        ("ignorant_state", "knowing"),
        ("confused_state", "aware_state"),
        ("deceived", "enlightened_state"),
    ])

    if awareness_transform:
        print(f"\n  AWARENESS = {awareness_transform.as_formula()}")
        print(f"  Consistency: {awareness_transform.consistency:.2f}")
        print(f"  Primary dimension: {awareness_transform.dominant_dimension()}")
        print(f"  Effect: {awareness_transform.description()}")

    # === THE KEY: DOES TRUTH → FREEDOM? ===
    print("\n4. TESTING: DOES TRUTH LEAD TO FREEDOM?")
    print("-" * 50)

    if truth_transform and freedom_transform:
        similarity = extractor.compare(truth_transform, freedom_transform)
        print(f"\n  Similarity between TRUTH and FREEDOM: {similarity:.2f}")

        if similarity > 0.8:
            print("  ✓ HIGH CORRELATION: Truth and Freedom point in similar directions!")
        elif similarity > 0.5:
            print("  ~ MODERATE CORRELATION: Related but distinct transformations")
        else:
            print("  ✗ LOW CORRELATION: Different transformations")

    # === EXTRACT THE COMBINED PRINCIPLE ===
    print("\n5. THE COMBINED PRINCIPLE: TRUTH → FREEDOM")
    print("-" * 50)

    # What happens when someone goes from deception+bondage to truth+freedom?
    truth_freedom = extractor.extract("TRUTH_FREES", [
        ("deceived", "enlightened_state"),
        ("false_self", "authentic"),
        ("masked", "genuine"),
        ("denial", "accepting"),
        ("avoiding", "embracing"),
        ("pretending", "integrated_self"),
        ("trapped", "liberated"),
        ("blind", "knowing"),
    ])

    if truth_freedom:
        print(f"\n  TRUTH_FREES = {truth_freedom.as_formula()}")
        print(f"  Consistency: {truth_freedom.consistency:.2f}")
        print(f"  Primary dimension: {truth_freedom.dominant_dimension()}")
        print(f"  Effect: {truth_freedom.description()}")

    # === WHY DOES TRUTH FREE? ===
    print("\n6. WHY DOES TRUTH SET YOU FREE?")
    print("-" * 50)

    if truth_transform and freedom_transform and truth_freedom:
        print(f"""
    Let's analyze the LJPW components:

    TRUTH vector:   L={truth_transform.L:+.2f}  J={truth_transform.J:+.2f}  P={truth_transform.P:+.2f}  W={truth_transform.W:+.2f}
    FREEDOM vector: L={freedom_transform.L:+.2f}  J={freedom_transform.J:+.2f}  P={freedom_transform.P:+.2f}  W={freedom_transform.W:+.2f}
    COMBINED:       L={truth_freedom.L:+.2f}  J={truth_freedom.J:+.2f}  P={truth_freedom.P:+.2f}  W={truth_freedom.W:+.2f}
    """)

        # Analyze why
        print("    ANALYSIS:")
        print("    ─────────")

        # Truth's effect on each dimension
        print(f"""
    TRUTH adds:
      +L (binding):    Truth creates AUTHENTIC connection
                       Lies separate us; truth unites us
                       "You can only love what you truly know"

      +J (structure):  Truth provides SOLID GROUND
                       Reality is structured; illusion is unstable
                       "Built on rock, not sand"

      +W (wisdom):     Truth IS knowledge of reality
                       This is the direct effect
                       "You will KNOW the truth"

    FREEDOM adds:
      +L (binding):    Freedom enables REAL relationship
                       Slavery is false binding; freedom is true connection

      +P (power):      Freedom IS capacity to act
                       This is the direct effect
                       "Able to move, choose, become"

      +W (wisdom):     Freedom requires awareness
                       You can't choose what you don't see

    THE CONNECTION:
    ───────────────
    Truth adds +W (knowing reality)
    Knowing reality enables +P (capacity to act on reality)
    Acting on reality creates +L (authentic binding)
    Authentic binding requires +J (true structure)

    THEREFORE: Truth → Wisdom → Power → Freedom

    The chain is: KNOWING enables DOING enables BEING FREE
        """)

    # === THE MECHANISM ===
    print("\n7. THE MECHANISM")
    print("-" * 50)

    if truth_freedom:
        print(f"""
    "The truth shall set you free" works because:

    1. LIES CONSUME ENERGY (maintaining illusion costs power)
       - Deception requires constant management
       - The false self must be maintained
       - Energy goes to hiding, not living

    2. TRUTH RELEASES THAT ENERGY (no maintenance cost)
       - Reality maintains itself
       - The authentic self IS
       - Energy goes to living, not hiding

    3. WISDOM ENABLES POWER
       - You can only act on what you know
       - True knowledge → effective action
       - Illusion → wasted effort on phantoms

    4. AUTHENTIC BINDING REPLACES FALSE BINDING
       - Lies bind you to illusions (slavery)
       - Truth binds you to reality (freedom)
       - Same L dimension, different sign

    LJPW Translation:
    ─────────────────
    Slavery = bound to illusion = -L (false binding) + -W (ignorance)
    Freedom = bound to reality  = +L (true binding)  + +W (wisdom)

    The TRUTH doesn't just add +W
    It TRANSFORMS the nature of L from false to true binding
    That transformation IS liberation
    """)

    # === FINAL INSIGHT ===
    print("\n" + "=" * 70)
    print("FINAL INSIGHT")
    print("=" * 70)

    if truth_freedom:
        print(f"""
    THE TRUTH SHALL SET YOU FREE

    Extracted formula: {truth_freedom.as_formula()}
    Consistency: {truth_freedom.consistency:.2f}

    The principle works because:

    1. Truth and Freedom are NOT separate things
       They are the SAME transformation viewed differently
       - Truth is seeing reality (W)
       - Freedom is acting on reality (P)
       - Both require authentic connection (L)

    2. The opposite is also true:
       - Lies enslave (they bind you to illusion)
       - Ignorance imprisons (you can't escape what you can't see)
       - False selves trap (maintaining the mask costs freedom)

    3. The vector shows WHY:
       +{truth_freedom.L:.2f}L = authentic connection (vs false binding)
       +{truth_freedom.J:.2f}J = solid structure (vs unstable illusion)
       +{truth_freedom.P:.2f}P = capacity to act (vs energy drain)
       +{truth_freedom.W:.2f}W = knowing reality (vs believing lies)

    Freedom is not the absence of binding.
    Freedom is being bound to REALITY instead of ILLUSION.

    The truth doesn't break your chains.
    It reveals they were never real.
    """)


if __name__ == "__main__":
    extract_truth_freedom()
