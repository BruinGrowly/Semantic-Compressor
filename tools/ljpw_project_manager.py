#!/usr/bin/env python3
"""
LJPW Project Management System
===============================

Manages the LJPW validation project using LJPW coordinates.

This is META-DEMONSTRATION:
- Use LJPW to coordinate project validating LJPW
- Prove LJPW optimizes complex project execution
- Show Natural Equilibrium applies to project management

Core Concepts:
- Each task has LJPW coordinates (semantic properties)
- Project health = distance from Natural Equilibrium
- Optimal execution = balanced across all dimensions
- Real-time dashboard shows project in 4D semantic space

Usage:
    python ljpw_project_manager.py --status
    python ljpw_project_manager.py --optimize
    python ljpw_project_manager.py --dashboard
"""

import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# === LJPW Constants ===

ANCHOR = (1.0, 1.0, 1.0, 1.0)
NATURAL_EQUILIBRIUM = (0.618, 0.414, 0.718, 0.693)


# === Data Structures ===


@dataclass
class Task:
    """A project task with LJPW coordinates"""

    id: str
    name: str
    track: str  # A, B, C, or D
    description: str

    # LJPW Coordinates
    L: float  # Love (Safety/Risk Management)
    J: float  # Justice (Structure/Organization)
    P: float  # Power (Performance/Impact)
    W: float  # Wisdom (Design/Elegance)

    # Metadata
    status: str  # pending, in_progress, completed, blocked
    priority: int  # 1-5 (5 = highest)
    effort_hours: float
    dependencies: List[str]
    assigned_to: str
    deadline: str

    def ljpw_coords(self) -> Tuple[float, float, float, float]:
        """Get LJPW coordinates as tuple"""
        return (self.L, self.J, self.P, self.W)

    def distance_from_ne(self) -> float:
        """Distance from Natural Equilibrium"""
        return math.sqrt(
            (self.L - NATURAL_EQUILIBRIUM[0]) ** 2
            + (self.J - NATURAL_EQUILIBRIUM[1]) ** 2
            + (self.P - NATURAL_EQUILIBRIUM[2]) ** 2
            + (self.W - NATURAL_EQUILIBRIUM[3]) ** 2
        )

    def health_score(self) -> float:
        """Task health (0-100, higher = better)"""
        d = self.distance_from_ne()
        return max(0, 100 * (2 - d) / 2)


# === Project Tasks Database ===

TASKS = [
    # TRACK A: Empirical Validation (Code Analysis)
    Task(
        id="A1",
        name="Collect 20 algorithm implementations",
        track="A",
        description="Gather 20 algorithms × 5 languages = 100 implementations",
        L=0.7,  # High safety (need quality control)
        J=0.8,  # High structure (systematic collection)
        P=0.5,  # Medium performance (data gathering)
        W=0.6,  # Medium wisdom (straightforward task)
        status="pending",
        priority=5,
        effort_hours=20,
        dependencies=[],
        assigned_to="team",
        deadline="2025-11-24",
    ),
    Task(
        id="A2",
        name="Batch analyze all implementations",
        track="A",
        description="Run LJPW analyzer on all 100 files",
        L=0.5,  # Medium safety (automated process)
        J=0.7,  # High structure (batch processing)
        P=0.9,  # Very high performance (computation)
        W=0.7,  # Good design (automated pipeline)
        status="pending",
        priority=4,
        effort_hours=10,
        dependencies=["A1"],
        assigned_to="automation",
        deadline="2025-11-26",
    ),
    Task(
        id="A3",
        name="Statistical analysis",
        track="A",
        description="Compute correlations, significance tests, visualizations",
        L=0.6,  # Safety (rigorous statistics)
        J=0.9,  # Very high structure (statistical framework)
        P=0.6,  # Medium performance (analysis)
        W=0.8,  # High wisdom (elegant statistical methods)
        status="pending",
        priority=5,
        effort_hours=30,
        dependencies=["A2"],
        assigned_to="data_scientist",
        deadline="2025-12-03",
    ),
    Task(
        id="A4",
        name="Write empirical validation paper",
        track="A",
        description="Manuscript for ICSE/OOPSLA submission",
        L=0.8,  # High safety (peer review standards)
        J=0.9,  # Very high structure (academic format)
        P=0.7,  # Good performance (high-impact publication)
        W=0.9,  # Very high wisdom (clear communication)
        status="pending",
        priority=5,
        effort_hours=60,
        dependencies=["A3"],
        assigned_to="research_lead",
        deadline="2025-12-20",
    ),
    # TRACK B: Meaning Research (Physics/Chemistry/Biology)
    Task(
        id="B1",
        name="Map chemistry constants",
        track="B",
        description="Bond energies, reaction rates, catalysis",
        L=0.6,  # Medium safety (domain knowledge needed)
        J=0.8,  # High structure (periodic table organization)
        P=0.6,  # Medium performance (exploratory)
        W=0.7,  # Good wisdom (elegant mapping)
        status="pending",
        priority=3,
        effort_hours=25,
        dependencies=[],
        assigned_to="chemist",
        deadline="2025-12-10",
    ),
    Task(
        id="B2",
        name="Map biology constants",
        track="B",
        description="Metabolic rates, enzyme kinetics, DNA",
        L=0.7,  # Good safety (complex domain)
        J=0.7,  # Good structure (biological systems)
        P=0.6,  # Medium performance
        W=0.8,  # High wisdom (life optimization)
        status="pending",
        priority=3,
        effort_hours=25,
        dependencies=[],
        assigned_to="biologist",
        deadline="2025-12-10",
    ),
    Task(
        id="B3",
        name="Cross-domain synthesis paper",
        track="B",
        description="'LJPW: Universal Coordinate System' for Nature/Science",
        L=0.9,  # Very high safety (bold claims need evidence)
        J=0.9,  # Very high structure (comprehensive)
        P=0.9,  # Very high performance (Nature/Science!)
        W=1.0,  # Maximum wisdom (paradigm shift)
        status="pending",
        priority=5,
        effort_hours=80,
        dependencies=["B1", "B2"],
        assigned_to="research_lead",
        deadline="2026-03-01",
    ),
    # TRACK C: Practical Tools (Developer Productivity)
    Task(
        id="C1",
        name="Build VSCode extension",
        track="C",
        description="Real-time LJPW analysis in IDE",
        L=0.8,  # High safety (user-facing tool)
        J=0.7,  # Good structure (extension architecture)
        P=0.8,  # High performance (real-time analysis)
        W=0.9,  # Very high wisdom (elegant UX)
        status="pending",
        priority=4,
        effort_hours=40,
        dependencies=[],
        assigned_to="frontend_engineer",
        deadline="2025-12-15",
    ),
    Task(
        id="C2",
        name="Train quality prediction model",
        track="C",
        description="ML model: LJPW → bugs/maintainability",
        L=0.7,  # Good safety (validation needed)
        J=0.8,  # High structure (ML pipeline)
        P=0.9,  # Very high performance (predictive power)
        W=0.8,  # High wisdom (feature engineering)
        status="pending",
        priority=4,
        effort_hours=35,
        dependencies=[],
        assigned_to="ml_engineer",
        deadline="2025-12-10",
    ),
    Task(
        id="C3",
        name="Build semantic search engine",
        track="C",
        description="Cross-language code search by LJPW coordinates",
        L=0.6,  # Medium safety
        J=0.8,  # High structure (indexing system)
        P=0.9,  # Very high performance (search speed)
        W=0.8,  # High wisdom (ranking algorithm)
        status="pending",
        priority=4,
        effort_hours=45,
        dependencies=[],
        assigned_to="backend_engineer",
        deadline="2025-12-20",
    ),
    Task(
        id="C4",
        name="Create demonstration website",
        track="C",
        description="Public demo of all tools at ljpw.demo",
        L=0.7,  # Good safety (production-ready)
        J=0.7,  # Good structure (web app)
        P=0.7,  # Good performance (user engagement)
        W=0.9,  # Very high wisdom (beautiful design)
        status="pending",
        priority=3,
        effort_hours=30,
        dependencies=["C1", "C2", "C3"],
        assigned_to="fullstack_engineer",
        deadline="2026-01-10",
    ),
    # TRACK D: Experimental Validation (Ψ and Θ)
    Task(
        id="D1",
        name="Contact quantum computing labs",
        track="D",
        description="Establish partnerships with IBM, JILA, Caltech",
        L=0.9,  # Very high safety (reputation risk)
        J=0.6,  # Medium structure (networking)
        P=0.8,  # High performance (enables experiments)
        W=0.7,  # Good wisdom (relationship building)
        status="pending",
        priority=4,
        effort_hours=15,
        dependencies=[],
        assigned_to="research_lead",
        deadline="2025-12-01",
    ),
    Task(
        id="D2",
        name="Design quantum coherence experiment",
        track="D",
        description="Protocol for testing Ψ enhancement prediction",
        L=0.9,  # Very high safety (experimental rigor)
        J=1.0,  # Maximum structure (scientific method)
        P=0.7,  # Good performance (breakthrough potential)
        W=0.9,  # Very high wisdom (elegant protocol)
        status="pending",
        priority=5,
        effort_hours=40,
        dependencies=["D1"],
        assigned_to="experimental_physicist",
        deadline="2026-01-15",
    ),
    Task(
        id="D3",
        name="Run pilot experiments",
        track="D",
        description="Initial tests on superconducting qubits",
        L=0.8,  # High safety (careful execution)
        J=0.8,  # High structure (experimental protocol)
        P=1.0,  # Maximum performance (Nobel-worthy!)
        W=0.7,  # Good wisdom (data collection)
        status="pending",
        priority=5,
        effort_hours=120,
        dependencies=["D2"],
        assigned_to="lab_team",
        deadline="2026-04-01",
    ),
    # META TASKS (Project Management)
    Task(
        id="M1",
        name="LJPW project dashboard",
        track="Meta",
        description="This system - manage project in LJPW space",
        L=0.7,  # Good safety (meta-validation)
        J=0.9,  # Very high structure (project management)
        P=0.6,  # Medium performance (coordination)
        W=1.0,  # Maximum wisdom (self-referential brilliance!)
        status="in_progress",
        priority=5,
        effort_hours=20,
        dependencies=[],
        assigned_to="claude",
        deadline="2025-11-17",
    ),
    Task(
        id="M2",
        name="Weekly progress reports",
        track="Meta",
        description="LJPW-based health monitoring",
        L=0.6,  # Medium safety
        J=0.8,  # High structure (regular reports)
        P=0.5,  # Medium performance (communication)
        W=0.7,  # Good wisdom (transparency)
        status="pending",
        priority=3,
        effort_hours=2,  # per week
        dependencies=["M1"],
        assigned_to="team",
        deadline="ongoing",
    ),
]


# === Analysis Functions ===


def calculate_project_ljpw(
    tasks: List[Task], status_filter: str = None
) -> Tuple[float, float, float, float]:
    """
    Calculate overall project LJPW coordinates.

    Weighted average of task coordinates by effort_hours.
    """
    if status_filter:
        tasks = [t for t in tasks if t.status == status_filter]

    if not tasks:
        return (0, 0, 0, 0)

    total_effort = sum(t.effort_hours for t in tasks)

    weighted_L = sum(t.L * t.effort_hours for t in tasks) / total_effort
    weighted_J = sum(t.J * t.effort_hours for t in tasks) / total_effort
    weighted_P = sum(t.P * t.effort_hours for t in tasks) / total_effort
    weighted_W = sum(t.W * t.effort_hours for t in tasks) / total_effort

    return (weighted_L, weighted_J, weighted_P, weighted_W)


def calculate_project_health(ljpw_coords: Tuple[float, float, float, float]) -> float:
    """Project health = closeness to Natural Equilibrium"""
    d = math.sqrt(sum((c - ne) ** 2 for c, ne in zip(ljpw_coords, NATURAL_EQUILIBRIUM)))
    return max(0, 100 * (2 - d) / 2)


def get_dimension_balance(tasks: List[Task]) -> Dict[str, float]:
    """
    Check if work is balanced across LJPW dimensions.

    Returns variance for each dimension (lower = more balanced).
    """
    if not tasks:
        return {}

    L_values = [t.L for t in tasks]
    J_values = [t.J for t in tasks]
    P_values = [t.P for t in tasks]
    W_values = [t.W for t in tasks]

    def variance(values):
        mean = sum(values) / len(values)
        return sum((v - mean) ** 2 for v in values) / len(values)

    return {
        "L_variance": variance(L_values),
        "J_variance": variance(J_values),
        "P_variance": variance(P_values),
        "W_variance": variance(W_values),
        "total_variance": (
            variance(L_values) + variance(J_values) + variance(P_values) + variance(W_values)
        )
        / 4,
    }


def prioritize_tasks_by_ljpw(tasks: List[Task]) -> List[Task]:
    """
    Optimize task execution order using LJPW principles.

    Priority factors:
    1. Tasks closer to Natural Equilibrium (better health)
    2. High-impact tasks (high P dimension)
    3. Dependencies resolved
    4. Balancing work across dimensions
    """
    # Filter pending tasks
    pending = [t for t in tasks if t.status == "pending"]

    # Calculate scores
    scored_tasks = []
    for task in pending:
        # Base score: task health
        health = task.health_score()

        # Impact bonus: P dimension
        impact = task.P * 20

        # Priority bonus
        priority_bonus = task.priority * 10

        # Dependency penalty
        unresolved_deps = sum(
            1
            for dep_id in task.dependencies
            if not any(t.id == dep_id and t.status == "completed" for t in tasks)
        )
        dep_penalty = unresolved_deps * 30

        # Total score
        score = health + impact + priority_bonus - dep_penalty

        scored_tasks.append((score, task))

    # Sort by score (descending)
    scored_tasks.sort(key=lambda x: x[0], reverse=True)

    return [task for score, task in scored_tasks]


def generate_gantt_chart(tasks: List[Task]) -> str:
    """Generate ASCII Gantt chart visualization"""
    # Group by track
    tracks = {}
    for task in tasks:
        if task.track not in tracks:
            tracks[task.track] = []
        tracks[task.track].append(task)

    # Build chart
    lines = []
    lines.append("\n" + "=" * 80)
    lines.append("PROJECT GANTT CHART (LJPW-Optimized Execution Order)".center(80))
    lines.append("=" * 80 + "\n")

    for track, track_tasks in sorted(tracks.items()):
        lines.append(f"\nTrack {track}:")
        lines.append("-" * 80)

        for task in sorted(track_tasks, key=lambda t: t.id):
            status_icon = {
                "completed": "✓",
                "in_progress": "▶",
                "pending": "○",
                "blocked": "✗",
            }.get(task.status, "?")

            health = task.health_score()
            health_bar = "█" * int(health / 10) + "░" * (10 - int(health / 10))

            lines.append(f"  {status_icon} {task.id}: {task.name:<40} [{health_bar}] {health:.0f}%")

    return "\n".join(lines)


# === Main Interface ===


def show_project_status():
    """Display current project status in LJPW space"""
    print("\n" + "=" * 80)
    print("LJPW PROJECT STATUS DASHBOARD".center(80))
    print("=" * 80 + "\n")

    # Overall project LJPW
    all_coords = calculate_project_ljpw(TASKS)
    all_health = calculate_project_health(all_coords)

    print("OVERALL PROJECT LJPW COORDINATES:")
    print(f"  L (Love/Safety):       {all_coords[0]:.3f}")
    print(f"  J (Justice/Structure): {all_coords[1]:.3f}")
    print(f"  P (Power/Performance): {all_coords[2]:.3f}")
    print(f"  W (Wisdom/Design):     {all_coords[3]:.3f}")
    print(f"\n  Project Health Score:  {all_health:.1f}%")

    # Distance from NE
    d_ne = math.sqrt(sum((c - ne) ** 2 for c, ne in zip(all_coords, NATURAL_EQUILIBRIUM)))
    print(f"  Distance from Natural Equilibrium: {d_ne:.3f}")

    if d_ne < 0.2:
        print("  ✓ EXCELLENT - Project is well-balanced!")
    elif d_ne < 0.4:
        print("  ⚠ GOOD - Minor imbalances")
    else:
        print("  ✗ NEEDS REBALANCING - Significant imbalance detected")

    # Task breakdown by status
    print("\n" + "-" * 80)
    print("TASK STATUS BREAKDOWN:")
    print("-" * 80)

    status_counts = {}
    for task in TASKS:
        status_counts[task.status] = status_counts.get(task.status, 0) + 1

    total_tasks = len(TASKS)
    for status, count in sorted(status_counts.items()):
        pct = count / total_tasks * 100
        print(f"  {status.capitalize():<15} {count:>3} tasks ({pct:.0f}%)")

    # Track breakdown
    print("\n" + "-" * 80)
    print("PROGRESS BY TRACK:")
    print("-" * 80)

    for track in ["A", "B", "C", "D", "Meta"]:
        track_tasks = [t for t in TASKS if t.track == track]
        if track_tasks:
            track_coords = calculate_project_ljpw(track_tasks)
            track_health = calculate_project_health(track_coords)
            completed = sum(1 for t in track_tasks if t.status == "completed")
            total = len(track_tasks)

            print(
                f"\n  Track {track}: {completed}/{total} tasks completed ({completed/total*100:.0f}%)"
            )
            print(
                f"    LJPW: L={track_coords[0]:.2f} J={track_coords[1]:.2f} P={track_coords[2]:.2f} W={track_coords[3]:.2f}"
            )
            print(f"    Health: {track_health:.1f}%")

    # Dimension balance
    print("\n" + "-" * 80)
    print("DIMENSIONAL BALANCE:")
    print("-" * 80)

    balance = get_dimension_balance(TASKS)
    print(f"  L variance: {balance['L_variance']:.4f}")
    print(f"  J variance: {balance['J_variance']:.4f}")
    print(f"  P variance: {balance['P_variance']:.4f}")
    print(f"  W variance: {balance['W_variance']:.4f}")
    print(f"  Total variance: {balance['total_variance']:.4f}")

    if balance["total_variance"] < 0.05:
        print("  ✓ EXCELLENT BALANCE across all dimensions")
    elif balance["total_variance"] < 0.10:
        print("  ⚠ GOOD BALANCE with minor variations")
    else:
        print("  ✗ IMBALANCED - Consider adding tasks to underrepresented dimensions")

    # Gantt chart
    print(generate_gantt_chart(TASKS))

    print("\n" + "=" * 80 + "\n")


def show_optimized_execution_order():
    """Display LJPW-optimized task execution order"""
    print("\n" + "=" * 80)
    print("LJPW-OPTIMIZED TASK EXECUTION ORDER".center(80))
    print("=" * 80 + "\n")

    prioritized = prioritize_tasks_by_ljpw(TASKS)

    print("Tasks ranked by LJPW optimization score:")
    print("(Health + Impact + Priority - Dependency penalty)\n")

    print(f"{'Rank':<6} {'ID':<6} {'Task':<40} {'Health':<10} {'Track':<8}")
    print("-" * 80)

    for rank, task in enumerate(prioritized[:15], 1):  # Top 15
        health = task.health_score()
        print(f"{rank:<6} {task.id:<6} {task.name:<40} {health:.1f}%     {task.track:<8}")

    print("\n" + "=" * 80 + "\n")


def save_project_state():
    """Save current project state to JSON"""
    output = {
        "timestamp": datetime.now().isoformat(),
        "tasks": [asdict(t) for t in TASKS],
        "overall_ljpw": calculate_project_ljpw(TASKS),
        "project_health": calculate_project_health(calculate_project_ljpw(TASKS)),
        "dimensional_balance": get_dimension_balance(TASKS),
    }

    output_file = Path(__file__).parent.parent / "results" / "project_status.json"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Project state saved to: {output_file}")


def main():
    """Main CLI"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--status":
            show_project_status()
        elif command == "--optimize":
            show_optimized_execution_order()
        elif command == "--save":
            save_project_state()
        else:
            print(f"Unknown command: {command}")
            print("Usage: ljpw_project_manager.py [--status|--optimize|--save]")
    else:
        # Default: show status
        show_project_status()
        show_optimized_execution_order()
        save_project_state()


if __name__ == "__main__":
    main()
