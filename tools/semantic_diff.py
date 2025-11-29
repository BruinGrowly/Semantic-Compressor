#!/usr/bin/env python3
"""
Semantic Diff Tool
==================

Compare code versions in semantic space, not just text.

Features:
- Git integration: Compare commits, branches, files over time
- Semantic distance tracking: How much did meaning change?
- Refactoring detection: Did code move toward/away from Natural Equilibrium?
- Visual output: ASCII art showing movement in 4D space
- Health score delta: Quality improvement/degradation

Usage:
    # Compare two files
    python semantic_diff.py file1.py file2.py

    # Compare git commits
    python semantic_diff.py --git HEAD~1 HEAD myfile.py

    # Compare branches
    python semantic_diff.py --git main feature-branch myfile.py

    # Analyze git history
    python semantic_diff.py --history myfile.py --commits 10
"""

import argparse
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.ljpw.ljpw_standalone import analyze_quick, calculate_distance

# Natural Equilibrium
NATURAL_EQUILIBRIUM = (0.618, 0.414, 0.718, 0.693)


def get_genome(result):
    """Create genome from LJPW result"""
    L = result["ljpw"]["L"]
    J = result["ljpw"]["J"]
    P = result["ljpw"]["P"]
    W = result["ljpw"]["W"]

    L_digit = int(round(L * 10)) % 10
    J_digit = int(round(J * 10)) % 10
    P_digit = int(round(P * 10)) % 10
    W_digit = int(round(W * 10)) % 10

    return f"L{L_digit}J{J_digit}P{P_digit}W{W_digit}"


def calculate_health(coords):
    """Calculate health score (0-100) based on distance from NE"""
    max_distance = 2.0  # Theoretical max in unit hypercube
    dist = calculate_distance(coords, NATURAL_EQUILIBRIUM)
    return max(0, 100 * (1 - dist / max_distance))


def read_file(filepath):
    """Read file contents"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)


def get_git_file_content(commit, filepath):
    """Get file content at specific git commit"""
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{filepath}"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        print(f"Error: Could not get {filepath} at commit {commit}")
        sys.exit(1)


def analyze_code(code, label):
    """Analyze code and return full analysis"""
    if not code.strip():
        return None

    result = analyze_quick(code)
    l = result["ljpw"]["L"]
    j = result["ljpw"]["J"]
    p = result["ljpw"]["P"]
    w = result["ljpw"]["W"]

    coords = (l, j, p, w)
    genome = get_genome(result)
    dist_to_ne = calculate_distance(coords, NATURAL_EQUILIBRIUM)
    health = calculate_health(coords)

    return {
        "label": label,
        "coords": coords,
        "genome": genome,
        "dist_to_ne": dist_to_ne,
        "health": health,
        "loc": len(code.split("\n")),
    }


def print_dimension_bar(value, dimension_name, max_value=1.0, width=40):
    """Print a horizontal bar chart for a dimension"""
    filled = int((value / max_value) * width)
    bar = "█" * filled + "░" * (width - filled)
    print(f"  {dimension_name:6} [{bar}] {value:.3f}")


def visualize_movement(before, after):
    """Visualize movement in 4D space using ASCII art"""
    print("\n" + "─" * 70)
    print("SEMANTIC SPACE MOVEMENT")
    print("─" * 70)

    dimensions = ["Love", "Justice", "Power", "Wisdom"]

    for i, dim in enumerate(dimensions):
        before_val = before["coords"][i]
        after_val = after["coords"][i]
        delta = after_val - before_val

        # Create arrow visualization
        if abs(delta) < 0.01:
            arrow = "→ (no change)"
        elif delta > 0:
            arrow = f"↗ +{delta:.3f}"
        else:
            arrow = f"↘ {delta:.3f}"

        print(f"\n{dim} ({['L', 'J', 'P', 'W'][i]}):")
        print(f"  Before: {before_val:.3f}  {arrow}  After: {after_val:.3f}")

        # Show bars
        width = 30
        before_bar = int(before_val * width)
        after_bar = int(after_val * width)

        print(f"  Before: {'█' * before_bar}{'░' * (width - before_bar)}")
        print(f"  After:  {'█' * after_bar}{'░' * (width - after_bar)}")


def semantic_diff(before_code, after_code, before_label="BEFORE", after_label="AFTER"):
    """Compare two code snippets in semantic space"""

    print("=" * 70)
    print("SEMANTIC DIFF ANALYSIS")
    print("=" * 70)
    print()

    # Analyze both versions
    before = analyze_code(before_code, before_label)
    after = analyze_code(after_code, after_label)

    if not before or not after:
        print("Error: Could not analyze code")
        return

    # Summary
    print(f"Comparing: {before['label']} → {after['label']}")
    print()

    # Genomes
    print("Semantic Genomes:")
    print(f"  {before['label']:12} {before['genome']}")
    print(f"  {after['label']:12} {after['genome']}")

    genome_changed = before["genome"] != after["genome"]
    print(f"  {'✓ Genome CHANGED' if genome_changed else '✗ Genome UNCHANGED'}")
    print()

    # Coordinates
    print("4D Coordinates:")
    print(
        f"  {before['label']:12} L={before['coords'][0]:.3f}, J={before['coords'][1]:.3f}, "
        f"P={before['coords'][2]:.3f}, W={before['coords'][3]:.3f}"
    )
    print(
        f"  {after['label']:12} L={after['coords'][0]:.3f}, J={after['coords'][1]:.3f}, "
        f"P={after['coords'][2]:.3f}, W={after['coords'][3]:.3f}"
    )
    print()

    # Semantic distance
    semantic_dist = calculate_distance(before["coords"], after["coords"])
    print(f"Semantic Distance: {semantic_dist:.3f}")

    if semantic_dist < 0.1:
        significance = "✓ MINIMAL change (likely minor refactoring)"
    elif semantic_dist < 0.3:
        significance = "⚠ MODERATE change (feature addition/modification)"
    else:
        significance = "✗ MAJOR change (significant rewrite)"

    print(f"  {significance}")
    print()

    # Distance to Natural Equilibrium
    print("Distance to Natural Equilibrium:")
    print(f"  {before['label']:12} {before['dist_to_ne']:.3f}")
    print(f"  {after['label']:12} {after['dist_to_ne']:.3f}")

    ne_delta = after["dist_to_ne"] - before["dist_to_ne"]
    if ne_delta < -0.05:
        ne_movement = f"✓ MOVED TOWARD NE ({ne_delta:+.3f}) — Quality improved!"
    elif ne_delta > 0.05:
        ne_movement = f"✗ MOVED AWAY from NE ({ne_delta:+.3f}) — Quality degraded"
    else:
        ne_movement = f"→ Stayed near same distance ({ne_delta:+.3f})"

    print(f"  {ne_movement}")
    print()

    # Health scores
    print("Health Scores (0-100):")
    print(f"  {before['label']:12} {before['health']:.1f}/100")
    print(f"  {after['label']:12} {after['health']:.1f}/100")

    health_delta = after["health"] - before["health"]
    if health_delta > 5:
        health_assessment = f"✓ Health IMPROVED ({health_delta:+.1f} points)"
    elif health_delta < -5:
        health_assessment = f"✗ Health DEGRADED ({health_delta:+.1f} points)"
    else:
        health_assessment = f"→ Health stable ({health_delta:+.1f} points)"

    print(f"  {health_assessment}")
    print()

    # Lines of code
    print("Lines of Code:")
    print(f"  {before['label']:12} {before['loc']} lines")
    print(f"  {after['label']:12} {after['loc']} lines")
    loc_delta = after["loc"] - before["loc"]
    print(f"  Delta: {loc_delta:+d} lines")
    print()

    # Visualization
    visualize_movement(before, after)

    # Recommendations
    print("\n" + "─" * 70)
    print("RECOMMENDATIONS")
    print("─" * 70)

    l_before, j_before, p_before, w_before = before["coords"]
    l_after, j_after, p_after, w_after = after["coords"]

    ne_l, ne_j, ne_p, ne_w = NATURAL_EQUILIBRIUM

    recommendations = []

    # Check each dimension
    if l_after < ne_l - 0.2:
        gap = ne_l - l_after
        recommendations.append(f"• Add error handling (+L) — Gap: {gap:.3f}")

    if j_after < ne_j - 0.2:
        gap = ne_j - j_after
        recommendations.append(f"• Add type annotations/documentation (+J) — Gap: {gap:.3f}")

    if p_after < ne_p - 0.2:
        gap = ne_p - p_after
        recommendations.append(f"• Consider optimization (+P) — Gap: {gap:.3f}")

    if w_after < ne_w - 0.2:
        gap = ne_w - w_after
        recommendations.append(f"• Improve modularity/design (+W) — Gap: {gap:.3f}")

    if recommendations:
        print("\nTo move toward Natural Equilibrium:")
        for rec in recommendations:
            print(rec)
    else:
        print("\n✓ Code is well-balanced relative to Natural Equilibrium")

    print()


def analyze_git_history(filepath, num_commits=10):
    """Analyze how a file evolved over git history"""
    print("=" * 70)
    print(f"SEMANTIC EVOLUTION: {filepath}")
    print("=" * 70)
    print()

    # Get commit history for file
    try:
        result = subprocess.run(
            ["git", "log", f"-{num_commits}", "--format=%H %s", "--", filepath],
            capture_output=True,
            text=True,
            check=True,
        )
        commits = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        print(f"Error: Could not get git history for {filepath}")
        return

    if not commits or commits[0] == "":
        print(f"No commits found for {filepath}")
        return

    print(f"Analyzing last {len(commits)} commits:\n")

    # Analyze each commit
    history = []
    for commit_line in commits:
        if not commit_line.strip():
            continue

        commit_hash = commit_line.split()[0]
        commit_msg = " ".join(commit_line.split()[1:])

        try:
            code = get_git_file_content(commit_hash[:7], filepath)
            analysis = analyze_code(code, commit_hash[:7])

            if analysis:
                analysis["commit_msg"] = commit_msg
                history.append(analysis)
        except:
            continue

    if not history:
        print("Could not analyze any commits")
        return

    # Print evolution table
    print(f"{'Commit':<8} {'Genome':<12} {'Health':<8} {'Dist NE':<9} {'Message'}")
    print("─" * 100)

    for h in history:
        print(
            f"{h['label']:<8} {h['genome']:<12} {h['health']:>6.1f}/100  "
            f"{h['dist_to_ne']:>7.3f}  {h['commit_msg'][:50]}"
        )

    # Evolution summary
    print("\n" + "=" * 70)
    print("EVOLUTION SUMMARY")
    print("=" * 70)

    if len(history) >= 2:
        oldest = history[-1]
        newest = history[0]

        print(f"\nFrom {oldest['label']} to {newest['label']}:")
        print(f"  Genome:  {oldest['genome']} → {newest['genome']}")
        print(
            f"  Health:  {oldest['health']:.1f} → {newest['health']:.1f} "
            f"({newest['health'] - oldest['health']:+.1f})"
        )
        print(
            f"  Dist NE: {oldest['dist_to_ne']:.3f} → {newest['dist_to_ne']:.3f} "
            f"({newest['dist_to_ne'] - oldest['dist_to_ne']:+.3f})"
        )

        # Overall trend
        if newest["health"] > oldest["health"] + 5:
            trend = "✓ Overall IMPROVEMENT"
        elif newest["health"] < oldest["health"] - 5:
            trend = "✗ Overall DEGRADATION"
        else:
            trend = "→ Overall STABLE"

        print(f"\n{trend}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Semantic Diff Tool")

    parser.add_argument("file1", help="First file or git ref")
    parser.add_argument("file2", nargs="?", help="Second file or git ref")
    parser.add_argument("--git", action="store_true", help="Use git comparison mode")
    parser.add_argument("--history", action="store_true", help="Analyze git history")
    parser.add_argument("--commits", type=int, default=10, help="Number of commits to analyze")

    args = parser.parse_args()

    if args.history:
        # History mode
        analyze_git_history(args.file1, args.commits)
    elif args.git:
        # Git comparison mode
        if not args.file2:
            print("Error: Git mode requires both commit refs and filepath")
            print("Usage: semantic_diff.py --git COMMIT1 COMMIT2 filepath")
            sys.exit(1)

        commit1 = args.file1
        commit2 = args.file2
        filepath = sys.argv[-1]  # Last argument is the file

        code1 = get_git_file_content(commit1, filepath)
        code2 = get_git_file_content(commit2, filepath)

        semantic_diff(code1, code2, commit1, commit2)
    else:
        # File comparison mode
        if not args.file2:
            print("Error: Two files required for comparison")
            print("Usage: semantic_diff.py file1.py file2.py")
            sys.exit(1)

        code1 = read_file(args.file1)
        code2 = read_file(args.file2)

        semantic_diff(code1, code2, args.file1, args.file2)


if __name__ == "__main__":
    main()
