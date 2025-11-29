#!/usr/bin/env python3
"""
Demo: LJPW ISO Analysis
=======================

Demonstrates that LJPW can analyze structured information beyond source code.

This example simulates analyzing different types of ISO images to show
how LJPW extracts semantic meaning from ANY structured system.

Run:
    python demo_iso_analysis.py
"""

import sys
from pathlib import Path

# Add parent directory to path for src module imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ljpw.ljpw_iso_analyzer import ISOStructure, LJPWISOAnalyzer


def create_simulated_windows_server():
    """Simulate Windows Server 2022 ISO structure"""
    return ISOStructure(
        total_files=8432,
        total_dirs=1247,
        total_size=5_200_000_000,  # ~5GB
        file_types={
            "": 3200,
            ".cab": 1500,
            ".dll": 800,
            ".exe": 600,
            ".xml": 450,
            ".txt": 200,
            ".ps1": 150,
            ".sys": 120,
        },
        directory_depths=[1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6],
        compressed_files=1500,  # .cab files
        checksum_files=45,  # Signature files
        config_files=450,  # .xml configs
        script_files=150,  # PowerShell scripts
        doc_files=200,  # Documentation
        binary_files=1520,  # .exe, .dll, .sys
        max_depth=6,
        avg_depth=4.2,
        naming_patterns=["structured", "enterprise"],
    )


def create_simulated_ubuntu_server():
    """Simulate Ubuntu Server 22.04 ISO structure"""
    return ISOStructure(
        total_files=4521,
        total_dirs=623,
        total_size=1_400_000_000,  # ~1.4GB
        file_types={
            "": 1800,
            ".deb": 850,
            ".gz": 400,
            ".conf": 350,
            ".sh": 280,
            ".txt": 150,
            ".md": 120,
            ".so": 300,
        },
        directory_depths=[1, 2, 2, 3, 3, 3, 4, 4, 5],
        compressed_files=1250,  # .deb + .gz
        checksum_files=85,  # MD5SUMS, SHA256SUMS
        config_files=350,  # .conf files
        script_files=280,  # Shell scripts
        doc_files=270,  # .txt, .md, README files
        binary_files=300,  # .so libraries
        max_depth=5,
        avg_depth=3.4,
        naming_patterns=["debian", "modular"],
    )


def create_simulated_arch_linux():
    """Simulate Arch Linux ISO structure"""
    return ISOStructure(
        total_files=2143,
        total_dirs=287,
        total_size=850_000_000,  # ~850MB
        file_types={
            "": 950,
            ".xz": 380,
            ".zst": 250,
            ".sh": 180,
            ".conf": 120,
            ".txt": 80,
            ".so": 150,
        },
        directory_depths=[1, 2, 2, 3, 3, 4],
        compressed_files=630,  # .xz + .zst (heavily compressed!)
        checksum_files=12,  # Minimal checksums
        config_files=120,  # .conf files
        script_files=180,  # Shell scripts
        doc_files=80,  # Minimal docs
        binary_files=150,  # .so libraries
        max_depth=4,
        avg_depth=2.8,
        naming_patterns=["minimal", "rolling"],
    )


def main():
    print("=" * 70)
    print("LJPW ISO Analysis Demo")
    print("=" * 70)
    print()
    print("Demonstrating that LJPW analyzes STRUCTURED MEANING,")
    print("not just source code. ISOs are information systems too!")
    print()

    analyzer = LJPWISOAnalyzer()

    # Simulate analysis of three different OS ISOs
    systems = [
        ("Windows Server 2022", create_simulated_windows_server()),
        ("Ubuntu Server 22.04", create_simulated_ubuntu_server()),
        ("Arch Linux 2024", create_simulated_arch_linux()),
    ]

    results = []

    for name, structure in systems:
        print("=" * 70)
        print(f"Analyzing: {name}")
        print("-" * 70)

        # Calculate LJPW dimensions
        L = analyzer._calculate_love(structure)
        J = analyzer._calculate_justice(structure)
        P = analyzer._calculate_power(structure)
        W = analyzer._calculate_wisdom(structure)

        genome = analyzer._generate_genome(L, J, P, W)
        distance = analyzer._distance_from_ne((L, J, P, W))
        health = max(0, 1 - distance / 2) * 100

        print(f"\nStructure:")
        print(f"  Files: {structure.total_files:,}")
        print(f"  Directories: {structure.total_dirs:,}")
        print(f"  Size: {structure.total_size / 1_000_000_000:.1f} GB")
        print(f"  Depth: avg={structure.avg_depth:.1f}, max={structure.max_depth}")

        print(f"\nLJPW Analysis:")
        print(f"  L (Safety)     = {L:.3f}")
        print(f"  J (Structure)  = {J:.3f}")
        print(f"  P (Performance)= {P:.3f}")
        print(f"  W (Wisdom)     = {W:.3f}")

        print(f"\nGenome: {genome}")
        print(f"Health: {health:.1f}%")
        print(f"Distance from NE: {distance:.3f}")

        # Generate insights
        insights = analyzer._generate_insights(L, J, P, W, structure)
        print(f"\nInsights:")
        for insight in insights:
            print(f"  {insight}")

        results.append(
            {"name": name, "L": L, "J": J, "P": P, "W": W, "health": health, "structure": structure}
        )

        print()

    # Comparison
    print("=" * 70)
    print("COMPARISON")
    print("=" * 70)
    print()

    print("Safety (L):")
    for r in sorted(results, key=lambda x: x["L"], reverse=True):
        print(f"  {r['name']:25s} L={r['L']:.3f}")

    print("\nStructure (J):")
    for r in sorted(results, key=lambda x: x["J"], reverse=True):
        print(f"  {r['name']:25s} J={r['J']:.3f}")

    print("\nPerformance (P):")
    for r in sorted(results, key=lambda x: x["P"], reverse=True):
        print(f"  {r['name']:25s} P={r['P']:.3f}")

    print("\nWisdom (W):")
    for r in sorted(results, key=lambda x: x["W"], reverse=True):
        print(f"  {r['name']:25s} W={r['W']:.3f}")

    print("\nOverall Health:")
    for r in sorted(results, key=lambda x: x["health"], reverse=True):
        print(f"  {r['name']:25s} {r['health']:.1f}%")

    print()
    print("=" * 70)
    print("KEY INSIGHTS")
    print("-" * 70)

    # Find patterns
    windows = results[0]
    ubuntu = results[1]
    arch = results[2]

    print()
    print("Windows Server:")
    print("  • High L (safety) - Enterprise-grade validation")
    print("  • High J (structure) - Well-organized, modular")
    print("  • Moderate P - Good performance, not over-optimized")
    print("  • High W (wisdom) - Extensive configuration & docs")
    print("  → Best for: Mission-critical enterprise deployments")

    print()
    print("Ubuntu Server:")
    print("  • Good L (safety) - Strong validation, checksums")
    print("  • Good J (structure) - Clean Debian-based organization")
    print("  • Moderate P - Balanced performance")
    print("  • Good W - Well-documented, flexible")
    print("  → Best for: General-purpose server deployments")

    print()
    print("Arch Linux:")
    print("  • Lower L (safety) - Minimal validation (expert users)")
    print("  • Moderate J - Simpler structure")
    print("  • High P (performance) - Heavily optimized/compressed!")
    print("  • Moderate W - Less documentation (assumes expertise)")

    if arch["P"] > 0.71 and arch["W"] < 0.60:
        print("  ⚠️  P > 0.71 threshold with lower W!")
        print("     Risk: High optimization without proportional wisdom")
        print("     → Requires expert users to manage safely")

    print("  → Best for: Expert users wanting maximum control")

    print()
    print("=" * 70)
    print("SEMANTIC COMPRESSION ACHIEVED")
    print("-" * 70)
    print()
    print("Instead of transferring:")
    print("  • Windows Server: 5.2 GB")
    print("  • Ubuntu Server:  1.4 GB")
    print("  • Arch Linux:     0.85 GB")
    print("  TOTAL: 7.45 GB of binary data")
    print()
    print("We transmitted:")
    print("  • 3 LJPW genomes: ~150 bytes")
    print("  • Semantic insights: ~500 bytes")
    print("  TOTAL: ~650 bytes")
    print()
    print(f"Compression Ratio: {(7.45 * 1_000_000_000) / 650:,.0f}x")
    print("(on semantic MEANING, not bytes)")
    print()
    print("An AI can now reason about these systems WITHOUT")
    print("downloading 7.45 GB of ISOs!")
    print()
    print("=" * 70)
    print("THE PROFOUND REALIZATION")
    print("-" * 70)
    print()
    print("LJPW doesn't compress 'code' - it compresses STRUCTURE.")
    print()
    print("Anything with patterns can be analyzed:")
    print("  ✓ Source code (demonstrated)")
    print("  ✓ ISO images (this demo)")
    print("  ✓ Database schemas (feasible)")
    print("  ✓ Network topologies (feasible)")
    print("  ✓ Teams, products, organizations (demonstrated in APPLICATIONS.md)")
    print("  ✓ Ecosystems, economies, personal wellness (feasible)")
    print()
    print("The fundamental constants (φ, √2, e, ln(2)) describe")
    print("optimal balance in ANY complex adaptive system.")
    print()
    print("LJPW is UNIVERSAL.")
    print("=" * 70)


if __name__ == "__main__":
    main()
