#!/usr/bin/env python3
"""
Integration Example: Pre-commit Hook

This script can be used as a git pre-commit hook to:
- Analyze code being committed
- Block commits with low health scores
- Provide immediate feedback

Setup:
    1. Copy this file to .git/hooks/pre-commit
    2. Make it executable: chmod +x .git/hooks/pre-commit
    3. Adjust HEALTH_THRESHOLD as needed

Or use directly:
    python pre_commit_hook.py --check
"""

import subprocess
import sys
from pathlib import Path

# Add parent directory to path for src module imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ljpw.ljpw_standalone import SimpleCodeAnalyzer

# Configuration
HEALTH_THRESHOLD = 0.50  # 50% minimum health
STRICT_MODE = False  # If True, also check individual dimensions


def get_staged_files():
    """Get list of staged Python files"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = result.stdout.strip().split("\n")
        # Filter for code files
        code_extensions = {".py", ".js", ".java", ".rs", ".go", ".cpp", ".c", ".ts"}
        return [f for f in files if Path(f).suffix in code_extensions and Path(f).exists()]
    except subprocess.CalledProcessError:
        return []


def check_file_quality(filepath):
    """Check if file meets quality standards"""
    analyzer = SimpleCodeAnalyzer()

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        result = analyzer.analyze(code, filepath)

        # Check health threshold
        health = result["health"]
        ljpw = result["ljpw"]

        issues = []

        if health < HEALTH_THRESHOLD:
            issues.append(f"Health {health*100:.1f}% < {HEALTH_THRESHOLD*100:.0f}% threshold")

        if STRICT_MODE:
            # Check individual dimensions
            if ljpw["L"] < 0.3:
                issues.append("CRITICAL: Very low safety (L<0.3)")
            if ljpw["J"] < 0.2:
                issues.append("CRITICAL: Very low structure (J<0.2)")

        return {
            "filepath": filepath,
            "health": health,
            "ljpw": ljpw,
            "issues": issues,
            "passes": len(issues) == 0,
        }

    except Exception as e:
        return {
            "filepath": filepath,
            "health": 0,
            "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0},
            "issues": [f"Error analyzing: {e}"],
            "passes": True,  # Don't block on analysis errors
        }


def main():
    print("=" * 70)
    print("LJPW Pre-commit Hook")
    print("=" * 70)
    print()

    # Get staged files
    staged_files = get_staged_files()

    if not staged_files:
        print("No code files to check")
        return 0

    print(f"Checking {len(staged_files)} staged file(s)...")
    print()

    # Analyze each file
    results = []
    for filepath in staged_files:
        result = check_file_quality(filepath)
        results.append(result)

    # Print results
    failed_files = [r for r in results if not r["passes"]]

    if failed_files:
        print("❌ COMMIT BLOCKED - Quality issues found:")
        print("-" * 70)

        for result in failed_files:
            print(f"\n{result['filepath']}:")
            print(f"  Health: {result['health']*100:.1f}%")
            ljpw = result["ljpw"]
            print(
                f"  LJPW: L={ljpw['L']:.2f}, J={ljpw['J']:.2f}, P={ljpw['P']:.2f}, W={ljpw['W']:.2f}"
            )

            print("  Issues:")
            for issue in result["issues"]:
                print(f"    - {issue}")

            print("\n  Suggestions:")
            if ljpw["L"] < 0.5:
                print("    - Add error handling (try/except)")
                print("    - Add input validation")
            if ljpw["J"] < 0.4:
                print("    - Add type annotations")
                print("    - Add docstrings")
            if ljpw["W"] < 0.5:
                print("    - Refactor into smaller functions")
                print("    - Add abstractions")

        print()
        print("-" * 70)
        print("Fix the issues above and try again")
        print(f"Or bypass check with: git commit --no-verify")
        print("=" * 70)
        return 1

    else:
        print("✅ All files pass quality check!")
        print("-" * 70)

        for result in results:
            ljpw = result["ljpw"]
            print(f"{result['filepath']}: {result['health']*100:.1f}%")
            print(f"  L={ljpw['L']:.2f}, J={ljpw['J']:.2f}, P={ljpw['P']:.2f}, W={ljpw['W']:.2f}")

        print()
        print("=" * 70)
        print("Proceeding with commit...")
        return 0


if __name__ == "__main__":
    sys.exit(main())
