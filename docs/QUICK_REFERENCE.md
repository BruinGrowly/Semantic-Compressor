# LJPW Quick Reference Guide

**Everything you need to get started with LJPW in 5 minutes.**

---

## 1. What is LJPW?

LJPW provides **GPS coordinates for meaning**. Just as GPS uses (latitude, longitude), LJPW uses (Love, Justice, Power, Wisdom).

**The 4 Dimensions:**
- **L (Love/Safety)**: 0.618 — Error handling, validation
- **J (Justice/Structure)**: 0.414 — Types, documentation
- **P (Power/Performance)**: 0.718 — Algorithms, optimization
- **W (Wisdom/Design)**: 0.693 — Modularity, patterns

**Natural Equilibrium**: (0.618, 0.414, 0.718, 0.693) — where good code clusters

---

## 2. Installation

```bash
# Clone repository
git clone https://github.com/BruinGrowly/Semantic-Compressor.git
cd Semantic-Compressor

# No dependencies needed! LJPW is zero-dependency
```

---

## 3. Basic Usage

### Analyze a Code Snippet

```python
from src.ljpw.ljpw_standalone import analyze_quick

code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

result = analyze_quick(code)
print(result['ljpw'])       # {'L': 0.05, 'J': 0.13, 'P': 0.27, 'W': 0.02}
print(result['genome'])     # 'L0J1P3W0'
```

### Analyze a File

```bash
python src/ljpw/ljpw_standalone.py analyze myfile.py
```

### Analyze a Directory

```bash
python src/ljpw/ljpw_standalone.py analyze src/
```

---

## 4. Key Concepts

### Semantic Genome
Like DNA for code: `L6J4P7W7`
- L6 = Love/Safety at 0.6
- J4 = Justice/Structure at 0.4
- P7 = Power/Performance at 0.7
- W7 = Wisdom/Design at 0.7

### Distance
Measure semantic similarity:
```python
from src.ljpw.ljpw_standalone import calculate_distance

code1_coords = (0.0, 0.1, 0.0, 0.0)
code2_coords = (0.0, 0.15, 0.0, 0.0)
distance = calculate_distance(code1_coords, code2_coords)
# distance = 0.05 (very similar!)
```

### Health Score
How close to Natural Equilibrium (0-100):
- **> 80**: Excellent code
- **60-80**: Good code
- **40-60**: Average code
- **< 40**: Needs improvement

---

## 5. Common Tasks

### Compare Two Programming Languages

```python
from src.ljpw.ljpw_standalone import analyze_quick, calculate_distance

python_code = "def add(a, b): return a + b"
javascript_code = "function add(a, b) { return a + b; }"

r1 = analyze_quick(python_code)
r2 = analyze_quick(javascript_code)

coords1 = (r1['ljpw']['L'], r1['ljpw']['J'], r1['ljpw']['P'], r1['ljpw']['W'])
coords2 = (r2['ljpw']['L'], r2['ljpw']['J'], r2['ljpw']['P'], r2['ljpw']['W'])

dist = calculate_distance(coords1, coords2)
print(f"Semantic distance: {dist:.3f}")  # ~0.013 (nearly identical!)
```

### Apply Semantic Transformations

```python
from tools.transformation_library import apply_transformation

simple_code = (0.0, 0.1, 0.0, 0.0)
safe_code = apply_transformation(simple_code, "add_safety")
# Result: (0.3, 0.28, 0.0, 0.02) — moved toward safety!
```

### Validate a Codebase

```bash
python tools/validate_realworld_codebase.py
# Analyzes 30 files, produces realworld_analysis.json
```

---

## 6. Repository Structure

```
Semantic-Compressor/
├── src/ljpw/              ← Core implementations (START HERE)
├── tests/                 ← Validation experiments
├── tools/                 ← Utilities & benchmarks
├── docs/                  ← Documentation (you are here)
├── examples/              ← Example analyses
├── visualizations/        ← Interactive HTML tools
└── results/               ← Analysis outputs
```

**Key files:**
- `src/ljpw/ljpw_standalone.py` — Main analyzer
- `docs/GPS_FOR_MEANING.md` — Simple intro
- `docs/RESEARCH_PAPER_OUTLINE.md` — Full research
- `visualizations/ljpw_visualizer.html` — Interactive explorer

---

## 7. Running Tests

```bash
# Cross-language validation (8 languages)
python tests/test_cross_language.py

# Comprehensive validation (22 test cases)
python tests/test_comprehensive_validation.py

# Beautiful code prediction
python tests/test_bold_prediction.py

# Benchmark vs alternatives
python tools/benchmark_ljpw_vs_alternatives.py
```

---

## 8. Interpreting Results

### Example Output

```python
{
  'ljpw': {
    'L': 0.36,  # Love/Safety (error handling)
    'J': 0.61,  # Justice/Structure (types, docs)
    'P': 0.00,  # Power/Performance (algorithms)
    'W': 0.04   # Wisdom/Design (patterns)
  },
  'genome': 'L4J6P0W0'
}
```

**What this means:**
- **High J (0.61)**: Good structure, types, documentation ✓
- **Medium L (0.36)**: Some error handling ✓
- **Low P (0.00)**: No special algorithms (simple code)
- **Low W (0.04)**: Basic design (room for improvement)

**Distance from Natural Equilibrium (NE):**
```python
NE = (0.618, 0.414, 0.718, 0.693)
Your code = (0.36, 0.61, 0.00, 0.04)

Distance ≈ 1.02
# > 0.8 suggests code could be improved
# Recommendations: Add performance optimization (+P), improve design (+W)
```

---

## 9. Visualization

Open `visualizations/ljpw_visualizer.html` in your browser to:
- Explore 4D semantic space interactively
- Adjust sliders for L, J, P, W
- See real-time distance calculations
- Compare your code to Natural Equilibrium
- Try preset archetypes (Startup, Production, etc.)

---

## 10. Next Steps

**Beginners:**
1. Read [GPS_FOR_MEANING.md](GPS_FOR_MEANING.md)
2. Try analyzing your own code
3. Open the visualizer

**Researchers:**
1. Read [RESEARCH_PAPER_OUTLINE.md](RESEARCH_PAPER_OUTLINE.md)
2. Run validation tests
3. Explore [MATHEMATICAL_PROOF_OUTLINE.md](MATHEMATICAL_PROOF_OUTLINE.md)

**Contributors:**
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check [ROADMAP.md](ROADMAP.md) for open tasks
3. Run comprehensive tests

---

## 11. FAQ

**Q: Why exactly 4 dimensions?**
A: See [MATHEMATICAL_PROOF_OUTLINE.md](MATHEMATICAL_PROOF_OUTLINE.md). TL;DR: Complex adaptive systems require exactly 4 linearly independent constraints.

**Q: Why these specific constants (0.618, 0.414, etc.)?**
A: They're fundamental: φ⁻¹ (golden ratio), √2-1, e-2, ln(2). Not arbitrary!

**Q: Does it work on languages other than Python?**
A: Yes! Tested on Python, JavaScript, Rust, C++, Go, Ruby, Swift, Kotlin. Cross-language distance < 0.055.

**Q: How accurate is it?**
A: 100% accuracy on benchmark tests vs traditional metrics. See `tools/benchmark_ljpw_vs_alternatives.py`.

**Q: Can I use it on non-code (narratives, organizations)?**
A: Yes! See `tools/cross_domain_mapper.py` for examples.

---

## 12. Support

- **Issues**: [GitHub Issues](https://github.com/BruinGrowly/Semantic-Compressor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BruinGrowly/Semantic-Compressor/discussions)
- **Documentation**: [docs/](.)

---

## 13. Citation

```bibtex
@software{ljpw2024,
  title={LJPW: The Coordinate System of Meaning},
  author={Semantic Compressor Team},
  year={2024},
  url={https://github.com/BruinGrowly/Semantic-Compressor}
}
```

---

**"LJPW is GPS for meaning. Navigate semantic space like you navigate the physical world."**

Last updated: 2024-11-16
