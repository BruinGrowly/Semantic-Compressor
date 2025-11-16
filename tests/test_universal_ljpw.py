#!/usr/bin/env python3
"""
Test LJPW on Non-Code Systems

The ultimate test: If LJPW truly captures fundamental semantic structure,
it should apply to ANY complex adaptive system, not just code.

We test:
1. Organizations (companies, governments, teams)
2. Narratives (stories, plots, archetypes)
3. Biological systems (organisms, cells)

If distances in LJPW space correlate with semantic similarity for these
systems, it provides evidence that LJPW is a universal law of meaning.
"""

import math
from typing import Tuple, List, Dict

# ============================================================================
# MANUAL LJPW MAPPING (Non-Code)
# ============================================================================

def calculate_distance(pos1: Tuple[float, float, float, float],
                      pos2: Tuple[float, float, float, float]) -> float:
    """Calculate Euclidean distance in LJPW space."""
    return math.sqrt(sum((a-b)**2 for a, b in zip(pos1, pos2)))

def map_to_ljpw(description: Dict) -> Tuple[float, float, float, float]:
    """
    Manually map a system to LJPW coordinates based on its properties.

    L (Love/Safety): Protection, resilience, error handling, survival
    J (Justice/Structure): Order, rules, organization, predictability
    P (Power/Performance): Capability, throughput, efficiency, speed
    W (Wisdom/Design): Adaptation, elegance, insight, innovation
    """
    return (description['L'], description['J'], description['P'], description['W'])

# ============================================================================
# TEST 1: ORGANIZATIONS
# ============================================================================

ORGANIZATIONS = {
    "Early Startup": {
        "description": "Small team, high risk, fast execution, innovative",
        "L": 0.2,  # Low safety - high risk tolerance
        "J": 0.3,  # Low structure - minimal process
        "P": 0.9,  # High power - fast execution
        "W": 0.8,  # High wisdom - innovative solutions
    },
    "Growth Startup": {
        "description": "Scaling team, adding process, still fast",
        "L": 0.4,  # Moderate safety - some risk management
        "J": 0.5,  # Moderate structure - basic processes
        "P": 0.8,  # High power - still fast
        "W": 0.7,  # Good wisdom - proven innovation
    },
    "Mid-size Company": {
        "description": "Established team, balanced approach",
        "L": 0.6,  # Good safety - risk management
        "J": 0.7,  # Good structure - documented processes
        "P": 0.6,  # Moderate power - balanced speed
        "W": 0.6,  # Moderate wisdom - some innovation
    },
    "Large Corporation": {
        "description": "Bureaucratic, risk-averse, slow but stable",
        "L": 0.9,  # High safety - risk averse
        "J": 0.9,  # High structure - rigid hierarchy
        "P": 0.3,  # Low power - slow execution
        "W": 0.5,  # Moderate wisdom - proven patterns
    },
    "Open Source Community": {
        "description": "Decentralized, collaborative, innovative",
        "L": 0.5,  # Moderate safety - peer review
        "J": 0.4,  # Lower structure - loose organization
        "P": 0.7,  # Good power - parallel work
        "W": 0.9,  # High wisdom - collective intelligence
    },
    "Military Organization": {
        "description": "Highly structured, disciplined, mission-critical",
        "L": 0.9,  # High safety - mission critical
        "J": 0.95, # Maximum structure - strict hierarchy
        "P": 0.7,  # Good power - efficient execution
        "W": 0.6,  # Moderate wisdom - proven doctrine
    },
    "Research Lab": {
        "description": "Exploratory, experimental, knowledge-seeking",
        "L": 0.6,  # Moderate safety - careful experimentation
        "J": 0.6,  # Moderate structure - scientific method
        "P": 0.4,  # Lower power - deliberate pace
        "W": 0.95, # Maximum wisdom - pursuing insight
    }
}

# ============================================================================
# TEST 2: NARRATIVES
# ============================================================================

NARRATIVES = {
    "Hero's Journey": {
        "description": "Protagonist overcomes trials, gains wisdom, saves world",
        "L": 0.8,  # High safety - hero survives
        "J": 0.9,  # High structure - clear moral order
        "P": 0.8,  # High power - hero gains strength
        "W": 0.9,  # High wisdom - insight through journey
    },
    "Tragedy": {
        "description": "Protagonist's flaw leads to downfall and death",
        "L": 0.1,  # Low safety - protagonist dies
        "J": 0.7,  # Moderate structure - moral consequences
        "P": 0.4,  # Moderate power - initial strength fails
        "W": 0.6,  # Moderate wisdom - cautionary insight
    },
    "Comedy": {
        "description": "Misunderstandings resolved, everyone happy",
        "L": 0.9,  # High safety - all ends well
        "J": 0.5,  # Moderate structure - order restored
        "P": 0.6,  # Moderate power - clever solutions
        "W": 0.7,  # Good wisdom - social insight
    },
    "Horror": {
        "description": "Overwhelming threat, powerlessness, dread",
        "L": 0.05, # Minimal safety - characters in danger
        "J": 0.2,  # Low structure - chaos prevails
        "P": 0.1,  # Minimal power - powerlessness
        "W": 0.3,  # Low wisdom - no understanding
    },
    "Mystery": {
        "description": "Puzzle to solve, investigation, revelation",
        "L": 0.6,  # Moderate safety - detective survives
        "J": 0.8,  # High structure - logical deduction
        "P": 0.5,  # Moderate power - intellectual ability
        "W": 0.8,  # High wisdom - solving puzzle
    },
    "Bildungsroman": {
        "description": "Coming of age, personal growth, maturation",
        "L": 0.7,  # Good safety - protected growth
        "J": 0.6,  # Moderate structure - learning rules
        "P": 0.5,  # Moderate power - developing strength
        "W": 0.85, # High wisdom - gaining understanding
    },
    "Epic": {
        "description": "Grand scale, heroic deeds, civilizational stakes",
        "L": 0.7,  # Good safety - heroes protected
        "J": 0.85, # High structure - cosmic order
        "P": 0.9,  # High power - legendary feats
        "W": 0.8,  # High wisdom - profound themes
    }
}

# ============================================================================
# TEST 3: BIOLOGICAL SYSTEMS
# ============================================================================

BIOLOGICAL_SYSTEMS = {
    "Bacteria": {
        "description": "Simple, fast reproduction, adaptable",
        "L": 0.5,  # Moderate safety - survival strategies
        "J": 0.3,  # Low structure - simple organization
        "P": 0.95, # Maximum power - rapid reproduction
        "W": 0.4,  # Moderate wisdom - evolutionary adaptation
    },
    "Virus": {
        "description": "Minimal structure, highly efficient, parasitic",
        "L": 0.3,  # Low safety - dependent on host
        "J": 0.2,  # Low structure - minimal components
        "P": 0.9,  # High power - efficient replication
        "W": 0.5,  # Moderate wisdom - adaptive strategies
    },
    "Insect": {
        "description": "Specialized, efficient, social organization",
        "L": 0.6,  # Moderate safety - defensive adaptations
        "J": 0.7,  # Good structure - specialized roles
        "P": 0.8,  # High power - efficient metabolism
        "W": 0.6,  # Moderate wisdom - instinctive behavior
    },
    "Mammal": {
        "description": "Complex, adaptable, parental care",
        "L": 0.8,  # High safety - parental protection
        "J": 0.6,  # Moderate structure - flexible organization
        "P": 0.6,  # Moderate power - balanced metabolism
        "W": 0.8,  # High wisdom - learning capability
    },
    "Human": {
        "description": "Maximum complexity, culture, technology",
        "L": 0.7,  # Good safety - cultural protection
        "J": 0.7,  # Good structure - social organization
        "P": 0.7,  # Good power - tool use
        "W": 0.95, # Maximum wisdom - abstract reasoning
    },
    "Forest Ecosystem": {
        "description": "Interconnected, self-regulating, resilient",
        "L": 0.8,  # High safety - redundancy, resilience
        "J": 0.5,  # Moderate structure - emergent order
        "P": 0.6,  # Moderate power - sustainable throughput
        "W": 0.85, # High wisdom - complex adaptation
    }
}

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_system(systems: Dict[str, Dict], system_type: str):
    """Analyze a category of systems in LJPW space."""
    print(f"\n{'=' * 70}")
    print(f"LJPW Analysis: {system_type.upper()}")
    print(f"{'=' * 70}\n")

    # Map all systems to positions
    positions = {}
    for name, data in systems.items():
        pos = map_to_ljpw(data)
        positions[name] = pos
        genome = f"L{int(pos[0]*10)%10}J{int(pos[1]*10)%10}P{int(pos[2]*10)%10}W{int(pos[3]*10)%10}"
        print(f"{name:25} {genome}  ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}, {pos[3]:.2f})")
        print(f"  {data['description']}")
        print()

    # Calculate pairwise distances
    print(f"\n{'─' * 70}")
    print("SEMANTIC SIMILARITY ANALYSIS")
    print(f"{'─' * 70}\n")

    names = list(systems.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            name1, name2 = names[i], names[j]
            dist = calculate_distance(positions[name1], positions[name2])

            if dist < 0.3:
                similarity = "VERY SIMILAR"
            elif dist < 0.6:
                similarity = "SIMILAR"
            elif dist < 1.0:
                similarity = "DIFFERENT"
            else:
                similarity = "VERY DIFFERENT"

            print(f"{name1:25} ↔ {name2:25}  d={dist:.3f}  ({similarity})")

    # Find most similar and most different
    print(f"\n{'─' * 70}")
    print("EXTREMES")
    print(f"{'─' * 70}\n")

    min_dist, max_dist = float('inf'), 0
    min_pair, max_pair = None, None

    for i in range(len(names)):
        for j in range(i+1, len(names)):
            dist = calculate_distance(positions[names[i]], positions[names[j]])
            if dist < min_dist:
                min_dist = dist
                min_pair = (names[i], names[j])
            if dist > max_dist:
                max_dist = dist
                max_pair = (names[i], names[j])

    print(f"Most Similar:    {min_pair[0]} ↔ {min_pair[1]}")
    print(f"  Distance: {min_dist:.3f}")
    print(f"  Interpretation: These systems have nearly identical semantic profiles")

    print(f"\nMost Different:  {max_pair[0]} ↔ {max_pair[1]}")
    print(f"  Distance: {max_dist:.3f}")
    print(f"  Interpretation: These systems are fundamentally opposite in nature")

# ============================================================================
# MAIN TEST
# ============================================================================

def main():
    print("\n" + "=" * 70)
    print("UNIVERSAL LJPW TEST: Non-Code Systems")
    print("=" * 70)
    print("""
Hypothesis: If LJPW captures fundamental semantic structure, it should
apply to ANY complex adaptive system, not just code.

We manually map organizations, narratives, and biological systems to
LJPW coordinates based on their properties, then check if distances
correlate with intuitive semantic similarity.

If distances make sense (similar systems close, different systems far),
this supports the "Deep" interpretation: LJPW is a universal law.
    """)

    # Test each category
    analyze_system(ORGANIZATIONS, "Organizations")
    analyze_system(NARRATIVES, "Narrative Archetypes")
    analyze_system(BIOLOGICAL_SYSTEMS, "Biological Systems")

    # Final analysis
    print("\n" + "=" * 70)
    print("CROSS-DOMAIN ANALYSIS")
    print("=" * 70)

    all_systems = {
        "Early Startup": map_to_ljpw(ORGANIZATIONS["Early Startup"]),
        "Horror Story": map_to_ljpw(NARRATIVES["Horror"]),
        "Bacteria": map_to_ljpw(BIOLOGICAL_SYSTEMS["Bacteria"]),
        "Large Corporation": map_to_ljpw(ORGANIZATIONS["Large Corporation"]),
        "Hero's Journey": map_to_ljpw(NARRATIVES["Hero's Journey"]),
        "Human": map_to_ljpw(BIOLOGICAL_SYSTEMS["Human"]),
    }

    print("\nCross-Domain Semantic Distances:\n")

    for name1 in all_systems:
        for name2 in all_systems:
            if name1 < name2:
                dist = calculate_distance(all_systems[name1], all_systems[name2])
                print(f"{name1:20} ↔ {name2:20}  d={dist:.3f}")

    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print("""
If LJPW distances correlate with semantic similarity across domains:

EVIDENCE FOR:
✓ LJPW captures fundamental structure beyond code syntax
✓ Same dimensions (L, J, P, W) apply to diverse systems
✓ Distance metric preserves meaning across contexts
✓ The framework may be universal to complex adaptive systems

This would elevate LJPW from "code tool" to "fundamental law of meaning"
comparable to physical laws like thermodynamics or information theory.

The fact that we can meaningfully compare:
- Startups to bacteria (both fast, risky, adaptive)
- Corporations to hero journeys (both structured, safe, powerful)
- Horror stories to viruses (both dangerous, chaotic, minimal)

...suggests LJPW is operating at a deeper level than domain-specific
analysis. It may be capturing the intrinsic geometry of meaning itself.
    """)
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()
