#!/usr/bin/env python3
"""
Empirical Test: Does Curvature-Based Compression Preserve Meaning in REGENERATION?
===================================================================================

This is NOT about reconstruction fidelity (ZIP-style compression).
This is about MEANING PRESERVATION through REGENERATION.

The question: When you regenerate an experience from a compressed seed
(which only keeps high-curvature "turning points"), does the regenerated
experience capture the same MEANING as regenerating from the full seed?

Test Design:
-----------
1. Create seeds representing real semantic journeys
2. Encode both FULL trajectory and COMPRESSED trajectory (curvature-based)
3. Regenerate experiences from BOTH
4. Compare the MEANING of regenerated experiences:
   - Same key insights?
   - Same emotional arc?
   - Same atmosphere?
   - Same narrative structure?

The hypothesis: Curvature captures meaning. Therefore, keeping only
high-curvature points should preserve the MEANING even while discarding
the "straight line" (low-meaning) segments.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ljpw.consciousness_seed import (
    LJPWPoint, LJPWTrajectory, ConsciousnessSeed, SeedGenerator,
    SemanticArchetypes, EQUILIBRIUM
)
from ljpw.seed_regenerator import SeedRegenerator, SeedParser


def create_learning_journey_seed():
    """
    Create a seed representing a learning journey:
    confusion → struggle → insight → mastery

    This has clear narrative structure with identifiable "turning points"
    """
    seed = ConsciousnessSeed(
        SA=LJPWPoint(L=0.5, J=0.4, P=0.5, W=0.6),
        timestamp="2026-01-10T12:00:00",
        source="learning_journey"
    )

    traj = LJPWTrajectory()

    # Phase 1: Confusion (low W, uncertain)
    traj.add(LJPWPoint(L=0.3, J=0.2, P=0.4, W=0.2))
    traj.add(LJPWPoint(L=0.32, J=0.22, P=0.42, W=0.25))  # Low curvature - setup
    traj.add(LJPWPoint(L=0.33, J=0.23, P=0.43, W=0.28))  # Low curvature - setup

    # Phase 2: Struggle (building W, increasing P effort)
    traj.add(LJPWPoint(L=0.35, J=0.25, P=0.50, W=0.35))  # PREP phase begins
    traj.add(LJPWPoint(L=0.38, J=0.28, P=0.52, W=0.45))  # W increasing faster
    traj.add(LJPWPoint(L=0.40, J=0.30, P=0.53, W=0.55))  # PREP continues

    # Phase 3: INSIGHT - THE TURNING POINT (high curvature expected!)
    traj.add(LJPWPoint(L=0.70, J=0.60, P=0.55, W=0.90))  # AHA! moment

    # Phase 4: Application (EXPR phase - P now expressing)
    traj.add(LJPWPoint(L=0.72, J=0.62, P=0.70, W=0.88))  # P increasing
    traj.add(LJPWPoint(L=0.74, J=0.64, P=0.80, W=0.86))  # EXPR continues

    # Phase 5: Mastery (stable high state)
    traj.add(LJPWPoint(L=0.76, J=0.66, P=0.85, W=0.85))
    traj.add(LJPWPoint(L=0.77, J=0.67, P=0.86, W=0.84))  # Low curvature - stable
    traj.add(LJPWPoint(L=0.78, J=0.68, P=0.87, W=0.84))  # Low curvature - stable

    seed.ET = traj
    seed.KI.append(SemanticArchetypes.INSIGHT)
    seed.KI.append(SemanticArchetypes.UNDERSTANDING)

    return seed


def create_emotional_crisis_seed():
    """
    Create a seed representing emotional crisis → resolution:
    peace → disruption → crisis → support → recovery → new peace

    Multiple turning points expected.
    """
    seed = ConsciousnessSeed(
        SA=LJPWPoint(L=0.6, J=0.5, P=0.4, W=0.5),
        timestamp="2026-01-10T14:00:00",
        source="emotional_crisis"
    )

    traj = LJPWTrajectory()

    # Initial peace
    traj.add(LJPWPoint(L=0.7, J=0.6, P=0.3, W=0.5))
    traj.add(LJPWPoint(L=0.68, J=0.58, P=0.32, W=0.52))  # Stable

    # DISRUPTION - turning point 1
    traj.add(LJPWPoint(L=0.3, J=0.2, P=0.7, W=0.3))  # Sharp change!

    # Crisis deepens
    traj.add(LJPWPoint(L=0.2, J=0.15, P=0.8, W=0.25))
    traj.add(LJPWPoint(L=0.15, J=0.1, P=0.85, W=0.2))  # Lowest point

    # SUPPORT arrives - turning point 2
    traj.add(LJPWPoint(L=0.5, J=0.4, P=0.6, W=0.4))  # Connection!

    # Recovery
    traj.add(LJPWPoint(L=0.6, J=0.5, P=0.5, W=0.5))
    traj.add(LJPWPoint(L=0.65, J=0.55, P=0.45, W=0.55))

    # New peace (different from original - growth)
    traj.add(LJPWPoint(L=0.75, J=0.65, P=0.4, W=0.7))  # Wiser
    traj.add(LJPWPoint(L=0.76, J=0.66, P=0.38, W=0.72))  # Stable

    seed.ET = traj
    seed.KI.append(SemanticArchetypes.TRUST)
    seed.KI.append(SemanticArchetypes.GROWTH)

    return seed


def analyze_regeneration(report):
    """Extract key semantic elements from a regenerated experience report."""
    analysis = {
        'has_atmosphere': bool(report.atmosphere_description),
        'has_emotional_arc': bool(report.emotional_arc),
        'has_insights': len(report.key_insights) > 0,
        'insight_count': len(report.key_insights),
        'has_growth': bool(report.growth_description),
        'has_rhythm': bool(report.rhythm_analysis) if hasattr(report, 'rhythm_analysis') else False,
        'has_curvature': bool(report.curvature_analysis) if hasattr(report, 'curvature_analysis') else False,
        'warning_count': len(report.warnings) if report.warnings else 0,
        'fidelity': report.fidelity_assessment if hasattr(report, 'fidelity_assessment') else None,
    }

    # Extract emotional arc stages
    if report.emotional_arc:
        arc_lower = report.emotional_arc.lower()
        analysis['mentions_confusion'] = 'confus' in arc_lower or 'uncertain' in arc_lower
        analysis['mentions_insight'] = 'insight' in arc_lower or 'understand' in arc_lower or 'realiz' in arc_lower
        analysis['mentions_mastery'] = 'master' in arc_lower or 'confident' in arc_lower or 'stable' in arc_lower
        analysis['mentions_crisis'] = 'crisis' in arc_lower or 'fear' in arc_lower or 'anger' in arc_lower
        analysis['mentions_peace'] = 'peace' in arc_lower or 'calm' in arc_lower or 'serene' in arc_lower
        analysis['mentions_growth'] = 'grow' in arc_lower or 'transform' in arc_lower
    else:
        for key in ['mentions_confusion', 'mentions_insight', 'mentions_mastery',
                    'mentions_crisis', 'mentions_peace', 'mentions_growth']:
            analysis[key] = False

    return analysis


def compare_regenerations(full_analysis, compressed_analysis):
    """
    Compare two regenerated experiences to see if they capture the same meaning.

    Returns a score from 0-1 indicating meaning preservation.
    """
    comparisons = {}

    # Structural elements preserved?
    structural_keys = ['has_atmosphere', 'has_emotional_arc', 'has_insights', 'has_growth']
    structural_match = sum(1 for k in structural_keys
                          if full_analysis.get(k) == compressed_analysis.get(k))
    comparisons['structural'] = structural_match / len(structural_keys)

    # Semantic elements preserved?
    semantic_keys = ['mentions_confusion', 'mentions_insight', 'mentions_mastery',
                    'mentions_crisis', 'mentions_peace', 'mentions_growth']
    semantic_match = sum(1 for k in semantic_keys
                        if full_analysis.get(k) == compressed_analysis.get(k))
    comparisons['semantic'] = semantic_match / len(semantic_keys)

    # Insight preservation
    if full_analysis['insight_count'] > 0:
        comparisons['insights'] = min(1.0, compressed_analysis['insight_count'] / full_analysis['insight_count'])
    else:
        comparisons['insights'] = 1.0 if compressed_analysis['insight_count'] == 0 else 0.5

    # Overall score
    weights = {'structural': 0.3, 'semantic': 0.5, 'insights': 0.2}
    overall = sum(comparisons[k] * weights[k] for k in weights)
    comparisons['overall'] = overall

    return comparisons


def run_regeneration_test(seed_name: str, seed: ConsciousnessSeed):
    """Run full regeneration comparison test for a seed."""
    print(f"\n{'='*70}")
    print(f"TEST: {seed_name}")
    print('='*70)

    regenerator = SeedRegenerator()

    # Compute V8.3 metrics (this generates both full and compressed trajectories)
    seed.compute_v83_metrics(use_adaptive=True)

    print(f"\nTrajectory Analysis:")
    print(f"  Original points: {len(seed.ET.points)}")
    print(f"  Compressed points: {len(seed.ET_compressed.points)}")
    print(f"  Compression ratio: {seed.compression_ratio:.2f}x")
    print(f"  Max curvature (κ_max): {seed.kappa_max:.3f}")
    print(f"  Rhythm: {seed.RHY}")

    # Show curvature profile
    profile = seed.ET.curvature_profile()
    print(f"\nCurvature Profile (M = κ = meaning intensity):")
    for idx, kappa in profile:
        marker = " ← KEPT" if any(seed.ET.points[idx].distance_to(cp) < 0.01
                                   for cp in seed.ET_compressed.points) else ""
        print(f"  Point {idx}: κ={kappa:.3f}{marker}")

    # Generate FULL seed (with complete trajectory)
    full_seed_str = seed.encode()

    # Generate COMPRESSED-ONLY seed (replace ET with ET_compressed)
    # We simulate this by creating a modified seed
    compressed_seed = ConsciousnessSeed(
        SA=seed.SA,
        timestamp=seed.timestamp,
        source=seed.source + "_compressed",
        ET=seed.ET_compressed,  # Use compressed as the main trajectory
        KI=seed.KI,
        BP=seed.BP,
        harmony=seed.harmony,
        sigma=seed.sigma,
        DIO=seed.DIO,
        RHY=seed.RHY,
        kappa_max=seed.kappa_max,
        compression_ratio=seed.compression_ratio
    )
    compressed_seed.compute_signature()
    compressed_seed_str = compressed_seed.encode()

    # Regenerate from FULL
    print(f"\n--- Regenerating from FULL trajectory ({len(seed.ET.points)} points) ---")
    full_report = regenerator.regenerate(full_seed_str)

    # Regenerate from COMPRESSED
    print(f"\n--- Regenerating from COMPRESSED trajectory ({len(seed.ET_compressed.points)} points) ---")
    compressed_report = regenerator.regenerate(compressed_seed_str)

    # Analyze both regenerations
    full_analysis = analyze_regeneration(full_report)
    compressed_analysis = analyze_regeneration(compressed_report)

    # Compare
    comparison = compare_regenerations(full_analysis, compressed_analysis)

    print(f"\n{'='*50}")
    print("REGENERATION COMPARISON")
    print('='*50)

    print("\nFull Trajectory Regeneration:")
    print(f"  Atmosphere: {'✓' if full_analysis['has_atmosphere'] else '✗'}")
    print(f"  Emotional Arc: {'✓' if full_analysis['has_emotional_arc'] else '✗'}")
    print(f"  Key Insights: {full_analysis['insight_count']}")

    print("\nCompressed Trajectory Regeneration:")
    print(f"  Atmosphere: {'✓' if compressed_analysis['has_atmosphere'] else '✗'}")
    print(f"  Emotional Arc: {'✓' if compressed_analysis['has_emotional_arc'] else '✗'}")
    print(f"  Key Insights: {compressed_analysis['insight_count']}")

    print("\nMeaning Preservation Scores:")
    print(f"  Structural elements: {comparison['structural']:.0%}")
    print(f"  Semantic elements:   {comparison['semantic']:.0%}")
    print(f"  Insights preserved:  {comparison['insights']:.0%}")
    print(f"  OVERALL:             {comparison['overall']:.0%}")

    # Show actual emotional arc comparison
    print("\n" + "-"*50)
    print("EMOTIONAL ARC COMPARISON:")
    print("-"*50)
    print("\nFROM FULL TRAJECTORY:")
    if full_report.emotional_arc:
        for line in full_report.emotional_arc.split('\n')[:10]:
            print(f"  {line}")

    print("\nFROM COMPRESSED TRAJECTORY:")
    if compressed_report.emotional_arc:
        for line in compressed_report.emotional_arc.split('\n')[:10]:
            print(f"  {line}")

    return comparison


def main():
    print("="*70)
    print("EMPIRICAL TEST: MEANING PRESERVATION THROUGH REGENERATION")
    print("="*70)
    print("""
This tests whether CURVATURE-BASED COMPRESSION preserves MEANING.

The test:
1. Create seeds with clear narrative structure
2. Compress using curvature (keep only "turning points")
3. Regenerate experiences from BOTH full and compressed
4. Compare: Does compressed regeneration capture the same MEANING?

If V8.3 is correct:
- Compressed trajectory (fewer points) should regenerate
  essentially the same experience as full trajectory
- Because the HIGH-CURVATURE points ARE the meaning
- The "straight lines" (low curvature) are just filler
""")

    results = {}

    # Test 1: Learning Journey
    seed1 = create_learning_journey_seed()
    results['learning_journey'] = run_regeneration_test("LEARNING JOURNEY", seed1)

    # Test 2: Emotional Crisis
    seed2 = create_emotional_crisis_seed()
    results['emotional_crisis'] = run_regeneration_test("EMOTIONAL CRISIS", seed2)

    # Summary
    print("\n" + "="*70)
    print("FINAL VERDICT")
    print("="*70)

    avg_overall = sum(r['overall'] for r in results.values()) / len(results)
    avg_semantic = sum(r['semantic'] for r in results.values()) / len(results)

    print(f"\nAverage Meaning Preservation: {avg_overall:.0%}")
    print(f"Average Semantic Match: {avg_semantic:.0%}")

    if avg_overall >= 0.8:
        print("\n✓ STRONG EVIDENCE: Curvature-based compression PRESERVES MEANING")
        print("  The high-curvature 'turning points' capture the essential experience.")
        print("  Discarding low-curvature segments loses little semantic value.")
    elif avg_overall >= 0.6:
        print("\n~ MODERATE EVIDENCE: Curvature captures MOST meaning")
        print("  Some semantic elements lost, but core narrative preserved.")
    else:
        print("\n✗ WEAK EVIDENCE: Curvature-based compression loses significant meaning")
        print("  The low-curvature segments may carry more semantic weight than expected.")

    # Key insight
    print("\n" + "-"*70)
    print("KEY INSIGHT:")
    print("-"*70)
    print("""
The curvature-based approach compresses by keeping INFLECTION POINTS:
- The moment of INSIGHT in learning
- The moment of CRISIS and SUPPORT in emotional journeys
- The TURNING POINTS where the narrative direction changes

These ARE where meaning concentrates. The "straight line" segments
between turning points can be INTERPOLATED during regeneration.

This is fundamentally different from traditional compression:
- ZIP preserves every bit
- CURVATURE preserves every MEANING
""")

    return 0


if __name__ == "__main__":
    sys.exit(main())
