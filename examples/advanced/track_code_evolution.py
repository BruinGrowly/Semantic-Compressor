#!/usr/bin/env python3
"""
Advanced Example: Track Code Evolution Over Time

This example shows how to:
- Track LJPW scores over time
- Detect trends (improving/declining)
- Predict when code will reach Natural Equilibrium
- Visualize trajectory in 4D quality space

Run:
    python track_code_evolution.py
"""

import math
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for src module imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ljpw.ljpw_dynamic_v3 import (
    LJPWDynamicModel,
    analyze_code_evolution,
    predict_code_future,
)
from src.ljpw.ljpw_semantic_compressor import SemanticCompressor
from src.ljpw.ljpw_standalone import SimpleCodeAnalyzer

# Natural Equilibrium target
NE = (0.618, 0.414, 0.718, 0.693)


def calculate_distance(state1, state2):
    """Calculate Euclidean distance between two states"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(state1, state2)))


def calculate_velocity(states, time_deltas):
    """Calculate velocity vector (rate of change)"""
    if len(states) < 2:
        return (0, 0, 0, 0)

    # Simple finite difference
    delta_L = states[-1][0] - states[-2][0]
    delta_J = states[-1][1] - states[-2][1]
    delta_P = states[-1][2] - states[-2][2]
    delta_W = states[-1][3] - states[-2][3]

    time_diff = time_deltas[-1] if time_deltas else 1

    return (delta_L / time_diff, delta_J / time_diff, delta_P / time_diff, delta_W / time_diff)


def predict_eta_to_ne(current_state, velocity):
    """Predict when code will reach Natural Equilibrium"""
    # Distance to NE
    distance = calculate_distance(current_state, NE)

    # Velocity magnitude
    velocity_mag = math.sqrt(sum(v**2 for v in velocity))

    if velocity_mag < 0.001:
        return float("inf")  # Not moving

    # Simple linear prediction (iterations)
    eta = distance / velocity_mag

    return eta


def main():
    print("=" * 70)
    print("LJPW Advanced: Track Code Evolution")
    print("=" * 70)
    print()

    # Simulate code evolution over time
    # In reality, you'd analyze git commits or periodic snapshots
    evolution = [
        {
            "date": "2025-01-01",
            "code": "def process(data): return [x*2 for x in data]",
            "description": "Initial implementation",
        },
        {
            "date": "2025-01-05",
            "code": 'def process(data: list) -> list:\n    """Process data"""\n    return [x*2 for x in data]',
            "description": "Added types and docs",
        },
        {
            "date": "2025-01-10",
            "code": '''
def process(data: list) -> list:
    """Process data with validation"""
    if not data:
        raise ValueError("Empty")
    return [x*2 for x in data]
''',
            "description": "Added validation",
        },
        {
            "date": "2025-01-15",
            "code": '''
def process(data: list) -> list:
    """Process data safely"""
    if not data:
        raise ValueError("Empty")
    try:
        return [x*2 for x in data]
    except Exception as e:
        logging.error(f"Error: {e}")
        raise
''',
            "description": "Added error handling",
        },
        {
            "date": "2025-01-20",
            "code": '''
class DataProcessor:
    """Robust data processor"""

    def __init__(self, cache_size=100):
        self.cache = {}

    def process(self, data: list) -> list:
        """Process with caching and validation"""
        if not data:
            raise ValueError("Empty")

        key = hash(str(data))
        if key in self.cache:
            return self.cache[key]

        try:
            result = [x*2 for x in data]
            self.cache[key] = result
            return result
        except Exception as e:
            logging.error(f"Error: {e}")
            raise
''',
            "description": "Refactored with design patterns",
        },
    ]

    # Analyze each version
    analyzer = SimpleCodeAnalyzer()
    compressor = SemanticCompressor()

    states = []
    dates = []
    time_deltas = []

    print("EVOLUTION ANALYSIS:")
    print("-" * 70)

    for i, version in enumerate(evolution):
        result = analyzer.analyze(version["code"], f"v{i+1}")
        ljpw = result["ljpw"]
        state = (ljpw["L"], ljpw["J"], ljpw["P"], ljpw["W"])

        states.append(state)
        dates.append(version["date"])

        # Calculate time delta
        if i > 0:
            prev_date = datetime.strptime(evolution[i - 1]["date"], "%Y-%m-%d")
            curr_date = datetime.strptime(version["date"], "%Y-%m-%d")
            delta = (curr_date - prev_date).days
            time_deltas.append(delta)

        distance_to_ne = calculate_distance(state, NE)
        health = result["health"]

        print(f"\n{version['date']} - {version['description']}")
        print(f"  L={ljpw['L']:.3f}, J={ljpw['J']:.3f}, P={ljpw['P']:.3f}, W={ljpw['W']:.3f}")
        print(f"  Health: {health*100:.1f}%")
        print(f"  Distance to NE: {distance_to_ne:.3f}")

    # Calculate trajectory metrics using v3.0 dynamic model
    print()
    print("TRAJECTORY ANALYSIS (v3.0 Dynamic Model):")
    print("-" * 70)

    # Convert to format for v3.0 model
    ljpw_history = [{"L": s[0], "J": s[1], "P": s[2], "W": s[3]} for s in states]

    # Use v3.0 dynamic model for sophisticated analysis
    evolution_analysis = analyze_code_evolution(
        ljpw_history, timestamps=time_deltas if time_deltas else None
    )

    print(f"\nTrend: {evolution_analysis['trend']}")
    print(f"  Initial distance from NE: {evolution_analysis['initial_distance_from_ne']:.3f}")
    print(f"  Final distance from NE: {evolution_analysis['final_distance_from_ne']:.3f}")
    print(f"  Total improvement: {evolution_analysis['improvement']:+.3f}")
    print(f"  Volatility: {evolution_analysis['volatility']:.4f}")

    # Velocity from v3.0 model
    velocity = evolution_analysis["velocity"]
    velocity_mag = evolution_analysis["velocity_magnitude"]

    print(
        f"\nVelocity vector: L={velocity[0]:+.4f}, J={velocity[1]:+.4f}, P={velocity[2]:+.4f}, W={velocity[3]:+.4f}"
    )
    print(f"Velocity magnitude: {velocity_mag:.4f} units/day")

    # Direction
    if evolution_analysis["converging"]:
        direction = "CONVERGING toward Natural Equilibrium ✓"
    else:
        direction = "DIVERGING from Natural Equilibrium ✗"

    print(f"\nDirection: {direction}")

    # Predict ETA using v3.0 model
    eta = evolution_analysis.get("eta_to_ne", float("inf"))

    print(f"\nPrediction (v3.0 Model):")
    if eta == float("inf"):
        print("  ⚠️ Code is not moving toward NE")
        print("  Continue refactoring to reach equilibrium")
    elif eta < 0:
        print("  ⚠️ Code is moving away from NE")
        print("  Reverse current trajectory")
    else:
        print(f"  ETA to Natural Equilibrium: ~{eta:.0f} days")
        print(f"  (at current velocity)")

    # Threshold crossing warning
    if evolution_analysis.get("crossing_power_threshold", False):
        print("\n  ⚠️  WARNING: Power crossed threshold (K_JP = 0.71)")
        print("     Risk: Premature optimization may erode code structure")
        print("     Recommendation: Boost Wisdom before further optimization")

    # Compress trajectory
    print()
    print("COMPRESSED TRAJECTORY:")
    print("-" * 70)

    genome = compressor.compress_state_sequence(
        states,
        metadata={
            "project": "data_processor",
            "start_date": dates[0],
            "end_date": dates[-1],
            "versions": len(states),
        },
    )

    print(f"\nOriginal: {len(states)} versions, {sum(len(v['code']) for v in evolution)} bytes")
    print(f"Compressed: {len(genome.to_string())} bytes")
    print(f"Ratio: {sum(len(v['code']) for v in evolution) / len(genome.to_string()):.0f}x")
    print(f"\nGenome: {genome.to_string()}")

    # Recommendations
    print()
    print("RECOMMENDATIONS:")
    print("-" * 70)

    current = states[-1]
    print(
        f"\nCurrent state: L={current[0]:.3f}, J={current[1]:.3f}, P={current[2]:.3f}, W={current[3]:.3f}"
    )
    print(f"Target (NE):   L={NE[0]:.3f}, J={NE[1]:.3f}, P={NE[2]:.3f}, W={NE[3]:.3f}")

    print("\nNext improvements:")
    if abs(current[0] - NE[0]) > 0.1:
        if current[0] < NE[0]:
            print(
                f"  1. Increase Safety (L): {current[0]:.3f} → {NE[0]:.3f} (+{NE[0]-current[0]:.3f})"
            )
            print("     - Add more error handling")
            print("     - Add input validation")
        else:
            print(f"  1. Reduce excessive safety checks (over-engineering)")

    if abs(current[1] - NE[1]) > 0.1:
        if current[1] < NE[1]:
            print(
                f"  2. Increase Structure (J): {current[1]:.3f} → {NE[1]:.3f} (+{NE[1]-current[1]:.3f})"
            )
            print("     - Add more documentation")
            print("     - Improve type annotations")

    if abs(current[2] - NE[2]) > 0.1:
        if current[2] < NE[2]:
            print(
                f"  3. Optimize Performance (P): {current[2]:.3f} → {NE[2]:.3f} (+{NE[2]-current[2]:.3f})"
            )
            print("     - Use better algorithms")
            print("     - Add caching")

    if abs(current[3] - NE[3]) > 0.1:
        if current[3] < NE[3]:
            print(
                f"  4. Improve Design (W): {current[3]:.3f} → {NE[3]:.3f} (+{NE[3]-current[3]:.3f})"
            )
            print("     - Use design patterns")
            print("     - Better abstraction")

    print()
    print("=" * 70)
    print("KEY INSIGHTS:")
    print("-" * 70)
    print("1. Track LJPW scores over time to monitor code health trends")
    print("2. v3.0 dynamic model uses RK4 integration for accurate predictions")
    print("3. Saturation effects: diminishing returns at high Love (K_JL=0.59)")
    print("4. Threshold effects: Power > 0.71 erodes Justice unless Wisdom is high")
    print("5. Compress entire evolution history into tiny genome")
    print("6. Use trajectory analysis to guide refactoring priorities")
    print()
    print("See also: ljpw_dynamic_v3.py and docs/THEORY.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
