# LJPW Python API Reference

**Complete reference for using LJPW programmatically**

Version: 1.0
Last Updated: November 2025

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Modules](#core-modules)
3. [SimpleCodeAnalyzer](#simplecodeanalyzer)
4. [SemanticCompressor](#semanticcompressor)
5. [SemanticDecompressor](#semanticdecompressor)
6. [Data Structures](#data-structures)
7. [Constants](#constants)
8. [Utilities](#utilities)
9. [Examples](#examples)

---

## Quick Start

### Basic Analysis

```python
from ljpw_standalone import SimpleCodeAnalyzer

analyzer = SimpleCodeAnalyzer()
code = """
def process(data: list) -> list:
    if not data:
        raise ValueError("Empty data")
    return [x * 2 for x in data]
"""

result = analyzer.analyze(code, filename="example.py")
print(f"Health: {result['health'] * 100:.1f}%")
print(f"LJPW: L={result['ljpw']['L']:.2f}, J={result['ljpw']['J']:.2f}")
```

### Semantic Compression

```python
from ljpw_semantic_compressor import SemanticCompressor, SemanticDecompressor

# Compress LJPW state sequence
compressor = SemanticCompressor()
states = [(0.6, 0.4, 0.7, 0.7), (0.62, 0.41, 0.72, 0.69)]
genome = compressor.compress_state_sequence(states)

# Decompress
decompressor = SemanticDecompressor()
reconstructed = decompressor.decompress_genome(genome)
```

---

## Core Modules

### ljpw_standalone.py

Single-file analyzer with zero dependencies. Perfect for:
- Quick code analysis
- Command-line usage
- Embedding in other tools
- Minimal installations

### ljpw_semantic_compressor.py

DNA-inspired compression engine. Features:
- 4-letter LJPW encoding
- Complementary pairing
- Error correction
- Codon-based compression

### ljpw_pipeline.py

Full pipeline orchestrator. Includes:
- Multi-file analysis
- Batch processing
- Result aggregation
- Export capabilities

---

## SimpleCodeAnalyzer

**Module:** `ljpw_standalone.py`

The main code analysis class for calculating LJPW scores.

### Constructor

```python
analyzer = SimpleCodeAnalyzer()
```

**Parameters:** None

**Returns:** SimpleCodeAnalyzer instance

### Methods

#### analyze()

Analyze code and return LJPW scores.

```python
result = analyzer.analyze(code: str, filename: str = 'code') -> Dict[str, Any]
```

**Parameters:**
- `code` (str): Source code to analyze
- `filename` (str, optional): Name for display purposes. Default: 'code'

**Returns:** Dictionary with:
- `filename` (str): Name of analyzed file
- `lines` (int): Number of code lines (excluding blanks/comments)
- `ljpw` (dict): Scores for L, J, P, W dimensions (0.0-1.5 range)
- `health` (float): Overall health score (0.0-1.0)
- `insights` (list): Actionable recommendations
- `distance_from_ne` (float): Distance from Natural Equilibrium

**Example:**
```python
result = analyzer.analyze("def hello(): pass")
# {
#   'filename': 'code',
#   'lines': 1,
#   'ljpw': {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.15},
#   'health': 0.42,
#   'insights': ['LOW SAFETY: Add error handling...'],
#   'distance_from_ne': 1.16
# }
```

---

## SemanticCompressor

**Module:** `ljpw_semantic_compressor.py`

DNA-inspired compression for LJPW state sequences.

### Constructor

```python
compressor = SemanticCompressor(quantization_levels: int = 4)
```

**Parameters:**
- `quantization_levels` (int, optional): Discrete levels per dimension. Default: 4

**Returns:** SemanticCompressor instance

### Methods

#### compress_state_sequence()

Compress LJPW state sequence into semantic genome.

```python
genome = compressor.compress_state_sequence(
    states: List[Tuple[float, float, float, float]],
    metadata: Dict = None
) -> SemanticGenome
```

**Parameters:**
- `states` (List[Tuple]): List of (L, J, P, W) tuples
- `metadata` (Dict, optional): Additional context

**Returns:** SemanticGenome object

**Example:**
```python
states = [
    (0.6, 0.4, 0.7, 0.7),  # State 1
    (0.62, 0.41, 0.72, 0.69)  # State 2
]
genome = compressor.compress_state_sequence(
    states,
    metadata={'project': 'MyApp', 'version': '1.0'}
)
print(f"Compressed to {len(genome)} codons")
```

---

## SemanticDecompressor

**Module:** `ljpw_semantic_compressor.py`

Decompresses semantic genomes with error correction.

### Constructor

```python
decompressor = SemanticDecompressor(quantization_levels: int = 4)
```

**Parameters:**
- `quantization_levels` (int, optional): Must match compressor. Default: 4

### Methods

#### decompress_genome()

Decompress semantic genome to LJPW states.

```python
states = decompressor.decompress_genome(genome: SemanticGenome) -> List[Tuple[float, float, float, float]]
```

**Parameters:**
- `genome` (SemanticGenome): Compressed genome

**Returns:** List of (L, J, P, W) tuples

**Example:**
```python
reconstructed = decompressor.decompress_genome(genome)
for i, (L, J, P, W) in enumerate(reconstructed):
    print(f"State {i}: L={L:.2f}, J={J:.2f}, P={P:.2f}, W={W:.2f}")
```

#### validate_genome()

Validate genome integrity using checksums.

```python
validation = decompressor.validate_genome(genome: SemanticGenome) -> Dict[str, Any]
```

**Returns:** Dictionary with:
- `valid` (bool): True if no errors
- `error_count` (int): Number of checksum mismatches
- `errors` (list): First 10 error descriptions
- `integrity_score` (float): 0.0-1.0 integrity rating

**Example:**
```python
validation = decompressor.validate_genome(genome)
if validation['valid']:
    print("Genome is intact!")
else:
    print(f"Found {validation['error_count']} errors")
```

---

## Data Structures

### SemanticGenome

Container for compressed LJPW sequence.

**Attributes:**
- `codons` (List[LJPWCodon]): Sequence of codons
- `metadata` (Dict): Additional information

**Methods:**

```python
# Convert to compact string
genome_str = genome.to_string()  # "L2J1P3-W2L2P3-..."

# Serialize to JSON
json_str = genome.to_json()

# Deserialize from JSON
genome = SemanticGenome.from_json(json_str)

# Get length
num_codons = len(genome)
```

### LJPWCodon

Single codon encoding semantic primitive.

**Attributes:**
- `base1`, `base2`, `base3` (str): L, J, P, or W
- `level1`, `level2`, `level3` (int): Quantization levels (0-3)

**Methods:**

```python
# String representation
codon_str = codon.to_string()  # "L2J1P3"

# Parse from string
codon = LJPWCodon.from_string("L2J1P3")

# Get complement (using DNA-like pairing)
complement = codon.complement()
```

---

## Constants

### NATURAL_EQUILIBRIUM

Optimal LJPW balance point.

```python
from ljpw_standalone import NATURAL_EQUILIBRIUM

print(NATURAL_EQUILIBRIUM)
# {
#   'L': 0.618034,  # Love (Safety)
#   'J': 0.414214,  # Justice (Structure)
#   'P': 0.718282,  # Power (Performance)
#   'W': 0.693147,  # Wisdom (Design)
# }
```

### LJPWBase (Enum)

The four semantic bases.

```python
from ljpw_semantic_compressor import LJPWBase

print(LJPWBase.L.value)  # 0.618034
print(LJPWBase.J.value)  # 0.414214
```

### COMPLEMENTARY_PAIRS

DNA-like base pairing rules.

```python
from ljpw_semantic_compressor import COMPLEMENTARY_PAIRS

print(COMPLEMENTARY_PAIRS)
# {
#   'L': 'W',  # Love ↔ Wisdom (stable, like G-C)
#   'W': 'L',
#   'P': 'J',  # Power ↔ Justice (dynamic, like A-T)
#   'J': 'P',
# }
```

---

## Utilities

### File Analysis

Analyze single file:

```python
from ljpw_standalone import analyze_file

result = analyze_file('mycode.py')
print(f"Health: {result['health']*100:.1f}%")
```

### Directory Analysis

Analyze all files in directory:

```python
from ljpw_standalone import analyze_directory

results = analyze_directory('./src')
for result in results:
    print(f"{result['filename']}: {result['health']*100:.1f}%")
```

### Quick Snippet Analysis

Analyze code snippet:

```python
from ljpw_standalone import analyze_quick

result = analyze_quick("def test(): pass")
print(result['ljpw'])
```

### Format Output

Format result for display:

```python
from ljpw_standalone import format_result

result = analyzer.analyze(code)
print(format_result(result))
# ======================================================================
# LJPW Analysis: code
# ======================================================================
# ...
```

---

## Examples

### Example 1: Batch File Analysis

```python
from ljpw_standalone import SimpleCodeAnalyzer
from pathlib import Path

analyzer = SimpleCodeAnalyzer()
results = []

for file in Path('./src').rglob('*.py'):
    with open(file) as f:
        code = f.read()
    result = analyzer.analyze(code, str(file))
    results.append(result)

# Find files with low safety
low_safety = [r for r in results if r['ljpw']['L'] < 0.5]
print(f"Found {len(low_safety)} files with low safety")
```

### Example 2: Tracking Code Evolution

```python
from ljpw_semantic_compressor import SemanticCompressor, SemanticDecompressor
from ljpw_standalone import SimpleCodeAnalyzer

analyzer = SimpleCodeAnalyzer()
compressor = SemanticCompressor()

# Analyze code over time
versions = [
    "def process(data): return data * 2",  # v1
    "def process(data): return [x * 2 for x in data]",  # v2
    "def process(data: list) -> list: return [x * 2 for x in data]",  # v3
]

states = []
for i, code in enumerate(versions):
    result = analyzer.analyze(code, f"v{i+1}")
    ljpw = result['ljpw']
    states.append((ljpw['L'], ljpw['J'], ljpw['P'], ljpw['W']))

# Compress evolution
genome = compressor.compress_state_sequence(
    states,
    metadata={'project': 'MyApp', 'versions': len(versions)}
)

print(f"Compressed {len(states)} versions into {len(genome)} codons")
print(f"Genome: {genome.to_string()}")
```

### Example 3: Custom Analysis Pipeline

```python
from ljpw_standalone import SimpleCodeAnalyzer
import json

class CustomAnalyzer:
    def __init__(self):
        self.analyzer = SimpleCodeAnalyzer()
        self.threshold_health = 0.6

    def analyze_project(self, directory):
        from pathlib import Path

        results = []
        for file in Path(directory).rglob('*.py'):
            try:
                with open(file) as f:
                    code = f.read()
                result = self.analyzer.analyze(code, str(file))

                # Add custom metrics
                result['passes_threshold'] = result['health'] >= self.threshold_health
                result['critical_issues'] = self._find_critical_issues(result)

                results.append(result)
            except Exception as e:
                print(f"Error analyzing {file}: {e}")

        return self._generate_report(results)

    def _find_critical_issues(self, result):
        issues = []
        ljpw = result['ljpw']

        if ljpw['L'] < 0.3:
            issues.append("CRITICAL: Very low safety")
        if ljpw['J'] < 0.2:
            issues.append("CRITICAL: Very low structure")
        if ljpw['P'] > 1.0 and ljpw['W'] < 0.4:
            issues.append("WARNING: Performance without design")

        return issues

    def _generate_report(self, results):
        total_files = len(results)
        passing = sum(1 for r in results if r['passes_threshold'])

        avg_health = sum(r['health'] for r in results) / total_files

        return {
            'total_files': total_files,
            'passing': passing,
            'passing_rate': passing / total_files,
            'average_health': avg_health,
            'files_needing_attention': [
                r['filename'] for r in results
                if not r['passes_threshold']
            ]
        }

# Use custom analyzer
custom = CustomAnalyzer()
report = custom.analyze_project('./src')
print(json.dumps(report, indent=2))
```

### Example 4: Integration with CI/CD

```python
#!/usr/bin/env python3
"""
CI/CD Integration Script
Analyzes code and fails if health is below threshold
"""
import sys
from ljpw_standalone import analyze_directory

def main():
    MIN_HEALTH = 0.65  # 65% minimum health

    results = analyze_directory('./src')

    failures = []
    for result in results:
        if result['health'] < MIN_HEALTH:
            failures.append({
                'file': result['filename'],
                'health': result['health'],
                'issues': result['insights']
            })

    if failures:
        print("❌ Code quality check FAILED")
        print(f"\n{len(failures)} files below {MIN_HEALTH*100:.0f}% health:\n")

        for failure in failures:
            print(f"📄 {failure['file']}")
            print(f"   Health: {failure['health']*100:.1f}%")
            for issue in failure['issues']:
                print(f"   - {issue}")
            print()

        sys.exit(1)
    else:
        print("✅ Code quality check PASSED")
        avg_health = sum(r['health'] for r in results) / len(results)
        print(f"Average health: {avg_health*100:.1f}%")
        sys.exit(0)

if __name__ == '__main__':
    main()
```

---

## Error Handling

All API functions handle errors gracefully:

```python
try:
    result = analyzer.analyze(code)
except Exception as e:
    print(f"Analysis failed: {e}")
    # Fallback behavior
```

File operations return error information in results:

```python
result = analyze_file('nonexistent.py')
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Health: {result['health']}")
```

---

## Performance Considerations

### Memory Usage

- SimpleCodeAnalyzer: Minimal (regex-based)
- SemanticCompressor: O(n) where n = number of states
- Large files (>1MB): Consider chunking

### Speed

Typical performance on modern hardware:
- Small files (<10KB): <10ms
- Medium files (100KB): <100ms
- Large files (1MB): <1s
- Directory scan (1000 files): <30s

### Optimization Tips

```python
# Reuse analyzer instance (faster)
analyzer = SimpleCodeAnalyzer()
for file in files:
    result = analyzer.analyze(file)  # ✅

# Don't recreate each time (slower)
for file in files:
    analyzer = SimpleCodeAnalyzer()  # ❌
    result = analyzer.analyze(file)
```

---

## API Stability

**Stable APIs** (won't change):
- `SimpleCodeAnalyzer.analyze()`
- `NATURAL_EQUILIBRIUM` constants
- Core LJPW dimensions (L, J, P, W)

**Evolving APIs** (may change):
- Quantization algorithms
- Pattern matching regexes
- Metadata structures

**Version:** Follow semantic versioning (MAJOR.MINOR.PATCH)

---

## Getting Help

**Documentation:**
- Full guide: [README.md](../README.md)
- Quick start: [docs/QUICKSTART.md](QUICKSTART.md)
- Examples: [docs/00_START_HERE.md](00_START_HERE.md)

**Issues:**
- Bug reports: [GitHub Issues](https://github.com/BruinGrowly/Semantic-Compressor/issues)
- Feature requests: [GitHub Discussions](https://github.com/BruinGrowly/Semantic-Compressor/discussions)

**Community:**
- Share your usage patterns
- Contribute improvements
- Help others learn

---

## License

MIT License - Free for all uses, commercial or personal.

---

**Last Updated:** November 2025
**Version:** 1.0
**Status:** Production Ready
