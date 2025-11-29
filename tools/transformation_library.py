#!/usr/bin/env python3
"""
Semantic Transformation Library

Catalog of reusable transformation vectors discovered through
analogical reasoning experiments.

These vectors represent SEMANTIC OPERATIONS that can be applied
to any code to achieve specific quality improvements.

Usage:
    from transformation_library import TRANSFORMATIONS, apply_transformation

    # Apply "add safety" to any code
    new_coords = apply_transformation(old_coords, "add_safety")
"""

import math
from typing import Dict, List, Tuple

# ============================================================================
# DISCOVERED TRANSFORMATIONS
# ============================================================================

TRANSFORMATIONS: Dict[str, Tuple[float, float, float, float]] = {
    # Safety Transformations
    "add_safety": (+0.30, +0.18, 0.00, +0.02),
    "add_validation": (+0.25, +0.10, 0.00, 0.00),
    "add_error_handling": (+0.35, +0.20, 0.00, +0.05),
    # Structure Transformations
    "add_documentation": (0.00, +0.18, 0.00, +0.02),
    "add_types": (0.00, +0.20, 0.00, +0.05),
    "add_structure": (+0.05, +0.25, 0.00, +0.10),
    # Performance Transformations
    "optimize": (0.00, 0.00, +0.40, +0.20),
    "add_caching": (-0.05, +0.05, +0.30, +0.10),
    "parallelize": (0.00, +0.05, +0.35, +0.15),
    # Design Transformations
    "add_abstraction": (+0.05, +0.10, 0.00, +0.30),
    "apply_patterns": (+0.10, +0.15, 0.00, +0.35),
    "refactor": (+0.10, +0.15, +0.05, +0.40),
    # Composite Transformations
    "productionize": (+0.40, +0.30, +0.10, +0.20),
    "harden": (+0.45, +0.35, +0.05, +0.15),
    "modernize": (+0.15, +0.30, +0.20, +0.35),
    # Direction Transformations
    "move_to_ne": None,  # Special: move toward Natural Equilibrium
    "move_to_anchor": None,  # Special: move toward (1,1,1,1)
}

# Natural Equilibrium coordinates
NATURAL_EQUILIBRIUM = (0.618, 0.414, 0.718, 0.693)
ANCHOR_POINT = (1.0, 1.0, 1.0, 1.0)

# ============================================================================
# TRANSFORMATION METADATA
# ============================================================================

TRANSFORMATION_INFO: Dict[str, Dict] = {
    "add_safety": {
        "description": "Add error handling and validation",
        "use_case": "Make risky code safer",
        "example": "simple function → defensive function",
        "discovered": "Experiment 2 (analogical reasoning)",
        "confidence": "high",
    },
    "add_documentation": {
        "description": "Add docstrings and type annotations",
        "use_case": "Make code more maintainable",
        "example": "undocumented → documented",
        "discovered": "Experiment 2 (analogical reasoning)",
        "confidence": "high",
    },
    "optimize": {
        "description": "Apply performance optimizations",
        "use_case": "Make slow code faster",
        "example": "loop → list comprehension, caching",
        "discovered": "Pattern analysis",
        "confidence": "medium",
    },
    "productionize": {
        "description": "Transform prototype to production code",
        "use_case": "Prepare code for deployment",
        "example": "prototype → production",
        "discovered": "Experiment 2 (analogical reasoning)",
        "confidence": "high",
    },
    "refactor": {
        "description": "Improve design and architecture",
        "use_case": "Clean up messy code",
        "example": "spaghetti → well-designed",
        "discovered": "Pattern analysis",
        "confidence": "medium",
    },
}

# ============================================================================
# TRANSFORMATION OPERATIONS
# ============================================================================


def apply_transformation(
    coords: Tuple[float, float, float, float], transformation_name: str, strength: float = 1.0
) -> Tuple[float, float, float, float]:
    """
    Apply a semantic transformation to coordinates.

    Args:
        coords: Current LJPW coordinates (L, J, P, W)
        transformation_name: Name of transformation to apply
        strength: Multiplier for transformation (0.0-1.0)

    Returns:
        New coordinates after transformation

    Example:
        old_coords = (0.3, 0.2, 0.5, 0.3)
        new_coords = apply_transformation(old_coords, "add_safety")
        # new_coords ≈ (0.6, 0.38, 0.5, 0.32)
    """
    if transformation_name not in TRANSFORMATIONS:
        raise ValueError(f"Unknown transformation: {transformation_name}")

    vector = TRANSFORMATIONS[transformation_name]

    # Special transformations
    if vector is None:
        if transformation_name == "move_to_ne":
            return move_toward(coords, NATURAL_EQUILIBRIUM, strength)
        elif transformation_name == "move_to_anchor":
            return move_toward(coords, ANCHOR_POINT, strength)

    # Standard vector transformation
    L, J, P, W = coords
    dL, dJ, dP, dW = vector

    return (
        max(0.0, min(1.5, L + strength * dL)),
        max(0.0, min(1.5, J + strength * dJ)),
        max(0.0, min(1.5, P + strength * dP)),
        max(0.0, min(1.5, W + strength * dW)),
    )


def move_toward(
    coords: Tuple[float, float, float, float],
    target: Tuple[float, float, float, float],
    alpha: float = 0.5,
) -> Tuple[float, float, float, float]:
    """
    Move coordinates toward a target position.

    Args:
        coords: Current position
        target: Target position
        alpha: How far to move (0.0 = no change, 1.0 = reach target)

    Returns:
        New position
    """
    L, J, P, W = coords
    tL, tJ, tP, tW = target

    return (L + alpha * (tL - L), J + alpha * (tJ - J), P + alpha * (tP - P), W + alpha * (tW - W))


def compose_transformations(
    coords: Tuple[float, float, float, float], transformations: List[str]
) -> Tuple[float, float, float, float]:
    """
    Apply multiple transformations in sequence.

    Args:
        coords: Starting coordinates
        transformations: List of transformation names to apply

    Returns:
        Final coordinates after all transformations

    Example:
        # Make code safe AND well-documented
        final = compose_transformations(
            (0.3, 0.2, 0.5, 0.3),
            ["add_safety", "add_documentation"]
        )
    """
    result = coords
    for transformation in transformations:
        result = apply_transformation(result, transformation)
    return result


def suggest_transformation(
    current: Tuple[float, float, float, float], target: Tuple[float, float, float, float]
) -> List[str]:
    """
    Suggest transformations to move from current to target.

    Args:
        current: Current coordinates
        target: Desired coordinates

    Returns:
        List of suggested transformation names

    Example:
        current = (0.3, 0.2, 0.5, 0.3)  # Prototype
        target = (0.8, 0.7, 0.5, 0.6)   # Production
        suggestions = suggest_transformation(current, target)
        # → ["add_safety", "add_documentation"]
    """
    L1, J1, P1, W1 = current
    L2, J2, P2, W2 = target

    suggestions = []

    # Calculate needed changes
    dL = L2 - L1
    dJ = J2 - J1
    dP = P2 - P1
    dW = W2 - W1

    # Suggest transformations based on deltas
    if dL > 0.2:
        suggestions.append("add_safety")
    if dJ > 0.2:
        suggestions.append("add_documentation")
    if dP > 0.2:
        suggestions.append("optimize")
    if dW > 0.2:
        suggestions.append("refactor")

    # Special cases
    if dL > 0.3 and dJ > 0.2:
        suggestions = ["productionize"]

    return suggestions if suggestions else ["move_to_ne"]


def calculate_distance(
    coords1: Tuple[float, float, float, float], coords2: Tuple[float, float, float, float]
) -> float:
    """Calculate Euclidean distance between two positions."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coords1, coords2)))


# ============================================================================
# VISUALIZATION
# ============================================================================


def visualize_transformation(
    coords: Tuple[float, float, float, float], transformation_name: str
) -> str:
    """
    Generate a text visualization of a transformation.

    Returns:
        Formatted string showing before/after
    """
    new_coords = apply_transformation(coords, transformation_name)

    L1, J1, P1, W1 = coords
    L2, J2, P2, W2 = new_coords

    output = []
    output.append(f"\nTransformation: {transformation_name}")
    output.append("=" * 50)

    if transformation_name in TRANSFORMATION_INFO:
        info = TRANSFORMATION_INFO[transformation_name]
        output.append(f"Description: {info['description']}")
        output.append(f"Use case: {info['use_case']}")
        output.append("")

    output.append(f"Before: L={L1:.2f}, J={J1:.2f}, P={P1:.2f}, W={W1:.2f}")
    output.append(f"After:  L={L2:.2f}, J={J2:.2f}, P={P2:.2f}, W={W2:.2f}")
    output.append("")
    output.append("Changes:")

    if abs(L2 - L1) > 0.05:
        direction = "↑" if L2 > L1 else "↓"
        output.append(f"  Love (Safety):       {L1:.2f} → {L2:.2f} {direction}")

    if abs(J2 - J1) > 0.05:
        direction = "↑" if J2 > J1 else "↓"
        output.append(f"  Justice (Structure): {J1:.2f} → {J2:.2f} {direction}")

    if abs(P2 - P1) > 0.05:
        direction = "↑" if P2 > P1 else "↓"
        output.append(f"  Power (Performance): {P1:.2f} → {P2:.2f} {direction}")

    if abs(W2 - W1) > 0.05:
        direction = "↑" if W2 > W1 else "↓"
        output.append(f"  Wisdom (Design):     {W1:.2f} → {W2:.2f} {direction}")

    return "\n".join(output)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SEMANTIC TRANSFORMATION LIBRARY")
    print("=" * 70)

    # Example 1: Transform prototype to production
    print("\n" + "-" * 70)
    print("Example 1: Productionizing Code")
    print("-" * 70)

    prototype = (0.3, 0.2, 0.5, 0.3)
    print(f"Prototype code: {prototype}")

    production = apply_transformation(prototype, "productionize")
    print(f"After productionize: {production}")
    print(f"Distance moved: {calculate_distance(prototype, production):.3f}")

    # Example 2: Add safety to risky code
    print("\n" + "-" * 70)
    print("Example 2: Adding Safety")
    print("-" * 70)

    risky_code = (0.2, 0.3, 0.8, 0.4)
    print(visualize_transformation(risky_code, "add_safety"))

    # Example 3: Compose transformations
    print("\n" + "-" * 70)
    print("Example 3: Composing Transformations")
    print("-" * 70)

    start = (0.3, 0.2, 0.5, 0.3)
    final = compose_transformations(start, ["add_safety", "add_documentation", "refactor"])

    print(f"Start:  {start}")
    print(f"Final:  {final}")
    print(f"Applied: add_safety → add_documentation → refactor")

    # Example 4: Get suggestions
    print("\n" + "-" * 70)
    print("Example 4: Transformation Suggestions")
    print("-" * 70)

    current = (0.3, 0.2, 0.5, 0.3)
    target = (0.8, 0.7, 0.5, 0.6)

    suggestions = suggest_transformation(current, target)
    print(f"Current: {current}")
    print(f"Target:  {target}")
    print(f"Suggested transformations: {', '.join(suggestions)}")

    # Example 5: Move toward Natural Equilibrium
    print("\n" + "-" * 70)
    print("Example 5: Moving Toward Natural Equilibrium")
    print("-" * 70)

    imbalanced = (0.9, 0.2, 0.3, 0.2)
    balanced = apply_transformation(imbalanced, "move_to_ne", strength=0.5)

    print(f"Imbalanced code: {imbalanced}")
    print(f"Natural Equilibrium: {NATURAL_EQUILIBRIUM}")
    print(f"50% toward NE: {balanced}")
    print(f"Distance from NE: {calculate_distance(balanced, NATURAL_EQUILIBRIUM):.3f}")

    print("\n" + "=" * 70)
    print(f"Total transformations available: {len(TRANSFORMATIONS)}")
    print("=" * 70 + "\n")
