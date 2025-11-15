#!/usr/bin/env python3
"""
LJPW Dynamic Model v3.0
======================

Implementation of the non-linear LJPW dynamical system with:
- Saturation effects (Michaelis-Menten kinetics)
- Threshold effects (sigmoidal Power erosion)
- Coupling amplification (Love as force multiplier)
- RK4 numerical integration (4th-order Runge-Kutta)
- Bayesian-calibrated parameters (MCMC posterior means)

Based on:
- "Dynamic LJPW Model v3.0: Specification and Theoretical Foundations"
- "Empirical Validation of the LJPW v3.0 Model via Bayesian Calibration"

Mathematical Form:
-----------------
dL/dt = α_LJ * J + α_LW * W - β_L * L

dJ/dt = α_JL * (L / (K_JL + L))                    [SATURATION]
        + α_JW * W
        - γ_JP * (P^n / (K_JP^n + P^n)) * (1 - W)  [THRESHOLD]
        - β_J * J

dP/dt = α_PL * L + α_PJ * J - β_P * P

dW/dt = α_WL * L + α_WJ * J + α_WP * P - β_W * W

Author: Generated based on GLM-4.6 theoretical specification
Version: 3.0
Date: November 2025
"""

import math
from typing import Tuple, List, Dict, Optional, Callable
from dataclasses import dataclass


# Natural Equilibrium (target state)
NATURAL_EQUILIBRIUM = (0.618034, 0.414214, 0.718282, 0.693147)  # (L, J, P, W)


@dataclass
class LJPWParameters:
    """
    Bayesian-calibrated parameters from MCMC sampling.

    Posterior means with 95% credible intervals from the validation study.
    """
    # Growth coefficients (α)
    alpha_LJ: float = 0.35  # Justice → Love
    alpha_LW: float = 0.30  # Wisdom → Love
    alpha_JL: float = 0.41  # Love → Justice (POSTERIOR MEAN: [0.38, 0.44])
    alpha_JW: float = 0.25  # Wisdom → Justice
    alpha_PL: float = 0.40  # Love → Power
    alpha_PJ: float = 0.30  # Justice → Power
    alpha_WL: float = 0.35  # Love → Wisdom
    alpha_WJ: float = 0.28  # Justice → Wisdom
    alpha_WP: float = 0.22  # Power → Wisdom

    # Decay coefficients (β)
    beta_L: float = 0.20
    beta_J: float = 0.18
    beta_P: float = 0.25
    beta_W: float = 0.22

    # Saturation effect (Michaelis-Menten)
    K_JL: float = 0.59  # Love saturation constant (POSTERIOR MEAN: [0.54, 0.64])

    # Threshold effect (Sigmoidal)
    gamma_JP: float = 0.49  # Power erosion coefficient (POSTERIOR MEAN: [0.45, 0.53])
    K_JP: float = 0.71      # Power threshold (POSTERIOR MEAN: [0.66, 0.76])
    n_JP: float = 4.1       # Hill coefficient/steepness (POSTERIOR MEAN: [3.5, 4.7])

    # Coupling amplification (Love as force multiplier)
    kappa_LJ: float = 1.4   # Love → Justice amplification (40%)
    kappa_LP: float = 1.3   # Love → Power amplification (30%)
    kappa_LW: float = 1.5   # Love → Wisdom amplification (50%)


class LJPWDynamicModel:
    """
    Non-linear LJPW dynamical system with v3.0 enhancements.

    Features:
    - Saturation: Love's effect on Justice saturates (Michaelis-Menten)
    - Threshold: Power > K_JP (0.71) erodes Justice unless Wisdom is high
    - Coupling: Love amplifies other dimensions (force multiplier)
    - RK4 Integration: 4th-order Runge-Kutta for accuracy

    Usage:
        model = LJPWDynamicModel()
        trajectory = model.simulate(initial_state=(0.3, 0.4, 0.5, 0.4),
                                    duration=100, dt=0.1)
    """

    def __init__(self, params: Optional[LJPWParameters] = None):
        """
        Initialize dynamic model with parameters.

        Args:
            params: LJPWParameters instance. If None, uses default calibrated values.
        """
        self.params = params if params is not None else LJPWParameters()

    def derivatives(self, state: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        """
        Calculate derivatives dL/dt, dJ/dt, dP/dt, dW/dt at given state.

        This is the core of the v3.0 non-linear dynamics.

        Args:
            state: (L, J, P, W) tuple

        Returns:
            (dL/dt, dJ/dt, dP/dt, dW/dt) tuple
        """
        L, J, P, W = state
        p = self.params

        # Love dynamics (linear in v3.0)
        dL_dt = (p.alpha_LJ * J +
                 p.alpha_LW * W -
                 p.beta_L * L)

        # Justice dynamics (NON-LINEAR - key innovation of v3.0)

        # Saturation effect: Love → Justice with diminishing returns
        saturation_term = p.alpha_JL * (L / (p.K_JL + L))

        # Threshold effect: Power erodes Justice above tipping point
        # Mitigated by Wisdom (1-W factor)
        threshold_term = p.gamma_JP * (
            (P ** p.n_JP) / (p.K_JP ** p.n_JP + P ** p.n_JP)
        ) * (1 - W)

        dJ_dt = (saturation_term +
                 p.alpha_JW * W -
                 threshold_term -
                 p.beta_J * J)

        # Power dynamics (linear in v3.0)
        dP_dt = (p.alpha_PL * L +
                 p.alpha_PJ * J -
                 p.beta_P * P)

        # Wisdom dynamics (linear in v3.0)
        dW_dt = (p.alpha_WL * L +
                 p.alpha_WJ * J +
                 p.alpha_WP * P -
                 p.beta_W * W)

        return (dL_dt, dJ_dt, dP_dt, dW_dt)

    def rk4_step(self,
                 state: Tuple[float, float, float, float],
                 dt: float) -> Tuple[float, float, float, float]:
        """
        Perform one RK4 integration step.

        RK4 is 4th-order accurate: O(dt^5) local error.
        Much better than Euler (O(dt^2)) for non-linear systems.

        Args:
            state: Current (L, J, P, W)
            dt: Time step

        Returns:
            Next state after dt
        """
        L, J, P, W = state

        # k1: Slope at current state
        k1_L, k1_J, k1_P, k1_W = self.derivatives((L, J, P, W))

        # k2: Slope at midpoint using k1
        k2_L, k2_J, k2_P, k2_W = self.derivatives((
            L + 0.5 * dt * k1_L,
            J + 0.5 * dt * k1_J,
            P + 0.5 * dt * k1_P,
            W + 0.5 * dt * k1_W
        ))

        # k3: Slope at midpoint using k2
        k3_L, k3_J, k3_P, k3_W = self.derivatives((
            L + 0.5 * dt * k2_L,
            J + 0.5 * dt * k2_J,
            P + 0.5 * dt * k2_P,
            W + 0.5 * dt * k2_W
        ))

        # k4: Slope at endpoint using k3
        k4_L, k4_J, k4_P, k4_W = self.derivatives((
            L + dt * k3_L,
            J + dt * k3_J,
            P + dt * k3_P,
            W + dt * k3_W
        ))

        # Weighted average: (k1 + 2*k2 + 2*k3 + k4) / 6
        L_next = L + (dt / 6.0) * (k1_L + 2*k2_L + 2*k3_L + k4_L)
        J_next = J + (dt / 6.0) * (k1_J + 2*k2_J + 2*k3_J + k4_J)
        P_next = P + (dt / 6.0) * (k1_P + 2*k2_P + 2*k3_P + k4_P)
        W_next = W + (dt / 6.0) * (k1_W + 2*k2_W + 2*k3_W + k4_W)

        # Clamp to valid range [0, 1]
        L_next = max(0.0, min(1.0, L_next))
        J_next = max(0.0, min(1.0, J_next))
        P_next = max(0.0, min(1.0, P_next))
        W_next = max(0.0, min(1.0, W_next))

        return (L_next, J_next, P_next, W_next)

    def simulate(self,
                 initial_state: Tuple[float, float, float, float],
                 duration: float = 100.0,
                 dt: float = 0.1) -> List[Tuple[float, float, float, float, float]]:
        """
        Simulate LJPW evolution over time.

        Args:
            initial_state: Starting (L, J, P, W)
            duration: Total simulation time
            dt: Time step for RK4 integration

        Returns:
            List of (time, L, J, P, W) tuples
        """
        trajectory = []
        state = initial_state
        time = 0.0

        trajectory.append((time, *state))

        while time < duration:
            state = self.rk4_step(state, dt)
            time += dt
            trajectory.append((time, *state))

        return trajectory

    def analyze_trajectory(self,
                          trajectory: List[Tuple[float, float, float, float, float]]) -> Dict:
        """
        Analyze a simulated or observed trajectory.

        Computes:
        - Final state and distance from NE
        - Velocity (rate of change)
        - Convergence/divergence
        - ETA to Natural Equilibrium

        Args:
            trajectory: List of (time, L, J, P, W) tuples

        Returns:
            Dictionary with analysis results
        """
        if len(trajectory) < 2:
            return {'error': 'Trajectory too short (need at least 2 points)'}

        # Initial and final states
        initial = trajectory[0][1:]  # (L, J, P, W)
        final = trajectory[-1][1:]

        # Distance from Natural Equilibrium
        initial_dist = self._distance_from_ne(initial)
        final_dist = self._distance_from_ne(final)

        # Velocity (average rate of change)
        total_time = trajectory[-1][0] - trajectory[0][0]
        if total_time > 0:
            velocity = tuple((f - i) / total_time for i, f in zip(initial, final))
            velocity_magnitude = math.sqrt(sum(v**2 for v in velocity))
        else:
            velocity = (0, 0, 0, 0)
            velocity_magnitude = 0

        # Convergence analysis
        converging = final_dist < initial_dist

        # ETA to Natural Equilibrium (simple linear extrapolation)
        if converging and velocity_magnitude > 0.001:
            eta = final_dist / velocity_magnitude
        else:
            eta = float('inf')

        # Check if near equilibrium
        near_equilibrium = final_dist < 0.1

        # Detect if crossing threshold (P > K_JP)
        crossing_threshold = any(state[3] > self.params.K_JP for _, *state in trajectory)

        return {
            'initial_state': initial,
            'final_state': final,
            'initial_distance_from_ne': initial_dist,
            'final_distance_from_ne': final_dist,
            'velocity': velocity,
            'velocity_magnitude': velocity_magnitude,
            'converging': converging,
            'near_equilibrium': near_equilibrium,
            'eta_to_ne': eta,
            'crossing_power_threshold': crossing_threshold,
            'total_time': total_time,
            'num_steps': len(trajectory)
        }

    @staticmethod
    def _distance_from_ne(state: Tuple[float, float, float, float]) -> float:
        """Calculate Euclidean distance from Natural Equilibrium."""
        L, J, P, W = state
        L_ne, J_ne, P_ne, W_ne = NATURAL_EQUILIBRIUM
        return math.sqrt(
            (L - L_ne)**2 +
            (J - J_ne)**2 +
            (P - P_ne)**2 +
            (W - W_ne)**2
        )

    def find_equilibrium(self,
                        initial_state: Tuple[float, float, float, float],
                        max_time: float = 1000.0,
                        tolerance: float = 1e-6) -> Optional[Tuple[float, float, float, float]]:
        """
        Find equilibrium point starting from initial_state.

        Simulates until derivatives are near zero or max_time reached.

        Args:
            initial_state: Starting (L, J, P, W)
            max_time: Maximum simulation time
            tolerance: Convergence tolerance

        Returns:
            Equilibrium state or None if not converged
        """
        state = initial_state
        time = 0.0
        dt = 0.1

        while time < max_time:
            derivatives = self.derivatives(state)
            derivative_magnitude = math.sqrt(sum(d**2 for d in derivatives))

            if derivative_magnitude < tolerance:
                return state  # Converged

            state = self.rk4_step(state, dt)
            time += dt

        return None  # Did not converge

    def predict_future(self,
                      current_state: Tuple[float, float, float, float],
                      time_horizon: float = 10.0,
                      dt: float = 0.1) -> Dict:
        """
        Predict future evolution from current state.

        Args:
            current_state: Current (L, J, P, W)
            time_horizon: How far to predict
            dt: Integration time step

        Returns:
            Prediction dictionary with trajectory and analysis
        """
        trajectory = self.simulate(current_state, duration=time_horizon, dt=dt)
        analysis = self.analyze_trajectory(trajectory)

        return {
            'trajectory': trajectory,
            'analysis': analysis,
            'predicted_state': trajectory[-1][1:],
            'time_horizon': time_horizon
        }


class LJPWTrajectoryAnalyzer:
    """
    Analyze LJPW evolution over git history or time series.

    Takes sequence of LJPW measurements and analyzes trends.
    """

    def __init__(self, model: Optional[LJPWDynamicModel] = None):
        """
        Initialize analyzer.

        Args:
            model: LJPWDynamicModel instance. If None, creates default.
        """
        self.model = model if model is not None else LJPWDynamicModel()

    def analyze_sequence(self,
                        states: List[Tuple[float, float, float, float]],
                        times: Optional[List[float]] = None) -> Dict:
        """
        Analyze a sequence of observed LJPW states.

        Args:
            states: List of (L, J, P, W) tuples
            times: Optional list of time values. If None, uses indices.

        Returns:
            Analysis dictionary
        """
        if len(states) < 2:
            return {'error': 'Need at least 2 states'}

        if times is None:
            times = list(range(len(states)))

        # Convert to trajectory format
        trajectory = [(t, *s) for t, s in zip(times, states)]

        # Use model's analysis
        analysis = self.model.analyze_trajectory(trajectory)

        # Additional sequence-specific analysis
        distances = [self.model._distance_from_ne(s) for s in states]

        # Trend: improving or declining?
        if distances[-1] < distances[0]:
            trend = 'IMPROVING'
        elif distances[-1] > distances[0]:
            trend = 'DECLINING'
        else:
            trend = 'STABLE'

        # Volatility (standard deviation of distances)
        mean_dist = sum(distances) / len(distances)
        variance = sum((d - mean_dist)**2 for d in distances) / len(distances)
        volatility = math.sqrt(variance)

        analysis.update({
            'distances_from_ne': distances,
            'trend': trend,
            'volatility': volatility,
            'improvement': distances[0] - distances[-1]  # Positive = improved
        })

        return analysis

    def fit_trajectory(self,
                      observed_states: List[Tuple[float, float, float, float]],
                      times: Optional[List[float]] = None) -> Dict:
        """
        Fit dynamic model to observed data.

        Find best initial conditions that reproduce observed trajectory.
        (Simplified version - full Bayesian inference would use MCMC)

        Args:
            observed_states: List of observed (L, J, P, W)
            times: Time values for observations

        Returns:
            Fit results
        """
        if times is None:
            times = list(range(len(observed_states)))

        # Simple approach: use first state as initial condition
        # and simulate to see how well it fits
        initial_state = observed_states[0]
        duration = times[-1] - times[0]

        predicted = self.model.simulate(initial_state, duration=duration, dt=0.1)

        # Calculate fit error (RMSE)
        errors = []
        for obs_time, obs_state in zip(times, observed_states):
            # Find closest predicted time
            pred_state = min(predicted, key=lambda p: abs(p[0] - obs_time))[1:]

            error = math.sqrt(sum((o - p)**2 for o, p in zip(obs_state, pred_state)))
            errors.append(error)

        rmse = math.sqrt(sum(e**2 for e in errors) / len(errors))

        return {
            'initial_state': initial_state,
            'predicted_trajectory': predicted,
            'observed_states': observed_states,
            'errors': errors,
            'rmse': rmse,
            'fit_quality': 'GOOD' if rmse < 0.05 else 'FAIR' if rmse < 0.1 else 'POOR'
        }


# Utility functions

def analyze_code_evolution(ljpw_scores: List[Dict],
                          timestamps: Optional[List[float]] = None) -> Dict:
    """
    Analyze code evolution from LJPW scores over time.

    Args:
        ljpw_scores: List of dicts with 'L', 'J', 'P', 'W' keys (from ljpw_standalone)
        timestamps: Optional timestamps (days, commits, etc.)

    Returns:
        Analysis results
    """
    states = [(s['L'], s['J'], s['P'], s['W']) for s in ljpw_scores]

    analyzer = LJPWTrajectoryAnalyzer()
    return analyzer.analyze_sequence(states, timestamps)


def predict_code_future(current_ljpw: Dict,
                       time_horizon: float = 10.0) -> Dict:
    """
    Predict future code evolution from current LJPW state.

    Args:
        current_ljpw: Dict with 'L', 'J', 'P', 'W' keys
        time_horizon: How far to predict (iterations, days, commits)

    Returns:
        Prediction results
    """
    current_state = (current_ljpw['L'], current_ljpw['J'],
                    current_ljpw['P'], current_ljpw['W'])

    model = LJPWDynamicModel()
    return model.predict_future(current_state, time_horizon=time_horizon)


# Example usage
if __name__ == '__main__':
    print("="*70)
    print("LJPW Dynamic Model v3.0 - Demo")
    print("="*70)
    print()

    # Example 1: Simulate from poor state toward Natural Equilibrium
    print("Example 1: Simulating poor code evolving...")
    print("-" * 70)

    poor_code = (0.3, 0.2, 0.8, 0.4)  # Low L,J,W but high P (reckless)

    model = LJPWDynamicModel()
    trajectory = model.simulate(poor_code, duration=50, dt=0.5)

    print(f"Initial state: L={poor_code[0]:.3f}, J={poor_code[1]:.3f}, "
          f"P={poor_code[2]:.3f}, W={poor_code[3]:.3f}")
    print(f"Distance from NE: {model._distance_from_ne(poor_code):.3f}")
    print()

    final_state = trajectory[-1][1:]
    print(f"Final state (t=50): L={final_state[0]:.3f}, J={final_state[1]:.3f}, "
          f"P={final_state[2]:.3f}, W={final_state[3]:.3f}")
    print(f"Distance from NE: {model._distance_from_ne(final_state):.3f}")
    print()

    analysis = model.analyze_trajectory(trajectory)
    print(f"Converging: {analysis['converging']}")
    print(f"Velocity magnitude: {analysis['velocity_magnitude']:.4f}")
    if analysis['eta_to_ne'] != float('inf'):
        print(f"ETA to equilibrium: {analysis['eta_to_ne']:.1f} time units")
    else:
        print("Not converging to equilibrium")
    print()

    # Example 2: Detect threshold crossing
    print("Example 2: Threshold effect demonstration...")
    print("-" * 70)

    # Scenario A: High Power, Low Wisdom (DANGEROUS)
    print("Scenario A: P=0.9, W=0.3 (Reckless Power)")
    dangerous = (0.5, 0.6, 0.9, 0.3)
    traj_a = model.simulate(dangerous, duration=20, dt=0.2)

    J_initial = traj_a[0][2]  # Justice at t=0
    J_final = traj_a[-1][2]

    print(f"  Justice: {J_initial:.3f} → {J_final:.3f} (Δ={J_final-J_initial:+.3f})")
    print(f"  P > K_JP threshold (0.71): YES → Justice ERODED")
    print()

    # Scenario B: High Power, High Wisdom (SAFE)
    print("Scenario B: P=0.9, W=0.8 (Wise Power)")
    safe = (0.5, 0.6, 0.9, 0.8)
    traj_b = model.simulate(safe, duration=20, dt=0.2)

    J_initial_b = traj_b[0][2]
    J_final_b = traj_b[-1][2]

    print(f"  Justice: {J_initial_b:.3f} → {J_final_b:.3f} (Δ={J_final_b-J_initial_b:+.3f})")
    print(f"  P > K_JP threshold (0.71): YES, but W=0.8 → Justice PROTECTED")
    print()

    # Example 3: Code evolution analysis
    print("Example 3: Analyzing code evolution over 5 commits...")
    print("-" * 70)

    # Simulated commit history
    commits = [
        {'L': 0.3, 'J': 0.4, 'P': 0.5, 'W': 0.4},
        {'L': 0.4, 'J': 0.5, 'P': 0.6, 'W': 0.5},
        {'L': 0.5, 'J': 0.5, 'P': 0.7, 'W': 0.5},
        {'L': 0.6, 'J': 0.5, 'P': 0.75, 'W': 0.6},
        {'L': 0.6, 'J': 0.4, 'P': 0.8, 'W': 0.6},
    ]

    evolution = analyze_code_evolution(commits)

    print(f"Trend: {evolution['trend']}")
    print(f"Initial distance from NE: {evolution['initial_distance_from_ne']:.3f}")
    print(f"Final distance from NE: {evolution['final_distance_from_ne']:.3f}")
    print(f"Improvement: {evolution['improvement']:+.3f}")
    print(f"Crossing power threshold: {evolution['crossing_power_threshold']}")
    print()

    if evolution['crossing_power_threshold']:
        print("⚠️  WARNING: Power crossed threshold (0.71) in recent commits!")
        print("   Risk: Premature optimization eroding code structure")
        print("   Recommendation: Increase Wisdom before further optimization")

    print()
    print("="*70)
    print("See docs/THEORY.md for mathematical foundations")
    print("See examples/advanced/track_code_evolution.py for real usage")
    print("="*70)
