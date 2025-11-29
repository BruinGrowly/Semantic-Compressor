"""
LJPW Semantic Expander v1.0
The "Generative Compiler" - Third component of the LJPW Core Loop

Takes compressed LJPW genomes and expands them into:
- Actual code implementations
- Architecture documentation
- Design specifications
- Improvement recommendations

Uses semantic primitive templates to generate high-quality output
"""

import importlib.util
import math

# Load the compiler module dynamically
import os

# Import from the compressor
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

_current_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "ljpw_semantic_compiler", os.path.join(_current_dir, "ljpw_semantic_compiler.py")
)
compiler_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler_module)

SemanticPrimitive = compiler_module.SemanticPrimitive
CompressedSemanticUnit = compiler_module.CompressedSemanticUnit

# ============================================================================
# CODE GENERATION TEMPLATES
# ============================================================================


class CodeTemplate:
    """Templates for generating code from semantic primitives"""

    # Language-specific templates
    PYTHON_TEMPLATES = {
        SemanticPrimitive.SAFE_INIT: """
def __init__(self, {params}):
    '''Initialize with validated parameters'''
    # Validate inputs
    {validations}
    # Safe initialization
    {initializations}
""",
        SemanticPrimitive.ERROR_HANDLE: """
try:
    {operation}
except {exception_types} as e:
    logger.error(f"Error in {context}: {{e}}")
    {recovery_strategy}
    raise
""",
        SemanticPrimitive.VALIDATION: """
def validate_{name}(value: {type_hint}) -> bool:
    '''Validate {name} meets constraints'''
    if not isinstance(value, {type_hint}):
        raise TypeError(f"Expected {type_hint}, got {{type(value)}}")
    {constraints}
    return True
""",
        SemanticPrimitive.TYPE_DEF: """
@dataclass
class {name}:
    '''Type definition for {description}'''
    {fields}

    def __post_init__(self):
        '''Validate invariants'''
        {invariant_checks}
""",
        SemanticPrimitive.ALGORITHM: """
def {name}({params}) -> {return_type}:
    '''
    {description}

    Time complexity: O({time_complexity})
    Space complexity: O({space_complexity})
    '''
    {implementation}
    return result
""",
        SemanticPrimitive.ABSTRACTION: """
class {name}(ABC):
    '''Abstract interface for {description}'''

    @abstractmethod
    def {method_name}(self, {params}) -> {return_type}:
        '''Core operation'''
        pass

    {additional_methods}
""",
        SemanticPrimitive.PATTERN: """
# Design Pattern: {pattern_name}
class {name}:
    '''Implements {pattern_name} pattern for {purpose}'''

    {pattern_implementation}
""",
    }

    @classmethod
    def get_template(cls, primitive: SemanticPrimitive, language: str = "python") -> str:
        """Get template for a semantic primitive"""
        if language.lower() == "python":
            return cls.PYTHON_TEMPLATES.get(primitive, "# {primitive}")
        return "// Template not available"


# ============================================================================
# DOCUMENTATION TEMPLATES
# ============================================================================


class DocumentationTemplate:
    """Templates for generating documentation"""

    MARKDOWN_TEMPLATES = {
        SemanticPrimitive.SAFE_INIT: """
### Initialization Pattern

**Safety Score**: {safety_score}/1.0

This component implements safe initialization with:
- Input validation
- Defensive defaults
- Error handling

**LJPW Profile**: L={L:.2f}, J={J:.2f}, P={P:.2f}, W={W:.2f}
""",
        SemanticPrimitive.ARCHITECTURE: """
## Architectural Decision

**Component**: {component_name}
**Decision**: {decision}
**LJPW Profile**: L={L:.2f}, J={J:.2f}, P={P:.2f}, W={W:.2f}

### Rationale
{rationale}

### Trade-offs
- **Safety (L={L:.2f})**: {safety_analysis}
- **Structure (J={J:.2f})**: {structure_analysis}
- **Performance (P={P:.2f})**: {performance_analysis}
- **Maintainability (W={W:.2f})**: {maintainability_analysis}

### Recommendations
{recommendations}
""",
    }


# ============================================================================
# SEMANTIC EXPANDER
# ============================================================================


class SemanticExpander:
    """
    Expands compressed LJPW genomes into concrete artifacts

    The final step of the LJPW Core Loop:
    Compressed Genome → Generated Code/Docs/Specs
    """

    def __init__(self, target_language: str = "python"):
        self.target_language = target_language

    def expand_to_code(
        self, compressed_units: List[CompressedSemanticUnit], context: Dict[str, Any] = None
    ) -> str:
        """
        Expand compressed semantic units to actual code

        Args:
            compressed_units: Compressed LJPW genome
            context: Additional context for generation (names, types, etc.)

        Returns:
            Generated code as string
        """
        if context is None:
            context = {}

        generated_code = []
        generated_code.append(f"# Auto-generated from LJPW Semantic Genome")
        generated_code.append(f"# Total units: {len(compressed_units)}\n")

        for i, unit in enumerate(compressed_units):
            # Get template for this primitive
            template = CodeTemplate.get_template(unit.primitive, self.target_language)

            # Dequantize LJPW values
            L, J, P, W = self._dequantize_ljpw(unit.ljpw_state)

            # Generate context-specific parameters
            params = self._generate_parameters(unit, context, i)

            # Fill template
            try:
                code = template.format(**params)
                generated_code.append(f"\n# Unit {i}: {unit.primitive.value}")
                generated_code.append(f"# LJPW: L={L:.2f}, J={J:.2f}, P={P:.2f}, W={W:.2f}")
                generated_code.append(code)
            except KeyError as e:
                # Template missing parameters, generate placeholder
                generated_code.append(f"\n# TODO: Implement {unit.primitive.value}")
                generated_code.append(f"# LJPW: L={L:.2f}, J={J:.2f}, P={P:.2f}, W={W:.2f}")

        return "\n".join(generated_code)

    def expand_to_documentation(
        self, compressed_units: List[CompressedSemanticUnit], context: Dict[str, Any] = None
    ) -> str:
        """
        Expand compressed genome to documentation

        Returns:
            Markdown documentation
        """
        if context is None:
            context = {"system_name": "System"}

        docs = []
        docs.append(f"# {context.get('system_name', 'System')} Architecture")
        docs.append(f"\n**LJPW Genome Analysis**: {len(compressed_units)} semantic units\n")

        # Analyze overall system
        total_L, total_J, total_P, total_W = 0, 0, 0, 0
        primitive_counts = {}

        for unit in compressed_units:
            L, J, P, W = self._dequantize_ljpw(unit.ljpw_state)
            total_L += L
            total_J += J
            total_P += P
            total_W += W

            prim = unit.primitive
            primitive_counts[prim] = primitive_counts.get(prim, 0) + 1

        n = len(compressed_units)
        avg_L, avg_J, avg_P, avg_W = total_L / n, total_J / n, total_P / n, total_W / n

        # Overall system assessment
        docs.append("## System Profile\n")
        docs.append(f"**Average LJPW Scores**:")
        docs.append(f"- Love (Safety): {avg_L:.3f}")
        docs.append(f"- Justice (Structure): {avg_J:.3f}")
        docs.append(f"- Power (Performance): {avg_P:.3f}")
        docs.append(f"- Wisdom (Design): {avg_W:.3f}\n")

        # System health assessment
        docs.append(self._generate_health_assessment(avg_L, avg_J, avg_P, avg_W))

        # Semantic composition
        docs.append("\n## Semantic Composition\n")
        sorted_prims = sorted(primitive_counts.items(), key=lambda x: x[1], reverse=True)
        for prim, count in sorted_prims[:10]:
            pct = 100 * count / n
            docs.append(f"- **{prim.value}**: {count} units ({pct:.1f}%)")

        # Recommendations
        docs.append("\n## Recommendations\n")
        docs.append(self._generate_recommendations(avg_L, avg_J, avg_P, avg_W, primitive_counts))

        return "\n".join(docs)

    def expand_to_improvement_plan(
        self, compressed_units: List[CompressedSemanticUnit], target_ljpw: tuple = None
    ) -> str:
        """
        Generate an improvement plan to move system toward target LJPW state

        Args:
            compressed_units: Current system genome
            target_ljpw: Target (L, J, P, W) state (defaults to Natural Equilibrium)

        Returns:
            Improvement plan as markdown
        """
        if target_ljpw is None:
            # Default to Natural Equilibrium
            target_ljpw = (0.618, 0.414, 0.718, 0.693)

        target_L, target_J, target_P, target_W = target_ljpw

        # Calculate current state
        total_L, total_J, total_P, total_W = 0, 0, 0, 0
        for unit in compressed_units:
            L, J, P, W = self._dequantize_ljpw(unit.ljpw_state)
            total_L += L
            total_J += J
            total_P += P
            total_W += W

        n = len(compressed_units)
        current_L, current_J, current_P, current_W = (
            total_L / n,
            total_J / n,
            total_P / n,
            total_W / n,
        )

        plan = []
        plan.append("# LJPW Improvement Plan\n")
        plan.append("## Current State vs Target\n")
        plan.append("| Dimension | Current | Target | Gap | Priority |")
        plan.append("|-----------|---------|--------|-----|----------|")

        gaps = {
            "L": (current_L, target_L, target_L - current_L),
            "J": (current_J, target_J, target_J - current_J),
            "P": (current_P, target_P, target_P - current_P),
            "W": (current_W, target_W, target_W - current_W),
        }

        for dim, (curr, targ, gap) in gaps.items():
            priority = "HIGH" if abs(gap) > 0.15 else ("MEDIUM" if abs(gap) > 0.08 else "LOW")
            direction = "UP" if gap > 0 else ("DOWN" if gap < 0 else "OK")
            plan.append(
                f"| {dim} | {curr:.3f} | {targ:.3f} | {gap:+.3f} {direction} | {priority} |"
            )

        plan.append("\n## Recommended Actions\n")

        # Generate specific actions based on gaps
        if gaps["L"][2] > 0.1:  # Need more Love
            plan.append("### Increase Safety (Love)\n")
            plan.append("- [ ] Add error handling to critical paths")
            plan.append("- [ ] Implement input validation")
            plan.append("- [ ] Add defensive null checks")
            plan.append("- [ ] Increase test coverage\n")

        if gaps["J"][2] > 0.1:  # Need more Justice
            plan.append("### Improve Structure (Justice)\n")
            plan.append("- [ ] Define clear interfaces")
            plan.append("- [ ] Add type annotations")
            plan.append("- [ ] Enforce coding standards")
            plan.append("- [ ] Document contracts\n")

        if gaps["P"][2] < -0.1:  # Too much Power, need to reduce
            plan.append("### Optimize Performance (Power)\n")
            plan.append("- [ ] Profile and identify bottlenecks")
            plan.append("- [ ] Add caching where appropriate")
            plan.append("- [ ] Consider async operations")
            plan.append("- [ ] Review algorithmic complexity\n")

        if gaps["W"][2] > 0.1:  # Need more Wisdom
            plan.append("### Enhance Design (Wisdom)\n")
            plan.append("- [ ] Refactor into smaller modules")
            plan.append("- [ ] Apply design patterns")
            plan.append("- [ ] Improve abstraction layers")
            plan.append("- [ ] Add architectural documentation\n")

        # Calculate estimated effort
        total_gap = sum(abs(gap) for _, _, gap in gaps.values())
        effort_days = int(total_gap * 10)  # Rough estimate

        plan.append(f"\n## Estimated Effort\n")
        plan.append(f"**Total improvement gap**: {total_gap:.3f}")
        plan.append(f"**Estimated effort**: {effort_days} person-days")
        plan.append(
            f"**Expected improvement**: {100*total_gap/(4*0.3):.1f}% movement toward optimal"
        )

        return "\n".join(plan)

    def _dequantize_ljpw(self, state: tuple) -> tuple:
        """Convert quantized LJPW levels back to continuous values"""
        L_q, J_q, P_q, W_q = state

        # Dequantize (0-3 levels → 0-1.5 range)
        def dequant(level):
            # Midpoint of quantization bin
            normalized = (level + 0.5) / 4
            return normalized * 1.5

        return (dequant(L_q), dequant(J_q), dequant(P_q), dequant(W_q))

    def _generate_parameters(
        self, unit: CompressedSemanticUnit, context: Dict, index: int
    ) -> Dict[str, str]:
        """Generate parameters for code template"""
        L, J, P, W = self._dequantize_ljpw(unit.ljpw_state)

        # Generic parameters
        params = {
            "name": context.get("name", f"component_{index}"),
            "description": context.get("description", f"Component {index}"),
            "primitive": unit.primitive.value,
            "L": L,
            "J": J,
            "P": P,
            "W": W,
            "params": "self, *args, **kwargs",
            "type_hint": "Any",
            "return_type": "None",
            "fields": "    pass",
            "implementation": "    pass",
            "validations": "    pass",
            "initializations": "    pass",
            "constraints": "    pass",
            "invariant_checks": "    pass",
            "operation": "    pass",
            "exception_types": "Exception",
            "recovery_strategy": "    pass",
            "context": "operation",
            "method_name": "execute",
            "additional_methods": "    pass",
            "pattern_name": "Unknown",
            "purpose": "system operation",
            "pattern_implementation": "    pass",
            "time_complexity": "n",
            "space_complexity": "n",
        }

        return params

    def _generate_health_assessment(self, L: float, J: float, P: float, W: float) -> str:
        """Generate health assessment text"""
        assessment = ["## Health Assessment\n"]

        # Calculate distance from Natural Equilibrium
        NE = (0.618, 0.414, 0.718, 0.693)
        distance = math.sqrt(
            (NE[0] - L) ** 2 + (NE[1] - J) ** 2 + (NE[2] - P) ** 2 + (NE[3] - W) ** 2
        )

        if distance < 0.2:
            health = "EXCELLENT"
            assessment.append("[OK] System is near optimal equilibrium")
        elif distance < 0.4:
            health = "GOOD"
            assessment.append("[->] System is functional with room for improvement")
        elif distance < 0.6:
            health = "FAIR"
            assessment.append("[!] System has notable imbalances")
        else:
            health = "POOR"
            assessment.append("[X] System requires significant improvement")

        assessment.append(f"\n**Overall Health**: {health}")
        assessment.append(f"**Distance from Natural Equilibrium**: {distance:.3f}")

        return "\n".join(assessment)

    def _generate_recommendations(
        self, L: float, J: float, P: float, W: float, primitive_counts: Dict
    ) -> str:
        """Generate specific recommendations"""
        recs = []

        # Check for imbalances
        if L < 0.5:
            recs.append("- **CRITICAL**: Increase safety measures (error handling, validation)")
        if J < 0.4:
            recs.append("- **HIGH**: Improve structural consistency (types, interfaces, contracts)")
        if P > 0.8 and W < 0.6:
            recs.append("- **WARNING**: High power without wisdom - risk of technical debt")
        if W < 0.5:
            recs.append(
                "- **MEDIUM**: Enhance design quality (refactoring, patterns, documentation)"
            )

        # Check primitive distribution
        total = sum(primitive_counts.values())
        safe_prims = sum(
            count
            for prim, count in primitive_counts.items()
            if prim
            in [
                SemanticPrimitive.SAFE_INIT,
                SemanticPrimitive.ERROR_HANDLE,
                SemanticPrimitive.VALIDATION,
            ]
        )

        if safe_prims / total < 0.3:
            recs.append("- **SAFETY**: Low proportion of safety primitives - add defensive code")

        if not recs:
            recs.append("- System appears well-balanced. Continue maintaining quality.")

        return "\n".join(recs)


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LJPW SEMANTIC EXPANDER v1.0")
    print("Generative Compiler - Expanding Compressed Genomes")
    print("=" * 70)

    # Create sample compressed genome
    print("\n1. CREATING SAMPLE COMPRESSED GENOME")
    print("-" * 70)

    sample_genome = [
        CompressedSemanticUnit(SemanticPrimitive.SAFE_INIT, (3, 2, 1, 2)),
        CompressedSemanticUnit(SemanticPrimitive.TYPE_DEF, (2, 3, 1, 2)),
        CompressedSemanticUnit(SemanticPrimitive.VALIDATION, (3, 2, 1, 2)),
        CompressedSemanticUnit(SemanticPrimitive.ALGORITHM, (2, 2, 3, 2)),
        CompressedSemanticUnit(SemanticPrimitive.ERROR_HANDLE, (3, 2, 0, 2)),
        CompressedSemanticUnit(SemanticPrimitive.ABSTRACTION, (2, 2, 1, 3)),
    ]

    print(f"Sample genome: {len(sample_genome)} semantic units")
    for i, unit in enumerate(sample_genome):
        print(f"  Unit {i}: {unit.primitive.value} - LJPW{unit.ljpw_state}")

    # Expand to code
    print("\n2. EXPANDING TO CODE")
    print("-" * 70)

    expander = SemanticExpander(target_language="python")
    generated_code = expander.expand_to_code(sample_genome, context={"name": "DataProcessor"})

    print(generated_code[:500])
    print("\n... (truncated)")
    print(f"\nTotal generated code: {len(generated_code)} characters")

    # Expand to documentation
    print("\n3. EXPANDING TO DOCUMENTATION")
    print("-" * 70)

    documentation = expander.expand_to_documentation(
        sample_genome, context={"system_name": "Data Processing Module"}
    )

    print(documentation)

    # Generate improvement plan
    print("\n4. GENERATING IMPROVEMENT PLAN")
    print("-" * 70)

    improvement_plan = expander.expand_to_improvement_plan(sample_genome)
    print(improvement_plan)

    print("\n" + "=" * 70)
    print("EXPANSION SUCCESSFUL")
    print("=" * 70)
    print("\nThe Expander can generate:")
    print("  [OK] Code implementations")
    print("  [OK] Architecture documentation")
    print("  [OK] Improvement plans")
    print("  [OK] Health assessments")
