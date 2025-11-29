#!/usr/bin/env python3
"""
Semantic Code Generator

The ultimate LJPW capability: Generate code from semantic coordinates.

Instead of: Code → Analysis → Genome
We do:      Genome → Generation → Code

Input:  L8J7P5W6 + "user authentication"
Output: Code at position (0.8, 0.7, 0.5, 0.6) that handles authentication

This validates that LJPW coordinates truly determine semantic properties.
"""

import sys
from pathlib import Path
from typing import Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.ljpw.ljpw_standalone import analyze_quick

# ============================================================================
# CODE GENERATION ENGINE
# ============================================================================


def generate_code(
    L: float,
    J: float,
    P: float,
    W: float,
    domain: str = "data processing",
    function_name: str = "process",
) -> str:
    """
    Generate code at specified LJPW coordinates.

    Args:
        L: Love/Safety (0-1) - Error handling, validation
        J: Justice/Structure (0-1) - Types, documentation
        P: Power/Performance (0-1) - Optimization, efficiency
        W: Wisdom/Design (0-1) - Patterns, abstraction

    Returns:
        Generated code as string
    """

    code_parts = []

    # ========================================================================
    # J (Justice/Structure): Documentation and Type Annotations
    # ========================================================================

    if J >= 0.7:
        # High structure: Full docstring + type annotations
        code_parts.append(f"def {function_name}(data: List[Any]) -> List[Any]:")
        code_parts.append('    """')
        code_parts.append(f"    {domain.capitalize()} with comprehensive validation.")
        code_parts.append("    ")
        code_parts.append("    Args:")
        code_parts.append("        data: Input data to process")
        code_parts.append("    ")
        code_parts.append("    Returns:")
        code_parts.append("        Processed results")
        code_parts.append("    ")
        code_parts.append("    Raises:")
        code_parts.append("        ValueError: If data is invalid")
        code_parts.append("        TypeError: If data type is incorrect")
        code_parts.append('    """')
    elif J >= 0.4:
        # Medium structure: Simple docstring + some types
        code_parts.append(f"def {function_name}(data: List) -> List:")
        code_parts.append(f'    """{domain.capitalize()} function."""')
    else:
        # Low structure: No docstring or types
        code_parts.append(f"def {function_name}(data):")

    # ========================================================================
    # L (Love/Safety): Validation and Error Handling
    # ========================================================================

    if L >= 0.8:
        # High safety: Comprehensive validation + try/except + logging
        code_parts.append("    # Input validation")
        code_parts.append("    if data is None:")
        code_parts.append('        raise ValueError("Data cannot be None")')
        code_parts.append("    if not data:")
        code_parts.append('        raise ValueError("Data cannot be empty")')
        code_parts.append("    if not isinstance(data, list):")
        code_parts.append('        raise TypeError("Data must be a list")')
        code_parts.append("    ")
        code_parts.append("    try:")
        indent = "    "
    elif L >= 0.5:
        # Medium safety: Basic validation + try/except
        code_parts.append("    if not data:")
        code_parts.append('        raise ValueError("Data required")')
        code_parts.append("    ")
        code_parts.append("    try:")
        indent = "    "
    elif L >= 0.3:
        # Low safety: Minimal check
        code_parts.append("    if not data:")
        code_parts.append("        return []")
        code_parts.append("    ")
        indent = ""
    else:
        # Minimal safety: No checks
        indent = ""

    # ========================================================================
    # P (Power/Performance) + W (Wisdom/Design): Implementation
    # ========================================================================

    if W >= 0.7:
        # High wisdom: Use abstraction and design patterns
        if P >= 0.7:
            # High wisdom + high performance: Strategy pattern + optimization
            code_parts.append(f"{indent}    # Use strategy pattern for flexible processing")
            code_parts.append(f"{indent}    strategy = ProcessingStrategy.select(data)")
            code_parts.append(f"{indent}    result = strategy.execute(data)")
        else:
            # High wisdom + low performance: Clean abstraction
            code_parts.append(f"{indent}    # Delegate to processor for clean separation")
            code_parts.append(f"{indent}    processor = DataProcessor(data)")
            code_parts.append(f"{indent}    result = processor.process()")
    elif P >= 0.7:
        # Low wisdom + high performance: Optimized but direct
        if P >= 0.8:
            # Very high performance: List comprehension + caching
            code_parts.append(f"{indent}    # Optimized processing with comprehension")
            code_parts.append(f"{indent}    result = [transform_cached(item) for item in data]")
        else:
            # High performance: List comprehension
            code_parts.append(f"{indent}    # Efficient list comprehension")
            code_parts.append(f"{indent}    result = [transform(item) for item in data]")
    else:
        # Low wisdom + low performance: Simple loop
        code_parts.append(f"{indent}    # Basic processing")
        code_parts.append(f"{indent}    result = []")
        code_parts.append(f"{indent}    for item in data:")
        code_parts.append(f"{indent}        result.append(transform(item))")

    # ========================================================================
    # L (Love/Safety): Error Handling Completion
    # ========================================================================

    if L >= 0.8:
        # High safety: Comprehensive error handling
        code_parts.append("        return result")
        code_parts.append("    except TypeError as e:")
        code_parts.append('        logger.error(f"Type error during processing: {e}")')
        code_parts.append("        raise")
        code_parts.append("    except ValueError as e:")
        code_parts.append('        logger.error(f"Value error during processing: {e}")')
        code_parts.append("        raise")
        code_parts.append("    except Exception as e:")
        code_parts.append('        logger.error(f"Unexpected error: {e}")')
        code_parts.append("        raise")
    elif L >= 0.5:
        # Medium safety: Basic error handling
        code_parts.append("        return result")
        code_parts.append("    except Exception as e:")
        code_parts.append('        logger.error(f"Processing failed: {e}")')
        code_parts.append("        raise")
    else:
        # Low safety: Direct return
        code_parts.append("    return result")

    return "\n".join(code_parts)


# ============================================================================
# VALIDATION
# ============================================================================


def validate_generation(target_genome: str, generated_code: str) -> Dict:
    """
    Validate that generated code matches target genome.

    Returns dict with:
    - target: Target genome
    - actual: Actual genome of generated code
    - match: Whether they match
    - distance: Distance between target and actual positions
    """
    # Parse target genome
    target_L = int(target_genome[1]) / 10.0
    target_J = int(target_genome[3]) / 10.0
    target_P = int(target_genome[5]) / 10.0
    target_W = int(target_genome[7]) / 10.0
    target_pos = (target_L, target_J, target_P, target_W)

    # Analyze generated code
    result = analyze_quick(generated_code)
    actual_pos = (
        result["ljpw"]["L"],
        result["ljpw"]["J"],
        result["ljpw"]["P"],
        result["ljpw"]["W"],
    )

    # Calculate distance
    import math

    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(target_pos, actual_pos)))

    # Create actual genome
    actual_genome = f"L{int(actual_pos[0]*10)%10}J{int(actual_pos[1]*10)%10}P{int(actual_pos[2]*10)%10}W{int(actual_pos[3]*10)%10}"

    return {
        "target_genome": target_genome,
        "target_pos": target_pos,
        "actual_genome": actual_genome,
        "actual_pos": actual_pos,
        "distance": distance,
        "match": distance < 0.3,  # Close enough
        "similarity": "MATCH" if distance < 0.2 else "CLOSE" if distance < 0.4 else "DIFFERENT",
    }


# ============================================================================
# TEST CASES
# ============================================================================


def test_generator():
    print("\n" + "=" * 70)
    print("SEMANTIC CODE GENERATOR TEST")
    print("=" * 70)
    print("\nHypothesis: We can generate code at specified LJPW coordinates\n")

    test_cases = [
        {
            "name": "Minimal Code",
            "genome": "L2J2P3W2",
            "domain": "simple processing",
            "coords": (0.2, 0.2, 0.3, 0.2),
        },
        {
            "name": "Safe Code",
            "genome": "L8J6P5W5",
            "domain": "data validation",
            "coords": (0.8, 0.6, 0.5, 0.5),
        },
        {
            "name": "Structured Code",
            "genome": "L6J8P5W6",
            "domain": "api handling",
            "coords": (0.6, 0.8, 0.5, 0.6),
        },
        {
            "name": "High Performance Code",
            "genome": "L5J5P9W5",
            "domain": "data transformation",
            "coords": (0.5, 0.5, 0.9, 0.5),
        },
        {
            "name": "Well-Designed Code",
            "genome": "L6J6P6W9",
            "domain": "business logic",
            "coords": (0.6, 0.6, 0.6, 0.9),
        },
        {
            "name": "Production Code",
            "genome": "L8J8P7W8",
            "domain": "user authentication",
            "coords": (0.8, 0.8, 0.7, 0.8),
        },
    ]

    for test in test_cases:
        print("─" * 70)
        print(f"Test: {test['name']} (Target: {test['genome']})")
        print("─" * 70)

        # Generate code
        L, J, P, W = test["coords"]
        code = generate_code(L, J, P, W, test["domain"])

        print("\nGenerated Code:")
        print(code)

        # Validate
        validation = validate_generation(test["genome"], code)

        print(f"\nValidation:")
        print(f"  Target:   {validation['target_genome']} at {validation['target_pos']}")
        print(
            f"  Actual:   {validation['actual_genome']} at ({validation['actual_pos'][0]:.2f}, {validation['actual_pos'][1]:.2f}, {validation['actual_pos'][2]:.2f}, {validation['actual_pos'][3]:.2f})"
        )
        print(f"  Distance: {validation['distance']:.3f}")
        print(f"  Result:   {validation['similarity']} {'✓' if validation['match'] else '✗'}")
        print()

    print("=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print(
        """
If generated code consistently matches target genomes, this proves:

1. LJPW coordinates DETERMINE code properties (not just measure them)
2. Semantic compilation is possible (genome → code)
3. We can navigate semantic space intentionally
4. The coordinate system is bidirectional (code ↔ position)

This is the strongest possible validation of the LJPW framework.

Potential applications:
- AI-assisted coding: "Generate code at L8J8P7W8 for authentication"
- Automated refactoring: "Move this code toward L=0.9"
- Code templates: Library of archetypes at canonical positions
- Quality-driven development: Specify target genome, generate scaffold
    """
    )
    print("=" * 70 + "\n")


if __name__ == "__main__":
    test_generator()
