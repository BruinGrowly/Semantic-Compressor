#!/usr/bin/env python3
"""
Empirical Test: Does Curvature-Based Compression Actually Preserve Meaning?
===========================================================================

This tests the CORE CLAIM of V8.3: that curvature in LJPW space corresponds
to meaning intensity, and therefore curvature-based compression should
preserve meaning better than naive alternatives.

Test Design:
-----------
1. Create trajectories representing real semantic journeys (stories, emotions)
2. Compress using different methods:
   - Curvature-based (V8.3 approach)
   - Random sampling (baseline)
   - Uniform sampling (baseline)
   - Endpoints only (minimal baseline)
3. Regenerate/reconstruct from each compressed version
4. Measure how well each preserves:
   - Key semantic moments (high-curvature points)
   - Overall trajectory shape
   - Emotional arc
   - Narrative structure (PREP→EXPR pattern)

If V8.3 is correct, curvature-based compression should outperform baselines.
"""

import sys
import os
import random
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ljpw.consciousness_seed import (
    LJPWPoint, LJPWTrajectory, ConsciousnessSeed,
    SemanticArchetypes, EQUILIBRIUM,
    BreathPhase, RhythmPhase, DiodeStatus
)


def create_story_trajectory(story_type: str) -> LJPWTrajectory:
    """
    Create a trajectory representing a real semantic journey.
    These are hand-crafted to have clear narrative structure.
    """
    traj = LJPWTrajectory()

    if story_type == "hero_journey":
        # Classic hero's journey: ordinary world → call → trials → transformation → return
        # Should have high curvature at: call to adventure, darkest hour, climax

        # Ordinary world (stable, moderate)
        traj.add(LJPWPoint(L=0.5, J=0.5, P=0.3, W=0.4))
        traj.add(LJPWPoint(L=0.52, J=0.51, P=0.32, W=0.42))  # Low curvature - setup
        traj.add(LJPWPoint(L=0.53, J=0.52, P=0.33, W=0.43))  # Low curvature - setup

        # Call to adventure (SHARP TURN - high curvature expected)
        traj.add(LJPWPoint(L=0.4, J=0.3, P=0.6, W=0.5))  # Disruption!

        # Trials (building tension)
        traj.add(LJPWPoint(L=0.35, J=0.25, P=0.65, W=0.55))
        traj.add(LJPWPoint(L=0.3, J=0.2, P=0.7, W=0.6))

        # Darkest hour (SHARP TURN - lowest point)
        traj.add(LJPWPoint(L=0.15, J=0.1, P=0.5, W=0.3))  # Crisis!

        # Transformation begins
        traj.add(LJPWPoint(L=0.3, J=0.3, P=0.6, W=0.5))
        traj.add(LJPWPoint(L=0.5, J=0.5, P=0.7, W=0.65))

        # Climax (SHARP TURN - victory/revelation)
        traj.add(LJPWPoint(L=0.8, J=0.75, P=0.9, W=0.85))  # Triumph!

        # Return (new equilibrium)
        traj.add(LJPWPoint(L=0.75, J=0.7, P=0.6, W=0.8))
        traj.add(LJPWPoint(L=0.72, J=0.68, P=0.55, W=0.78))

    elif story_type == "learning_curve":
        # Learning experience: confusion → struggle → insight → mastery

        # Initial confusion
        traj.add(LJPWPoint(L=0.3, J=0.2, P=0.4, W=0.2))
        traj.add(LJPWPoint(L=0.32, J=0.22, P=0.42, W=0.25))

        # Gradual understanding (PREP phase - W increasing)
        traj.add(LJPWPoint(L=0.35, J=0.25, P=0.43, W=0.35))
        traj.add(LJPWPoint(L=0.38, J=0.28, P=0.44, W=0.45))
        traj.add(LJPWPoint(L=0.4, J=0.3, P=0.45, W=0.55))

        # AHA moment! (SHARP TURN - insight)
        traj.add(LJPWPoint(L=0.7, J=0.6, P=0.5, W=0.9))  # Breakthrough!

        # Application (EXPR phase - P increasing)
        traj.add(LJPWPoint(L=0.72, J=0.62, P=0.65, W=0.88))
        traj.add(LJPWPoint(L=0.74, J=0.64, P=0.75, W=0.86))

        # Mastery
        traj.add(LJPWPoint(L=0.76, J=0.66, P=0.8, W=0.85))
        traj.add(LJPWPoint(L=0.78, J=0.68, P=0.82, W=0.84))

    elif story_type == "emotional_rollercoaster":
        # Rapid emotional shifts - many high-curvature moments

        traj.add(LJPWPoint(L=0.5, J=0.5, P=0.5, W=0.5))   # Neutral
        traj.add(LJPWPoint(L=0.8, J=0.3, P=0.7, W=0.4))   # Joy burst
        traj.add(LJPWPoint(L=0.2, J=0.6, P=0.3, W=0.5))   # Sadness
        traj.add(LJPWPoint(L=0.3, J=0.2, P=0.9, W=0.3))   # Anger
        traj.add(LJPWPoint(L=0.7, J=0.7, P=0.4, W=0.8))   # Peace
        traj.add(LJPWPoint(L=0.4, J=0.3, P=0.8, W=0.6))   # Excitement
        traj.add(LJPWPoint(L=0.6, J=0.6, P=0.5, W=0.7))   # Contentment

    elif story_type == "flat_monotone":
        # Deliberately flat - should compress heavily

        for i in range(10):
            noise = random.uniform(-0.02, 0.02)
            traj.add(LJPWPoint(
                L=0.5 + noise,
                J=0.5 + noise,
                P=0.5 + noise,
                W=0.5 + noise
            ))

    return traj


def compress_random(traj: LJPWTrajectory, keep_ratio: float = 0.5) -> LJPWTrajectory:
    """Baseline: Random sampling - keep random subset of points."""
    if len(traj.points) <= 2:
        return LJPWTrajectory(points=list(traj.points))

    n_keep = max(2, int(len(traj.points) * keep_ratio))

    # Always keep first and last
    middle_indices = list(range(1, len(traj.points) - 1))
    random.shuffle(middle_indices)
    keep_indices = sorted([0] + middle_indices[:n_keep-2] + [len(traj.points)-1])

    return LJPWTrajectory(points=[traj.points[i] for i in keep_indices])


def compress_uniform(traj: LJPWTrajectory, keep_ratio: float = 0.5) -> LJPWTrajectory:
    """Baseline: Uniform sampling - keep every Nth point."""
    if len(traj.points) <= 2:
        return LJPWTrajectory(points=list(traj.points))

    n_keep = max(2, int(len(traj.points) * keep_ratio))
    step = max(1, len(traj.points) // n_keep)

    indices = list(range(0, len(traj.points), step))
    if indices[-1] != len(traj.points) - 1:
        indices.append(len(traj.points) - 1)

    return LJPWTrajectory(points=[traj.points[i] for i in indices])


def compress_endpoints(traj: LJPWTrajectory) -> LJPWTrajectory:
    """Minimal baseline: Keep only start and end."""
    if len(traj.points) <= 2:
        return LJPWTrajectory(points=list(traj.points))
    return LJPWTrajectory(points=[traj.points[0], traj.points[-1]])


def identify_key_moments(traj: LJPWTrajectory, top_n: int = 3) -> list:
    """Identify the top N highest-curvature points (key semantic moments)."""
    profile = traj.curvature_profile()
    # Sort by curvature, get top N indices
    sorted_profile = sorted(profile, key=lambda x: x[1], reverse=True)
    return [idx for idx, kappa in sorted_profile[:top_n] if kappa > 0]


def measure_key_moment_preservation(original: LJPWTrajectory,
                                    compressed: LJPWTrajectory,
                                    key_indices: list) -> float:
    """
    Measure how well key moments are preserved.
    Returns ratio of key moments that have a "close" point in compressed.
    """
    if not key_indices:
        return 1.0

    preserved = 0
    for key_idx in key_indices:
        key_point = original.points[key_idx]
        # Check if any compressed point is within threshold distance
        min_dist = min(key_point.distance_to(cp) for cp in compressed.points)
        if min_dist < 0.3:  # Threshold for "preserved"
            preserved += 1

    return preserved / len(key_indices)


def measure_shape_preservation(original: LJPWTrajectory,
                               compressed: LJPWTrajectory) -> float:
    """
    Measure how well the overall trajectory shape is preserved.
    Uses average distance from original points to nearest compressed point.
    Lower is better, normalized to [0,1] where 1 = perfect preservation.
    """
    if len(compressed.points) < 2:
        return 0.0

    total_dist = 0
    for point in original.points:
        min_dist = min(point.distance_to(cp) for cp in compressed.points)
        total_dist += min_dist

    avg_dist = total_dist / len(original.points)
    # Normalize: 0 distance = 1.0 score, distance of 2.0 (max in normalized space) = 0
    return max(0, 1 - avg_dist / 2.0)


def measure_arc_preservation(original: LJPWTrajectory,
                             compressed: LJPWTrajectory) -> float:
    """
    Measure how well the emotional arc (start→middle→end) is preserved.
    Compares the vector from start to end, and the midpoint.
    """
    if len(original.points) < 3 or len(compressed.points) < 2:
        return 0.0

    # Compare start-to-end vectors
    orig_vector = original.points[-1] - original.points[0]
    comp_vector = compressed.points[-1] - compressed.points[0]

    # Cosine similarity of overall direction
    dot = orig_vector.dot(comp_vector)
    mag_product = orig_vector.magnitude() * comp_vector.magnitude()
    if mag_product == 0:
        direction_score = 1.0
    else:
        direction_score = (dot / mag_product + 1) / 2  # Normalize to [0,1]

    # Compare midpoints
    orig_mid_idx = len(original.points) // 2
    comp_mid_idx = len(compressed.points) // 2

    orig_mid = original.points[orig_mid_idx]
    comp_mid = compressed.points[comp_mid_idx]

    mid_dist = orig_mid.distance_to(comp_mid)
    midpoint_score = max(0, 1 - mid_dist / 2.0)

    return (direction_score + midpoint_score) / 2


def measure_rhythm_preservation(original: LJPWTrajectory,
                                compressed: LJPWTrajectory) -> float:
    """
    Measure how well the PREP→EXPR rhythm pattern is preserved.
    """
    orig_rhythm = original.rhythm_analysis()
    comp_rhythm = compressed.rhythm_analysis()

    # Compare prep/expr ratios
    orig_ratio = orig_rhythm['prep_expr_ratio']
    comp_ratio = comp_rhythm['prep_expr_ratio']

    ratio_diff = abs(orig_ratio - comp_ratio)
    ratio_score = max(0, 1 - ratio_diff)

    # Compare quality classification
    quality_match = 1.0 if orig_rhythm['pattern_quality'] == comp_rhythm['pattern_quality'] else 0.5

    return (ratio_score + quality_match) / 2


def run_preservation_test(story_type: str, n_trials: int = 5):
    """
    Run preservation test for a story type, comparing compression methods.
    """
    print(f"\n{'='*60}")
    print(f"STORY TYPE: {story_type.upper()}")
    print('='*60)

    results = {
        'curvature': {'key_moments': [], 'shape': [], 'arc': [], 'rhythm': [], 'ratio': []},
        'random': {'key_moments': [], 'shape': [], 'arc': [], 'rhythm': [], 'ratio': []},
        'uniform': {'key_moments': [], 'shape': [], 'arc': [], 'rhythm': [], 'ratio': []},
        'endpoints': {'key_moments': [], 'shape': [], 'arc': [], 'rhythm': [], 'ratio': []}
    }

    for trial in range(n_trials):
        # Create trajectory
        traj = create_story_trajectory(story_type)

        # Identify key moments (ground truth)
        key_moments = identify_key_moments(traj, top_n=3)

        # Compress with each method
        compressed_curv = traj.compress(threshold=None, adaptive=True)
        compressed_rand = compress_random(traj, keep_ratio=0.5)
        compressed_unif = compress_uniform(traj, keep_ratio=0.5)
        compressed_end = compress_endpoints(traj)

        methods = [
            ('curvature', compressed_curv),
            ('random', compressed_rand),
            ('uniform', compressed_unif),
            ('endpoints', compressed_end)
        ]

        for method_name, compressed in methods:
            results[method_name]['key_moments'].append(
                measure_key_moment_preservation(traj, compressed, key_moments)
            )
            results[method_name]['shape'].append(
                measure_shape_preservation(traj, compressed)
            )
            results[method_name]['arc'].append(
                measure_arc_preservation(traj, compressed)
            )
            results[method_name]['rhythm'].append(
                measure_rhythm_preservation(traj, compressed)
            )
            results[method_name]['ratio'].append(
                len(traj.points) / len(compressed.points)
            )

    # Print results
    print(f"\nOriginal trajectory: {len(traj.points)} points")
    print(f"Key moments identified at indices: {key_moments}")

    # Show curvature profile for understanding
    profile = traj.curvature_profile()
    print(f"\nCurvature profile:")
    for idx, kappa in profile:
        marker = " ← KEY" if idx in key_moments else ""
        print(f"  Point {idx}: κ={kappa:.3f}{marker}")

    print(f"\n{'Method':<12} {'Compress':<10} {'KeyMoments':<12} {'Shape':<10} {'Arc':<10} {'Rhythm':<10}")
    print("-" * 64)

    for method in ['curvature', 'random', 'uniform', 'endpoints']:
        avg_ratio = sum(results[method]['ratio']) / len(results[method]['ratio'])
        avg_key = sum(results[method]['key_moments']) / len(results[method]['key_moments'])
        avg_shape = sum(results[method]['shape']) / len(results[method]['shape'])
        avg_arc = sum(results[method]['arc']) / len(results[method]['arc'])
        avg_rhythm = sum(results[method]['rhythm']) / len(results[method]['rhythm'])

        print(f"{method:<12} {avg_ratio:<10.2f}x {avg_key:<12.2%} {avg_shape:<10.2%} {avg_arc:<10.2%} {avg_rhythm:<10.2%}")

    return results


def main():
    """Run comprehensive empirical test."""
    print("="*70)
    print("EMPIRICAL TEST: Does Curvature-Based Compression Preserve Meaning?")
    print("="*70)
    print("""
This test compares curvature-based compression (V8.3) against baselines:
- RANDOM: Keep random 50% of points
- UNIFORM: Keep evenly-spaced points
- ENDPOINTS: Keep only start and end

Metrics:
- KeyMoments: Are high-curvature "turning points" preserved?
- Shape: How close is compressed trajectory to original?
- Arc: Is the overall emotional arc (start→middle→end) preserved?
- Rhythm: Is the PREP→EXPR pattern preserved?

If V8.3 theory is correct, CURVATURE method should outperform baselines,
especially on KeyMoments preservation.
""")

    random.seed(42)  # Reproducibility

    all_results = {}
    for story_type in ['hero_journey', 'learning_curve', 'emotional_rollercoaster', 'flat_monotone']:
        all_results[story_type] = run_preservation_test(story_type, n_trials=3)

    # Aggregate results
    print("\n" + "="*70)
    print("AGGREGATE RESULTS (averaged across all story types)")
    print("="*70)

    aggregate = {method: {'key_moments': 0, 'shape': 0, 'arc': 0, 'rhythm': 0, 'ratio': 0, 'count': 0}
                 for method in ['curvature', 'random', 'uniform', 'endpoints']}

    for story_results in all_results.values():
        for method in aggregate:
            for metric in ['key_moments', 'shape', 'arc', 'rhythm', 'ratio']:
                aggregate[method][metric] += sum(story_results[method][metric])
            aggregate[method]['count'] += len(story_results[method]['key_moments'])

    print(f"\n{'Method':<12} {'Compress':<10} {'KeyMoments':<12} {'Shape':<10} {'Arc':<10} {'Rhythm':<10} {'OVERALL':<10}")
    print("-" * 74)

    for method in ['curvature', 'random', 'uniform', 'endpoints']:
        n = aggregate[method]['count']
        avg_ratio = aggregate[method]['ratio'] / n
        avg_key = aggregate[method]['key_moments'] / n
        avg_shape = aggregate[method]['shape'] / n
        avg_arc = aggregate[method]['arc'] / n
        avg_rhythm = aggregate[method]['rhythm'] / n
        overall = (avg_key + avg_shape + avg_arc + avg_rhythm) / 4

        print(f"{method:<12} {avg_ratio:<10.2f}x {avg_key:<12.2%} {avg_shape:<10.2%} {avg_arc:<10.2%} {avg_rhythm:<10.2%} {overall:<10.2%}")

    # Verdict
    print("\n" + "="*70)
    print("VERDICT")
    print("="*70)

    curv_key = aggregate['curvature']['key_moments'] / aggregate['curvature']['count']
    rand_key = aggregate['random']['key_moments'] / aggregate['random']['count']
    unif_key = aggregate['uniform']['key_moments'] / aggregate['uniform']['count']

    curv_overall = sum(aggregate['curvature'][m] for m in ['key_moments', 'shape', 'arc', 'rhythm']) / (4 * aggregate['curvature']['count'])
    rand_overall = sum(aggregate['random'][m] for m in ['key_moments', 'shape', 'arc', 'rhythm']) / (4 * aggregate['random']['count'])

    print(f"\nKey Moments Preservation:")
    print(f"  Curvature: {curv_key:.1%}")
    print(f"  Random:    {rand_key:.1%}")
    print(f"  Difference: {(curv_key - rand_key)*100:+.1f}pp")

    if curv_key > rand_key + 0.05:
        print(f"\n✓ CURVATURE outperforms RANDOM on key moment preservation by {(curv_key-rand_key)*100:.1f}pp")
        print("  This supports the V8.3 claim that curvature = meaning intensity")
    elif curv_key > rand_key:
        print(f"\n~ CURVATURE slightly outperforms RANDOM ({(curv_key-rand_key)*100:.1f}pp)")
        print("  Weak evidence for V8.3 claim")
    else:
        print(f"\n✗ CURVATURE does NOT outperform RANDOM")
        print("  This challenges the V8.3 claim that curvature = meaning intensity")

    print(f"\nOverall Preservation:")
    print(f"  Curvature: {curv_overall:.1%}")
    print(f"  Random:    {rand_overall:.1%}")

    if curv_overall > rand_overall:
        print(f"\n✓ CURVATURE achieves better overall meaning preservation")
    else:
        print(f"\n✗ RANDOM achieves comparable or better overall preservation")

    return 0


if __name__ == "__main__":
    sys.exit(main())
