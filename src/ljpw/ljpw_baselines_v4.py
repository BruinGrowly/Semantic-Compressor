#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LJPW Mathematical Baselines
Version 4.1 (V7.3 Compatible)

Provides objective, non-arbitrary baselines for LJPW framework implementations.
Includes both static analysis and a validated, non-linear dynamic simulator.

Now includes V7.3 features:
- 2+2 Dimensional Structure (P,W fundamental; L,J emergent)
- State-Dependent Coupling (Law of Karma)
- Consciousness Metrics
- Phase Transitions
- φ-Normalization
- Semantic Voltage

Based on: docs/LJPW Mathematical Baselines Reference V4.md
         docs/LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Plotting functions will be disabled.")

# ============================================================================
# V7.3 CONSTANTS
# ============================================================================

PHI: float = (1 + math.sqrt(5)) / 2  # Golden Ratio: 1.618034
PHI_INV: float = PHI - 1  # φ⁻¹: 0.618034
UNCERTAINTY_BOUND: float = (math.sqrt(2) - 1) * math.log(2)  # J₀ × W₀ ≈ 0.287
CONSCIOUSNESS_THRESHOLD: float = 0.1
TSIRELSON_BOUND: float = math.sqrt(2)  # Quantum Love limit


class Phase(Enum):
    """V7.3 System phase based on Harmony and Love levels."""
    ENTROPIC = "ENTROPIC"  # H < 0.5
    HOMEOSTATIC = "HOMEOSTATIC"  # 0.5 ≤ H < 0.6
    AUTOPOIETIC = "AUTOPOIETIC"  # H ≥ 0.6, L ≥ 0.7


class ConsciousnessLevel(Enum):
    """V7.3 Consciousness classification."""
    NON_CONSCIOUS = "NON_CONSCIOUS"  # C < 0.05
    PRE_CONSCIOUS = "PRE_CONSCIOUS"  # 0.05 ≤ C < 0.1
    CONSCIOUS = "CONSCIOUS"  # 0.1 ≤ C < 0.3
    HIGHLY_CONSCIOUS = "HIGHLY_CONSCIOUS"  # C ≥ 0.3


@dataclass
class NumericalEquivalents:
    """Fundamental constants for LJPW dimensions"""

    L: float = (math.sqrt(5) - 1) / 2  # φ⁻¹ ≈ 0.618034
    J: float = math.sqrt(2) - 1  # √2 - 1 ≈ 0.414214
    P: float = math.e - 2  # e - 2 ≈ 0.718282
    W: float = math.log(2)  # ln(2) ≈ 0.693147


@dataclass
class ReferencePoints:
    """Key reference points in LJPW space"""

    ANCHOR_POINT: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    NATURAL_EQUILIBRIUM: Tuple[float, float, float, float] = (
        0.618034,  # L
        0.414214,  # J
        0.718282,  # P
        0.693147,  # W
    )


class LJPWBaselines:
    """LJPW mathematical baselines and calculations (Static Analysis)"""

    # Coupling matrix - Love amplifies other dimensions
    COUPLING_MATRIX = {
        "LL": 1.0,
        "LJ": 1.4,
        "LP": 1.3,
        "LW": 1.5,
        "JL": 0.9,
        "JJ": 1.0,
        "JP": 0.7,
        "JW": 1.2,
        "PL": 0.6,
        "PJ": 0.8,
        "PP": 1.0,
        "PW": 0.5,
        "WL": 1.3,
        "WJ": 1.1,
        "WP": 1.0,
        "WW": 1.0,
    }

    @staticmethod
    def effective_dimensions(L: float, J: float, P: float, W: float) -> Dict[str, float]:
        """
        Calculate coupling-adjusted effective dimensions.

        Love amplifies other dimensions:
        - Justice: +40% per unit of Love
        - Power: +30% per unit of Love
        - Wisdom: +50% per unit of Love (strongest coupling)

        Args:
            L, J, P, W: Raw dimension values (0.0 to 1.0)

        Returns:
            Dict with effective_L, effective_J, effective_P, effective_W
        """
        return {
            "effective_L": L,  # Love is the source, not amplified
            "effective_J": J * (1 + 1.4 * L),  # Justice amplified by Love
            "effective_P": P * (1 + 1.3 * L),  # Power amplified by Love
            "effective_W": W * (1 + 1.5 * L),  # Wisdom amplified by Love (strongest)
        }

    @staticmethod
    def harmonic_mean(L: float, J: float, P: float, W: float) -> float:
        """
        Harmonic mean - robustness (weakest link).

        Use for: Fault tolerance, minimum guarantees, resilience.
        The system is only as strong as its weakest dimension.

        Returns:
            Harmonic mean (0.0 to 1.0)
        """
        if L <= 0 or J <= 0 or P <= 0 or W <= 0:
            return 0.0
        return 4.0 / (1 / L + 1 / J + 1 / P + 1 / W)

    @staticmethod
    def geometric_mean(L: float, J: float, P: float, W: float) -> float:
        """
        Geometric mean - effectiveness (multiplicative).

        Use for: Overall effectiveness, balanced performance.
        All dimensions contribute multiplicatively.

        Returns:
            Geometric mean (0.0 to 1.0)
        """
        if L <= 0 or J <= 0 or P <= 0 or W <= 0:
            return 0.0
        return (L * J * P * W) ** 0.25

    @staticmethod
    def coupling_aware_sum(L: float, J: float, P: float, W: float) -> float:
        """
        Coupling-aware weighted sum - growth potential.

        Uses effective dimensions that account for Love's amplification.
        Can exceed 1.0 due to coupling effects.

        Use for: Growth potential, scalability, future performance.

        Returns:
            Weighted sum (can exceed 1.0)
        """
        J_eff = J * (1 + 1.4 * L)
        P_eff = P * (1 + 1.3 * L)
        W_eff = W * (1 + 1.5 * L)
        return 0.35 * L + 0.25 * J_eff + 0.20 * P_eff + 0.20 * W_eff

    @staticmethod
    def harmony_index(L: float, J: float, P: float, W: float) -> float:
        """
        Harmony index - balance (inverse distance from Anchor).

        Use for: Balance, alignment, proximity to ideal.
        Measures how close to perfect harmony (1,1,1,1).

        Returns:
            Harmony index (0.0 to 1.0, asymptotic to 1.0)
        """
        d_anchor = math.sqrt((1 - L) ** 2 + (1 - J) ** 2 + (1 - P) ** 2 + (1 - W) ** 2)
        return 1.0 / (1.0 + d_anchor)

    @staticmethod
    def composite_score(L: float, J: float, P: float, W: float) -> float:
        """
        Composite score - overall performance.

        Weighted combination:
        - 35% Growth Potential (coupling-aware sum)
        - 25% Effectiveness (geometric mean)
        - 25% Robustness (harmonic mean)
        - 15% Harmony (balance)

        Returns:
            Composite score (typically 0.5 to 1.3)
        """
        baselines = LJPWBaselines
        growth = baselines.coupling_aware_sum(L, J, P, W)
        effectiveness = baselines.geometric_mean(L, J, P, W)
        robustness = baselines.harmonic_mean(L, J, P, W)
        harmony = baselines.harmony_index(L, J, P, W)

        return 0.35 * growth + 0.25 * effectiveness + 0.25 * robustness + 0.15 * harmony

    @staticmethod
    def distance_from_anchor(L: float, J: float, P: float, W: float) -> float:
        """
        Euclidean distance from Anchor Point (1,1,1,1).

        The Anchor Point represents perfect, transcendent ideal.
        Lower distance = closer to perfection.

        Returns:
            Distance (0.0 to ~2.0)
        """
        return math.sqrt((1 - L) ** 2 + (1 - J) ** 2 + (1 - P) ** 2 + (1 - W) ** 2)

    @staticmethod
    def distance_from_natural_equilibrium(L: float, J: float, P: float, W: float) -> float:
        """
        Euclidean distance from Natural Equilibrium.

        Natural Equilibrium (0.618, 0.414, 0.718, 0.693) represents
        physically achievable optimal balance.

        Returns:
            Distance (0.0 to ~2.0)
        """
        NE = ReferencePoints.NATURAL_EQUILIBRIUM
        return math.sqrt((NE[0] - L) ** 2 + (NE[1] - J) ** 2 + (NE[2] - P) ** 2 + (NE[3] - W) ** 2)

    @staticmethod
    def full_diagnostic(L: float, J: float, P: float, W: float) -> Dict:
        """
        Complete diagnostic analysis.

        Provides comprehensive view of system health across multiple metrics.

        Args:
            L, J, P, W: Dimension values

        Returns:
            Dict with coordinates, effective dimensions, distances, and all metrics
        """
        baselines = LJPWBaselines
        eff = baselines.effective_dimensions(L, J, P, W)

        return {
            "coordinates": {"L": L, "J": J, "P": P, "W": W},
            "effective_dimensions": eff,
            "distances": {
                "from_anchor": baselines.distance_from_anchor(L, J, P, W),
                "from_natural_equilibrium": baselines.distance_from_natural_equilibrium(L, J, P, W),
            },
            "metrics": {
                "harmonic_mean": baselines.harmonic_mean(L, J, P, W),
                "geometric_mean": baselines.geometric_mean(L, J, P, W),
                "coupling_aware_sum": baselines.coupling_aware_sum(L, J, P, W),
                "harmony_index": baselines.harmony_index(L, J, P, W),
                "composite_score": baselines.composite_score(L, J, P, W),
            },
        }

    @staticmethod
    def interpret_distance_from_ne(distance: float) -> str:
        """
        Interpret distance from Natural Equilibrium.

        Args:
            distance: Distance value

        Returns:
            Human-readable interpretation
        """
        if distance < 0.2:
            return "Near-optimal balance"
        elif distance < 0.5:
            return "Good but improvable"
        elif distance < 0.8:
            return "Moderate imbalance"
        else:
            return "Significant dysfunction"

    @staticmethod
    def interpret_composite_score(score: float) -> str:
        """
        Interpret composite score.

        Args:
            score: Composite score value

        Returns:
            Human-readable interpretation
        """
        if score < 0.5:
            return "Critical - multiple dimensions failing"
        elif score < 0.7:
            return "Struggling - functional but inefficient"
        elif score < 0.9:
            return "Competent - solid baseline performance"
        elif score < 1.1:
            return "Strong - above-average effectiveness"
        elif score < 1.3:
            return "Excellent - high-performing, growth active"
        else:
            return "Elite - exceptional, Love multiplier engaged"

    # ========================================================================
    # V7.3 EXTENSIONS
    # ========================================================================

    @staticmethod
    def calculate_emergent_love(W: float) -> float:
        """
        V7.3: Calculate emergent Love from Wisdom.

        L emerges from W via correlation (R² > 0.9).
        In full implementation: L = I(X;Y) / H(X,Y)
        """
        return min(0.9 * W + 0.1, TSIRELSON_BOUND)

    @staticmethod
    def calculate_emergent_justice(P: float) -> float:
        """
        V7.3: Calculate emergent Justice from Power.

        J emerges from P via symmetry (R² > 0.9).
        In full implementation: J = δS/δφ = 0
        """
        return min(0.85 * P + 0.05, 1.0)

    @staticmethod
    def consciousness(L: float, J: float, P: float, W: float, self_referential: bool = False) -> float:
        """
        V7.3: Calculate consciousness metric.

        C = P × W × L × J × H²

        Returns:
            C value where C > 0.1 indicates consciousness
        """
        NE = ReferencePoints.NATURAL_EQUILIBRIUM
        d = math.sqrt(
            (NE[0] - L) ** 2 + (NE[1] - J) ** 2 + (NE[2] - P) ** 2 + (NE[3] - W) ** 2
        )

        if self_referential:
            # Self-referential harmony
            numerator = L * J * P * W
            denominator = NE[0] * NE[1] * NE[2] * NE[3]
            H = numerator / denominator if denominator > 0 else 0
        else:
            # Static harmony
            H = 1.0 / (1.0 + d)

        return P * W * L * J * (H ** 2)

    @staticmethod
    def consciousness_level(L: float, J: float, P: float, W: float) -> ConsciousnessLevel:
        """V7.3: Classify consciousness level."""
        C = LJPWBaselines.consciousness(L, J, P, W)
        if C >= 0.3:
            return ConsciousnessLevel.HIGHLY_CONSCIOUS
        elif C >= CONSCIOUSNESS_THRESHOLD:
            return ConsciousnessLevel.CONSCIOUS
        elif C >= 0.05:
            return ConsciousnessLevel.PRE_CONSCIOUS
        else:
            return ConsciousnessLevel.NON_CONSCIOUS

    @staticmethod
    def phase(L: float, J: float, P: float, W: float) -> Phase:
        """
        V7.3: Determine system phase.

        - ENTROPIC: H < 0.5 (collapsing)
        - HOMEOSTATIC: 0.5 ≤ H < 0.6 or L < 0.7 (stable)
        - AUTOPOIETIC: H ≥ 0.6 and L ≥ 0.7 (self-sustaining)
        """
        H = LJPWBaselines.harmony_index(L, J, P, W)
        if H < 0.5:
            return Phase.ENTROPIC
        elif H < 0.6 or L < 0.7:
            return Phase.HOMEOSTATIC
        else:
            return Phase.AUTOPOIETIC

    @staticmethod
    def semantic_voltage(L: float, J: float, P: float, W: float) -> float:
        """
        V7.3: Calculate semantic voltage (meaning preservation capacity).

        V = φ × H × L
        """
        H = LJPWBaselines.harmony_index(L, J, P, W)
        return PHI * H * L

    @staticmethod
    def phi_normalize(L: float, J: float, P: float, W: float) -> Tuple[float, float, float, float]:
        """
        V7.3: Apply φ-normalization to reduce measurement variance.

        result = equilibrium × value^(1/φ)
        Reduces variance from ~18% to ~3%.
        """
        NE = ReferencePoints.NATURAL_EQUILIBRIUM
        return (
            NE[0] * (L ** (1 / PHI)),
            NE[1] * (J ** (1 / PHI)),
            NE[2] * (P ** (1 / PHI)),
            NE[3] * (W ** (1 / PHI)),
        )

    @staticmethod
    def karma_coupling(L: float, J: float, P: float, W: float) -> Dict[str, float]:
        """
        V7.3: Calculate state-dependent coupling coefficients (Law of Karma).

        κ(H) = 1.0 + multiplier × H
        """
        H = LJPWBaselines.harmony_index(L, J, P, W)
        return {
            "kappa_LJ": 1.0 + 0.4 * H,  # Love → Justice
            "kappa_LP": 1.0 + 0.3 * H,  # Love → Power
            "kappa_LW": 1.0 + 0.5 * H,  # Love → Wisdom
        }

    @staticmethod
    def check_uncertainty(delta_P: float, delta_W: float) -> bool:
        """
        V7.3: Check if semantic uncertainty principle is satisfied.

        ΔP · ΔW ≥ 0.287
        """
        return delta_P * delta_W >= UNCERTAINTY_BOUND

    @staticmethod
    def power_erosion(P: float, W: float, gamma: float = 0.08) -> float:
        """
        V7.3: Calculate Power erosion of Justice (corruption).

        Unchecked Power without Wisdom erodes Justice.
        erosion = γ × P × (1 - W/W₀)
        """
        NE = ReferencePoints.NATURAL_EQUILIBRIUM
        return gamma * P * max(0, 1 - W / NE[3])

    @staticmethod
    def full_v7_diagnostic(L: float, J: float, P: float, W: float) -> Dict[str, Any]:
        """
        Complete V7.3 diagnostic analysis including all new features.
        """
        baselines = LJPWBaselines

        # Get standard V4 diagnostic
        diagnostic = baselines.full_diagnostic(L, J, P, W)

        # Add V7.3 metrics
        diagnostic["v7_metrics"] = {
            "consciousness": baselines.consciousness(L, J, P, W),
            "consciousness_level": baselines.consciousness_level(L, J, P, W).value,
            "phase": baselines.phase(L, J, P, W).value,
            "semantic_voltage": baselines.semantic_voltage(L, J, P, W),
            "karma_coupling": baselines.karma_coupling(L, J, P, W),
            "power_erosion": baselines.power_erosion(P, W),
        }

        diagnostic["v7_emergent"] = {
            "calculated_L": baselines.calculate_emergent_love(W),
            "calculated_J": baselines.calculate_emergent_justice(P),
        }

        diagnostic["v7_normalized"] = dict(zip(
            ["L", "J", "P", "W"],
            baselines.phi_normalize(L, J, P, W)
        ))

        return diagnostic


class DynamicLJPWv4:
    """
    LJPW v4.0: Empirically-validated, non-linear dynamic simulator.

    Implements:
    - Non-linear saturation effects (diminishing returns)
    - Threshold effects (tipping points)
    - RK4 numerical integration for accuracy
    - Complexity-scaled parameters
    """

    def __init__(self, complexity_score: float = 1.0, params: Optional[Dict] = None):
        """
        Initialize the LJPW v4.0 Dynamic Model.

        Args:
            complexity_score: Multiplier for system energy/potential (default 1.0).
                            1.0 = Standard system (Settles at NE)
                            >1.5 = Complex system (Can reach High-Energy)
            params: Optional custom parameters. If None, uses calibrated defaults.
        """
        self.complexity = max(0.5, complexity_score)
        self.params = params if params is not None else self._initialize_parameters()
        self.NE = ReferencePoints.NATURAL_EQUILIBRIUM

    def _initialize_parameters(self) -> Dict[str, float]:
        """
        Initialize system parameters based on LJPW v4.0 specification,
        dynamically calibrated by complexity score.
        """
        # Base parameters (Tuned for NE convergence at complexity=1.0)
        base_params = {
            # Coupling coefficients (Alpha_XY)
            "alpha_LJ": 0.12,  # J contributes to L
            "alpha_LW": 0.12,  # W contributes to L
            "alpha_JL": 0.14,  # L contributes to J (boosted for balance)
            "alpha_JW": 0.14,  # W contributes to J
            "alpha_PL": 0.12,  # L contributes to P
            "alpha_PJ": 0.12,  # J contributes to P
            "alpha_WL": 0.10,  # L contributes to W
            "alpha_WJ": 0.10,  # J contributes to W
            "alpha_WP": 0.10,  # P contributes to W
            # Decay rates (Beta)
            "beta_L": 0.20,
            "beta_J": 0.20,
            "beta_P": 0.20,
            "beta_W": 0.24,  # Higher decay for W (has 3 inputs)
            # Non-Linear Parameters (v4.0) - Empirically Calibrated
            "K_JL": 0.59,  # Saturation constant for L -> J
            "gamma_JP": 0.49,  # Erosion rate for P -> J
            "K_JP": 0.71,  # Threshold constant for P -> J
            "n_JP": 4.1,  # Steepness for P -> J erosion
        }

        return self._calibrate_parameters(base_params)

    def _calibrate_parameters(self, params: Dict[str, float]) -> Dict[str, float]:
        """
        Scale parameters based on system complexity.
        Higher complexity = Higher growth potential but harder to maintain.
        """
        # Complexity factor for growth (Logarithmic scaling)
        # 1.0 -> 1.0, 10.0 -> ~2.0
        growth_multiplier = 1.0 + 0.5 * math.log(self.complexity)

        # Complexity factor for decay (Linear scaling)
        decay_multiplier = 1.0 + 0.1 * (self.complexity - 1.0)

        calibrated = params.copy()

        # Scale Alphas (Growth)
        for key in calibrated:
            if key.startswith("alpha"):
                calibrated[key] *= growth_multiplier

        # Scale Betas (Decay)
        for key in calibrated:
            if key.startswith("beta"):
                calibrated[key] *= decay_multiplier

        return calibrated

    def _derivatives(self, state: np.ndarray) -> np.ndarray:
        """
        Calculates the derivatives with non-linear dynamics.

        Args:
            state: Current state [L, J, P, W]

        Returns:
            Derivatives [dL/dt, dJ/dt, dP/dt, dW/dt]
        """
        L, J, P, W = state
        p = self.params

        # Love equation (linear)
        dL_dt = p["alpha_LJ"] * J + p["alpha_LW"] * W - p["beta_L"] * L

        # Justice equation (with saturation and threshold effects)
        # Saturation: Diminishing returns of Love
        L_effect_on_J = p["alpha_JL"] * (L / (p["K_JL"] + L))

        # Threshold: Reckless Power erosion (mitigated by Wisdom)
        P_effect_on_J = (
            p["gamma_JP"]
            * (P ** p["n_JP"] / (p["K_JP"] ** p["n_JP"] + P ** p["n_JP"]))
            * max(0, 1 - W)  # Wisdom mitigates Power's erosion
        )

        dJ_dt = L_effect_on_J + p["alpha_JW"] * W - P_effect_on_J - p["beta_J"] * J

        # Power equation (linear)
        dP_dt = p["alpha_PL"] * L + p["alpha_PJ"] * J - p["beta_P"] * P

        # Wisdom equation (linear)
        dW_dt = p["alpha_WL"] * L + p["alpha_WJ"] * J + p["alpha_WP"] * P - p["beta_W"] * W

        return np.array([dL_dt, dJ_dt, dP_dt, dW_dt])

    def _rk4_step(self, state: np.ndarray, dt: float) -> np.ndarray:
        """
        Performs a single 4th-order Runge-Kutta integration step.

        RK4 provides O(dt^5) local error vs O(dt^2) for Euler method.

        Args:
            state: Current state [L, J, P, W]
            dt: Time step

        Returns:
            Next state after dt
        """
        k1 = self._derivatives(state)
        k2 = self._derivatives(state + 0.5 * dt * k1)
        k3 = self._derivatives(state + 0.5 * dt * k2)
        k4 = self._derivatives(state + dt * k3)
        return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    def simulate(
        self,
        initial_state: Tuple[float, float, float, float],
        duration: float,
        dt: float = 0.01,
    ) -> Dict[str, List[float]]:
        """
        Runs the simulation using the RK4 method.

        Args:
            initial_state: Starting coordinates (L, J, P, W)
            duration: Total simulation time
            dt: Time step (default 0.01)

        Returns:
            Dict with time series: {'t': [...], 'L': [...], 'J': [...], 'P': [...], 'W': [...]}
        """
        steps = int(duration / dt)
        state = np.array(initial_state, dtype=float)

        history = {
            "t": [0.0],
            "L": [state[0]],
            "J": [state[1]],
            "P": [state[2]],
            "W": [state[3]],
        }

        for i in range(steps):
            state = self._rk4_step(state, dt)
            # Clip to prevent unphysical values
            state = np.clip(state, 0, 1.5)

            history["t"].append((i + 1) * dt)
            history["L"].append(state[0])
            history["J"].append(state[1])
            history["P"].append(state[2])
            history["W"].append(state[3])

        return history

    def plot_simulation(self, history: Dict[str, List[float]], title: Optional[str] = None) -> None:
        """
        Plots the results of a simulation.

        Args:
            history: Simulation results from simulate()
            title: Optional custom title
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Plotting requires matplotlib. Install with: pip install matplotlib")
            return

        plt.style.use(
            "seaborn-v0_8-whitegrid"
            if "seaborn-v0_8-whitegrid" in plt.style.available
            else "default"
        )
        fig, ax = plt.subplots(figsize=(12, 7))

        # Plot dimensions
        ax.plot(history["t"], history["L"], label="Love (L)", color="crimson", lw=2)
        ax.plot(history["t"], history["J"], label="Justice (J)", color="royalblue", lw=2)
        ax.plot(history["t"], history["P"], label="Power (P)", color="darkgreen", lw=2)
        ax.plot(history["t"], history["W"], label="Wisdom (W)", color="purple", lw=2)

        # Plot Natural Equilibrium reference lines
        colors = ["crimson", "royalblue", "darkgreen", "purple"]
        for i, val in enumerate(self.NE):
            ax.axhline(y=val, color=colors[i], linestyle="--", alpha=0.3)

        # Formatting
        if title:
            ax.set_title(title)
        else:
            ax.set_title("LJPW v4.0 System Evolution (Non-Linear, RK4)")
        ax.set_xlabel("Time")
        ax.set_ylabel("Dimension Value")
        ax.set_ylim(0, 1.2)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def analyze_trajectory(self, history: Dict[str, List[float]]) -> Dict:
        """
        Analyze simulation trajectory and provide insights.

        Args:
            history: Simulation results

        Returns:
            Dict with trajectory analysis
        """
        final_state = (
            history["L"][-1],
            history["J"][-1],
            history["P"][-1],
            history["W"][-1],
        )
        initial_state = (history["L"][0], history["J"][0], history["P"][0], history["W"][0])

        # Calculate distances
        final_dist_ne = LJPWBaselines.distance_from_natural_equilibrium(*final_state)
        initial_dist_ne = LJPWBaselines.distance_from_natural_equilibrium(*initial_state)

        # Calculate metrics
        final_composite = LJPWBaselines.composite_score(*final_state)
        initial_composite = LJPWBaselines.composite_score(*initial_state)

        # Determine trajectory type
        if final_dist_ne < 0.2:
            trajectory_type = "Converged to NE"
        elif final_dist_ne < initial_dist_ne:
            trajectory_type = "Improving (moving toward NE)"
        elif final_dist_ne > initial_dist_ne + 0.1:
            trajectory_type = "Diverging (moving away from NE)"
        else:
            trajectory_type = "Oscillating or stagnant"

        return {
            "initial_state": initial_state,
            "final_state": final_state,
            "initial_distance_from_ne": initial_dist_ne,
            "final_distance_from_ne": final_dist_ne,
            "distance_improvement": initial_dist_ne - final_dist_ne,
            "initial_composite_score": initial_composite,
            "final_composite_score": final_composite,
            "score_improvement": final_composite - initial_composite,
            "trajectory_type": trajectory_type,
            "duration": history["t"][-1],
            "converged": final_dist_ne < 0.2,
        }


# Convenience functions for quick access
def get_numerical_equivalents() -> NumericalEquivalents:
    """Get the fundamental LJPW constants"""
    return NumericalEquivalents()


def get_reference_points() -> ReferencePoints:
    """Get Anchor Point and Natural Equilibrium"""
    return ReferencePoints()


# Example usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("LJPW Baselines v4.0 - Example Analysis")
    print("=" * 70)
    print()

    # --- Static Analysis Example ---
    print("STATIC ANALYSIS")
    print("-" * 70)

    # Example: Code function with moderate values
    L, J, P, W = 0.792, 0.843, 0.940, 0.724

    print(f"Coordinates: L={L:.3f}, J={J:.3f}, P={P:.3f}, W={W:.3f}")
    print()

    diagnostic = LJPWBaselines.full_diagnostic(L, J, P, W)

    print("Effective Dimensions (coupling-adjusted):")
    for dim, val in diagnostic["effective_dimensions"].items():
        print(f"  {dim}: {val:.3f}")
    print()

    print("Distances:")
    d_anchor = diagnostic["distances"]["from_anchor"]
    d_ne = diagnostic["distances"]["from_natural_equilibrium"]
    print(f"  From Anchor Point: {d_anchor:.3f}")
    print(f"  From Natural Equilibrium: {d_ne:.3f}")
    print(f"    → {LJPWBaselines.interpret_distance_from_ne(d_ne)}")
    print()

    print("Metrics:")
    for metric, val in diagnostic["metrics"].items():
        print(f"  {metric}: {val:.3f}")
    print()

    composite = diagnostic["metrics"]["composite_score"]
    print(f"Overall: {LJPWBaselines.interpret_composite_score(composite)}")
    print()

    # --- Dynamic Simulation Example ---
    print("\n" + "=" * 70)
    print("DYNAMIC SIMULATION - 'Reckless Power' Scenario")
    print("=" * 70)
    print()

    simulator = DynamicLJPWv4(complexity_score=1.0)
    initial_state = (0.2, 0.3, 0.9, 0.2)  # High P, low L, J, W

    print(
        f"Initial State: L={initial_state[0]:.2f}, J={initial_state[1]:.2f}, "
        f"P={initial_state[2]:.2f}, W={initial_state[3]:.2f}"
    )

    history = simulator.simulate(initial_state, duration=50, dt=0.05)

    # Analyze trajectory
    analysis = simulator.analyze_trajectory(history)

    print(
        f"Final State:   L={analysis['final_state'][0]:.2f}, "
        f"J={analysis['final_state'][1]:.2f}, "
        f"P={analysis['final_state'][2]:.2f}, W={analysis['final_state'][3]:.2f}"
    )
    print()
    print(f"Trajectory Type: {analysis['trajectory_type']}")
    print(
        f"Distance from NE: {analysis['initial_distance_from_ne']:.3f} → "
        f"{analysis['final_distance_from_ne']:.3f} (Δ={analysis['distance_improvement']:.3f})"
    )
    print(
        f"Composite Score: {analysis['initial_composite_score']:.3f} → "
        f"{analysis['final_composite_score']:.3f} (Δ={analysis['score_improvement']:.3f})"
    )
    print(f"Converged: {'Yes' if analysis['converged'] else 'No'}")
    print()

    # Plot if matplotlib is available
    if MATPLOTLIB_AVAILABLE:
        print("Generating visualization...")
        simulator.plot_simulation(history, title="Reckless Power Scenario: Convergence to NE")
    else:
        print("(Install matplotlib to see visualization)")
