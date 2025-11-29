#!/usr/bin/env python3
"""
LJPW ISO Analyzer - Extract semantic structure from ISO images
==============================================================

Demonstrates that LJPW can analyze ANY structured information system,
not just source code. An ISO is fundamentally structured meaning:
- Boot sector (initialization logic)
- File hierarchy (organization)
- Installation scripts (sequencing)
- Dependencies (relationships)
- Checksums (validation)
- Metadata (structure)

This proves LJPW's universality: it analyzes PATTERNS, not just code.

Requirements:
    pip install pycdlib

Usage:
    python ljpw_iso_analyzer.py analyze ubuntu-22.04-server.iso
    python ljpw_iso_analyzer.py compare *.iso

Author: Generated from LJPW framework
Version: 1.0 (Proof of Concept)
Date: November 2025
"""

import math
import os
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import pycdlib

    PYCDLIB_AVAILABLE = True
except ImportError:
    PYCDLIB_AVAILABLE = False
    print("Warning: pycdlib not installed. Install with: pip install pycdlib")


# Natural Equilibrium
NATURAL_EQUILIBRIUM = (0.618034, 0.414214, 0.718282, 0.693147)


@dataclass
class ISOStructure:
    """Extracted structural information from ISO"""

    total_files: int
    total_dirs: int
    total_size: int
    file_types: Counter
    directory_depths: List[int]
    compressed_files: int
    checksum_files: int
    config_files: int
    script_files: int
    doc_files: int
    binary_files: int
    max_depth: int
    avg_depth: float
    naming_patterns: List[str]


class LJPWISOAnalyzer:
    """
    Analyze ISO images through LJPW lens.

    Extracts semantic structure and maps to L, J, P, W dimensions.
    """

    def __init__(self):
        self.iso = None

    def analyze(self, iso_path: str) -> Dict:
        """
        Analyze ISO and generate LJPW assessment.

        Args:
            iso_path: Path to ISO file

        Returns:
            Dictionary with LJPW scores, genome, and insights
        """
        if not os.path.exists(iso_path):
            return {"error": f"ISO file not found: {iso_path}"}

        if not PYCDLIB_AVAILABLE:
            # Fallback: basic file-based analysis
            return self._analyze_fallback(iso_path)

        # Extract structure
        structure = self._extract_structure(iso_path)

        # Calculate LJPW dimensions
        L_score = self._calculate_love(structure)
        J_score = self._calculate_justice(structure)
        P_score = self._calculate_power(structure)
        W_score = self._calculate_wisdom(structure)

        # Generate genome
        genome = self._generate_genome(L_score, J_score, P_score, W_score)

        # Calculate health with improved formula
        distance = self._distance_from_ne((L_score, J_score, P_score, W_score))

        # Improved health calculation (matching ljpw_standalone.py)
        distance_health = max(0, 1.0 - distance / 3.0)
        magnitude = (L_score + J_score + P_score + W_score) / 4.0
        ne_magnitude = (0.618 + 0.414 + 0.718 + 0.693) / 4.0
        magnitude_health = min(1.0, magnitude / ne_magnitude)
        health = 0.7 * distance_health + 0.3 * magnitude_health

        # Generate insights
        insights = self._generate_insights(L_score, J_score, P_score, W_score, structure)

        # Detect ISO type
        iso_type = self._detect_type(structure)

        return {
            "filename": os.path.basename(iso_path),
            "size_mb": structure.total_size / (1024 * 1024),
            "type": iso_type,
            "ljpw": {
                "L": round(L_score, 3),
                "J": round(J_score, 3),
                "P": round(P_score, 3),
                "W": round(W_score, 3),
            },
            "genome": genome,
            "health": round(health * 100, 1),
            "distance_from_ne": round(distance, 3),
            "insights": insights,
            "structure": {
                "files": structure.total_files,
                "directories": structure.total_dirs,
                "max_depth": structure.max_depth,
                "avg_depth": round(structure.avg_depth, 2),
            },
        }

    def _extract_structure(self, iso_path: str) -> ISOStructure:
        """Extract structural information from ISO using pycdlib"""
        iso = pycdlib.PyCdlib()
        iso.open(iso_path)

        total_files = 0
        total_dirs = 0
        total_size = 0
        file_types = Counter()
        directory_depths = []
        compressed = 0
        checksums = 0
        configs = 0
        scripts = 0
        docs = 0
        binaries = 0

        # Walk the ISO filesystem
        for dirname, dirlist, filelist in iso.walk(iso_path="/"):
            depth = dirname.count("/")
            directory_depths.append(depth)
            total_dirs += 1

            for filename in filelist:
                total_files += 1

                # Get file extension
                ext = Path(filename.lower()).suffix
                file_types[ext] += 1

                # Categorize files
                if ext in [".gz", ".xz", ".bz2", ".zst", ".cab", ".zip"]:
                    compressed += 1
                if ext in [".md5", ".sha256", ".sha1", ".sig", ".asc"]:
                    checksums += 1
                if ext in [".conf", ".cfg", ".xml", ".json", ".yaml", ".ini"]:
                    configs += 1
                if ext in [".sh", ".py", ".pl", ".rb", ".ps1", ".bat"]:
                    scripts += 1
                if ext in [".md", ".txt", ".rst", ".pdf", ".html"] or "readme" in filename.lower():
                    docs += 1
                if ext in [".exe", ".dll", ".so", ".bin", ".elf"]:
                    binaries += 1

                # Try to get file size (if available)
                try:
                    full_path = os.path.join(dirname, filename)
                    entry = iso.get_entry(iso_path=full_path)
                    if hasattr(entry, "get_data_length"):
                        total_size += entry.get_data_length()
                except Exception:
                    pass

        iso.close()

        max_depth = max(directory_depths) if directory_depths else 0
        avg_depth = sum(directory_depths) / len(directory_depths) if directory_depths else 0

        return ISOStructure(
            total_files=total_files,
            total_dirs=total_dirs,
            total_size=total_size,
            file_types=file_types,
            directory_depths=directory_depths,
            compressed_files=compressed,
            checksum_files=checksums,
            config_files=configs,
            script_files=scripts,
            doc_files=docs,
            binary_files=binaries,
            max_depth=max_depth,
            avg_depth=avg_depth,
            naming_patterns=[],
        )

    def _analyze_fallback(self, iso_path: str) -> Dict:
        """Fallback analysis using basic file properties"""
        size_mb = os.path.getsize(iso_path) / (1024 * 1024)

        # Simple heuristics based on size and filename
        filename = os.path.basename(iso_path).lower()

        # Guess type from filename
        if "server" in filename:
            iso_type = "Server Operating System"
            L, J, P, W = 0.70, 0.75, 0.65, 0.80
        elif "desktop" in filename or "live" in filename:
            iso_type = "Desktop Operating System"
            L, J, P, W = 0.65, 0.70, 0.70, 0.75
        elif "minimal" in filename or "net" in filename:
            iso_type = "Minimal Installation"
            L, J, P, W = 0.50, 0.65, 0.75, 0.70
        else:
            iso_type = "Unknown ISO"
            L, J, P, W = 0.60, 0.65, 0.65, 0.70

        genome = self._generate_genome(L, J, P, W)
        distance = self._distance_from_ne((L, J, P, W))

        # Improved health calculation (matching ljpw_standalone.py)
        distance_health = max(0, 1.0 - distance / 3.0)
        magnitude = (L + J + P + W) / 4.0
        ne_magnitude = (0.618 + 0.414 + 0.718 + 0.693) / 4.0
        magnitude_health = min(1.0, magnitude / ne_magnitude)
        health = 0.7 * distance_health + 0.3 * magnitude_health

        return {
            "filename": os.path.basename(iso_path),
            "size_mb": size_mb,
            "type": iso_type,
            "ljpw": {"L": L, "J": J, "P": P, "W": W},
            "genome": genome,
            "health": round(health * 100, 1),
            "distance_from_ne": round(distance, 3),
            "insights": ["(Basic analysis - install pycdlib for detailed analysis)"],
            "structure": {"note": "Install pycdlib for detailed structure analysis"},
        }

    def _calculate_love(self, s: ISOStructure) -> float:
        """
        Calculate Love (Safety) dimension.

        Indicators:
        - Checksum files (validation)
        - Backup/redundancy
        - Error handling scripts
        - Safety documentation
        """
        score = 0.0

        # Checksum files indicate validation
        if s.total_files > 0:
            checksum_ratio = s.checksum_files / s.total_files
            score += min(0.35, checksum_ratio * 100)

        # Documentation indicates safety awareness
        if s.total_files > 0:
            doc_ratio = s.doc_files / s.total_files
            score += min(0.25, doc_ratio * 50)

        # Configuration files enable proper setup
        if s.total_files > 0:
            config_ratio = s.config_files / s.total_files
            score += min(0.20, config_ratio * 40)

        # Scripts can contain validation logic
        if s.total_files > 0:
            script_ratio = s.script_files / s.total_files
            score += min(0.20, script_ratio * 30)

        return min(1.0, score)

    def _calculate_justice(self, s: ISOStructure) -> float:
        """
        Calculate Justice (Structure) dimension.

        Indicators:
        - Directory hierarchy depth (organization)
        - Naming consistency
        - File type distribution
        - Modularity
        """
        score = 0.0

        # Well-structured systems have moderate, consistent depth
        if 3 <= s.avg_depth <= 6:
            score += 0.40
        elif 2 <= s.avg_depth < 3 or 6 < s.avg_depth <= 8:
            score += 0.25
        else:
            score += 0.10

        # File type diversity indicates modular organization
        num_types = len(s.file_types)
        if num_types > 20:
            score += 0.30
        elif num_types > 10:
            score += 0.20
        else:
            score += 0.10

        # Directory to file ratio
        if s.total_files > 0:
            dir_ratio = s.total_dirs / s.total_files
            if 0.1 <= dir_ratio <= 0.3:  # Good organization
                score += 0.30
            else:
                score += 0.15

        return min(1.0, score)

    def _calculate_power(self, s: ISOStructure) -> float:
        """
        Calculate Power (Performance) dimension.

        Indicators:
        - Compressed files (optimization)
        - Binary files (compiled/optimized)
        - File size efficiency
        """
        score = 0.0

        # Compression indicates optimization
        if s.total_files > 0:
            compression_ratio = s.compressed_files / s.total_files
            score += min(0.40, compression_ratio * 2)

        # Binary files indicate optimized executables
        if s.total_files > 0:
            binary_ratio = s.binary_files / s.total_files
            score += min(0.30, binary_ratio * 1.5)

        # Overall file count (capability)
        if s.total_files > 5000:
            score += 0.30
        elif s.total_files > 1000:
            score += 0.20
        else:
            score += 0.10

        return min(1.0, score)

    def _calculate_wisdom(self, s: ISOStructure) -> float:
        """
        Calculate Wisdom (Design) dimension.

        Indicators:
        - Documentation quality
        - Configuration flexibility
        - Architectural modularity
        - Script sophistication
        """
        score = 0.0

        # Documentation indicates thoughtful design
        if s.total_files > 0:
            doc_ratio = s.doc_files / s.total_files
            score += min(0.30, doc_ratio * 60)

        # Configuration files indicate flexibility
        if s.total_files > 0:
            config_ratio = s.config_files / s.total_files
            score += min(0.30, config_ratio * 60)

        # Scripts indicate automation and design
        if s.total_files > 0:
            script_ratio = s.script_files / s.total_files
            score += min(0.25, script_ratio * 50)

        # Balanced depth indicates architectural thinking
        depth_variance = (
            max(s.directory_depths) - min(s.directory_depths) if s.directory_depths else 0
        )
        if depth_variance <= 5:  # Consistent depth
            score += 0.15

        return min(1.0, score)

    def _generate_genome(self, L: float, J: float, P: float, W: float) -> str:
        """Generate LJPW genome string"""

        def encode_dimension(value: float) -> str:
            # Map 0.0-1.0 to 0-9
            level = int(value * 10)
            return str(min(9, level))

        return f"L{encode_dimension(L)}J{encode_dimension(J)}P{encode_dimension(P)}W{encode_dimension(W)}"

    def _distance_from_ne(self, state: Tuple[float, float, float, float]) -> float:
        """Calculate Euclidean distance from Natural Equilibrium"""
        L, J, P, W = state
        L_ne, J_ne, P_ne, W_ne = NATURAL_EQUILIBRIUM
        return math.sqrt((L - L_ne) ** 2 + (J - J_ne) ** 2 + (P - P_ne) ** 2 + (W - W_ne) ** 2)

    def _generate_insights(
        self, L: float, J: float, P: float, W: float, s: ISOStructure
    ) -> List[str]:
        """Generate actionable insights"""
        insights = []

        # Threshold warning
        if P > 0.71 and W < 0.60:
            insights.append(f"⚠️  Power (P={P:.2f}) > threshold (0.71) with low Wisdom (W={W:.2f})")
            insights.append("   Risk: Over-optimization without adequate design")

        # Dimension-specific insights
        if L < 0.50:
            insights.append(
                f"Low Safety (L={L:.2f}): Few checksums ({s.checksum_files}), minimal validation"
            )
        elif L > 0.75:
            insights.append(f"High Safety (L={L:.2f}): Excellent validation and error handling")

        if J < 0.50:
            insights.append(
                f"Low Structure (J={J:.2f}): Disorganized hierarchy (depth: {s.avg_depth:.1f})"
            )
        elif J > 0.75:
            insights.append(f"Good Structure (J={J:.2f}): Well-organized, modular design")

        if P > 0.80:
            insights.append(
                f"High Performance (P={P:.2f}): Heavily optimized ({s.compressed_files} compressed files)"
            )
        elif P < 0.50:
            insights.append(f"Low Performance (P={P:.2f}): Minimal optimization")

        if W > 0.75:
            insights.append(
                f"High Wisdom (W={W:.2f}): Thoughtful design ({s.doc_files} docs, {s.config_files} configs)"
            )
        elif W < 0.50:
            insights.append(f"Low Wisdom (W={W:.2f}): Limited documentation and configuration")

        # Overall assessment
        distance = self._distance_from_ne((L, J, P, W))
        if distance < 0.3:
            insights.append("✓ Near Natural Equilibrium - well-balanced system")
        elif distance > 0.7:
            insights.append("✗ Far from equilibrium - significant imbalances")

        return insights

    def _detect_type(self, s: ISOStructure) -> str:
        """Detect ISO type from structural patterns"""
        # Heuristics based on file patterns
        has_kernel = any(
            ".vmlinuz" in str(ext) or "kernel" in str(ext) for ext in s.file_types.keys()
        )
        has_installer = s.script_files > 10
        has_docs = s.doc_files > 20

        if has_kernel and has_installer:
            if s.total_size > 3_000_000_000:  # > 3GB
                return "Enterprise Operating System"
            elif s.total_size > 1_000_000_000:  # > 1GB
                return "Desktop Operating System"
            else:
                return "Minimal Operating System"
        elif s.script_files > 50:
            return "Installation Media"
        elif s.doc_files > s.total_files * 0.3:
            return "Documentation Archive"
        else:
            return "Generic ISO Image"

    def compare(self, iso_paths: List[str]) -> Dict:
        """Compare multiple ISOs"""
        results = []

        for iso_path in iso_paths:
            result = self.analyze(iso_path)
            results.append(result)

        return {"comparison": results, "summary": self._generate_comparison_summary(results)}

    def _generate_comparison_summary(self, results: List[Dict]) -> str:
        """Generate comparison summary"""
        if not results:
            return "No ISOs to compare"

        # Find highest in each dimension
        highest_L = max(results, key=lambda r: r["ljpw"]["L"])
        highest_J = max(results, key=lambda r: r["ljpw"]["J"])
        highest_P = max(results, key=lambda r: r["ljpw"]["P"])
        highest_W = max(results, key=lambda r: r["ljpw"]["W"])
        healthiest = max(results, key=lambda r: r["health"])

        summary = []
        summary.append(
            f"Most Safe (L):      {highest_L['filename']} (L={highest_L['ljpw']['L']:.2f})"
        )
        summary.append(
            f"Best Structured (J): {highest_J['filename']} (J={highest_J['ljpw']['J']:.2f})"
        )
        summary.append(
            f"Most Optimized (P):  {highest_P['filename']} (P={highest_P['ljpw']['P']:.2f})"
        )
        summary.append(
            f"Most Wise (W):       {highest_W['filename']} (W={highest_W['ljpw']['W']:.2f})"
        )
        summary.append(
            f"Healthiest Overall:  {healthiest['filename']} ({healthiest['health']:.1f}%)"
        )

        return "\n".join(summary)


# CLI Interface


def format_result(result: Dict) -> str:
    """Format analysis result for display"""
    output = []
    output.append("=" * 70)
    output.append(f"ISO: {result['filename']}")
    output.append(f"Type: {result.get('type', 'Unknown')}")
    output.append(f"Size: {result.get('size_mb', 0):.1f} MB")
    output.append("-" * 70)

    ljpw = result["ljpw"]
    output.append(
        f"LJPW State: L={ljpw['L']:.3f}, J={ljpw['J']:.3f}, P={ljpw['P']:.3f}, W={ljpw['W']:.3f}"
    )
    output.append(f"Genome: {result['genome']}")
    output.append(f"Health: {result['health']}%")
    output.append(f"Distance from NE: {result['distance_from_ne']:.3f}")

    if (
        "structure" in result
        and isinstance(result["structure"], dict)
        and "files" in result["structure"]
    ):
        s = result["structure"]
        output.append(f"\nStructure: {s['files']} files, {s['directories']} dirs")
        output.append(f"Depth: avg={s['avg_depth']:.1f}, max={s['max_depth']}")

    output.append("\nInsights:")
    for insight in result["insights"]:
        output.append(f"  {insight}")

    output.append("=" * 70)
    return "\n".join(output)


def main():
    """CLI entry point"""
    if len(sys.argv) < 3:
        print("LJPW ISO Analyzer - Semantic Analysis of ISO Images")
        print()
        print("Usage:")
        print("  python ljpw_iso_analyzer.py analyze <iso_file>")
        print("  python ljpw_iso_analyzer.py compare <iso1> <iso2> [iso3...]")
        print()
        print("Examples:")
        print("  python ljpw_iso_analyzer.py analyze ubuntu-22.04-server.iso")
        print("  python ljpw_iso_analyzer.py compare windows.iso ubuntu.iso arch.iso")
        print()
        if not PYCDLIB_AVAILABLE:
            print("Note: Install pycdlib for detailed analysis:")
            print("  pip install pycdlib")
        return

    command = sys.argv[1]
    analyzer = LJPWISOAnalyzer()

    if command == "analyze":
        iso_path = sys.argv[2]
        result = analyzer.analyze(iso_path)
        print(format_result(result))

    elif command == "compare":
        iso_paths = sys.argv[2:]
        comparison = analyzer.compare(iso_paths)

        print("=" * 70)
        print("ISO COMPARISON")
        print("=" * 70)
        print()

        for result in comparison["comparison"]:
            print(format_result(result))
            print()

        print("=" * 70)
        print("SUMMARY")
        print("-" * 70)
        print(comparison["summary"])
        print("=" * 70)

    else:
        print(f"Unknown command: {command}")
        print("Use 'analyze' or 'compare'")


if __name__ == "__main__":
    main()
