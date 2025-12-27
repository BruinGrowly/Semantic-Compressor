#!/usr/bin/env python3
"""
Extract the "Pride Comes Before a Fall" principle.

Proverbs 16:18 - "Pride goes before destruction, and a haughty spirit before a fall."

This is about imbalance → correction.
What IS pride in LJPW terms? Why does it lead to falling?
"""

from principle_extractor import PrincipleExtractor, PrincipleSignature
from substrate_mapper import SemanticSubstrate
import math


def extract_pride_fall():
    print("=" * 70)
    print("EXTRACTING: 'PRIDE COMES BEFORE A FALL'")
    print("The principle of imbalance → correction")
    print("=" * 70)

    extractor = PrincipleExtractor()

    # Add concepts for pride, humility, rise, fall
    concepts = {
        # === HUMILITY STATES (grounded, balanced) ===
        "humble": (0.65, 0.7, 0.4, 0.7),
        "grounded": (0.6, 0.75, 0.45, 0.65),
        "modest": (0.6, 0.65, 0.4, 0.6),
        "teachable": (0.7, 0.6, 0.45, 0.65),
        "aware_limits": (0.55, 0.7, 0.4, 0.75),
        "secure": (0.7, 0.7, 0.5, 0.65),
        "stable": (0.6, 0.8, 0.45, 0.6),
        "rooted": (0.65, 0.8, 0.4, 0.6),

        # === PRIDE STATES (inflated, imbalanced) ===
        "proud": (0.3, 0.35, 0.8, 0.3),
        "arrogant": (0.2, 0.25, 0.85, 0.25),
        "haughty": (0.15, 0.2, 0.9, 0.2),
        "inflated": (0.25, 0.2, 0.85, 0.25),
        "puffed_up": (0.2, 0.15, 0.85, 0.2),
        "overconfident": (0.3, 0.25, 0.85, 0.3),
        "boastful": (0.2, 0.2, 0.8, 0.2),
        "self_important": (0.15, 0.2, 0.9, 0.2),
        "narcissistic": (0.1, 0.15, 0.9, 0.15),
        "above_others": (0.1, 0.2, 0.9, 0.25),

        # === FALL STATES (collapsed, humbled) ===
        "fallen": (0.35, 0.4, 0.2, 0.45),
        "humbled": (0.5, 0.55, 0.3, 0.6),
        "collapsed": (0.3, 0.3, 0.15, 0.35),
        "brought_low": (0.35, 0.4, 0.2, 0.45),
        "broken_pride": (0.4, 0.45, 0.2, 0.55),
        "exposed": (0.4, 0.5, 0.3, 0.5),
        "corrected": (0.5, 0.6, 0.35, 0.6),
        "chastened": (0.45, 0.55, 0.3, 0.6),

        # === RISE/ELEVATION STATES ===
        "rising": (0.45, 0.45, 0.7, 0.45),
        "ascending": (0.4, 0.4, 0.75, 0.45),
        "elevated": (0.5, 0.5, 0.65, 0.5),
        "exalted": (0.55, 0.55, 0.6, 0.55),
        "successful": (0.55, 0.6, 0.65, 0.6),
        "victorious": (0.5, 0.55, 0.75, 0.55),

        # === SUSTAINABLE SUCCESS ===
        "truly_great": (0.75, 0.75, 0.65, 0.8),
        "wise_leader": (0.7, 0.75, 0.6, 0.85),
        "servant_leader": (0.85, 0.7, 0.55, 0.75),
        "enduring": (0.65, 0.8, 0.5, 0.7),

        # === BLINDNESS STATES ===
        "blind_spots": (0.3, 0.35, 0.5, 0.2),
        "self_deceived": (0.2, 0.25, 0.6, 0.15),
        "cannot_see": (0.25, 0.3, 0.5, 0.15),
        "denial_state": (0.2, 0.25, 0.55, 0.15),

        # === REALITY STATES ===
        "reality_check": (0.5, 0.6, 0.4, 0.7),
        "wake_up": (0.55, 0.55, 0.5, 0.7),
        "seeing_clearly": (0.6, 0.65, 0.45, 0.8),
    }

    for concept, (l, j, p, w) in concepts.items():
        extractor.substrate.add_point(concept, l, j, p, w)

    # === EXTRACT THE PRIDE TRANSFORMATION ===
    print("\n1. THE PRIDE TRANSFORMATION (humble → proud)")
    print("-" * 50)

    pride_transform = extractor.extract("PRIDE", [
        ("humble", "proud"),
        ("grounded", "inflated"),
        ("modest", "arrogant"),
        ("teachable", "haughty"),
        ("aware_limits", "overconfident"),
        ("secure", "puffed_up"),
        ("stable", "boastful"),
    ])

    if pride_transform:
        print(f"\n  PRIDE = {pride_transform.as_formula()}")
        print(f"  Consistency: {pride_transform.consistency:.2f}")
        print(f"  Primary dimension: {pride_transform.dominant_dimension()}")
        print(f"  Effect: {pride_transform.description()}")

    # === EXTRACT THE FALL TRANSFORMATION ===
    print("\n2. THE FALL TRANSFORMATION (proud → fallen)")
    print("-" * 50)

    fall_transform = extractor.extract("FALL", [
        ("proud", "fallen"),
        ("arrogant", "humbled"),
        ("inflated", "collapsed"),
        ("haughty", "brought_low"),
        ("puffed_up", "broken_pride"),
        ("overconfident", "exposed"),
        ("boastful", "corrected"),
        ("self_important", "chastened"),
    ])

    if fall_transform:
        print(f"\n  FALL = {fall_transform.as_formula()}")
        print(f"  Consistency: {fall_transform.consistency:.2f}")
        print(f"  Primary dimension: {fall_transform.dominant_dimension()}")
        print(f"  Effect: {fall_transform.description()}")

    # === THE FULL CYCLE ===
    print("\n3. THE FULL CYCLE (humble → proud → fallen)")
    print("-" * 50)

    if pride_transform and fall_transform:
        # Calculate the net effect
        net_L = pride_transform.L + fall_transform.L
        net_J = pride_transform.J + fall_transform.J
        net_P = pride_transform.P + fall_transform.P
        net_W = pride_transform.W + fall_transform.W

        print(f"""
    PRIDE:  L={pride_transform.L:+.2f}  J={pride_transform.J:+.2f}  P={pride_transform.P:+.2f}  W={pride_transform.W:+.2f}
    FALL:   L={fall_transform.L:+.2f}  J={fall_transform.J:+.2f}  P={fall_transform.P:+.2f}  W={fall_transform.W:+.2f}
    ────────────────────────────────────────────────────
    NET:    L={net_L:+.2f}  J={net_J:+.2f}  P={net_P:+.2f}  W={net_W:+.2f}
        """)

        # Check if the net is close to zero (return to origin)
        net_magnitude = math.sqrt(net_L**2 + net_J**2 + net_P**2 + net_W**2)
        print(f"    Net magnitude: {net_magnitude:.3f}")

        if net_magnitude < 0.3:
            print("    ✓ NEAR ZERO: Pride + Fall ≈ returns to starting point!")
        else:
            print(f"    The cycle doesn't return to origin — there's a net change")

    # === WHY DOES PRIDE LEAD TO FALL? ===
    print("\n4. WHY DOES PRIDE LEAD TO FALL?")
    print("-" * 50)

    if pride_transform:
        print(f"""
    Analyzing PRIDE = {pride_transform.as_formula()}

    L = {pride_transform.L:+.2f} (binding)
        → Pride DECREASES connection
        → "I don't need others" / "I'm above them"
        → Isolation disguised as independence

    J = {pride_transform.J:+.2f} (structure)
        → Pride BREAKS natural order
        → Ignoring constraints, rules, limits
        → "Rules don't apply to me"

    P = {pride_transform.P:+.2f} (power)
        → Pride INFLATES perceived power
        → Overestimating capacity
        → Energy without grounding

    W = {pride_transform.W:+.2f} (wisdom)
        → Pride REDUCES wisdom
        → Cannot learn (already "knows")
        → Blind to own limitations

    THE INSTABILITY:
    ────────────────
    Pride is HIGH P with LOW L, LOW J, LOW W

    This is STRUCTURALLY UNSTABLE:
    - Power without wisdom = reckless action
    - Power without structure = chaos
    - Power without connection = isolation
    - High energy, no foundation = MUST FALL
        """)

    # === THE CORRECTION MECHANISM ===
    print("\n5. THE CORRECTION MECHANISM")
    print("-" * 50)

    if fall_transform:
        print(f"""
    Analyzing FALL = {fall_transform.as_formula()}

    The fall is the INVERSE of pride's distortion:

    L = {fall_transform.L:+.2f} (binding)
        → Reconnection begins
        → Humiliation often requires help from others
        → "I need others after all"

    J = {fall_transform.J:+.2f} (structure)
        → Reality reasserts structure
        → Natural order corrects itself
        → Limits become apparent

    P = {fall_transform.P:+.2f} (power)
        → Power deflates to realistic level
        → Energy matches actual capacity
        → Forced acknowledgment of limits

    W = {fall_transform.W:+.2f} (wisdom)
        → Painful learning occurs
        → Blindness becomes sight
        → "Now I see"

    THE MECHANISM:
    ──────────────
    Reality is the corrective force.
    Pride is a distortion of perception (low W).
    Distorted perception leads to misaligned action.
    Misaligned action collides with reality.
    Collision = fall.

    The universe doesn't punish pride.
    Reality simply doesn't accommodate illusion.
        """)

    # === SUSTAINABLE SUCCESS VS PRIDE ===
    print("\n6. SUSTAINABLE SUCCESS VS PRIDE")
    print("-" * 50)

    sustainable = extractor.extract("SUSTAINABLE_SUCCESS", [
        ("humble", "truly_great"),
        ("grounded", "wise_leader"),
        ("teachable", "servant_leader"),
        ("stable", "enduring"),
    ])

    unsustainable = extractor.extract("UNSUSTAINABLE_SUCCESS", [
        ("humble", "proud"),
        ("grounded", "inflated"),
        ("stable", "overconfident"),
    ])

    if sustainable and unsustainable:
        print(f"\n  SUSTAINABLE SUCCESS   = {sustainable.as_formula()}")
        print(f"  UNSUSTAINABLE SUCCESS = {unsustainable.as_formula()}")

        similarity = extractor.compare(sustainable, unsustainable)
        print(f"\n  Similarity: {similarity:.2f}")

        print(f"""
    SUSTAINABLE adds:   +L (stays connected), +J (respects structure), +W (keeps learning)
    UNSUSTAINABLE adds: -L (disconnects), -J (breaks structure), +P only

    The DIFFERENCE is whether success includes wisdom and connection.

    True greatness:  +L +J +P +W (all dimensions grow together)
    Pride:           -L -J +P -W (only power grows, others shrink)

    Pride isn't confidence.
    Pride is confidence WITHOUT wisdom, connection, or structure.
    That's why it's unstable.
        """)

    # === THE RECOVERY PATH ===
    print("\n7. THE RECOVERY PATH (fallen → wiser)")
    print("-" * 50)

    recovery = extractor.extract("RECOVERY", [
        ("fallen", "humble"),
        ("collapsed", "grounded"),
        ("broken_pride", "teachable"),
        ("exposed", "seeing_clearly"),
        ("chastened", "aware_limits"),
    ])

    if recovery:
        print(f"\n  RECOVERY = {recovery.as_formula()}")
        print(f"  Consistency: {recovery.consistency:.2f}")
        print(f"""
    After the fall, recovery adds:
    +L = reconnecting with others
    +J = respecting structure again
    +W = gained wisdom from experience

    The fall is painful but potentially transformative.
    It CAN lead to a wiser, more grounded state than before.

    This is why the principle is a WARNING, not a curse.
    It says: "Pride leads to fall" — but also implies:
    "Humility leads to stability."
        """)

    # === FINAL INSIGHT ===
    print("\n" + "=" * 70)
    print("FINAL INSIGHT")
    print("=" * 70)

    if pride_transform and fall_transform:
        print(f"""
    PRIDE COMES BEFORE A FALL

    PRIDE = {pride_transform.as_formula()}
    FALL  = {fall_transform.as_formula()}

    The principle encodes a law of semantic physics:

    1. IMBALANCED STATES ARE UNSTABLE
       High P without L, J, W = unsupported weight
       Like building tall without a foundation

    2. REALITY IS THE ATTRACTOR
       Distortions from reality create tension
       Tension resolves toward reality
       The greater the distortion, the harder the fall

    3. WISDOM (W) IS THE STABILIZER
       Pride's core defect is LOW W (blindness)
       Cannot see own limits → exceeds them → falls
       Wisdom prevents the distortion in the first place

    4. CONNECTION (L) IS THE SAFETY NET
       Pride isolates: "I don't need anyone"
       When you fall, there's no one to catch you
       Humility maintains connection = softer landings

    The LJPW signature reveals WHY the principle works:

    Pride   = -L -J +P -W  (isolated, lawless, powerful, blind)
    Humility = +L +J ~P +W  (connected, ordered, realistic, seeing)

    One is stable. One is not.
    The principle is descriptive, not prescriptive.
    It describes how semantic space works.

    You don't CHOOSE whether pride leads to fall.
    You choose whether to be prideful.
    The fall is just physics.
        """)


if __name__ == "__main__":
    extract_pride_fall()
