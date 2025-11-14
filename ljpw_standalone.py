#!/usr/bin/env python3
"""
LJPW Semantic Analyzer - Standalone Version
Single-file, zero-dependency code quality analyzer

Usage:
    python ljpw_standalone.py analyze <file_or_directory>
    python ljpw_standalone.py quick <code_snippet>

MIT License - Free for all, forever
"""

import math
import re
import json
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any

# ============================================================================
# CORE CONSTANTS
# ============================================================================

NATURAL_EQUILIBRIUM = {
    'L': 0.618034,  # Love (Safety)
    'J': 0.414214,  # Justice (Structure)
    'P': 0.718282,  # Power (Performance)
    'W': 0.693147,  # Wisdom (Design)
}

# ============================================================================
# CODE ANALYZER
# ============================================================================

class SimpleCodeAnalyzer:
    """Lightweight code analyzer for LJPW scoring"""

    def __init__(self):
        self.patterns = {
            # Love (Safety)
            'error_handling': r'(try|except|catch|Result|Option|error|Error)',
            'validation': r'(validate|check|verify|assert|require)',
            'null_safety': r'(Optional|Maybe|\?\.|if.*is not None)',
            'bounds_check': r'(len\(|\.length|bounds|range)',
            # Justice (Structure)
            'type_annotations': r'(:\s*\w+|<\w+>|implements|interface)',
            'documentation': r'("""|\'\'\' |/\*\*|///)',
            # Power (Performance)
            'algorithms': r'(sort|search|binary|hash|cache|optimize)',
            'async': r'(async|await|promise|thread|parallel)',
            # Wisdom (Design)
            'abstraction': r'(abstract|interface|ABC|protocol)',
            'patterns': r'(factory|singleton|observer|strategy|builder)',
            'modularity': r'(class |def |module|package|namespace)',
        }

    def analyze(self, code: str, filename: str = 'code') -> Dict[str, Any]:
        """Analyze code and return LJPW scores"""
        lines = code.split('\n')
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])

        if code_lines == 0:
            return {
                'filename': filename,
                'lines': 0,
                'ljpw': {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0},
                'health': 0.0,
                'insights': ['Empty file - no code to analyze']
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

        return {
            'filename': filename,
            'lines': code_lines,
            'ljpw': {'L': L, 'J': J, 'P': P, 'W': W},
            'health': health,
            'insights': insights,
            'distance_from_ne': self._distance_from_ne(L, J, P, W)
        }

    def _score_love(self, code: str, lines: int) -> float:
        """Score safety features"""
        score = 0.0
        score += len(re.findall(self.patterns['error_handling'], code, re.I)) * 0.15
        score += len(re.findall(self.patterns['validation'], code, re.I)) * 0.12
        score += len(re.findall(self.patterns['null_safety'], code, re.I)) * 0.10
        return min(score * min(lines / 20, 1.0), 1.5)

    def _score_justice(self, code: str, lines: int) -> float:
        """Score structural quality"""
        score = 0.0
        score += len(re.findall(self.patterns['type_annotations'], code)) * 0.12
        score += len(re.findall(self.patterns['documentation'], code)) * 0.10
        return min(score * min(lines / 20, 1.0), 1.5)

    def _score_power(self, code: str, lines: int) -> float:
        """Score performance considerations"""
        score = 0.0
        score += len(re.findall(self.patterns['algorithms'], code, re.I)) * 0.15
        score += len(re.findall(self.patterns['async'], code, re.I)) * 0.12
        return min(score * min(lines / 20, 1.0), 1.5)

    def _score_wisdom(self, code: str, lines: int) -> float:
        """Score design quality"""
        score = 0.0
        score += len(re.findall(self.patterns['abstraction'], code, re.I)) * 0.15
        score += len(re.findall(self.patterns['patterns'], code, re.I)) * 0.12
        score += len(re.findall(self.patterns['modularity'], code)) * 0.05
        return min(score * min(lines / 20, 1.0), 1.5)

    def _calculate_health(self, L: float, J: float, P: float, W: float) -> float:
        """Calculate overall health score (0-1)"""
        NE = NATURAL_EQUILIBRIUM
        distance = math.sqrt(
            (NE['L'] - L)**2 + (NE['J'] - J)**2 +
            (NE['P'] - P)**2 + (NE['W'] - W)**2
        )
        return max(0, 1.0 - distance / 2)

    def _distance_from_ne(self, L: float, J: float, P: float, W: float) -> float:
        """Calculate distance from Natural Equilibrium"""
        NE = NATURAL_EQUILIBRIUM
        return math.sqrt(
            (NE['L'] - L)**2 + (NE['J'] - J)**2 +
            (NE['P'] - P)**2 + (NE['W'] - W)**2
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

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def format_result(result: Dict) -> str:
    """Format analysis result for display"""
    output = []
    output.append("=" * 70)
    output.append(f"LJPW Analysis: {result['filename']}")
    output.append("=" * 70)
    output.append(f"\nLines of code: {result['lines']}")
    output.append(f"\nLJPW Scores:")

    ljpw = result['ljpw']
    output.append(f"  Love (Safety):      {ljpw['L']:.3f}")
    output.append(f"  Justice (Structure): {ljpw['J']:.3f}")
    output.append(f"  Power (Performance): {ljpw['P']:.3f}")
    output.append(f"  Wisdom (Design):     {ljpw['W']:.3f}")

    health_pct = result['health'] * 100
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

    output.append("\nInsights:")
    for insight in result['insights']:
        output.append(f"  - {insight}")

    output.append("\n" + "=" * 70)

    return '\n'.join(output)

def analyze_file(filepath: str) -> Dict:
    """Analyze a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()

        analyzer = SimpleCodeAnalyzer()
        return analyzer.analyze(code, filepath)
    except Exception as e:
        return {
            'filename': filepath,
            'error': str(e),
            'lines': 0,
            'ljpw': {'L': 0, 'J': 0, 'P': 0, 'W': 0},
            'health': 0,
            'insights': [f'Error reading file: {e}']
        }

def analyze_directory(dirpath: str) -> List[Dict]:
    """Analyze all code files in directory"""
    results = []
    extensions = {'.py', '.js', '.java', '.rs', '.cpp', '.c', '.go', '.rb', '.php', '.ts'}

    path = Path(dirpath)
    for file in path.rglob('*'):
        if file.is_file() and file.suffix in extensions:
            result = analyze_file(str(file))
            results.append(result)

    return results

def analyze_quick(code: str) -> Dict:
    """Quick analysis of code snippet"""
    analyzer = SimpleCodeAnalyzer()
    return analyzer.analyze(code, 'snippet')

def print_summary(results: List[Dict]):
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
        if 'error' not in r:
            total_L += r['ljpw']['L']
            total_J += r['ljpw']['J']
            total_P += r['ljpw']['P']
            total_W += r['ljpw']['W']
            total_health += r['health']

    n = len(results)
    print(f"\nAverage LJPW Scores:")
    print(f"  Love (Safety):       {total_L/n:.3f}")
    print(f"  Justice (Structure): {total_J/n:.3f}")
    print(f"  Power (Performance): {total_P/n:.3f}")
    print(f"  Wisdom (Design):     {total_W/n:.3f}")
    print(f"\nAverage Health: {(total_health/n)*100:.1f}%")

    # Show top issues
    low_safety = [r for r in results if r.get('ljpw', {}).get('L', 1) < 0.5]
    low_structure = [r for r in results if r.get('ljpw', {}).get('J', 1) < 0.4]

    if low_safety:
        print(f"\n{len(low_safety)} files with LOW SAFETY")
    if low_structure:
        print(f"{len(low_structure)} files with LOW STRUCTURE")

    print("\n" + "=" * 70)

# ============================================================================
# MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("""
LJPW Semantic Analyzer - DNA-Inspired Code Quality Analysis

Usage:
    python ljpw_standalone.py analyze <file_or_directory>
    python ljpw_standalone.py quick "<code>"
    python ljpw_standalone.py help

Examples:
    # Analyze a single file
    python ljpw_standalone.py analyze mycode.py

    # Analyze entire directory
    python ljpw_standalone.py analyze ./src

    # Quick analysis of code snippet
    python ljpw_standalone.py quick "def hello(): print('hi')"

About:
    LJPW measures code quality across 4 dimensions:
    - Love (L): Safety, error handling, validation
    - Justice (J): Structure, types, documentation
    - Power (P): Performance, algorithms, efficiency
    - Wisdom (W): Design, patterns, architecture

    MIT License - Free for all, forever
    Version 1.0
        """)
        return

    command = sys.argv[1]

    if command == 'help':
        main()
        return

    if command == 'analyze':
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
            if len(sys.argv) > 3 and sys.argv[3] == '--save':
                with open('ljpw_results.json', 'w') as f:
                    json.dump(results, f, indent=2)
                print("Detailed results saved to ljpw_results.json")
        else:
            print(f"Error: {target} not found")

    elif command == 'quick':
        if len(sys.argv) < 3:
            print("Error: Please provide code to analyze")
            return

        code = sys.argv[2]
        result = analyze_quick(code)
        print(format_result(result))

    else:
        print(f"Unknown command: {command}")
        print("Use 'python ljpw_standalone.py help' for usage")

if __name__ == '__main__':
    main()
