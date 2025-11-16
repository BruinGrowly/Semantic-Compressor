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
                'filename': filename,
                'lines': 0,
                'ljpw': {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0},
                'health': 0.0,
                'insights': ['ERROR: None input provided'],
                'distance_from_ne': self._distance_from_ne(0, 0, 0, 0),
                'error': 'None input'
            }

        # Edge case: Invalid type
        if not isinstance(code, str):
            return {
                'filename': filename,
                'lines': 0,
                'ljpw': {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0},
                'health': 0.0,
                'insights': [f'ERROR: Expected str, got {type(code).__name__}'],
                'distance_from_ne': self._distance_from_ne(0, 0, 0, 0),
                'error': f'Invalid type: {type(code).__name__}'
            }

        # Edge case: Extremely large file (>10MB)
        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        if len(code) > MAX_SIZE:
            return {
                'filename': filename,
                'lines': 0,
                'ljpw': {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0},
                'health': 0.0,
                'insights': [f'ERROR: File too large ({len(code)} bytes > {MAX_SIZE} bytes)'],
                'distance_from_ne': self._distance_from_ne(0, 0, 0, 0),
                'error': 'File too large'
            }

        # Edge case: Binary data detection (lots of null bytes or non-printable chars)
        try:
            # Check for excessive null bytes or control characters
            null_count = code.count('\x00')
            if null_count > len(code) * 0.1:  # More than 10% null bytes
                return {
                    'filename': filename,
                    'lines': 0,
                    'ljpw': {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0},
                    'health': 0.0,
                    'insights': ['ERROR: Binary data detected (too many null bytes)'],
                    'distance_from_ne': self._distance_from_ne(0, 0, 0, 0),
                    'error': 'Binary data'
                }
        except Exception:
            pass  # Continue if check fails

        # Process code normally
        try:
            lines = code.split('\n')
            code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        except Exception as e:
            return {
                'filename': filename,
                'lines': 0,
                'ljpw': {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0},
                'health': 0.0,
                'insights': [f'ERROR: Failed to parse code: {str(e)}'],
                'distance_from_ne': self._distance_from_ne(0, 0, 0, 0),
                'error': f'Parse error: {str(e)}'
            }

        if code_lines == 0:
            return {
                'filename': filename,
                'lines': 0,
                'ljpw': {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0},
                'health': 0.0,
                'insights': ['Empty file - no code to analyze'],
                'distance_from_ne': self._distance_from_ne(0, 0, 0, 0)
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
    from pathlib import Path
    path = Path(filepath)

    if not path.exists():
        return {
            'filename': filepath,
            'error': 'File not found',
            'lines': 0,
            'ljpw': {'L': 0, 'J': 0, 'P': 0, 'W': 0},
            'health': 0,
            'insights': [f'ERROR: File not found: {filepath}'],
            'distance_from_ne': 0
        }

    if not path.is_file():
        return {
            'filename': filepath,
            'error': 'Not a file',
            'lines': 0,
            'ljpw': {'L': 0, 'J': 0, 'P': 0, 'W': 0},
            'health': 0,
            'insights': [f'ERROR: Not a file: {filepath}'],
            'distance_from_ne': 0
        }

    # Try reading with UTF-8, fall back to other encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    code = None
    used_encoding = None

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                code = f.read()
            used_encoding = encoding
            break
        except UnicodeDecodeError:
            continue
        except PermissionError:
            return {
                'filename': filepath,
                'error': 'Permission denied',
                'lines': 0,
                'ljpw': {'L': 0, 'J': 0, 'P': 0, 'W': 0},
                'health': 0,
                'insights': [f'ERROR: Permission denied: {filepath}'],
                'distance_from_ne': 0
            }
        except Exception as e:
            return {
                'filename': filepath,
                'error': str(e),
                'lines': 0,
                'ljpw': {'L': 0, 'J': 0, 'P': 0, 'W': 0},
                'health': 0,
                'insights': [f'ERROR: {str(e)}'],
                'distance_from_ne': 0
            }

    if code is None:
        return {
            'filename': filepath,
            'error': 'Encoding error',
            'lines': 0,
            'ljpw': {'L': 0, 'J': 0, 'P': 0, 'W': 0},
            'health': 0,
            'insights': [f'ERROR: Could not decode file with any known encoding'],
            'distance_from_ne': 0
        }

    analyzer = SimpleCodeAnalyzer()
    result = analyzer.analyze(code, filepath)

    # Add encoding info if not UTF-8
    if used_encoding != 'utf-8':
        result['encoding'] = used_encoding
        if 'insights' not in result:
            result['insights'] = []
        result['insights'].append(f'NOTE: File encoded as {used_encoding}, not UTF-8')

    return result

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

def calculate_distance(coords1: Tuple[float, float, float, float],
                      coords2: Tuple[float, float, float, float]) -> float:
    """Calculate Euclidean distance between two LJPW coordinates"""
    L1, J1, P1, W1 = coords1
    L2, J2, P2, W2 = coords2
    return math.sqrt((L1-L2)**2 + (J1-J2)**2 + (P1-P2)**2 + (W1-W2)**2)

def calculate_file_distance(file1: str, file2: str) -> Dict:
    """Calculate semantic distance between two files"""
    # Analyze both files
    result1 = analyze_file(file1)
    result2 = analyze_file(file2)

    # Check for errors
    if 'error' in result1:
        return {'error': f"Failed to analyze {file1}: {result1['error']}"}
    if 'error' in result2:
        return {'error': f"Failed to analyze {file2}: {result2['error']}"}

    # Extract coordinates
    coords1 = (result1['ljpw']['L'], result1['ljpw']['J'],
               result1['ljpw']['P'], result1['ljpw']['W'])
    coords2 = (result2['ljpw']['L'], result2['ljpw']['J'],
               result2['ljpw']['P'], result2['ljpw']['W'])

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
        'file1': file1,
        'file2': file2,
        'coords1': coords1,
        'coords2': coords2,
        'distance': distance,
        'similarity': similarity,
        'interpretation': interpretation,
        'result1': result1,
        'result2': result2
    }

def format_distance_result(result: Dict) -> str:
    """Format distance calculation result for display"""
    if 'error' in result:
        return f"\nError: {result['error']}\n"

    output = []
    output.append("\n" + "=" * 70)
    output.append("LJPW Semantic Distance Analysis")
    output.append("=" * 70)

    # File 1
    output.append(f"\nFile 1: {result['file1']}")
    L1, J1, P1, W1 = result['coords1']
    output.append(f"  Coordinates: L={L1:.2f}, J={J1:.2f}, P={P1:.2f}, W={W1:.2f}")
    output.append(f"  Health: {result['result1']['health']:.0%}")

    # File 2
    output.append(f"\nFile 2: {result['file2']}")
    L2, J2, P2, W2 = result['coords2']
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
        ('Safety', abs(L1-L2), 'more' if L1 > L2 else 'less'),
        ('Structure', abs(J1-J2), 'more' if J1 > J2 else 'less'),
        ('Performance', abs(P1-P2), 'more' if P1 > P2 else 'less'),
        ('Design quality', abs(W1-W2), 'better' if W1 > W2 else 'worse')
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

def format_distance_result_json(result: Dict) -> str:
    """Format distance calculation result as JSON"""
    # Create clean JSON output (remove full analysis results, keep key info)
    json_result = {
        'file1': result.get('file1'),
        'file2': result.get('file2'),
        'coordinates': {
            'file1': {
                'L': result['coords1'][0],
                'J': result['coords1'][1],
                'P': result['coords1'][2],
                'W': result['coords1'][3]
            },
            'file2': {
                'L': result['coords2'][0],
                'J': result['coords2'][1],
                'P': result['coords2'][2],
                'W': result['coords2'][3]
            }
        },
        'health': {
            'file1': result['result1']['health'],
            'file2': result['result2']['health']
        },
        'distance': result['distance'],
        'similarity': result['similarity'],
        'interpretation': result['interpretation'],
        'differences': {
            'Love': abs(result['coords1'][0] - result['coords2'][0]),
            'Justice': abs(result['coords1'][1] - result['coords2'][1]),
            'Power': abs(result['coords1'][2] - result['coords2'][2]),
            'Wisdom': abs(result['coords1'][3] - result['coords2'][3])
        }
    }

    if 'error' in result:
        json_result = {'error': result['error']}

    return json.dumps(json_result, indent=2)

def calculate_batch_distance(files: List[str]) -> Dict:
    """
    Calculate distances between multiple files.
    Returns a distance matrix and analysis for all pairs.
    """
    if len(files) < 2:
        return {'error': 'Need at least 2 files for distance calculation'}

    # Analyze all files
    analyses = {}
    for filepath in files:
        result = analyze_file(filepath)
        if 'error' in result:
            return {'error': f"Failed to analyze {filepath}: {result['error']}"}
        analyses[filepath] = result

    # Build distance matrix
    n = len(files)
    distance_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i+1, n):
            file1 = files[i]
            file2 = files[j]

            coords1 = (analyses[file1]['ljpw']['L'], analyses[file1]['ljpw']['J'],
                      analyses[file1]['ljpw']['P'], analyses[file1]['ljpw']['W'])
            coords2 = (analyses[file2]['ljpw']['L'], analyses[file2]['ljpw']['J'],
                      analyses[file2]['ljpw']['P'], analyses[file2]['ljpw']['W'])

            dist = calculate_distance(coords1, coords2)
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist

    # Find most similar and most different pairs
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            pairs.append((files[i], files[j], distance_matrix[i][j]))

    pairs.sort(key=lambda x: x[2])

    return {
        'files': files,
        'analyses': analyses,
        'distance_matrix': distance_matrix,
        'most_similar': pairs[0] if pairs else None,
        'most_different': pairs[-1] if pairs else None,
        'all_pairs': pairs
    }

def format_batch_distance_result(result: Dict) -> str:
    """Format batch distance calculation result for display"""
    if 'error' in result:
        return f"\nError: {result['error']}\n"

    output = []
    output.append("\n" + "=" * 70)
    output.append("LJPW Batch Semantic Distance Analysis")
    output.append("=" * 70)

    files = result['files']
    n = len(files)

    # Show file coordinates
    output.append(f"\nAnalyzed {n} files:\n")
    for i, filepath in enumerate(files):
        analysis = result['analyses'][filepath]
        coords = (analysis['ljpw']['L'], analysis['ljpw']['J'],
                 analysis['ljpw']['P'], analysis['ljpw']['W'])
        output.append(f"{i+1}. {filepath}")
        output.append(f"   L={coords[0]:.2f}, J={coords[1]:.2f}, P={coords[2]:.2f}, W={coords[3]:.2f}")
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
    if result['most_similar']:
        file1, file2, dist = result['most_similar']
        output.append(f"\nMost Similar: {file1} ↔ {file2}")
        output.append(f"  Distance: {dist:.3f}")

    if result['most_different']:
        file1, file2, dist = result['most_different']
        output.append(f"\nMost Different: {file1} ↔ {file2}")
        output.append(f"  Distance: {dist:.3f}")

    output.append("\n" + "=" * 70)

    return "\n".join(output)

def format_batch_distance_result_json(result: Dict) -> str:
    """Format batch distance calculation result as JSON"""
    if 'error' in result:
        return json.dumps({'error': result['error']}, indent=2)

    # Create clean JSON structure
    json_result = {
        'files': result['files'],
        'coordinates': {},
        'health': {},
        'distance_matrix': result['distance_matrix'],
        'most_similar': {
            'file1': result['most_similar'][0],
            'file2': result['most_similar'][1],
            'distance': result['most_similar'][2]
        } if result['most_similar'] else None,
        'most_different': {
            'file1': result['most_different'][0],
            'file2': result['most_different'][1],
            'distance': result['most_different'][2]
        } if result['most_different'] else None
    }

    # Add coordinates for each file
    for filepath in result['files']:
        analysis = result['analyses'][filepath]
        json_result['coordinates'][filepath] = {
            'L': analysis['ljpw']['L'],
            'J': analysis['ljpw']['J'],
            'P': analysis['ljpw']['P'],
            'W': analysis['ljpw']['W']
        }
        json_result['health'][filepath] = analysis['health']

    return json.dumps(json_result, indent=2)

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
    Version 1.1
        """)
        return

    command = sys.argv[1]

    if command == 'help':
        # Show help text (already printed above)
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

    elif command == 'distance':
        if len(sys.argv) < 4:
            print("Error: Please provide at least two files to compare")
            print("Usage: python ljpw_standalone.py distance <file1> <file2> [file3...] [--json] [--save <filename>]")
            return

        # Parse arguments
        files = []
        use_json = False
        save_file = None
        i = 2

        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == '--json':
                use_json = True
                i += 1
            elif arg == '--save':
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
                with open(save_file, 'w') as f:
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
                with open(save_file, 'w') as f:
                    f.write(output)
                print(f"\nResults saved to {save_file}")

    else:
        print(f"Unknown command: {command}")
        print("Use 'python ljpw_standalone.py help' for usage")

if __name__ == '__main__':
    main()
