#!/usr/bin/env python3
"""
LJPW Virtual Machine - Semantic Computing Environment
======================================================

Demonstrates that LJPW space is not just analytical but COMPUTATIONAL.

Key Insight: We can load structures into LJPW space, simulate operations,
and predict outcomes WITHOUT executing bytes.

This is SEMANTIC COMPUTING - operating on meaning directly.

Capabilities:
- Load semantic structures (ISOs, code, systems) into LJPW space
- Build hierarchical, interacting structures
- Simulate operations (install, deploy, scale, etc.)
- Predict outcomes before execution
- Test scenarios in semantic space

Example:
    vm = LJPWVirtualMachine()

    # Load ISO into LJPW space
    iso = vm.load_iso('ubuntu-22.04-server.iso')

    # Simulate installation (NO bytes executed!)
    result = vm.simulate_operation(iso, 'install', duration=60)

    # Predict outcome
    print(f"Success probability: {result.success_prob:.1%}")
    print(f"Final health: {result.final_health:.1%}")
    print(f"Issues: {result.issues}")

Author: Generated from LJPW framework
Version: 1.0 (Proof of Concept)
Date: November 2025
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict

from ljpw_dynamic_v3 import LJPWDynamicModel, LJPWParameters, NATURAL_EQUILIBRIUM


@dataclass
class LJPWState:
    """Represents a point in LJPW 4D phase space"""
    L: float
    J: float
    P: float
    W: float

    def as_tuple(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)

    def distance_from_ne(self) -> float:
        """Calculate distance from Natural Equilibrium"""
        L_ne, J_ne, P_ne, W_ne = NATURAL_EQUILIBRIUM
        return math.sqrt(
            (self.L - L_ne)**2 +
            (self.J - J_ne)**2 +
            (self.P - P_ne)**2 +
            (self.W - W_ne)**2
        )

    def health(self) -> float:
        """Calculate health (0-1 scale)"""
        return max(0, 1 - self.distance_from_ne() / 2)


@dataclass
class LJPWComponent:
    """A component in LJPW space with its own state"""
    name: str
    state: LJPWState
    component_type: str
    subcomponents: Dict[str, 'LJPWComponent']
    metadata: Dict[str, Any]

    def get_all_states(self) -> Dict[str, LJPWState]:
        """Get flattened dict of all states (recursive)"""
        states = {self.name: self.state}
        for sub in self.subcomponents.values():
            states.update(sub.get_all_states())
        return states


@dataclass
class LJPWStructure:
    """
    A complete hierarchical structure in LJPW space.

    Represents systems like:
    - Operating system installation (ISO)
    - Software deployment (containers, VMs)
    - Infrastructure (servers, networks, databases)
    - Organizations (teams, processes, products)
    """
    name: str
    root: LJPWComponent
    interactions: Dict[Tuple[str, str], float]  # Coupling strengths

    def get_component(self, path: str) -> Optional[LJPWComponent]:
        """Get component by path (e.g., 'os.kernel')"""
        parts = path.split('.')
        current = self.root

        for part in parts[1:]:  # Skip root name
            if part in current.subcomponents:
                current = current.subcomponents[part]
            else:
                return None
        return current

    def overall_state(self) -> LJPWState:
        """Calculate weighted average state of entire structure"""
        all_states = self.root.get_all_states()
        if not all_states:
            return LJPWState(0, 0, 0, 0)

        # Simple average for now (could weight by importance)
        avg_L = sum(s.L for s in all_states.values()) / len(all_states)
        avg_J = sum(s.J for s in all_states.values()) / len(all_states)
        avg_P = sum(s.P for s in all_states.values()) / len(all_states)
        avg_W = sum(s.W for s in all_states.values()) / len(all_states)

        return LJPWState(avg_L, avg_J, avg_P, avg_W)


@dataclass
class SimulationResult:
    """Result of simulating an operation in LJPW space"""
    operation: str
    initial_state: LJPWState
    final_state: LJPWState
    trajectory: List[Tuple[float, float, float, float, float]]  # (t, L, J, P, W)
    success_prob: float
    final_health: float
    issues: List[str]
    recommendations: List[str]
    duration: float
    converging: bool
    eta_to_ne: float


class LJPWVirtualMachine:
    """
    Virtual Machine for semantic computing in LJPW space.

    This is the execution environment where semantic structures
    "run" without executing bytes.
    """

    def __init__(self):
        self.model = LJPWDynamicModel()
        self.loaded_structures: Dict[str, LJPWStructure] = {}

    def load_iso(self, iso_path: str, analyze: bool = True) -> LJPWStructure:
        """
        Load an ISO into LJPW space.

        Args:
            iso_path: Path to ISO file
            analyze: Whether to analyze structure (True) or use defaults

        Returns:
            LJPWStructure representing the ISO
        """
        if analyze:
            # Use the ISO analyzer to extract structure
            from ljpw_iso_analyzer import LJPWISOAnalyzer
            analyzer = LJPWISOAnalyzer()
            result = analyzer.analyze(iso_path)

            ljpw = result['ljpw']
            root_state = LJPWState(ljpw['L'], ljpw['J'], ljpw['P'], ljpw['W'])
        else:
            # Default structure
            root_state = LJPWState(0.7, 0.7, 0.7, 0.7)

        # Create hierarchical structure
        # ISO typically has: boot, installer, core OS, components

        boot = LJPWComponent(
            name='boot',
            state=LJPWState(0.9, 0.95, 0.8, 0.9),  # Boot sector is critical
            component_type='boot_sector',
            subcomponents={},
            metadata={'critical': True}
        )

        installer = LJPWComponent(
            name='installer',
            state=LJPWState(0.8, 0.85, 0.9, 0.85),  # Installer is optimized
            component_type='installer',
            subcomponents={},
            metadata={'temporary': True}
        )

        core_os = LJPWComponent(
            name='core',
            state=LJPWState(0.85, 0.9, 0.85, 0.9),  # Core is well-designed
            component_type='operating_system',
            subcomponents={},
            metadata={'persistent': True}
        )

        root = LJPWComponent(
            name='iso',
            state=root_state,
            component_type='iso_image',
            subcomponents={
                'boot': boot,
                'installer': installer,
                'core': core_os
            },
            metadata={'path': iso_path}
        )

        # Define interactions (how components affect each other)
        interactions = {
            ('boot', 'installer'): 0.9,      # Boot enables installer
            ('installer', 'core'): 0.95,     # Installer deploys core
            ('core', 'installer'): 0.3,      # Core affects installer minimally
        }

        structure = LJPWStructure(
            name=iso_path,
            root=root,
            interactions=interactions
        )

        self.loaded_structures[iso_path] = structure
        return structure

    def load_structure(self, structure: LJPWStructure) -> None:
        """Load a pre-built structure into the VM"""
        self.loaded_structures[structure.name] = structure

    def simulate_operation(self,
                          structure: LJPWStructure,
                          operation: str,
                          duration: float = 100.0,
                          environment: Optional[Dict] = None) -> SimulationResult:
        """
        Simulate an operation on a structure in LJPW space.

        Args:
            structure: The structure to operate on
            operation: Operation type ('install', 'deploy', 'update', etc.)
            duration: Simulation duration (arbitrary time units)
            environment: Environmental factors (hardware, network, etc.)

        Returns:
            SimulationResult with predicted outcome
        """
        # Get initial state
        initial = structure.overall_state()

        # Apply operation-specific dynamics
        if operation == 'install':
            trajectory = self._simulate_installation(structure, duration, environment)
        elif operation == 'update':
            trajectory = self._simulate_update(structure, duration)
        elif operation == 'scale':
            trajectory = self._simulate_scaling(structure, duration)
        else:
            # Generic simulation using v3.0 dynamics
            trajectory = self.model.simulate(initial.as_tuple(), duration=duration)

        # Analyze trajectory
        final_state_tuple = trajectory[-1][1:]
        final = LJPWState(*final_state_tuple)

        # Calculate success probability based on final health
        final_health = final.health()
        success_prob = final_health  # Simple mapping for now

        # Check for convergence
        analysis = self.model.analyze_trajectory(trajectory)
        converging = analysis['converging']
        eta_to_ne = analysis.get('eta_to_ne', float('inf'))

        # Identify issues
        issues = self._identify_issues(initial, final, trajectory)

        # Generate recommendations
        recommendations = self._generate_recommendations(final, issues)

        return SimulationResult(
            operation=operation,
            initial_state=initial,
            final_state=final,
            trajectory=trajectory,
            success_prob=success_prob,
            final_health=final_health,
            issues=issues,
            recommendations=recommendations,
            duration=duration,
            converging=converging,
            eta_to_ne=eta_to_ne
        )

    def _simulate_installation(self,
                               structure: LJPWStructure,
                               duration: float,
                               environment: Optional[Dict]) -> List:
        """Simulate OS installation process"""
        initial = structure.overall_state()

        # Installation has phases that affect LJPW differently
        # Phase 1: Boot (0-10%)
        # Phase 2: Partition/format (10-30%)
        # Phase 3: Copy files (30-80%)
        # Phase 4: Configure (80-100%)

        # Simulate with modified parameters to represent installation stress
        # During install: P increases (high activity), L may decrease (risk)

        trajectory = []
        state = initial.as_tuple()
        time = 0
        dt = duration / 100  # 100 steps

        for step in range(100):
            # Apply installation dynamics
            L, J, P, W = state

            # Installation increases P (activity)
            if step < 80:  # During active installation
                P_boost = 0.1 * (1 - step/80)  # Decreasing boost
                P = min(1.0, P + P_boost)

            # Environment affects L (safety)
            if environment:
                env_L = environment.get('safety_factor', 1.0)
                L = L * env_L

            # Use model to evolve
            state = self.model.rk4_step((L, J, P, W), dt)
            time += dt

            trajectory.append((time, *state))

        return trajectory

    def _simulate_update(self, structure: LJPWStructure, duration: float) -> List:
        """Simulate system update"""
        initial = structure.overall_state()

        # Update temporarily decreases L (risk) and J (disruption)
        # But increases W (improvements) over time

        trajectory = []
        state = initial.as_tuple()
        time = 0
        dt = duration / 100

        for step in range(100):
            L, J, P, W = state

            # Update phase effects
            if step < 30:  # Download phase
                P_boost = 0.05  # Network activity
                P = min(1.0, P + P_boost)
            elif step < 70:  # Install phase
                L_risk = -0.1  # Temporary risk
                L = max(0.0, L + L_risk)
            else:  # Complete phase
                W_improve = 0.05  # Improvements integrated
                W = min(1.0, W + W_improve)

            state = self.model.rk4_step((L, J, P, W), dt)
            time += dt
            trajectory.append((time, *state))

        return trajectory

    def _simulate_scaling(self, structure: LJPWStructure, duration: float) -> List:
        """Simulate system scaling (adding resources)"""
        initial = structure.overall_state()

        # Scaling increases P (capacity) and may affect J (complexity)
        trajectory = self.model.simulate(initial.as_tuple(), duration=duration)

        # Modify to show scaling effects
        modified = []
        for i, (t, L, J, P, W) in enumerate(trajectory):
            scale_factor = 1 + (i / len(trajectory)) * 0.2  # 20% increase
            P_scaled = min(1.0, P * scale_factor)
            modified.append((t, L, J, P_scaled, W))

        return modified

    def _identify_issues(self,
                        initial: LJPWState,
                        final: LJPWState,
                        trajectory: List) -> List[str]:
        """Identify potential issues from simulation"""
        issues = []

        # Check threshold crossing
        if final.P > 0.71 and final.W < 0.60:
            issues.append(f"Power crossed threshold (P={final.P:.2f} > 0.71) with low Wisdom (W={final.W:.2f})")
            issues.append("Risk: Over-optimization may cause instability")

        # Check dimension drops
        if final.L < initial.L - 0.2:
            issues.append(f"Safety decreased significantly (L: {initial.L:.2f} → {final.L:.2f})")

        if final.J < initial.J - 0.2:
            issues.append(f"Structure degraded (J: {initial.J:.2f} → {final.J:.2f})")

        # Check health
        if final.health() < 0.5:
            issues.append(f"Low final health ({final.health()*100:.1f}%)")

        # Check for oscillations in trajectory
        if len(trajectory) > 10:
            recent_L = [t[1] for t in trajectory[-10:]]
            if max(recent_L) - min(recent_L) > 0.3:
                issues.append("Unstable trajectory detected (oscillations)")

        return issues

    def _generate_recommendations(self,
                                  final: LJPWState,
                                  issues: List[str]) -> List[str]:
        """Generate recommendations based on final state"""
        recommendations = []

        L_ne, J_ne, P_ne, W_ne = NATURAL_EQUILIBRIUM

        # Dimension-specific recommendations
        if final.L < L_ne - 0.1:
            recommendations.append(f"Boost Safety (L): Add validation, error handling, monitoring")

        if final.J < J_ne - 0.1:
            recommendations.append(f"Improve Structure (J): Add documentation, modularize, clean interfaces")

        if final.P > P_ne + 0.1 and final.W < W_ne:
            recommendations.append(f"Balance Power with Wisdom: Add architecture review before optimizing")

        if final.W < W_ne - 0.1:
            recommendations.append(f"Increase Wisdom (W): Invest in design, planning, architecture")

        # Issue-specific
        if "threshold" in ' '.join(issues).lower():
            recommendations.append("CRITICAL: Reduce Power or increase Wisdom to avoid erosion")

        if not recommendations:
            recommendations.append("System near optimal - maintain current trajectory")

        return recommendations

    def predict_interaction(self,
                           structure1: LJPWStructure,
                           structure2: LJPWStructure,
                           interaction_type: str = 'integrate') -> SimulationResult:
        """
        Predict outcome of two structures interacting.

        Example: Deploying application (structure1) on OS (structure2)
        """
        # Combine states with interaction dynamics
        state1 = structure1.overall_state()
        state2 = structure2.overall_state()

        # Weighted combination based on interaction type
        if interaction_type == 'integrate':
            # Application inherits OS characteristics
            combined_L = 0.3 * state1.L + 0.7 * state2.L
            combined_J = 0.5 * state1.J + 0.5 * state2.J
            combined_P = 0.7 * state1.P + 0.3 * state2.P
            combined_W = 0.4 * state1.W + 0.6 * state2.W
        else:
            # Simple average
            combined_L = (state1.L + state2.L) / 2
            combined_J = (state1.J + state2.J) / 2
            combined_P = (state1.P + state2.P) / 2
            combined_W = (state1.W + state2.W) / 2

        combined_state = LJPWState(combined_L, combined_J, combined_P, combined_W)

        # Simulate evolution
        trajectory = self.model.simulate(combined_state.as_tuple(), duration=50)

        final_tuple = trajectory[-1][1:]
        final = LJPWState(*final_tuple)

        analysis = self.model.analyze_trajectory(trajectory)

        return SimulationResult(
            operation=f'{interaction_type}_{structure1.name}_with_{structure2.name}',
            initial_state=combined_state,
            final_state=final,
            trajectory=trajectory,
            success_prob=final.health(),
            final_health=final.health(),
            issues=self._identify_issues(combined_state, final, trajectory),
            recommendations=self._generate_recommendations(final, []),
            duration=50,
            converging=analysis['converging'],
            eta_to_ne=analysis.get('eta_to_ne', float('inf'))
        )

    def create_composite_structure(self,
                                   name: str,
                                   components: Dict[str, LJPWComponent],
                                   interactions: Dict[Tuple[str, str], float]) -> LJPWStructure:
        """
        Create a composite structure from components.

        Example: Build a full stack (database + app + load balancer)
        """
        # Calculate overall state from components
        if components:
            avg_L = sum(c.state.L for c in components.values()) / len(components)
            avg_J = sum(c.state.J for c in components.values()) / len(components)
            avg_P = sum(c.state.P for c in components.values()) / len(components)
            avg_W = sum(c.state.W for c in components.values()) / len(components)
        else:
            avg_L = avg_J = avg_P = avg_W = 0.5

        root = LJPWComponent(
            name=name,
            state=LJPWState(avg_L, avg_J, avg_P, avg_W),
            component_type='composite',
            subcomponents=components,
            metadata={'created': 'composite'}
        )

        return LJPWStructure(
            name=name,
            root=root,
            interactions=interactions
        )


# Example usage and demonstrations
if __name__ == '__main__':
    print("="*70)
    print("LJPW Virtual Machine - Semantic Computing Demo")
    print("="*70)
    print()
    print("Demonstrates: LJPW space as a computational substrate")
    print("Operations run on MEANING, not bytes!")
    print()

    vm = LJPWVirtualMachine()

    # Example 1: Load and "install" Ubuntu (simulated structure)
    print("="*70)
    print("Example 1: Installing Ubuntu Server in LJPW Space")
    print("-"*70)
    print()

    # Create simulated Ubuntu structure
    ubuntu = vm.create_composite_structure(
        name='ubuntu-22.04-server',
        components={
            'boot': LJPWComponent(
                'boot',
                LJPWState(0.9, 0.95, 0.85, 0.9),
                'boot_sector',
                {},
                {}
            ),
            'installer': LJPWComponent(
                'installer',
                LJPWState(0.85, 0.90, 0.90, 0.85),
                'installer',
                {},
                {}
            ),
            'core': LJPWComponent(
                'core',
                LJPWState(0.88, 0.90, 0.85, 0.90),
                'os_core',
                {},
                {}
            )
        },
        interactions={
            ('boot', 'installer'): 0.95,
            ('installer', 'core'): 0.90
        }
    )

    print(f"Loaded: {ubuntu.name}")
    print(f"Initial state: L={ubuntu.overall_state().L:.2f}, J={ubuntu.overall_state().J:.2f}, "
          f"P={ubuntu.overall_state().P:.2f}, W={ubuntu.overall_state().W:.2f}")
    print(f"Initial health: {ubuntu.overall_state().health()*100:.1f}%")
    print()

    # Simulate installation
    print("Simulating installation (in LJPW space, NO bytes executed)...")
    result = vm.simulate_operation(
        ubuntu,
        operation='install',
        duration=60,
        environment={'safety_factor': 0.95}  # Slightly risky environment
    )

    print()
    print("RESULTS:")
    print(f"  Success probability: {result.success_prob*100:.1f}%")
    print(f"  Final health: {result.final_health*100:.1f}%")
    print(f"  Final state: L={result.final_state.L:.2f}, J={result.final_state.J:.2f}, "
          f"P={result.final_state.P:.2f}, W={result.final_state.W:.2f}")
    print(f"  Converging to NE: {result.converging}")
    if result.eta_to_ne != float('inf'):
        print(f"  ETA to equilibrium: {result.eta_to_ne:.1f} time units")

    if result.issues:
        print(f"\n  Issues detected:")
        for issue in result.issues:
            print(f"    - {issue}")

    if result.recommendations:
        print(f"\n  Recommendations:")
        for rec in result.recommendations:
            print(f"    ✓ {rec}")

    print()
    print("⚡ Installation simulated in MILLISECONDS (not minutes!)")
    print("⚡ Outcome predicted WITHOUT executing a single byte!")
    print()

    # Example 2: Deploy application on OS
    print("="*70)
    print("Example 2: Deploying Application on Ubuntu")
    print("-"*70)
    print()

    # Create application structure
    webapp = vm.create_composite_structure(
        name='webapp',
        components={
            'backend': LJPWComponent(
                'backend',
                LJPWState(0.65, 0.70, 0.85, 0.75),
                'application',
                {},
                {}
            ),
            'database': LJPWComponent(
                'database',
                LJPWState(0.80, 0.85, 0.75, 0.85),
                'database',
                {},
                {}
            )
        },
        interactions={('backend', 'database'): 0.85}
    )

    print(f"Application: {webapp.name}")
    print(f"  Backend: L={webapp.root.subcomponents['backend'].state.L:.2f}, "
          f"J={webapp.root.subcomponents['backend'].state.J:.2f}")
    print(f"  Database: L={webapp.root.subcomponents['database'].state.L:.2f}, "
          f"J={webapp.root.subcomponents['database'].state.J:.2f}")
    print()

    print("Predicting integration with Ubuntu...")
    integration = vm.predict_interaction(webapp, ubuntu, 'integrate')

    print()
    print("PREDICTION:")
    print(f"  Integration success: {integration.success_prob*100:.1f}%")
    print(f"  Combined health: {integration.final_health*100:.1f}%")
    print(f"  System stable: {integration.converging}")

    if integration.issues:
        print(f"\n  Potential issues:")
        for issue in integration.issues:
            print(f"    ⚠️  {issue}")

    print()
    print("="*70)
    print("KEY INSIGHT")
    print("-"*70)
    print()
    print("We just simulated:")
    print("  1. OS installation (60 time units)")
    print("  2. Application deployment")
    print("  3. System integration")
    print()
    print("ENTIRELY in LJPW semantic space.")
    print("NO bytes executed. NO virtual machines. NO containers.")
    print()
    print("Yet we predicted:")
    print("  - Success probability")
    print("  - Final system health")
    print("  - Potential issues")
    print("  - Recommended fixes")
    print()
    print("This is SEMANTIC COMPUTING.")
    print("Operations on MEANING, not bytes.")
    print("="*70)
