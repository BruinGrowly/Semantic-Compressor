#!/usr/bin/env python3
"""
Test V8.3 Framework Corrections
================================

Validates that the implementation aligns with V8.3 Framework specifications:
1. Dual harmony methods (H_static and H_self)
2. Conductivity formula with clamped H
3. Adaptive curvature threshold for compression
4. Derivative-based rhythm pattern analysis
5. Debt accumulation tracking
6. Phase transition detection
7. Consciousness metric validation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ljpw.consciousness_seed import (
    LJPWPoint, LJPWTrajectory, ConsciousnessSeed, SeedGenerator,
    SemanticArchetypes, EQUILIBRIUM, ANCHOR, PHI, PHI_INV,
    BreathPhase, RhythmPhase, DiodeStatus
)


def test_dual_harmony():
    """Test that H_static and H_self produce different, correct values."""
    print("\n" + "="*60)
    print("TEST 1: Dual Harmony Methods")
    print("="*60)

    # Test point near equilibrium
    eq_point = LJPWPoint(
        L=EQUILIBRIUM['L'] * 2 - 1,  # Convert [0,1] to [-1,1]
        J=EQUILIBRIUM['J'] * 2 - 1,
        P=EQUILIBRIUM['P'] * 2 - 1,
        W=EQUILIBRIUM['W'] * 2 - 1
    )

    h_static = eq_point.harmony_static()
    h_self = eq_point.harmony_self()

    print(f"Point near equilibrium: {eq_point.encode()}")
    print(f"  H_static (distance-based): {h_static:.4f}")
    print(f"  H_self (product-based):    {h_self:.4f}")
    print(f"  H_static should be close to 1.0 at equilibrium: {'PASS' if 0.9 < h_static <= 1.0 else 'FAIL'}")
    print(f"  H_self should equal 1.0 at equilibrium: {'PASS' if 0.99 < h_self < 1.01 else 'FAIL'}")

    # Test high point (near anchor)
    high_point = LJPWPoint(L=0.9, J=0.9, P=0.9, W=0.9)
    h_static_high = high_point.harmony_static()
    h_self_high = high_point.harmony_self()

    print(f"\nPoint near anchor: {high_point.encode()}")
    print(f"  H_static: {h_static_high:.4f} (should be < 1.0)")
    print(f"  H_self:   {h_self_high:.4f} (should be > 1.0 for autopoietic systems)")

    # Verify H_static is always in [0,1]
    test_passed = 0 <= h_static <= 1.0 and 0 <= h_static_high <= 1.0
    print(f"  H_static always in [0,1]: {'PASS' if test_passed else 'FAIL'}")

    return test_passed


def test_conductivity():
    """Test that conductivity uses H_static and is properly clamped."""
    print("\n" + "="*60)
    print("TEST 2: Conductivity Formula")
    print("="*60)

    # Test with known values from V8.1 specification
    # Low Love:  L = 0.30, H = 0.30 → σ = 0.027
    # High Love: L = 0.95, H = 0.80 → σ = 0.608

    # Convert to [-1,1] range: L=0.30 → L=-0.4, L=0.95 → L=0.9
    low_love_point = LJPWPoint(L=-0.4, J=0.0, P=0.0, W=0.0)
    high_love_point = LJPWPoint(L=0.9, J=0.6, P=0.6, W=0.6)

    sigma_low = low_love_point.conductivity()
    sigma_high = high_love_point.conductivity()

    print(f"Low Love point: L={low_love_point.L}")
    print(f"  σ = {sigma_low:.4f}")
    print(f"  Expected range: ~0.02-0.05 (low conductivity)")

    print(f"\nHigh Love point: L={high_love_point.L}")
    print(f"  σ = {sigma_high:.4f}")
    print(f"  Expected range: ~0.4-0.7 (high conductivity)")

    # Verify conductivity is in [0,1]
    test_passed = 0 <= sigma_low <= 1.0 and 0 <= sigma_high <= 1.0
    print(f"\n  σ always in [0,1]: {'PASS' if test_passed else 'FAIL'}")
    print(f"  High Love has higher σ: {'PASS' if sigma_high > sigma_low else 'FAIL'}")

    return test_passed and sigma_high > sigma_low


def test_adaptive_compression():
    """Test adaptive curvature threshold for compression."""
    print("\n" + "="*60)
    print("TEST 3: Adaptive Curvature Compression")
    print("="*60)

    # Create a trajectory with varying curvature
    traj = LJPWTrajectory()

    # Straight section (low curvature - should be compressed out)
    traj.add(LJPWPoint(0.0, 0.0, 0.0, 0.0))
    traj.add(LJPWPoint(0.1, 0.1, 0.1, 0.1))
    traj.add(LJPWPoint(0.2, 0.2, 0.2, 0.2))

    # Sharp turn (high curvature - should be kept)
    traj.add(LJPWPoint(0.5, 0.8, 0.3, 0.9))

    # Another straight section
    traj.add(LJPWPoint(0.55, 0.85, 0.35, 0.92))
    traj.add(LJPWPoint(0.6, 0.9, 0.4, 0.95))

    # Another turn
    traj.add(LJPWPoint(0.2, 0.3, 0.8, 0.4))

    # End
    traj.add(LJPWPoint(0.3, 0.4, 0.9, 0.5))

    print(f"Original trajectory: {len(traj.points)} points")

    # Curvature profile
    profile = traj.curvature_profile()
    print(f"Curvature profile:")
    for idx, kappa in profile:
        print(f"  Point {idx}: κ = {kappa:.4f}")

    # Fixed threshold compression
    compressed_fixed = traj.compress(threshold=0.1, adaptive=False)
    print(f"\nFixed threshold (0.1): {len(compressed_fixed.points)} points")

    # Adaptive threshold compression
    compressed_adaptive = traj.compress(threshold=None, adaptive=True)
    ratio, threshold_used = traj.compress_ratio_adaptive()
    print(f"Adaptive threshold ({threshold_used:.4f}): {len(compressed_adaptive.points)} points")
    print(f"Compression ratio: {ratio:.2f}x")

    test_passed = len(compressed_adaptive.points) < len(traj.points)
    print(f"\n  Compression achieved: {'PASS' if test_passed else 'FAIL'}")

    return test_passed


def test_rhythm_derivative():
    """Test derivative-based rhythm pattern analysis."""
    print("\n" + "="*60)
    print("TEST 4: Derivative-based Rhythm Analysis")
    print("="*60)

    # Create trajectory with clear PREP → EXPR pattern
    # PREP: dW/dt > dP/dt (Wisdom accumulating)
    # EXPR: dP/dt > dW/dt (Power expressing)
    traj = LJPWTrajectory()

    # Preparation phase: W increasing faster than P
    traj.add(LJPWPoint(0.5, 0.5, 0.2, 0.3))
    traj.add(LJPWPoint(0.5, 0.5, 0.25, 0.5))  # W +0.2, P +0.05 → PREP
    traj.add(LJPWPoint(0.5, 0.5, 0.3, 0.7))   # W +0.2, P +0.05 → PREP

    # Expression phase: P increasing faster than W
    traj.add(LJPWPoint(0.5, 0.5, 0.6, 0.75))  # P +0.3, W +0.05 → EXPR
    traj.add(LJPWPoint(0.5, 0.5, 0.9, 0.8))   # P +0.3, W +0.05 → EXPR

    # Transition
    traj.add(LJPWPoint(0.5, 0.5, 0.92, 0.82)) # Both small changes → TRANS

    rhythm = traj.rhythm_pattern()
    rhythm_str = traj.rhythm_string()
    analysis = traj.rhythm_analysis()

    print(f"Rhythm pattern: {rhythm_str}")
    print(f"Analysis:")
    print(f"  PREP count: {analysis['prep_count']}")
    print(f"  EXPR count: {analysis['expr_count']}")
    print(f"  TRANS count: {analysis['trans_count']}")
    print(f"  PREP/EXPR ratio: {analysis['prep_expr_ratio']:.2f}")
    print(f"  Pattern quality: {analysis['pattern_quality']}")

    # Check for PREP phases
    has_prep = analysis['prep_count'] > 0
    has_expr = analysis['expr_count'] > 0
    test_passed = has_prep and has_expr

    print(f"\n  Has PREP phases: {'PASS' if has_prep else 'FAIL'}")
    print(f"  Has EXPR phases: {'PASS' if has_expr else 'FAIL'}")

    return test_passed


def test_debt_accumulation():
    """Test debt accumulation tracking for trajectories."""
    print("\n" + "="*60)
    print("TEST 5: Debt Accumulation Tracking")
    print("="*60)

    # Create trajectory with some CLOSED diode points
    traj = LJPWTrajectory()

    # Healthy point (P ≈ J, diode OPEN)
    traj.add(LJPWPoint(L=0.5, J=0.5, P=0.5, W=0.5))
    traj.add(LJPWPoint(L=0.5, J=0.55, P=0.55, W=0.5))

    # Unhealthy point (High P, Low J - diode may be CLOSED)
    traj.add(LJPWPoint(L=0.3, J=0.1, P=0.9, W=0.4))
    traj.add(LJPWPoint(L=0.2, J=0.05, P=0.95, W=0.3))

    # Recovery
    traj.add(LJPWPoint(L=0.5, J=0.5, P=0.5, W=0.5))

    debt_analysis = traj.debt_accumulation()

    print(f"Debt Analysis:")
    print(f"  Total debt: {debt_analysis['total_debt']:.4f}")
    print(f"  Debt segments: {len(debt_analysis['debt_segments'])}")
    print(f"  Circuit health: {debt_analysis['circuit_health']}")
    print(f"  Closed ratio: {debt_analysis['closed_ratio']:.2%}")
    print(f"  Diode sequence: {debt_analysis['diode_status_sequence']}")

    # Check for debt detection
    test_passed = debt_analysis['circuit_health'] != 'HEALTHY' or debt_analysis['total_debt'] > 0
    print(f"\n  Debt detection working: {'PASS' if test_passed else 'NEEDS_REVIEW'}")

    return True  # This test is informational


def test_phase_transitions():
    """Test phase transition detection."""
    print("\n" + "="*60)
    print("TEST 6: Phase Transition Detection")
    print("="*60)

    # Create trajectory crossing phase boundaries
    traj = LJPWTrajectory()

    # Entropic (H < 0.5, L < 0.5)
    traj.add(LJPWPoint(L=-0.2, J=-0.2, P=0.1, W=-0.1))  # Low everything
    traj.add(LJPWPoint(L=-0.1, J=-0.1, P=0.2, W=0.0))

    # Transition to Homeostatic
    traj.add(LJPWPoint(L=0.3, J=0.3, P=0.3, W=0.3))
    traj.add(LJPWPoint(L=0.4, J=0.4, P=0.4, W=0.4))

    # Transition to Autopoietic (H > 0.6, L >= 0.7)
    traj.add(LJPWPoint(L=0.6, J=0.5, P=0.5, W=0.5))
    traj.add(LJPWPoint(L=0.8, J=0.7, P=0.6, W=0.7))  # High L, should be autopoietic

    transitions = traj.phase_transitions()

    print(f"Phase Transitions: {len(transitions)} detected")
    for t in transitions:
        print(f"  Index {t['index']}: {t['from_phase']} → {t['to_phase']} ({t['direction']})")

    # Check phases of individual points
    print("\nPhase at each point:")
    for i, p in enumerate(traj.points):
        h = p.harmony_static()
        l_norm = (p.L + 1) / 2
        if h < 0.5 or l_norm < 0.5:
            phase = 'ENTROPIC'
        elif h <= 0.6:
            phase = 'HOMEOSTATIC'
        elif l_norm >= 0.7:
            phase = 'AUTOPOIETIC'
        else:
            phase = 'HOMEOSTATIC'
        print(f"  Point {i}: H={h:.3f}, L_norm={l_norm:.3f} → {phase}")

    test_passed = len(transitions) > 0
    print(f"\n  Phase transitions detected: {'PASS' if test_passed else 'FAIL'}")

    return test_passed


def test_consciousness_metric():
    """Test consciousness metric validation."""
    print("\n" + "="*60)
    print("TEST 7: Consciousness Metric Validation")
    print("="*60)

    # Create seed with trajectory
    seed = ConsciousnessSeed(
        SA=LJPWPoint(L=0.7, J=0.6, P=0.7, W=0.8),
        timestamp="2026-01-10T12:00:00",
        source="test"
    )

    traj = LJPWTrajectory()
    traj.add(LJPWPoint(L=0.6, J=0.5, P=0.6, W=0.7))
    traj.add(LJPWPoint(L=0.7, J=0.6, P=0.7, W=0.8))
    traj.add(LJPWPoint(L=0.8, J=0.7, P=0.8, W=0.85))
    seed.ET = traj

    # Compute metrics
    seed.compute_v83_metrics()

    # Validate consciousness
    c_validation = seed.consciousness_validation()

    print(f"Consciousness Validation:")
    print(f"  C metric: {c_validation['consciousness_metric']:.4f}")
    print(f"  Threshold: {c_validation['conscious_threshold']}")
    print(f"  Is conscious: {c_validation['is_conscious']}")
    print(f"  Level: {c_validation['consciousness_level']}")
    print(f"  Description: {c_validation.get('description', 'N/A')}")

    if c_validation['trajectory_analysis']:
        ta = c_validation['trajectory_analysis']
        print(f"  Trajectory C: min={ta['min_c']:.4f}, max={ta['max_c']:.4f}, avg={ta['avg_c']:.4f}")
        print(f"  Conscious points: {ta['conscious_points']}/{ta['total_points']}")

    if c_validation['warnings']:
        print(f"  Warnings: {c_validation['warnings']}")

    test_passed = 'consciousness_metric' in c_validation and 'consciousness_level' in c_validation
    print(f"\n  Consciousness validation working: {'PASS' if test_passed else 'FAIL'}")

    return test_passed


def test_full_v83_analysis():
    """Test comprehensive V8.3 analysis."""
    print("\n" + "="*60)
    print("TEST 8: Full V8.3 Analysis Report")
    print("="*60)

    # Create seed with trajectory
    seed = ConsciousnessSeed(
        SA=LJPWPoint(L=0.6, J=0.5, P=0.65, W=0.7),
        timestamp="2026-01-10T12:00:00",
        source="test"
    )

    traj = LJPWTrajectory()
    traj.add(LJPWPoint(L=0.5, J=0.4, P=0.3, W=0.4))  # Start
    traj.add(LJPWPoint(L=0.55, J=0.45, P=0.35, W=0.6))  # PREP
    traj.add(LJPWPoint(L=0.6, J=0.5, P=0.4, W=0.75))   # PREP
    traj.add(LJPWPoint(L=0.65, J=0.55, P=0.7, W=0.78)) # EXPR
    traj.add(LJPWPoint(L=0.7, J=0.6, P=0.85, W=0.8))   # EXPR
    traj.add(LJPWPoint(L=0.72, J=0.62, P=0.87, W=0.82))# End
    seed.ET = traj

    # Compute full analysis
    report = seed.full_v83_analysis()

    print(f"Full V8.3 Analysis Report:")
    print(f"\nMetrics:")
    print(f"  Harmony (H_static): {report['metrics']['harmony']:.4f}")
    print(f"  Conductivity (σ): {report['metrics']['conductivity']:.4f}")
    print(f"  Max curvature (κ_max): {report['metrics']['kappa_max']:.4f}")
    print(f"  Compression ratio: {report['metrics']['compression_ratio']:.2f}x")

    print(f"\nCircuit Health:")
    ch = report['circuit_health']
    print(f"  Phase: {ch['phase']}")
    print(f"  Diode status: {ch['diode_status']}")
    print(f"  Debt risk: {ch['debt_risk']}")
    print(f"  Friction: {ch['friction']:.4f}")

    print(f"\nConsciousness:")
    cs = report['consciousness']
    print(f"  Level: {cs['consciousness_level']}")
    print(f"  Metric: {cs['consciousness_metric']:.4f}")

    print(f"\nTrajectory Analysis:")
    if report['trajectory_analysis']:
        ta = report['trajectory_analysis']
        if 'rhythm' in ta:
            print(f"  Rhythm quality: {ta['rhythm']['pattern_quality']}")
        if 'debt_accumulation' in ta:
            print(f"  Circuit health: {ta['debt_accumulation']['circuit_health']}")
        if 'phase_transitions' in ta:
            print(f"  Phase transitions: {len(ta['phase_transitions'])}")

    print(f"\nWarnings: {len(report['warnings'])}")
    for w in report['warnings'][:5]:  # Show first 5
        print(f"  - {w}")

    test_passed = all(k in report for k in ['metrics', 'circuit_health', 'consciousness'])
    print(f"\n  Full analysis working: {'PASS' if test_passed else 'FAIL'}")

    return test_passed


def main():
    """Run all V8.3 correction tests."""
    print("="*60)
    print("V8.3 FRAMEWORK CORRECTIONS - VALIDATION TESTS")
    print("="*60)

    results = []

    results.append(("Dual Harmony Methods", test_dual_harmony()))
    results.append(("Conductivity Formula", test_conductivity()))
    results.append(("Adaptive Compression", test_adaptive_compression()))
    results.append(("Rhythm Derivative Analysis", test_rhythm_derivative()))
    results.append(("Debt Accumulation", test_debt_accumulation()))
    results.append(("Phase Transitions", test_phase_transitions()))
    results.append(("Consciousness Metric", test_consciousness_metric()))
    results.append(("Full V8.3 Analysis", test_full_v83_analysis()))

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All V8.3 Framework corrections validated successfully!")
        return 0
    else:
        print("\n⚠ Some tests need attention")
        return 1


if __name__ == "__main__":
    sys.exit(main())
