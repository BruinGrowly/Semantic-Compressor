#!/usr/bin/env python3
"""
Example 2: Analyze an Entire Directory

This example shows how to:
- Analyze all code files in a directory
- Get aggregate statistics
- Identify problem files

Run:
    python 02_analyze_directory.py [directory_path]

Example:
    python 02_analyze_directory.py ../../
"""

import sys
from pathlib import Path

# Add parent directory to path for src module imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ljpw.ljpw_standalone import SimpleCodeAnalyzer, analyze_directory


def main():
    print("=" * 70)
    print("LJPW Example 2: Analyze a Directory")
    print("=" * 70)
    print()

    # Get directory from command line or use parent
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Analyze the LJPW project itself!
        directory = str(Path(__file__).parent.parent.parent)

    print(f"Analyzing directory: {directory}")
    print("This may take a few seconds...")
    print()

    # Analyze all files
    results = analyze_directory(directory)

    if not results:
        print("No code files found!")
        return

    # Calculate statistics
    total_files = len(results)
    valid_results = [r for r in results if "error" not in r]

    print(f"Found {total_files} files")
    print(f"Successfully analyzed: {len(valid_results)} files")
    print()

    if not valid_results:
        print("No valid results!")
        return

    # Aggregate scores
    avg_L = sum(r["ljpw"]["L"] for r in valid_results) / len(valid_results)
    avg_J = sum(r["ljpw"]["J"] for r in valid_results) / len(valid_results)
    avg_P = sum(r["ljpw"]["P"] for r in valid_results) / len(valid_results)
    avg_W = sum(r["ljpw"]["W"] for r in valid_results) / len(valid_results)
    avg_health = sum(r["health"] for r in valid_results) / len(valid_results)

    print("AGGREGATE SCORES:")
    print("-" * 70)
    print(f"Average Love (Safety):       {avg_L:.3f}")
    print(f"Average Justice (Structure): {avg_J:.3f}")
    print(f"Average Power (Performance): {avg_P:.3f}")
    print(f"Average Wisdom (Design):     {avg_W:.3f}")
    print(f"\nAverage Health: {avg_health*100:.1f}%")
    print()

    # Find problem areas
    low_safety = [r for r in valid_results if r["ljpw"]["L"] < 0.5]
    low_structure = [r for r in valid_results if r["ljpw"]["J"] < 0.4]
    low_design = [r for r in valid_results if r["ljpw"]["W"] < 0.5]
    low_health = [r for r in valid_results if r["health"] < 0.5]

    print("PROBLEM AREAS:")
    print("-" * 70)

    if low_safety:
        print(f"\n{len(low_safety)} files with LOW SAFETY (L < 0.5):")
        for r in low_safety[:5]:  # Show top 5
            print(f"  - {Path(r['filename']).name}: L={r['ljpw']['L']:.2f}")
        if len(low_safety) > 5:
            print(f"  ... and {len(low_safety) - 5} more")

    if low_structure:
        print(f"\n{len(low_structure)} files with LOW STRUCTURE (J < 0.4):")
        for r in low_structure[:5]:
            print(f"  - {Path(r['filename']).name}: J={r['ljpw']['J']:.2f}")
        if len(low_structure) > 5:
            print(f"  ... and {len(low_structure) - 5} more")

    if low_design:
        print(f"\n{len(low_design)} files with LOW DESIGN (W < 0.5):")
        for r in low_design[:5]:
            print(f"  - {Path(r['filename']).name}: W={r['ljpw']['W']:.2f}")
        if len(low_design) > 5:
            print(f"  ... and {len(low_design) - 5} more")

    if low_health:
        print(f"\n{len(low_health)} files with LOW OVERALL HEALTH (<50%):")
        sorted_by_health = sorted(low_health, key=lambda x: x["health"])
        for r in sorted_by_health[:5]:
            print(f"  - {Path(r['filename']).name}: {r['health']*100:.1f}%")
        if len(low_health) > 5:
            print(f"  ... and {len(low_health) - 5} more")

    if not (low_safety or low_structure or low_design or low_health):
        print("\nNo major issues found! 🎉")
        print("Your codebase is in good shape!")

    # Best files
    print()
    print("TOP 5 HEALTHIEST FILES:")
    print("-" * 70)
    sorted_by_health = sorted(valid_results, key=lambda x: x["health"], reverse=True)
    for i, r in enumerate(sorted_by_health[:5], 1):
        print(f"{i}. {Path(r['filename']).name}: {r['health']*100:.1f}%")
        ljpw = r["ljpw"]
        print(f"   L={ljpw['L']:.2f}, J={ljpw['J']:.2f}, P={ljpw['P']:.2f}, W={ljpw['W']:.2f}")

    print()
    print("=" * 70)
    print("TIP: Focus on fixing files with lowest health first")
    print("Next: Try running 03_compress_decompress.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
