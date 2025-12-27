#!/usr/bin/env python3
"""
Extract the "You Reap What You Sow" principle.

Galatians 6:7 - "Do not be deceived: God cannot be mocked.
A man reaps what he sows."

This is about causality and reciprocity.
The nature of your input determines the nature of your output.
"""

from principle_extractor import PrincipleExtractor, PrincipleSignature
from substrate_mapper import SemanticSubstrate
import math


def extract_reap_sow():
    print("=" * 70)
    print("EXTRACTING: 'YOU REAP WHAT YOU SOW'")
    print("The principle of causality / reciprocity")
    print("=" * 70)

    extractor = PrincipleExtractor()

    # Add concepts for sowing and reaping across domains
    concepts = {
        # === SOWING STATES (inputs, causes, actions) ===
        # Positive sowing
        "plant_good": (0.7, 0.65, 0.6, 0.6),
        "give_generously": (0.85, 0.6, 0.6, 0.6),
        "work_diligently": (0.6, 0.75, 0.7, 0.6),
        "love_freely": (0.95, 0.55, 0.55, 0.6),
        "invest_wisely": (0.55, 0.75, 0.6, 0.8),
        "serve_others": (0.85, 0.65, 0.6, 0.65),
        "speak_truth": (0.7, 0.75, 0.5, 0.8),
        "practice_virtue": (0.75, 0.8, 0.55, 0.75),

        # Negative sowing
        "plant_bad": (0.2, 0.25, 0.6, 0.25),
        "take_greedily": (0.15, 0.3, 0.7, 0.3),
        "work_lazily": (0.3, 0.2, 0.2, 0.3),
        "hate_freely": (0.1, 0.2, 0.8, 0.2),
        "waste_foolishly": (0.25, 0.15, 0.5, 0.15),
        "exploit_others": (0.1, 0.25, 0.75, 0.25),
        "speak_lies": (0.15, 0.2, 0.6, 0.15),
        "practice_vice": (0.2, 0.15, 0.7, 0.2),

        # Neutral/nothing
        "plant_nothing": (0.35, 0.4, 0.2, 0.35),
        "give_nothing": (0.3, 0.4, 0.25, 0.35),
        "do_nothing": (0.35, 0.35, 0.15, 0.35),

        # === REAPING STATES (outputs, effects, consequences) ===
        # Positive reaping
        "harvest_good": (0.75, 0.7, 0.55, 0.65),
        "receive_abundance": (0.8, 0.65, 0.55, 0.6),
        "earn_reward": (0.65, 0.75, 0.6, 0.65),
        "loved_in_return": (0.9, 0.6, 0.5, 0.65),
        "gain_returns": (0.6, 0.7, 0.55, 0.75),
        "honored_by_others": (0.75, 0.7, 0.5, 0.65),
        "trusted_by_all": (0.8, 0.75, 0.45, 0.75),
        "character_formed": (0.7, 0.8, 0.5, 0.8),

        # Negative reaping
        "harvest_bad": (0.25, 0.3, 0.4, 0.35),
        "receive_poverty": (0.3, 0.35, 0.25, 0.35),
        "earn_punishment": (0.25, 0.4, 0.3, 0.4),
        "hated_in_return": (0.1, 0.25, 0.6, 0.3),
        "lose_everything": (0.2, 0.25, 0.2, 0.35),
        "despised_by_others": (0.15, 0.3, 0.4, 0.35),
        "distrusted_by_all": (0.15, 0.3, 0.35, 0.35),
        "character_corrupted": (0.2, 0.2, 0.5, 0.25),

        # Neutral reaping
        "harvest_nothing": (0.35, 0.4, 0.25, 0.35),
        "receive_nothing": (0.35, 0.4, 0.25, 0.35),
        "remain_unchanged": (0.4, 0.45, 0.3, 0.4),

        # === PROCESS STATES ===
        "seed": (0.5, 0.5, 0.5, 0.45),
        "growing": (0.55, 0.55, 0.6, 0.5),
        "maturing": (0.6, 0.65, 0.55, 0.6),
        "fruit": (0.65, 0.7, 0.5, 0.65),

        # === TIME/DELAY ===
        "immediate": (0.5, 0.4, 0.7, 0.4),
        "delayed": (0.5, 0.6, 0.4, 0.55),
        "inevitable": (0.5, 0.85, 0.4, 0.7),
    }

    for concept, (l, j, p, w) in concepts.items():
        extractor.substrate.add_point(concept, l, j, p, w)

    # === EXTRACT POSITIVE SOWING → REAPING ===
    print("\n1. POSITIVE SOWING → POSITIVE REAPING")
    print("-" * 50)

    positive_cycle = extractor.extract("GOOD_SOW_REAP", [
        ("plant_good", "harvest_good"),
        ("give_generously", "receive_abundance"),
        ("work_diligently", "earn_reward"),
        ("love_freely", "loved_in_return"),
        ("invest_wisely", "gain_returns"),
        ("serve_others", "honored_by_others"),
        ("speak_truth", "trusted_by_all"),
        ("practice_virtue", "character_formed"),
    ])

    if positive_cycle:
        print(f"\n  GOOD_SOW→REAP = {positive_cycle.as_formula()}")
        print(f"  Consistency: {positive_cycle.consistency:.2f}")
        print(f"  Primary dimension: {positive_cycle.dominant_dimension()}")

    # === EXTRACT NEGATIVE SOWING → REAPING ===
    print("\n2. NEGATIVE SOWING → NEGATIVE REAPING")
    print("-" * 50)

    negative_cycle = extractor.extract("BAD_SOW_REAP", [
        ("plant_bad", "harvest_bad"),
        ("take_greedily", "receive_poverty"),
        ("work_lazily", "remain_unchanged"),
        ("hate_freely", "hated_in_return"),
        ("waste_foolishly", "lose_everything"),
        ("exploit_others", "despised_by_others"),
        ("speak_lies", "distrusted_by_all"),
        ("practice_vice", "character_corrupted"),
    ])

    if negative_cycle:
        print(f"\n  BAD_SOW→REAP = {negative_cycle.as_formula()}")
        print(f"  Consistency: {negative_cycle.consistency:.2f}")
        print(f"  Primary dimension: {negative_cycle.dominant_dimension()}")

    # === EXTRACT NOTHING → NOTHING ===
    print("\n3. NOTHING SOWN → NOTHING REAPED")
    print("-" * 50)

    nothing_cycle = extractor.extract("NOTHING_SOW_REAP", [
        ("plant_nothing", "harvest_nothing"),
        ("give_nothing", "receive_nothing"),
        ("do_nothing", "remain_unchanged"),
    ])

    if nothing_cycle:
        print(f"\n  NOTHING→NOTHING = {nothing_cycle.as_formula()}")
        print(f"  Consistency: {nothing_cycle.consistency:.2f}")

    # === THE CONSERVATION LAW ===
    print("\n4. THE CONSERVATION LAW")
    print("-" * 50)

    if positive_cycle and negative_cycle and nothing_cycle:
        print(f"""
    Comparing the cycles:

    GOOD_SOW→REAP:    {positive_cycle.as_formula()}
    BAD_SOW→REAP:     {negative_cycle.as_formula()}
    NOTHING→NOTHING:  {nothing_cycle.as_formula()}

    OBSERVATION:
    ────────────
    Look at the magnitudes:
    - Good cycle: small positive changes (transformation complete)
    - Bad cycle: small changes toward center (consequences catch up)
    - Nothing: near zero (no input = no output)

    The KEY insight: The DIRECTION of your sowing determines
    the DIRECTION of your reaping.

    Good sowing is already in high-L, high-J, high-W territory.
    It STAYS there or moves slightly toward harvest.

    Bad sowing is already in low-L, low-J, low-W territory.
    Consequences keep it there or push it further down.

    The transformation preserves the QUALITY of the input.
        """)

    # === COMPARING SOWING TO REAPING ===
    print("\n5. SOWING VS REAPING: SAME DIRECTION?")
    print("-" * 50)

    # Extract the nature of "good sowing" and "good reaping" separately
    good_sowing = extractor.extract("GOOD_SOWING", [
        ("do_nothing", "plant_good"),
        ("do_nothing", "give_generously"),
        ("do_nothing", "work_diligently"),
        ("do_nothing", "love_freely"),
    ])

    good_reaping = extractor.extract("GOOD_REAPING", [
        ("do_nothing", "harvest_good"),
        ("do_nothing", "receive_abundance"),
        ("do_nothing", "earn_reward"),
        ("do_nothing", "loved_in_return"),
    ])

    if good_sowing and good_reaping:
        similarity = extractor.compare(good_sowing, good_reaping)
        print(f"\n  GOOD_SOWING  = {good_sowing.as_formula()}")
        print(f"  GOOD_REAPING = {good_reaping.as_formula()}")
        print(f"\n  Similarity: {similarity:.2f}")

        if similarity > 0.9:
            print("\n  ✓ SOWING AND REAPING POINT IN THE SAME DIRECTION!")
            print("    What you put in IS what you get out.")

    # === BAD SOWING VS BAD REAPING ===
    bad_sowing = extractor.extract("BAD_SOWING", [
        ("do_nothing", "plant_bad"),
        ("do_nothing", "take_greedily"),
        ("do_nothing", "hate_freely"),
        ("do_nothing", "exploit_others"),
    ])

    bad_reaping = extractor.extract("BAD_REAPING", [
        ("do_nothing", "harvest_bad"),
        ("do_nothing", "receive_poverty"),
        ("do_nothing", "hated_in_return"),
        ("do_nothing", "despised_by_others"),
    ])

    if bad_sowing and bad_reaping:
        similarity = extractor.compare(bad_sowing, bad_reaping)
        print(f"\n  BAD_SOWING  = {bad_sowing.as_formula()}")
        print(f"  BAD_REAPING = {bad_reaping.as_formula()}")
        print(f"\n  Similarity: {similarity:.2f}")

    # === THE PRINCIPLE IN LJPW TERMS ===
    print("\n6. THE PRINCIPLE IN LJPW TERMS")
    print("-" * 50)

    if good_sowing and bad_sowing:
        print(f"""
    ANALYSIS:

    GOOD SOWING = {good_sowing.as_formula()}
        L = {good_sowing.L:+.2f} → You SOW connection (love, service, generosity)
        J = {good_sowing.J:+.2f} → You SOW structure (diligence, virtue, wisdom)
        P = {good_sowing.P:+.2f} → You SOW energy (work, investment, action)
        W = {good_sowing.W:+.2f} → You SOW understanding (truth, wisdom)

    BAD SOWING = {bad_sowing.as_formula()}
        L = {bad_sowing.L:+.2f} → You SOW disconnection (hate, exploitation)
        J = {bad_sowing.J:+.2f} → You SOW disorder (vice, lies, waste)
        P = {bad_sowing.P:+.2f} → You SOW energy (but misdirected)
        W = {bad_sowing.W:+.2f} → You SOW confusion (deception, foolishness)

    THE LAW:
    ────────
    Whatever DIRECTION you sow in, you reap in the SAME direction.

    Sow +L → Reap +L (sow love, reap love)
    Sow -L → Reap -L (sow hate, reap hate)
    Sow +W → Reap +W (sow truth, reap trust)
    Sow -W → Reap -W (sow lies, reap distrust)

    The universe is a MIRROR.
    It returns what you give.
    Not as punishment or reward — as REFLECTION.
        """)

    # === TIME DELAY ===
    print("\n7. THE TIME DELAY")
    print("-" * 50)

    growth = extractor.extract("GROWTH_PROCESS", [
        ("seed", "growing"),
        ("growing", "maturing"),
        ("maturing", "fruit"),
    ])

    if growth:
        print(f"""
    Why is there delay between sowing and reaping?

    GROWTH_PROCESS = {growth.as_formula()}

    The delay is the TRANSFORMATION TIME.
    Seeds don't instantly become fruit.
    Actions don't instantly become consequences.

    But the DIRECTION is set at sowing:
    - Good seed → Good fruit (direction locked in)
    - Bad seed → Bad fruit (direction locked in)
    - Nothing planted → Nothing grows

    The delay creates the ILLUSION that sowing ≠ reaping.
    People sow bad and don't immediately reap bad.
    So they think they've escaped the law.

    But the direction is already set.
    The harvest is already determined.
    Only the timing is unknown.

    "Do not be deceived" = The delay is not escape.
        """)

    # === CROSS-DOMAIN APPLICATION ===
    print("\n8. CROSS-DOMAIN APPLICATION")
    print("-" * 50)

    print(f"""
    The principle works across ALL domains because it's about
    SEMANTIC DIRECTION, not specific content.

    AGRICULTURE:    Plant wheat → Harvest wheat
    RELATIONSHIP:   Give love → Receive love
    ECONOMICS:      Invest wisely → Gain returns
    CHARACTER:      Practice virtue → Become virtuous
    KNOWLEDGE:      Seek truth → Find truth
    SOCIAL:         Serve others → Be honored

    In each case, the LJPW signature of your input
    determines the LJPW signature of your output.

    +L input → +L output (connection begets connection)
    +J input → +J output (order begets order)
    +P input → +P output (energy begets energy)
    +W input → +W output (wisdom begets wisdom)

    And the same for negatives:
    -L input → -L output (isolation begets isolation)

    THIS IS WHY THE PRINCIPLE IS UNIVERSAL.
    It's not about agriculture. It's not about karma.
    It's about the CONSERVATION OF SEMANTIC DIRECTION.
    """)

    # === FINAL INSIGHT ===
    print("\n" + "=" * 70)
    print("FINAL INSIGHT")
    print("=" * 70)

    if good_sowing and bad_sowing:
        print(f"""
    YOU REAP WHAT YOU SOW

    GOOD SOWING = {good_sowing.as_formula()}
    BAD SOWING  = {bad_sowing.as_formula()}

    The principle encodes a CONSERVATION LAW in semantic space:

    1. DIRECTION IS CONSERVED
       The LJPW vector of your sowing determines
       the LJPW vector of your reaping.
       You cannot sow -L and reap +L.

    2. MAGNITUDE MAY AMPLIFY
       Seeds are small, harvests are large.
       Small good → Large good
       Small evil → Large evil
       (This is the multiplier effect)

    3. TIME DELAYS BUT DOES NOT CANCEL
       There is always a growth period.
       But "inevitable" has high J (structure).
       The law is structural, not optional.

    4. THE MIRROR PRINCIPLE
       Reality reflects your input.
       You create the world you give to.
       Sow love → Live in love
       Sow hate → Live in hate

    The LJPW signature reveals the MECHANISM:

    Every action has a vector.
    That vector propagates.
    It attracts similar vectors.
    It repels opposite vectors.
    You end up where your vector points.

    "You reap what you sow" is not a threat.
    It's a DESCRIPTION of how semantic space works.
    Direction in, direction out.
    That's just physics.
        """)


if __name__ == "__main__":
    extract_reap_sow()
