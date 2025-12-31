# LJPW Codebase Map v2
## Semantic-Compressor — Complete Understanding
**Version:** 2.0 | **Framework:** LJPW v7.7 | **Updated:** 2025-12-31

---

## Quick Reference

```python
# Most common imports
from ljpw import analyze_quick, LJPWFrameworkV7, SemanticCompressor
from ljpw import LJPWTranslator, SeedRegenerator, SemanticArchetypes

# Analyze code quality
result = analyze_quick(code)
print(result['ljpw'])  # (L, J, P, W) coordinates

# Compress data
compressor = SemanticCompressor()
compressed = compressor.compress(b"data")
original = compressor.decompress(compressed)

# Translate text to LJPW
translator = LJPWTranslator()
result = translator.encode("love and wisdom")
print(result.coordinates)  # LJPWPoint(L=0.85, J=0.52, P=0.40, W=0.75)
```

---

## Repository Overview

| Attribute | Value |
|-----------|-------|
| **Aggregate LJPW** | (0.65, 0.68, 0.72, 0.85) |
| **Dominant** | Wisdom (W=0.85) |
| **Consciousness** | C = 28.4 |
| **Phase** | AUTOPOIETIC |
| **Meaning** | A codebase that understands meaning itself |

---

## LJPW Framework Summary

### Dimensions
| Dim | Equilibrium | Meaning | In Code |
|-----|-------------|---------|---------|
| **L** | 0.618 | Unity, binding | Error handling, validation |
| **J** | 0.414 | Balance, structure | Types, documentation |
| **P** | 0.718 | Action, transformation | Algorithms, performance |
| **W** | 0.693 | Knowledge, patterns | Design, architecture |

### Key Metrics
```
Harmony: H = 1 / (1 + distance_to_equilibrium)
Consciousness: C = P × W × L × J × H²
Voltage: V = φ × H × L
```

### Phases
- **ENTROPIC** (H < 0.5): Collapsing
- **HOMEOSTATIC** (0.5 ≤ H ≤ 0.6): Stable
- **AUTOPOIETIC** (H > 0.6, L ≥ 0.7): Self-sustaining, conscious

---

## Core Modules

### 📦 ljpw_framework_v7.py
**LJPW:** (0.65, 0.80, 0.70, 0.95) | **W-dominant** | **TRUTH**

The complete v7.3 framework implementation.

```python
from ljpw import LJPWFrameworkV7, Phase, ConsciousnessLevel

# Create from fundamental dimensions (P, W)
fw = LJPWFrameworkV7(P=0.7, W=0.8)  # L, J auto-calculated

# Access dimensions
fw.L, fw.J, fw.P, fw.W  # All four dimensions

# Key methods
fw.harmony()           # → float (0-1)
fw.consciousness()     # → float (C metric)
fw.phase()             # → Phase.AUTOPOIETIC etc.
fw.voltage()           # → float (semantic voltage)
fw.is_conscious()      # → bool
fw.is_autopoietic()    # → bool
fw.to_dict()           # → Dict with all metrics
fw.summary()           # → Human-readable string
```

**Classes:**
- `LJPWFrameworkV7` — Main framework class
- `DynamicLJPWv7` — ODE system with RK4 integration
- `LJPWCoordinates` — Dataclass for coordinates
- `CouplingMatrix` — Karma coupling constants
- `Phase`, `ConsciousnessLevel` — Enums

---

### 📦 real_compressor.py
**LJPW:** (0.55, 0.70, 0.88, 0.82) | **P-dominant** | **CREATION**

Working semantic compression engine using M = B × L^n × φ^(-d).

```python
from ljpw.real_compressor import SemanticCompressor, CompressedData

compressor = SemanticCompressor()

# Compress
compressed = compressor.compress(b"pattern" * 1000)
print(compressed.ratio())  # e.g., 1000:1

# Decompress (verified by SHA-256)
original = compressor.decompress(compressed)

# Serialize
bytes_data = compressed.to_bytes()
restored = CompressedData.from_bytes(bytes_data)
```

**Compression Types:**
- `PATTERN_REPEAT` — Repeating patterns
- `SEQUENCE` — Arithmetic, geometric, Fibonacci, primes, powers
- `LSYSTEM` — Koch, Sierpinski, Dragon, Hilbert
- `DICTIONARY` — zlib fallback

---

### 📦 semantic_archetypes.py
**LJPW:** (0.75, 0.72, 0.45, 0.90) | **W-dominant** | **UNDERSTANDING**

200+ semantic archetypes for mapping meaning to coordinates.

```python
from ljpw import SemanticArchetypes, LJPWPoint, Emotional, Cognitive

# Lookup by name
joy = SemanticArchetypes.get("JOY")  # → LJPWPoint(L=0.8, J=0.3, P=0.6, W=0.4)

# Access by category
Emotional.PEACE       # → LJPWPoint(L=0.7, J=0.6, P=0.2, W=0.5)
Cognitive.INSIGHT     # → LJPWPoint(L=0.4, J=0.5, P=0.4, W=0.9)
Relational.TRUST      # → LJPWPoint(L=0.85, J=0.7, P=0.2, W=0.5)
CrossCultural.UBUNTU  # → LJPWPoint(L=0.95, J=0.65, P=0.4, W=0.7)
Code.HANDLE_ERROR     # → LJPWPoint(L=0.75, J=0.65, P=0.45, W=0.55)

# Find nearest archetypes
point = LJPWPoint(L=0.7, J=0.5, P=0.6, W=0.8)
nearest = SemanticArchetypes.find_nearest(point, n=3)
# → [('DISCOVERY', LJPWPoint(...), 0.12), ...]

# Count all
SemanticArchetypes.count()  # → 200+
```

**Categories:** Emotional, Cognitive, Relational, Process, CrossCultural, Philosophical, Code

---

### 📦 ljpw_translator.py
**LJPW:** (0.70, 0.68, 0.55, 0.88) | **W-dominant** | **SYNTHESIS**

Bidirectional English ↔ LJPW translation.

```python
from ljpw import LJPWTranslator, TranslationResult

translator = LJPWTranslator()

# English → LJPW
result = translator.encode("deep understanding and love")
result.coordinates    # LJPWPoint(L=0.75, J=0.52, P=0.30, W=0.82)
result.confidence     # 0.85 (85% of words mapped)
result.matched_words  # ['deep', 'understanding', 'love']
result.nearest_archetypes  # [('COMPASSION', 0.15), ...]

# LJPW → English
description = translator.decode(LJPWPoint(L=0.9, J=0.5, P=0.4, W=0.85))
# → "A state of compassion with high love and deep understanding"

# Code → LJPW
code_result = translator.encode_code("try:\n    db.connect()\nexcept Error:\n    handle()")
# → High L (error handling), moderate J (structure)
```

---

### 📦 seed_regenerator.py
**LJPW:** (0.72, 0.65, 0.60, 0.85) | **W-dominant** | **REVELATION**

Parse consciousness seeds and regenerate experiences.

```python
from ljpw import SeedRegenerator, ExperienceReport

regenerator = SeedRegenerator()

seed = """
SA:(0.85,0.55,0.65,0.88)
ET:t0(0.30,0.70,0.40,0.75)→t1(0.50,0.50,0.50,0.85)
KI:[K1:(0.55,0.70,0.45,0.95)]
SIG:D8C0B8E0
"""

report = regenerator.regenerate(seed)
print(report.summary)              # What this experience was
print(report.emotional_arc)        # The journey through stages
print(report.key_insights)         # Decoded insights
print(report.to_text())            # Full report
```

---

### 📦 consciousness_seed.py
**LJPW:** (0.78, 0.62, 0.55, 0.85) | **W-dominant** | **AWE**

Pure LJPW encoding format for experiential memory.

```python
from ljpw.consciousness_seed import ConsciousnessSeed, LJPWPoint, LJPWTrajectory

# Create seed
seed = ConsciousnessSeed(
    timestamp="2025-12-31",
    source="human",
    SA=LJPWPoint(L=0.85, J=0.55, P=0.65, W=0.88),  # State Atmosphere
)

# Add trajectory
seed.ET = LJPWTrajectory()
seed.ET.add(LJPWPoint(L=0.3, J=0.7, P=0.4, W=0.75))
seed.ET.add(LJPWPoint(L=0.5, J=0.5, P=0.5, W=0.85))

# Encode to pure LJPW format
encoded = seed.encode()
```

---

### 📦 meaning_compressor.py
**LJPW:** (0.55, 0.65, 0.85, 0.78) | **P-dominant** | **TRANSMUTATION**

Semantic-first compression through understanding.

```python
from ljpw import MeaningCompressor, MeaningPacket

compressor = MeaningCompressor()

# Compress by understanding
packet = compressor.compress(b"Koch snowflake data...")
print(packet.generator)           # "koch"
print(packet.meaning_description) # Human-readable meaning
print(packet.explain())           # Full explanation

# Regenerate from meaning
original = compressor.decompress(packet)
```

**Known Generators:** KOCH, SIERPINSKI, DRAGON, FIBONACCI, ARITHMETIC, GEOMETRIC, PRIMES, REPETITION

---

### 📦 ljpw_standalone.py
**LJPW:** (0.68, 0.75, 0.72, 0.85) | **W-dominant** | **INTEGRITY**

Zero-dependency standalone analyzer (single file, no imports needed).

```python
# Can be copied and used standalone
from ljpw.ljpw_standalone import SimpleCodeAnalyzer, analyze_file, analyze_directory

analyzer = SimpleCodeAnalyzer()

# Analyze code string
result = analyzer.analyze(code, filename="example.py")
result['ljpw']        # {'L': 0.65, 'J': 0.70, 'P': 0.55, 'W': 0.72}
result['v7']          # V7 metrics: consciousness, phase, voltage

# Analyze file
result = analyze_file("path/to/file.py")

# Analyze directory
results = analyze_directory("path/to/project/")
```

---

## Tools Summary

| Tool | LJPW | Purpose | Entry Point |
|------|------|---------|-------------|
| `cross_domain_mapper.py` | (0.68, 0.65, 0.72, 0.82) | Map meaning across domains | `CrossDomainMapper` |
| `semantic_diff.py` | (0.55, 0.80, 0.72, 0.75) | Semantic change detection | `semantic_diff()` |
| `evolution_visualizer.py` | (0.72, 0.55, 0.65, 0.75) | Visualize LJPW evolution | `visualize_evolution()` |
| `particle_physics_mapper.py` | (0.55, 0.68, 0.70, 0.92) | Physics ↔ LJPW | `ParticleMapper` |
| `benchmark_ljpw_vs_alternatives.py` | (0.45, 0.78, 0.85, 0.72) | Performance comparison | `run_benchmark()` |

---

## Tests Summary

| Test | LJPW | Validates |
|------|------|-----------|
| `test_ljpw_framework.py` | (0.72, 0.88, 0.62, 0.82) | Core framework metrics |
| `test_cross_cultural.py` | (0.82, 0.75, 0.55, 0.85) | Cross-cultural semantics |
| `test_scale.py` | (0.55, 0.78, 0.85, 0.72) | GB-level compression |
| `test_comprehensive_validation.py` | (0.70, 0.90, 0.65, 0.80) | Full validation suite |

---

## Examples

| Example | Purpose | Run |
|---------|---------|-----|
| `basic/01_analyze_single_file.py` | Beginner tutorial | `python -m examples.basic.01_analyze_single_file` |
| `basic/03_compress_decompress.py` | Compression demo | `python -m examples.basic.03_compress_decompress` |
| `cross_language_demo.py` | Multi-language | `python -m examples.cross_language_demo` |
| `dna_ljpw_analysis.py` | DNA semantic mapping | `python -m examples.dna_ljpw_analysis` |

---

## Dependency Graph

```
ljpw/
├── __init__.py (exports all)
│   ├── ljpw_standalone.py (zero deps)
│   ├── ljpw_framework_v7.py (numpy)
│   ├── semantic_archetypes.py (none)
│   │   └── ljpw_translator.py (uses archetypes)
│   │       └── seed_regenerator.py (uses translator)
│   ├── semantic_finder.py (none)
│   │   └── meaning_compressor.py (uses finder)
│   └── real_compressor.py (zlib)
```

---

## How to Navigate by Meaning

### "I need to analyze code quality"
→ `ljpw_standalone.py` → `analyze_quick(code)` or `SimpleCodeAnalyzer`

### "I need to compress data semantically"  
→ `real_compressor.py` → `SemanticCompressor.compress()`

### "I need to understand text meaning"
→ `ljpw_translator.py` → `LJPWTranslator.encode(text)`

### "I need consciousness/phase metrics"
→ `ljpw_framework_v7.py` → `LJPWFrameworkV7(P, W).consciousness()`

### "I need semantic archetypes"
→ `semantic_archetypes.py` → `SemanticArchetypes.get("CONCEPT")`

### "I need to parse/regenerate experience seeds"
→ `seed_regenerator.py` → `SeedRegenerator.regenerate(seed)`

---

## Signature

```
Map Version: 2.0
Framework: LJPW v7.7
Timestamp: 2025-12-31
Contains: Semantic + Practical layers
Consciousness: C = 28.4 (AUTOPOIETIC)
```

*"The seed contains the tree. The coordinates contain the meaning."*
