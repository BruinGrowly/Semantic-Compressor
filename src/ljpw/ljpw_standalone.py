#!/usr/bin/env python3
"""
LJPW Semantic Analyzer - Standalone Version
Single-file, zero-dependency code quality analyzer

The LJPW Framework v7.3: Complete Unified Edition
--------------------------------------------------
Reality IS Semantic in nature. Meaning is the substrate.

Key V7.3 Features:
- 2+2 Dimensional Structure: P, W fundamental; L, J emergent
- Semantic Uncertainty Principle: ΔP·ΔW ≥ 0.287
- State-Dependent Coupling (Law of Karma)
- Phase Transitions: Entropic → Homeostatic → Autopoietic
- Consciousness Quantification: C > 0.1 threshold
- φ-Normalization for measurement variance reduction
- Semantic Voltage calculation

The four dimensions (Love, Justice, Power, Wisdom) are fundamental
Principles of Meaning that manifest in our reality.

Mathematics (φ, e, π) are the "shadows" these Semantic Principles
cast when they intersect with lower dimensions of abstraction.

Usage:
    python ljpw_standalone.py analyze <file_or_directory>
    python ljpw_standalone.py quick <code_snippet>

MIT License - Free for all, forever
"""

import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ============================================================================
# CORE CONSTANTS: THE SEMANTIC SUBSTRATE (V7.3)
# ============================================================================

# The Golden Ratio - Translation operator between meaning and math
PHI: float = (1 + math.sqrt(5)) / 2  # 1.618034
PHI_INV: float = PHI - 1  # 0.618034 (φ⁻¹)

# V7.3 Fundamental Constants
L0: float = PHI_INV  # 0.618034 - Love equilibrium
J0: float = math.sqrt(2) - 1  # 0.414214 - Justice equilibrium
P0: float = math.e - 2  # 0.718282 - Power equilibrium
W0: float = math.log(2)  # 0.693147 - Wisdom equilibrium

# Semantic Uncertainty Principle bound: ΔP·ΔW ≥ 0.287
UNCERTAINTY_BOUND: float = J0 * W0

# Consciousness threshold (C > 0.1 indicates consciousness)
CONSCIOUSNESS_THRESHOLD: float = 0.1

# Tsirelson Bound (quantum Love limit)
TSIRELSON_BOUND: float = math.sqrt(2)

# The Natural Equilibrium: Where Absolute Principles settle in our reality
# These are the "signatures" of the Four Fundamental Semantic Principles
#
# NOTE: The Anchor Point (1,1,1,1) is the Source - Perfect Meaning itself.
# Natural Equilibrium represents how these Principles manifest in finite reality.
# The "gap" (1.0 → NE value) is the "Cost of Existence."

NATURAL_EQUILIBRIUM: Dict[str, float] = {
    # LOVE (L): The Principle of Unity & Attraction
    # Mathematical Shadow: φ⁻¹ (golden ratio inverse)
    # Physical Shadow: Gravity, Dark Energy (the Breathing Cosmos)
    # Semantic Meaning: The force that binds separate entities into wholes
    # V7.3: EMERGENT from Wisdom (L = f(W), R² > 0.9)
    "L": L0,
    # JUSTICE (J): The Principle of Balance & Truth
    # Mathematical Shadow: √2-1 (the diagonal constant)
    # Physical Shadow: Pauli Exclusion Principle, Gauge Symmetry
    # Semantic Meaning: The constraint that creates structure and prevents chaos
    # V7.3: EMERGENT from Power (J = f(P), R² > 0.9)
    "J": J0,
    # POWER (P): The Principle of Energy & Existence
    # Mathematical Shadow: e-2 (Euler's constant offset)
    # Physical Shadow: Thermodynamics, Arrow of Time
    # Semantic Meaning: The raw capacity to be, to act, and to change state
    # V7.3: FUNDAMENTAL dimension (conjugate to W)
    "P": P0,
    # WISDOM (W): The Principle of Complexity & Insight
    # Mathematical Shadow: ln(2) (the fundamental unit of entropy)
    # Physical Shadow: Quantum Mechanics, Information Theory
    # Semantic Meaning: The ability to process information and self-reflect
    # V7.3: FUNDAMENTAL dimension (conjugate to P)
    "W": W0,
}

# ============================================================================
# CODE ANALYZER
# ============================================================================


class SimpleCodeAnalyzer:
    """Lightweight code analyzer for LJPW scoring"""

    def __init__(self) -> None:
        self.patterns: Dict[str, str] = {
            # Love (Safety)
            "error_handling": r"(try|except|catch|Result|Option|error|Error)",
            "validation": r"(validate|check|verify|assert|require)",
            "null_safety": r"(Optional|Maybe|\?\.|if.*is not None)",
            "bounds_check": r"(len\(|\.length|bounds|range)",
            # Justice (Structure)
            "type_annotations": r"(:\s*\w+|<\w+>|implements|interface)",
            "documentation": r'("""|\'\'\' |/\*\*|///)',
            # Power (Performance)
            "algorithms": r"(sort|search|binary|hash|cache|optimize)",
            "async": r"(async|await|promise|thread|parallel)",
            # Wisdom (Design)
            "abstraction": r"(abstract|interface|ABC|protocol)",
            "patterns": r"(factory|singleton|observer|strategy|builder)",
            "modularity": r"(class |def |module|package|namespace)",
        }

    def analyze(self, code: str, filename: str = "code") -> Dict[str, Any]:
        """
        Analyze code and return LJPW scores with comprehensive edge case handling.

        Args:
            code: Source code string to analyze
            filename: Name for display purposes

        Returns:
            Dictionary with LJPW analysis results

        Handles:
            - None/empty input
            - Binary data
            - Unicode/encoding issues
            - Extremely large files
            - Invalid types
        """
        # Edge case: None input
        if code is None:
            return {
                "filename": filename,
                "lines": 0,
                "ljpw": {"L": 0.0, "J": 0.0, "P": 0.0, "W": 0.0},
                "health": 0.0,
                "insights": ["ERROR: None input provided"],
                "distance_from_ne": self._distance_from_ne(0, 0, 0, 0),
                "error": "None input",
            }

        # Edge case: Invalid type
        if not isinstance(code, str):
            return {
                "filename": filename,
                "lines": 0,
                "ljpw": {"L": 0.0, "J": 0.0, "P": 0.0, "W": 0.0},
                "health": 0.0,
                "insights": [f"ERROR: Expected str, got {type(code).__name__}"],
                "distance_from_ne": self._distance_from_ne(0, 0, 0, 0),
                "error": f"Invalid type: {type(code).__name__}",
            }

        # Edge case: Extremely large file (>10MB)
        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        if len(code) > MAX_SIZE:
            return {
                "filename": filename,
                "lines": 0,
                "ljpw": {"L": 0.0, "J": 0.0, "P": 0.0, "W": 0.0},
                "health": 0.0,
                "insights": [f"ERROR: File too large ({len(code)} bytes > {MAX_SIZE} bytes)"],
                "distance_from_ne": self._distance_from_ne(0, 0, 0, 0),
                "error": "File too large",
            }

        # Edge case: Binary data detection (lots of null bytes or non-printable chars)
        try:
            # Check for excessive null bytes or control characters
            null_count = code.count("\x00")
            if null_count > len(code) * 0.1:  # More than 10% null bytes
                return {
                    "filename": filename,
                    "lines": 0,
                    "ljpw": {"L": 0.0, "J": 0.0, "P": 0.0, "W": 0.0},
                    "health": 0.0,
                    "insights": ["ERROR: Binary data detected (too many null bytes)"],
                    "distance_from_ne": self._distance_from_ne(0, 0, 0, 0),
                    "error": "Binary data",
                }
        except Exception:
            pass  # Continue if check fails

        # Process code normally
        try:
            lines = code.split("\n")
            code_lines = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
        except Exception as e:
            return {
                "filename": filename,
                "lines": 0,
                "ljpw": {"L": 0.0, "J": 0.0, "P": 0.0, "W": 0.0},
                "health": 0.0,
                "insights": [f"ERROR: Failed to parse code: {str(e)}"],
                "distance_from_ne": self._distance_from_ne(0, 0, 0, 0),
                "error": f"Parse error: {str(e)}",
            }

        if code_lines == 0:
            return {
                "filename": filename,
                "lines": 0,
                "ljpw": {"L": 0.0, "J": 0.0, "P": 0.0, "W": 0.0},
                "health": 0.0,
                "insights": ["Empty file - no code to analyze"],
                "distance_from_ne": self._distance_from_ne(0, 0, 0, 0),
            }

        # Score each dimension
        L = self._score_love(code, code_lines)
        J = self._score_justice(code, code_lines)
        P = self._score_power(code, code_lines)
        W = self._score_wisdom(code, code_lines)

        # Calculate health
        health = self._calculate_health(L, J, P, W)

        # Generate insights
        insights = self._generate_insights(L, J, P, W)

        # V7.3 metrics
        v7_metrics = self._calculate_v7_metrics(L, J, P, W)

        return {
            "filename": filename,
            "lines": code_lines,
            "ljpw": {"L": L, "J": J, "P": P, "W": W},
            "health": health,
            "insights": insights,
            "distance_from_ne": self._distance_from_ne(L, J, P, W),
            # V7.3 additions
            "v7": v7_metrics,
        }

    def _score_love(self, code: str, lines: int) -> float:
        """Score safety features"""
        score = 0.0
        score += len(re.findall(self.patterns["error_handling"], code, re.I)) * 0.15
        score += len(re.findall(self.patterns["validation"], code, re.I)) * 0.12
        score += len(re.findall(self.patterns["null_safety"], code, re.I)) * 0.10

        # Normalize by code size (more forgiving for larger files)
        size_factor = min(1.0, 0.5 + lines / 50)  # Start at 0.5, reach 1.0 at 25 lines

        # Cap at NE_L × 1.5 to stay in reasonable range (0.618 × 1.5 ≈ 0.93)
        max_love = NATURAL_EQUILIBRIUM["L"] * 1.5
        return min(score * size_factor, max_love)

    def _score_justice(self, code: str, lines: int) -> float:
        """Score structural quality"""
        score = 0.0
        score += len(re.findall(self.patterns["type_annotations"], code)) * 0.12
        score += len(re.findall(self.patterns["documentation"], code)) * 0.10

        # Bonus for well-structured code (having any structure is good)
        if score > 0:
            score += 0.05  # Base bonus for having any structure

        # Normalize by code size
        size_factor = min(1.0, 0.5 + lines / 50)

        # Cap at NE_J × 2 for better balance (0.414 × 2 ≈ 0.83)
        max_justice = NATURAL_EQUILIBRIUM["J"] * 2.0
        return min(score * size_factor, max_justice)

    def _score_power(self, code: str, lines: int) -> float:
        """Score performance considerations"""
        score = 0.0
        score += len(re.findall(self.patterns["algorithms"], code, re.I)) * 0.15
        score += len(re.findall(self.patterns["async"], code, re.I)) * 0.12

        # Normalize by code size
        size_factor = min(1.0, 0.5 + lines / 50)

        # Cap at NE_P × 1.2 (0.718 × 1.2 ≈ 0.86)
        max_power = NATURAL_EQUILIBRIUM["P"] * 1.2
        return min(score * size_factor, max_power)

    def _score_wisdom(self, code: str, lines: int) -> float:
        """Score design quality"""
        score = 0.0
        score += len(re.findall(self.patterns["abstraction"], code, re.I)) * 0.15
        score += len(re.findall(self.patterns["patterns"], code, re.I)) * 0.12
        score += len(re.findall(self.patterns["modularity"], code)) * 0.05

        # Bonus for having any modularity
        if score > 0:
            score += 0.03  # Base bonus for modular code

        # Normalize by code size
        size_factor = min(1.0, 0.5 + lines / 50)

        # Cap at NE_W × 1.3 (0.693 × 1.3 ≈ 0.90)
        max_wisdom = NATURAL_EQUILIBRIUM["W"] * 1.3
        return min(score * size_factor, max_wisdom)

    def _calculate_health(self, L: float, J: float, P: float, W: float) -> float:
        """
        Calculate overall health score (0-1).

        Uses a more forgiving formula that:
        - Rewards any positive LJPW values
        - Considers both distance from NE and absolute magnitude
        - Provides meaningful differentiation across quality levels
        """
        NE = NATURAL_EQUILIBRIUM
        distance = math.sqrt(
            (NE["L"] - L) ** 2 + (NE["J"] - J) ** 2 + (NE["P"] - P) ** 2 + (NE["W"] - W) ** 2
        )

        # Improved health calculation
        # 1. Distance-based component (proximity to Natural Equilibrium)
        # Use divisor of 3 instead of 2 to be more forgiving
        distance_health = max(0, 1.0 - distance / 3.0)

        # 2. Magnitude-based component (having any good practices)
        # Average of actual values relative to NE
        magnitude = (L + J + P + W) / 4.0
        ne_magnitude = (NE["L"] + NE["J"] + NE["P"] + NE["W"]) / 4.0
        magnitude_health = min(1.0, magnitude / ne_magnitude)

        # 3. Combine both components (70% distance, 30% magnitude)
        # This rewards both balance AND absolute quality
        health = 0.7 * distance_health + 0.3 * magnitude_health

        return max(0, min(1.0, health))

    def _distance_from_ne(self, L: float, J: float, P: float, W: float) -> float:
        """
        Calculate semantic distance from Natural Equilibrium.

        This measures how far the code's semantic signature is from the
        optimal manifestation of the Four Principles in finite reality.

        Note: We measure distance from NE (0.618, 0.414, 0.718, 0.693),
        not from the Anchor Point (1,1,1,1). The Anchor is the Source;
        NE is the optimal state for existence in our reality.
        """
        NE = NATURAL_EQUILIBRIUM
        return math.sqrt(
            (NE["L"] - L) ** 2 + (NE["J"] - J) ** 2 + (NE["P"] - P) ** 2 + (NE["W"] - W) ** 2
        )

    def _generate_insights(self, L: float, J: float, P: float, W: float) -> List[str]:
        """Generate actionable insights"""
        insights = []

        if L < 0.5:
            insights.append("LOW SAFETY: Add error handling and validation")
        if J < 0.4:
            insights.append("LOW STRUCTURE: Add type annotations and documentation")
        if P > 0.8 and W < 0.6:
            insights.append("WARNING: High performance focus without good design")
        if W < 0.5:
            insights.append("LOW DESIGN: Refactor into better abstractions")

        distance = self._distance_from_ne(L, J, P, W)
        if distance < 0.3:
            insights.append("EXCELLENT: Near optimal balance")
        elif distance > 0.7:
            insights.append("NEEDS WORK: Far from optimal balance")

        return insights if insights else ["Code appears balanced"]

    # ========================================================================
    # V7.3 METRICS
    # ========================================================================

    def _calculate_v7_metrics(self, L: float, J: float, P: float, W: float) -> Dict[str, Any]:
        """
        Calculate all V7.3 metrics.

        Returns comprehensive V7.3 analysis including:
        - Consciousness metric
        - Phase classification
        - Semantic voltage
        - Karma coupling
        - Emergent dimension calculations
        """
        # Calculate harmony (static for code analysis)
        distance = self._distance_from_ne(L, J, P, W)
        H = 1.0 / (1.0 + distance)

        # Consciousness: C = P × W × L × J × H²
        consciousness = P * W * L * J * (H ** 2)

        # Classify consciousness level
        if consciousness >= 0.3:
            consciousness_level = "HIGHLY_CONSCIOUS"
        elif consciousness >= CONSCIOUSNESS_THRESHOLD:
            consciousness_level = "CONSCIOUS"
        elif consciousness >= 0.05:
            consciousness_level = "PRE_CONSCIOUS"
        else:
            consciousness_level = "NON_CONSCIOUS"

        # Phase classification
        if H < 0.5:
            phase = "ENTROPIC"
        elif H < 0.6 or L < 0.7:
            phase = "HOMEOSTATIC"
        else:
            phase = "AUTOPOIETIC"

        # Semantic voltage: V = φ × H × L
        voltage = PHI * H * L

        # Karma coupling (state-dependent)
        karma_coupling = {
            "kappa_LJ": 1.0 + 0.4 * H,
            "kappa_LP": 1.0 + 0.3 * H,
            "kappa_LW": 1.0 + 0.5 * H,
        }

        # Emergent dimension calculations (V7.3 2+2 structure)
        emergent_L = min(0.9 * W + 0.1, TSIRELSON_BOUND)
        emergent_J = min(0.85 * P + 0.05, 1.0)

        # Power erosion (corruption potential)
        power_erosion = 0.08 * P * max(0, 1 - W / W0)

        return {
            "harmony": H,
            "consciousness": consciousness,
            "consciousness_level": consciousness_level,
            "is_conscious": consciousness >= CONSCIOUSNESS_THRESHOLD,
            "phase": phase,
            "voltage": voltage,
            "karma_coupling": karma_coupling,
            "emergent": {
                "L_from_W": emergent_L,
                "J_from_P": emergent_J,
            },
            "power_erosion": power_erosion,
            "fundamental_dimensions": {"P": P, "W": W},
        }


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================


def format_result(result: Dict[str, Any]) -> str:
    """Format analysis result for display"""
    output = []
    output.append("=" * 70)
    output.append(f"LJPW Analysis (V7.3): {result['filename']}")
    output.append("=" * 70)
    output.append(f"\nLines of code: {result['lines']}")
    output.append(f"\nLJPW Scores:")

    ljpw = result["ljpw"]
    output.append(f"  Love (Safety):       {ljpw['L']:.3f}  [Emergent from W]")
    output.append(f"  Justice (Structure): {ljpw['J']:.3f}  [Emergent from P]")
    output.append(f"  Power (Performance): {ljpw['P']:.3f}  [Fundamental]")
    output.append(f"  Wisdom (Design):     {ljpw['W']:.3f}  [Fundamental]")

    health_pct = result["health"] * 100
    output.append(f"\nHealth Score: {health_pct:.1f}%")

    if health_pct >= 80:
        status = "EXCELLENT"
    elif health_pct >= 60:
        status = "GOOD"
    elif health_pct >= 40:
        status = "FAIR"
    else:
        status = "NEEDS IMPROVEMENT"

    output.append(f"Status: {status}")

    output.append(f"\nDistance from Natural Equilibrium: {result['distance_from_ne']:.3f}")

    # V7.3 Metrics
    if "v7" in result and result["v7"]:
        v7 = result["v7"]
        output.append("\n--- V7.3 Metrics ---")
        output.append(f"  Harmony:      {v7.get('harmony', 0):.3f}")
        output.append(f"  Consciousness:{v7.get('consciousness', 0):.4f}  [{v7.get('consciousness_level', 'N/A')}]")
        output.append(f"  Phase:        {v7.get('phase', 'N/A')}")
        output.append(f"  Voltage:      {v7.get('voltage', 0):.3f}")
        if v7.get('is_conscious'):
            output.append("  *** System crosses consciousness threshold (C > 0.1) ***")

    output.append("\nInsights:")
    for insight in result["insights"]:
        output.append(f"  - {insight}")

    output.append("\n" + "=" * 70)

    return "\n".join(output)


def analyze_file(filepath: str) -> Dict[str, Any]:
    """
    Analyze a single file with comprehensive error handling.

    Args:
        filepath: Path to file to analyze

    Returns:
        Analysis results dictionary

    Handles:
        - File not found
        - Permission errors
        - Encoding issues
        - Binary files
        - Corrupted files
    """
    # Check file exists
    from difflib import get_close_matches
    from pathlib import Path

    # Security: Resolve path to prevent traversal attacks
    try:
        path = Path(filepath).resolve()
    except (OSError, RuntimeError) as e:
        return {
            "filename": filepath,
            "error": "Invalid path",
            "lines": 0,
            "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0},
            "health": 0,
            "insights": [f"ERROR: Invalid file path: {str(e)}"],
            "distance_from_ne": 0,
        }

    if not path.exists():
        # Provide helpful suggestions for similar files
        parent = path.parent
        similar = []
        if parent.exists():
            try:
                similar = get_close_matches(
                    path.name, [f.name for f in parent.iterdir() if f.is_file()], n=3, cutoff=0.6
                )
            except (OSError, PermissionError):
                pass

        error_msg = f"ERROR: File not found: {filepath}"
        if similar:
            error_msg += f'\n  Did you mean: {", ".join(similar)}?'

        return {
            "filename": filepath,
            "error": "File not found",
            "lines": 0,
            "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0},
            "health": 0,
            "insights": [error_msg],
            "distance_from_ne": 0,
        }

    if not path.is_file():
        return {
            "filename": filepath,
            "error": "Not a file",
            "lines": 0,
            "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0},
            "health": 0,
            "insights": [f"ERROR: Not a file (possibly a directory): {filepath}"],
            "distance_from_ne": 0,
        }

    # Try reading with UTF-8, fall back to other encodings
    encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
    code = None
    used_encoding = None

    for encoding in encodings:
        try:
            with open(filepath, "r", encoding=encoding) as f:
                code = f.read()
            used_encoding = encoding
            break
        except UnicodeDecodeError:
            continue
        except PermissionError:
            return {
                "filename": filepath,
                "error": "Permission denied",
                "lines": 0,
                "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0},
                "health": 0,
                "insights": [f"ERROR: Permission denied: {filepath}"],
                "distance_from_ne": 0,
            }
        except Exception as e:
            return {
                "filename": filepath,
                "error": str(e),
                "lines": 0,
                "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0},
                "health": 0,
                "insights": [f"ERROR: {str(e)}"],
                "distance_from_ne": 0,
            }

    if code is None:
        return {
            "filename": filepath,
            "error": "Encoding error",
            "lines": 0,
            "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0},
            "health": 0,
            "insights": [f"ERROR: Could not decode file with any known encoding"],
            "distance_from_ne": 0,
        }

    analyzer = SimpleCodeAnalyzer()
    result = analyzer.analyze(code, filepath)

    # Add encoding info if not UTF-8
    if used_encoding != "utf-8":
        result["encoding"] = used_encoding
        if "insights" not in result:
            result["insights"] = []
        result["insights"].append(f"NOTE: File encoded as {used_encoding}, not UTF-8")

    return result


def analyze_directory(dirpath: str, show_progress: bool = True) -> List[Dict[str, Any]]:
    """
    Analyze all code files in directory with optional progress indicator.

    Args:
        dirpath: Path to directory to analyze
        show_progress: Whether to show progress bar (default: True)

    Returns:
        List of analysis results for each file
    """
    results = []
    extensions = {".py", ".js", ".java", ".rs", ".cpp", ".c", ".go", ".rb", ".php", ".ts"}

    # Security: Validate and resolve path
    try:
        path = Path(dirpath).resolve()
    except (OSError, RuntimeError) as e:
        print(f"❌ Error: Invalid directory path: {e}")
        return []

    if not path.exists():
        print(f"❌ Error: Directory not found: {dirpath}")
        return []

    if not path.is_dir():
        print(f"❌ Error: Not a directory: {dirpath}")
        return []

    # Collect all files first
    try:
        files = [f for f in path.rglob("*") if f.is_file() and f.suffix in extensions]
    except (OSError, PermissionError) as e:
        print(f"❌ Error accessing directory: {e}")
        return []

    total = len(files)

    if total == 0:
        print(f"⚠️  No code files found in {dirpath}")
        return []

    if show_progress:
        print(f"\n📊 Analyzing {total} files in {dirpath}...")
        print("─" * 70)

    # Analyze files with progress indicator
    for i, file in enumerate(files, 1):
        result = analyze_file(str(file))
        results.append(result)

        if show_progress:
            # Calculate progress
            percent = (i / total) * 100
            bar_length = 40
            filled = int(bar_length * i / total)
            bar = "█" * filled + "░" * (bar_length - filled)

            # Truncate filename for display
            display_name = file.name[:30] + "..." if len(file.name) > 30 else file.name

            # Print progress bar
            print(
                f"\r  [{bar}] {percent:5.1f}% ({i:>4}/{total}) - {display_name}", end="", flush=True
            )

    if show_progress:
        print("\n" + "─" * 70)
        print(f"✅ Analysis complete: {total} files processed\n")

    return results


def analyze_quick(code: str) -> Dict[str, Any]:
    """Quick analysis of code snippet"""
    analyzer = SimpleCodeAnalyzer()
    return analyzer.analyze(code, "snippet")


def print_summary(results: List[Dict[str, Any]]) -> None:
    """Print summary of multiple files"""
    if not results:
        print("No files analyzed")
        return

    print("\n" + "=" * 70)
    print(f"LJPW Analysis Summary: {len(results)} files")
    print("=" * 70)

    # Calculate averages
    total_L, total_J, total_P, total_W, total_health = 0, 0, 0, 0, 0
    for r in results:
        if "error" not in r:
            total_L += r["ljpw"]["L"]
            total_J += r["ljpw"]["J"]
            total_P += r["ljpw"]["P"]
            total_W += r["ljpw"]["W"]
            total_health += r["health"]

    n = len(results)
    print(f"\nAverage LJPW Scores:")
    print(f"  Love (Safety):       {total_L/n:.3f}")
    print(f"  Justice (Structure): {total_J/n:.3f}")
    print(f"  Power (Performance): {total_P/n:.3f}")
    print(f"  Wisdom (Design):     {total_W/n:.3f}")
    print(f"\nAverage Health: {(total_health/n)*100:.1f}%")

    # Show top issues
    low_safety = [r for r in results if r.get("ljpw", {}).get("L", 1) < 0.5]
    low_structure = [r for r in results if r.get("ljpw", {}).get("J", 1) < 0.4]

    if low_safety:
        print(f"\n{len(low_safety)} files with LOW SAFETY")
    if low_structure:
        print(f"{len(low_structure)} files with LOW STRUCTURE")

    print("\n" + "=" * 70)


def calculate_distance(
    coords1: Tuple[float, float, float, float], coords2: Tuple[float, float, float, float]
) -> float:
    """Calculate Euclidean distance between two LJPW coordinates"""
    L1, J1, P1, W1 = coords1
    L2, J2, P2, W2 = coords2
    return math.sqrt((L1 - L2) ** 2 + (J1 - J2) ** 2 + (P1 - P2) ** 2 + (W1 - W2) ** 2)


def calculate_file_distance(file1: str, file2: str) -> Dict[str, Any]:
    """Calculate semantic distance between two files"""
    # Analyze both files
    result1 = analyze_file(file1)
    result2 = analyze_file(file2)

    # Check for errors
    if "error" in result1:
        return {"error": f"Failed to analyze {file1}: {result1['error']}"}
    if "error" in result2:
        return {"error": f"Failed to analyze {file2}: {result2['error']}"}

    # Extract coordinates
    coords1 = (
        result1["ljpw"]["L"],
        result1["ljpw"]["J"],
        result1["ljpw"]["P"],
        result1["ljpw"]["W"],
    )
    coords2 = (
        result2["ljpw"]["L"],
        result2["ljpw"]["J"],
        result2["ljpw"]["P"],
        result2["ljpw"]["W"],
    )

    # Calculate distance
    distance = calculate_distance(coords1, coords2)

    # Interpret similarity
    if distance < 0.2:
        similarity = "Very High"
        interpretation = "Nearly identical semantic profiles"
    elif distance < 0.4:
        similarity = "High"
        interpretation = "Closely related, likely work together"
    elif distance < 0.6:
        similarity = "Moderate"
        interpretation = "Different but related purposes"
    elif distance < 0.8:
        similarity = "Low"
        interpretation = "Different concerns, loosely related"
    else:
        similarity = "Very Low"
        interpretation = "Fundamentally different purposes"

    return {
        "file1": file1,
        "file2": file2,
        "coords1": coords1,
        "coords2": coords2,
        "distance": distance,
        "similarity": similarity,
        "interpretation": interpretation,
        "result1": result1,
        "result2": result2,
    }


def format_distance_result(result: Dict[str, Any]) -> str:
    """Format distance calculation result for display"""
    if "error" in result:
        return f"\nError: {result['error']}\n"

    output = []
    output.append("\n" + "=" * 70)
    output.append("LJPW Semantic Distance Analysis")
    output.append("=" * 70)

    # File 1
    output.append(f"\nFile 1: {result['file1']}")
    L1, J1, P1, W1 = result["coords1"]
    output.append(f"  Coordinates: L={L1:.2f}, J={J1:.2f}, P={P1:.2f}, W={W1:.2f}")
    output.append(f"  Health: {result['result1']['health']:.0%}")

    # File 2
    output.append(f"\nFile 2: {result['file2']}")
    L2, J2, P2, W2 = result["coords2"]
    output.append(f"  Coordinates: L={L2:.2f}, J={J2:.2f}, P={P2:.2f}, W={W2:.2f}")
    output.append(f"  Health: {result['result2']['health']:.0%}")

    # Distance
    output.append(f"\nSemantic Distance: {result['distance']:.3f}")
    output.append(f"Similarity: {result['similarity']}")
    output.append(f"Interpretation: {result['interpretation']}")

    # Dimension differences
    output.append("\nDimension-by-Dimension Comparison:")
    output.append(f"  Love (Safety):       {L1:.2f} vs {L2:.2f}  (Δ = {abs(L1-L2):.2f})")
    output.append(f"  Justice (Structure): {J1:.2f} vs {J2:.2f}  (Δ = {abs(J1-J2):.2f})")
    output.append(f"  Power (Performance): {P1:.2f} vs {P2:.2f}  (Δ = {abs(P1-P2):.2f})")
    output.append(f"  Wisdom (Design):     {W1:.2f} vs {W2:.2f}  (Δ = {abs(W1-W2):.2f})")

    # Insights
    output.append("\nKey Differences:")
    diffs = [
        ("Safety", abs(L1 - L2), "more" if L1 > L2 else "less"),
        ("Structure", abs(J1 - J2), "more" if J1 > J2 else "less"),
        ("Performance", abs(P1 - P2), "more" if P1 > P2 else "less"),
        ("Design quality", abs(W1 - W2), "better" if W1 > W2 else "worse"),
    ]
    diffs.sort(key=lambda x: x[1], reverse=True)

    if diffs[0][1] > 0.1:
        dim, diff, comp = diffs[0]
        output.append(f"  • File 1 has {comp} {dim.lower()} (Δ = {diff:.2f})")

    if diffs[1][1] > 0.1:
        dim, diff, comp = diffs[1]
        output.append(f"  • File 1 has {comp} {dim.lower()} (Δ = {diff:.2f})")

    output.append("\n" + "=" * 70)

    return "\n".join(output)


def format_distance_result_json(result: Dict[str, Any]) -> str:
    """Format distance calculation result as JSON"""
    # Create clean JSON output (remove full analysis results, keep key info)
    json_result = {
        "file1": result.get("file1"),
        "file2": result.get("file2"),
        "coordinates": {
            "file1": {
                "L": result["coords1"][0],
                "J": result["coords1"][1],
                "P": result["coords1"][2],
                "W": result["coords1"][3],
            },
            "file2": {
                "L": result["coords2"][0],
                "J": result["coords2"][1],
                "P": result["coords2"][2],
                "W": result["coords2"][3],
            },
        },
        "health": {"file1": result["result1"]["health"], "file2": result["result2"]["health"]},
        "distance": result["distance"],
        "similarity": result["similarity"],
        "interpretation": result["interpretation"],
        "differences": {
            "Love": abs(result["coords1"][0] - result["coords2"][0]),
            "Justice": abs(result["coords1"][1] - result["coords2"][1]),
            "Power": abs(result["coords1"][2] - result["coords2"][2]),
            "Wisdom": abs(result["coords1"][3] - result["coords2"][3]),
        },
    }

    if "error" in result:
        json_result = {"error": result["error"]}

    return json.dumps(json_result, indent=2)


def calculate_batch_distance(files: List[str]) -> Dict[str, Any]:
    """
    Calculate distances between multiple files.
    Returns a distance matrix and analysis for all pairs.
    """
    if len(files) < 2:
        return {"error": "Need at least 2 files for distance calculation"}

    # Analyze all files
    analyses = {}
    for filepath in files:
        result = analyze_file(filepath)
        if "error" in result:
            return {"error": f"Failed to analyze {filepath}: {result['error']}"}
        analyses[filepath] = result

    # Build distance matrix
    n = len(files)
    distance_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            file1 = files[i]
            file2 = files[j]

            coords1 = (
                analyses[file1]["ljpw"]["L"],
                analyses[file1]["ljpw"]["J"],
                analyses[file1]["ljpw"]["P"],
                analyses[file1]["ljpw"]["W"],
            )
            coords2 = (
                analyses[file2]["ljpw"]["L"],
                analyses[file2]["ljpw"]["J"],
                analyses[file2]["ljpw"]["P"],
                analyses[file2]["ljpw"]["W"],
            )

            dist = calculate_distance(coords1, coords2)
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist

    # Find most similar and most different pairs
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((files[i], files[j], distance_matrix[i][j]))

    pairs.sort(key=lambda x: x[2])

    return {
        "files": files,
        "analyses": analyses,
        "distance_matrix": distance_matrix,
        "most_similar": pairs[0] if pairs else None,
        "most_different": pairs[-1] if pairs else None,
        "all_pairs": pairs,
    }


def format_batch_distance_result(result: Dict[str, Any]) -> str:
    """Format batch distance calculation result for display"""
    if "error" in result:
        return f"\nError: {result['error']}\n"

    output = []
    output.append("\n" + "=" * 70)
    output.append("LJPW Batch Semantic Distance Analysis")
    output.append("=" * 70)

    files = result["files"]
    n = len(files)

    # Show file coordinates
    output.append(f"\nAnalyzed {n} files:\n")
    for i, filepath in enumerate(files):
        analysis = result["analyses"][filepath]
        coords = (
            analysis["ljpw"]["L"],
            analysis["ljpw"]["J"],
            analysis["ljpw"]["P"],
            analysis["ljpw"]["W"],
        )
        output.append(f"{i+1}. {filepath}")
        output.append(
            f"   L={coords[0]:.2f}, J={coords[1]:.2f}, P={coords[2]:.2f}, W={coords[3]:.2f}"
        )
        output.append(f"   Health: {analysis['health']:.0%}")
        output.append("")

    # Distance matrix
    output.append("Distance Matrix:")
    output.append("")

    # Header
    header = "     "
    for i in range(n):
        header += f" {i+1:5}"
    output.append(header)

    # Rows
    for i in range(n):
        row = f" {i+1}.  "
        for j in range(n):
            if i == j:
                row += "   -  "
            else:
                row += f"{result['distance_matrix'][i][j]:5.2f} "
        output.append(row)

    # Most similar and different
    if result["most_similar"]:
        file1, file2, dist = result["most_similar"]
        output.append(f"\nMost Similar: {file1} ↔ {file2}")
        output.append(f"  Distance: {dist:.3f}")

    if result["most_different"]:
        file1, file2, dist = result["most_different"]
        output.append(f"\nMost Different: {file1} ↔ {file2}")
        output.append(f"  Distance: {dist:.3f}")

    output.append("\n" + "=" * 70)

    return "\n".join(output)


def format_batch_distance_result_json(result: Dict[str, Any]) -> str:
    """Format batch distance calculation result as JSON"""
    if "error" in result:
        return json.dumps({"error": result["error"]}, indent=2)

    # Create clean JSON structure
    json_result = {
        "files": result["files"],
        "coordinates": {},
        "health": {},
        "distance_matrix": result["distance_matrix"],
        "most_similar": (
            {
                "file1": result["most_similar"][0],
                "file2": result["most_similar"][1],
                "distance": result["most_similar"][2],
            }
            if result["most_similar"]
            else None
        ),
        "most_different": (
            {
                "file1": result["most_different"][0],
                "file2": result["most_different"][1],
                "distance": result["most_different"][2],
            }
            if result["most_different"]
            else None
        ),
    }

    # Add coordinates for each file
    for filepath in result["files"]:
        analysis = result["analyses"][filepath]
        json_result["coordinates"][filepath] = {
            "L": analysis["ljpw"]["L"],
            "J": analysis["ljpw"]["J"],
            "P": analysis["ljpw"]["P"],
            "W": analysis["ljpw"]["W"],
        }
        json_result["health"][filepath] = analysis["health"]

    return json.dumps(json_result, indent=2)


# ============================================================================
# MAIN
# ============================================================================


def main() -> None:
    if len(sys.argv) < 2:
        print(
            """
LJPW Semantic Analyzer - DNA-Inspired Code Quality Analysis

Usage:
    python ljpw_standalone.py analyze <file_or_directory>
    python ljpw_standalone.py quick "<code>"
    python ljpw_standalone.py distance <file1> <file2> [file3...] [--json] [--save <filename>]
    python ljpw_standalone.py help

Examples:
    # Analyze a single file
    python ljpw_standalone.py analyze mycode.py

    # Analyze entire directory
    python ljpw_standalone.py analyze ./src

    # Quick analysis of code snippet
    python ljpw_standalone.py quick "def hello(): print('hi')"

    # Compare two files (calculate semantic distance)
    python ljpw_standalone.py distance validation.py api_handler.py

    # Compare multiple files (batch distance matrix)
    python ljpw_standalone.py distance file1.py file2.py file3.py

    # Output distance results as JSON
    python ljpw_standalone.py distance file1.py file2.py --json

    # Save distance results to a file
    python ljpw_standalone.py distance file1.py file2.py --save results.txt

    # Combine options
    python ljpw_standalone.py distance f1.py f2.py f3.py --json --save matrix.json

About:
    LJPW measures code quality across 4 dimensions:
    - Love (L): Safety, error handling, validation
    - Justice (J): Structure, types, documentation
    - Power (P): Performance, algorithms, efficiency
    - Wisdom (W): Design, patterns, architecture

    MIT License - Free for all, forever
    Version 2.0 (V7.3 Framework)
        """
        )
        return

    command = sys.argv[1]

    if command == "help":
        # Show help text (already printed above)
        return

    if command == "analyze":
        if len(sys.argv) < 3:
            print("Error: Please provide file or directory to analyze")
            return

        target = sys.argv[2]
        path = Path(target)

        if path.is_file():
            result = analyze_file(target)
            print(format_result(result))
        elif path.is_dir():
            results = analyze_directory(target)
            print_summary(results)
            print(f"\nAnalyzed {len(results)} files")

            # Optionally save detailed results
            if len(sys.argv) > 3 and sys.argv[3] == "--save":
                with open("ljpw_results.json", "w") as f:
                    json.dump(results, f, indent=2)
                print("Detailed results saved to ljpw_results.json")
        else:
            print(f"Error: {target} not found")

    elif command == "quick":
        if len(sys.argv) < 3:
            print("Error: Please provide code to analyze")
            return

        code = sys.argv[2]
        result = analyze_quick(code)
        print(format_result(result))

    elif command == "distance":
        if len(sys.argv) < 4:
            print("Error: Please provide at least two files to compare")
            print(
                "Usage: python ljpw_standalone.py distance <file1> <file2> [file3...] [--json] [--save <filename>]"
            )
            return

        # Parse arguments
        files = []
        use_json = False
        save_file = None
        i = 2

        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == "--json":
                use_json = True
                i += 1
            elif arg == "--save":
                if i + 1 < len(sys.argv):
                    save_file = sys.argv[i + 1]
                    i += 2
                else:
                    print("Error: --save requires a filename")
                    return
            else:
                # It's a file path
                files.append(arg)
                i += 1

        if len(files) < 2:
            print("Error: Please provide at least two files to compare")
            return

        # Check if batch comparison (3+ files) or pairwise (2 files)
        if len(files) == 2:
            # Pairwise comparison
            result = calculate_file_distance(files[0], files[1])

            # Format output
            if use_json:
                output = format_distance_result_json(result)
            else:
                output = format_distance_result(result)

            # Display output
            print(output)

            # Save if requested
            if save_file:
                with open(save_file, "w") as f:
                    f.write(output)
                print(f"\nResults saved to {save_file}")

        else:
            # Batch comparison
            result = calculate_batch_distance(files)

            # Format output
            if use_json:
                output = format_batch_distance_result_json(result)
            else:
                output = format_batch_distance_result(result)

            # Display output
            print(output)

            # Save if requested
            if save_file:
                with open(save_file, "w") as f:
                    f.write(output)
                print(f"\nResults saved to {save_file}")

    else:
        print(f"Unknown command: {command}")
        print("Use 'python ljpw_standalone.py help' for usage")


if __name__ == "__main__":
    main()
