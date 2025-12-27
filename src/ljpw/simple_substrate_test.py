#!/usr/bin/env python3
"""
Simple Substrate Test — Can we map meaning directly?
"""

from substrate_mapper import SemanticSubstrate, SemanticPoint
import math


def simple_test():
    """Test with the simplest possible concepts."""

    print("=" * 60)
    print("SIMPLE SUBSTRATE TEST")
    print("Can we map meaning? Let's start with basic words.")
    print("=" * 60)

    substrate = SemanticSubstrate()

    # Test 1: Opposites should be far apart
    print("\n1. OPPOSITES TEST")
    print("-" * 40)

    opposites = [
        ("hot", "cold"),
        ("up", "down"),
        ("give", "take"),
        ("begin", "end"),
    ]

    # Map them with intuitive coordinates
    substrate.add_point("hot", L=0.4, J=0.3, P=0.8, W=0.3)   # High energy
    substrate.add_point("cold", L=0.4, J=0.5, P=0.2, W=0.3)  # Low energy
    substrate.add_point("up", L=0.3, J=0.4, P=0.7, W=0.4)    # Rising
    substrate.add_point("down", L=0.3, J=0.4, P=0.3, W=0.4)  # Falling
    substrate.add_point("give", L=0.9, J=0.5, P=0.6, W=0.4)  # Outward, loving
    substrate.add_point("take", L=0.2, J=0.5, P=0.6, W=0.4)  # Inward, selfish
    substrate.add_point("begin", L=0.5, J=0.3, P=0.8, W=0.4) # Initiating
    substrate.add_point("end", L=0.5, J=0.7, P=0.2, W=0.6)   # Completing

    for word1, word2 in opposites:
        p1, p2 = substrate.points[word1], substrate.points[word2]
        dist = p1.distance_to(p2)
        angle = p1.angle_with(p2)
        print(f"  {word1} ↔ {word2}: distance={dist:.3f}, angle={angle:.1f}°")

    # Test 2: Synonyms should be close
    print("\n2. SYNONYMS TEST")
    print("-" * 40)

    synonyms = [
        ("happy", "joyful"),
        ("angry", "furious"),
        ("small", "tiny"),
    ]

    substrate.add_point("happy", L=0.7, J=0.5, P=0.6, W=0.5)
    substrate.add_point("joyful", L=0.75, J=0.5, P=0.65, W=0.55)
    substrate.add_point("angry", L=0.2, J=0.3, P=0.9, W=0.3)
    substrate.add_point("furious", L=0.15, J=0.25, P=0.95, W=0.25)
    substrate.add_point("small", L=0.4, J=0.4, P=0.3, W=0.4)
    substrate.add_point("tiny", L=0.4, J=0.4, P=0.25, W=0.4)

    for word1, word2 in synonyms:
        p1, p2 = substrate.points[word1], substrate.points[word2]
        dist = p1.distance_to(p2)
        angle = p1.angle_with(p2)
        print(f"  {word1} ↔ {word2}: distance={dist:.3f}, angle={angle:.1f}°")

    # Test 3: The same word in different contexts (polysemy)
    print("\n3. SAME WORD, DIFFERENT MEANING TEST")
    print("-" * 40)

    # "Light" as in brightness vs "Light" as in weight
    substrate.add_point("light_bright", L=0.5, J=0.4, P=0.7, W=0.8)  # Illumination
    substrate.add_point("light_weight", L=0.4, J=0.4, P=0.3, W=0.4)  # Not heavy

    # "Bank" as in river vs "Bank" as in money
    substrate.add_point("bank_river", L=0.4, J=0.6, P=0.2, W=0.3)   # Geography
    substrate.add_point("bank_money", L=0.3, J=0.9, P=0.5, W=0.5)   # Institution

    polysemes = [
        ("light_bright", "light_weight"),
        ("bank_river", "bank_money"),
    ]

    for word1, word2 in polysemes:
        p1, p2 = substrate.points[word1], substrate.points[word2]
        dist = p1.distance_to(p2)
        print(f"  {word1.split('_')[0]} (as {word1.split('_')[1]}) ↔ (as {word2.split('_')[1]}): distance={dist:.3f}")

    # Test 4: Find the center of related concepts
    print("\n4. CONCEPT CLUSTERS TEST")
    print("-" * 40)

    # Add emotion cluster
    emotions = {
        "love_e": (0.95, 0.4, 0.5, 0.5),
        "fear": (0.2, 0.3, 0.7, 0.4),
        "joy": (0.8, 0.5, 0.7, 0.5),
        "sadness": (0.5, 0.4, 0.2, 0.5),
        "anger": (0.2, 0.3, 0.9, 0.3),
    }

    for word, (l, j, p, w) in emotions.items():
        substrate.add_point(word, l, j, p, w)

    # Find center of emotions
    emotion_points = [substrate.points[e] for e in emotions]
    center_L = sum(p.L for p in emotion_points) / len(emotion_points)
    center_J = sum(p.J for p in emotion_points) / len(emotion_points)
    center_P = sum(p.P for p in emotion_points) / len(emotion_points)
    center_W = sum(p.W for p in emotion_points) / len(emotion_points)

    print(f"  Emotion cluster center: ({center_L:.2f}, {center_J:.2f}, {center_P:.2f}, {center_W:.2f})")
    print(f"  This represents the 'abstract concept of emotion' in semantic space")

    # Test 5: Transformation paths (verbs as vectors)
    print("\n5. VERBS AS TRANSFORMATION VECTORS")
    print("-" * 40)

    # "Learn" transforms student → teacher
    substrate.add_point("student_2", L=0.5, J=0.4, P=0.5, W=0.4)
    substrate.add_point("teacher", L=0.6, J=0.6, P=0.6, W=0.85)

    learn_path = substrate.find_path("student_2", "teacher")
    print(f"  'LEARN' as vector: {learn_path.vector()}")
    print(f"    → +L (connection), +J (structure), +P (ability), ++W (wisdom)")

    # "Break" transforms whole → pieces
    substrate.add_point("whole", L=0.8, J=0.8, P=0.4, W=0.5)
    substrate.add_point("pieces", L=0.2, J=0.3, P=0.3, W=0.4)

    break_path = substrate.find_path("whole", "pieces")
    print(f"  'BREAK' as vector: {break_path.vector()}")
    print(f"    → --L (disconnection), --J (disorder), -P (loss)")

    # "Unite" transforms separate → together
    substrate.add_point("separate", L=0.2, J=0.4, P=0.4, W=0.4)
    substrate.add_point("together", L=0.9, J=0.6, P=0.5, W=0.5)

    unite_path = substrate.find_path("separate", "together")
    print(f"  'UNITE' as vector: {unite_path.vector()}")
    print(f"    → ++L (connection), +J (order), +P (strength)")

    # Key insight
    print("\n" + "=" * 60)
    print("INSIGHT")
    print("=" * 60)
    print("""
    If words are POINTS and verbs are VECTORS...
    Then sentences are TRAJECTORIES through semantic space!

    "The student learned" = point + vector = new point
    "They broke apart" = point + vector = new point

    The substrate isn't just storage.
    It's the SPACE where meaning MOVES.
    """)


if __name__ == "__main__":
    simple_test()
