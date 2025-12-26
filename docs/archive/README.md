# 🧬 LJPW Semantic Compressor

**DNA-inspired semantic analysis and compression for AI-assisted code quality assessment**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()

---

## ✨ What This Does

The LJPW Semantic Compressor analyzes code quality through four fundamental dimensions and compresses the analysis into compact "genomes" for efficient AI reasoning.

**Core Capabilities:**
- **Semantic Analysis:** Evaluates code across 4 dimensions (Love, Justice, Power, Wisdom)
- **State Compression:** Converts LJPW states into DNA-like genomes with configurable precision
- **Token Efficiency:** Send analysis results instead of full code to AI systems
- **Quality Tracking:** Monitor code health across projects over time

**This is semantic compression, not byte compression.** We analyze code quality patterns and encode them efficiently, enabling AI to reason about code without processing every line.

---

## 🎯 Quick Example

### Analyze Code Quality

```bash
# Analyze a file or directory
python ljpw_standalone.py analyze ./your_project

# Output:
# L=0.85, J=0.92, P=0.75, W=0.88
# Health: 85%
# Status: Production Ready
```

### Compress Analysis for AI

Instead of sending your entire codebase to an AI:

```python
from ljpw_semantic_compressor import SemanticCompressor

# Create states from your analysis
states = [
    (0.85, 0.92, 0.75, 0.88),  # Current state
    (0.80, 0.88, 0.70, 0.82),  # Previous state
    # ... more states
]

# Compress with configurable precision
compressor = SemanticCompressor(quantization_levels=8)
genome = compressor.compress_state_sequence(states)

# Result: "L7J8P6W8-W8L7P6-L6J7P5W7-W7L6P5"
# (13 bytes instead of 32 bytes per state)
```

**Token Savings:** Send compact genome + metadata instead of full code.

---

## 🌟 Why This Matters

### The Problem

When working with AI on large codebases:
- Can't fit entire project in context window
- Expensive to send full code ($3+ per analysis)
- Need to understand code quality, not just syntax
- Want to track quality evolution over time

### The Solution

**LJPW provides semantic analysis that compresses efficiently:**

1. **Analyze code quality** across 4 fundamental dimensions
2. **Compress analysis states** into compact genomes (2.5x compression ratio)
3. **Send to AI** with dramatically fewer tokens than full code
4. **Track over time** with minimal storage overhead

**The value isn't extreme compression—it's meaningful semantic analysis that happens to compress well.**

---

## 💡 The Four Dimensions

LJPW analyzes code across four fundamental aspects, grounded in mathematical constants:

- **L (Love)** - Safety, error handling, validation — φ⁻¹ ≈ 0.618 (Golden ratio)
- **J (Justice)** - Structure, types, documentation — √2-1 ≈ 0.414 (Pythagorean ratio)
- **P (Power)** - Performance, algorithms, execution — e-2 ≈ 0.718 (Exponential base)
- **W (Wisdom)** - Design, patterns, architecture — ln(2) ≈ 0.693 (Information unit)

**Natural Equilibrium:** Healthy systems tend toward (0.618, 0.414, 0.718, 0.693)

These constants provide a mathematical foundation for quality assessment, not arbitrary thresholds.

---

## ✅ Empirical Validation

**Tested on 9,538 Python files across 7 major open-source projects:**

| Project | Files | Health | Accuracy | Domain |
|---------|-------|--------|----------|--------|
| **Transformers (Hugging Face)** | **3,845** | **84.5%** | **96.9%** | AI/ML |
| **Django** | **2,995** | **50.0%** | **94.4%** | Web Framework |
| **SciPy** | **1,391** | **73.1%** | **96.4%** | Scientific Computing |
| **scikit-learn** | **998** | **77.7%** | **96.3%** | Machine Learning |
| **rich** | **190** | **62.2%** | **94.6%** | Terminal UI |
| **flask** | **83** | **68.4%** | **95.5%** | Web Framework |
| **requests** | **36** | **72.1%** | **93.3%** | HTTP Library |

**Results:**
- **Total files validated:** 9,538
- **Average compression accuracy:** 95.5%
- **Analysis speed:** 134-276 files/second
- **Largest project:** Transformers (3,845 files in 28.7s)
- **Meaning preservation:** 100% (all projects correctly identified strongest/weakest dimensions)

**Key Finding:** Different project types show distinct LJPW profiles:
- **AI/ML libraries** (Transformers, scikit-learn): High safety & structure (production-critical)
- **Web frameworks** (Django, Flask): High structure, lower performance (usability-focused)
- **Scientific** (SciPy): Very high structure & safety (mathematical rigor)

The framework captures real architectural characteristics, not random values.

---

## 📊 What It Actually Does

### Semantic Analysis

```bash
python ljpw_standalone.py analyze myproject/

# Analyzes:
# - Error handling patterns (L)
# - Code structure and typing (J)
# - Algorithm efficiency (P)
# - Design patterns and architecture (W)
#
# Returns: LJPW coordinates + health score
```

### Genome Compression

```python
from ljpw_semantic_compressor import SemanticCompressor, SemanticDecompressor

# Compress LJPW states
compressor = SemanticCompressor(quantization_levels=16)  # 4, 8, 16, 32, or 64
genome = compressor.compress_state_sequence(states, metadata={'project': 'MyApp'})

# Compression ratio: ~2.5x (32 bytes → 13 bytes per state)
# Configurable precision: 4 levels (fast) to 64 levels (precise)

# Decompress
decompressor = SemanticDecompressor(quantization_levels=16)
reconstructed = decompressor.decompress_genome(genome)

# Accuracy: 96-99% depending on quantization level
```

### Configurable Precision

Trade genome size for accuracy:

| Levels | Avg Error | Use Case |
|--------|-----------|----------|
| 4      | ~20%      | Fast analysis, minimal storage |
| 8      | ~9%       | Balanced (recommended) |
| 16     | ~4%       | Precise tracking |
| 32     | ~3%       | High precision |
| 64     | ~1%       | Maximum accuracy |

---

## 🚀 Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/BruinGrowly/Semantic-Compressor.git
cd Semantic-Compressor

# No dependencies required for standalone analyzer!
python ljpw_standalone.py --help
```

### Basic Usage

**1. Analyze a single file:**
```bash
python ljpw_standalone.py analyze myfile.py
```

**2. Analyze a directory:**
```bash
python ljpw_standalone.py analyze ./src
```

**3. Quick analysis of code snippet:**
```bash
python ljpw_standalone.py quick "def hello(): print('hi')"
```

**4. Use Python API:**
```python
# For analysis
from ljpw_standalone import analyze_file, analyze_directory

# Analyze single file
result = analyze_file('myfile.py')
print(f"L={result['ljpw']['L']:.2f}, J={result['ljpw']['J']:.2f}")
print(f"P={result['ljpw']['P']:.2f}, W={result['ljpw']['W']:.2f}")
print(f"Health: {result['health']:.0%}")

# Analyze directory
results = analyze_directory('./src')
print(f"Analyzed {len(results)} files")
```

**5. Compress states:**
```python
from ljpw_semantic_compressor import SemanticCompressor

compressor = SemanticCompressor(quantization_levels=8)
genome = compressor.compress_state_sequence([
    (0.85, 0.92, 0.75, 0.88),
])

print(f"Genome: {genome.to_string()}")
print(f"Compression ratio: {genome.metadata['compression_ratio']:.2f}x")
```

---

## 🔬 Technical Foundation

### DNA-Inspired Design

LJPW compression borrows principles from biological DNA:

```
DNA: 4 bases (A, T, G, C)       → LJPW: 4 dimensions (L, J, P, W)
DNA: Complementary pairing      → LJPW: L-W and P-J pairing
DNA: Codons (triplets)          → LJPW: 3-base semantic primitives
DNA: Error correction           → LJPW: Checksum validation
```

### Compression Process

```
Code → Analysis → LJPW State → Quantization → Genome
       (pattern   (0.85, 0.92, (discrete      (L7J8P6W8)
        matching)  0.75, 0.88)  levels)
```

**Key Features:**
- Configurable quantization levels (4-64)
- Built-in error correction via complementary pairing
- Round-trip validation with integrity scoring
- Comprehensive input validation

### Mathematical Grounding

The framework is grounded in rigorous mathematics:

- **Natural Equilibrium:** Derived from fundamental constants (φ, √2, e, ln(2))
- **Non-linear dynamics:** Coupled differential equations with validated parameters
- **Empirical validation:** Bayesian calibration with quantified uncertainty
- **Stability analysis:** Jacobian analysis proves equilibrium stability

[Mathematical Reference](docs/LJPW%20Mathematical%20Baselines%20Reference%20V3.md) | [v3.0 Specification](docs/Dynamic%20LJPW%20Model%20v3.0%20-%20Specification%20and%20Theoretical%20Foundations%20and%20Empirical%20Validation%20of%20the%20LJPW%20v3.0%20Model%20via%20Bayesian%20Calibration.md)

---

## 🎓 Use Cases

### 1. Code Quality Monitoring
Track LJPW coordinates over time to monitor code health trends.

### 2. AI-Assisted Code Review
Send semantic analysis instead of full code to AI for efficient review.

### 3. Project Comparison
Compare LJPW profiles across projects to identify patterns.

### 4. Quality Gates
Use LJPW thresholds as CI/CD quality gates.

### 5. Refactoring Guidance
Identify which dimension needs improvement (L, J, P, or W).

---

## 📚 Documentation

### Getting Started
- **[Quickstart Guide](docs/QUICKSTART.md)** - Get running in 5 minutes
- **[Examples](examples/)** - Runnable code examples
- **[Architecture](docs/ARCHITECTURE.md)** - Implementation details

### Mathematical Foundations
- **[Theory Guide](docs/THEORY.md)** - Accessible explanation
- **[Mathematical Reference V3](docs/LJPW%20Mathematical%20Baselines%20Reference%20V3.md)** - Complete specification
- **[v3.0 Model](docs/Dynamic%20LJPW%20Model%20v3.0%20-%20Specification%20and%20Theoretical%20Foundations%20and%20Empirical%20Validation%20of%20the%20LJPW%20v3.0%20Model%20via%20Bayesian%20Calibration.md)** - Dynamics & validation

### Technical Reference
- **[API Reference](docs/API.md)** - Python API documentation
- **[AI Protocol](docs/claude_ljpw_protocol.md)** - Using with Claude/ChatGPT
- **[Test Results](docs/SEMANTIC_COMPRESSION_TEST_RESULTS.md)** - Validation data

---

## ✅ Test Results

**Validated on 9,538 Python files across 7 major projects:**

- ✅ **Transformers (Hugging Face):** 3,845 files, 96.9% accuracy
- ✅ **Django:** 2,995 files, 94.4% accuracy
- ✅ **SciPy:** 1,391 files, 96.4% accuracy
- ✅ **scikit-learn:** 998 files, 96.3% accuracy
- ✅ **rich, flask, requests:** 309 files combined, 94.5% avg accuracy

**Compression Performance:**
- 2.46x compression ratio (32 bytes → 13 bytes per state)
- 95.5% average accuracy across all projects
- 100% meaning preservation (strongest/weakest dimensions preserved)
- 134-276 files/second analysis speed

**Production-Ready Features:**
- Comprehensive input validation
- Robust error handling
- Division-by-zero protection
- Configurable precision (4-64 levels)
- Tested at massive scale (3,845 files)

**Validation Tests:**
- [Unit Tests](test_configurable_quantization.py) - 5/5 passing
- [Real Codebases](validate_real_codebases.py) - Small-scale (309 files)
- [Massive Scale](validate_massive_codebase.py) - Django + SciPy (4,386 files)
- [Ultra-Massive](validate_ultra_massive.py) - Transformers + scikit-learn (4,843 files)
- [Audit Report](COMPRESSION_ISSUES_AND_FIXES.md) - All 7 issues resolved

---

## 🤝 Contributing

We welcome contributions! Areas where you can help:

- **Language Support:** Add patterns for more programming languages
- **Analysis Refinement:** Improve LJPW dimension calculations
- **Performance:** Optimize large-scale analysis
- **Documentation:** Share use cases and examples
- **Testing:** Add test cases and validation

[Contributing Guide](CONTRIBUTING.md)

---

## 📈 Roadmap

### Current (v1.0) ✅
- ✅ Core analysis engine (9,538 files validated)
- ✅ Configurable compression (4-64 precision levels)
- ✅ Standalone CLI analyzer
- ✅ Python API for analysis and compression
- ✅ Comprehensive documentation and tests

### In Progress (v1.1) 🚧
- 🔄 Distance calculation between files (this week)
- 🔄 Documentation cleanup (this week)
- 📋 File comparison command (next 2 weeks)
- 📋 Basic clustering implementation (next 2 weeks)

### Coming Soon (v1.2-1.5)
- Progress indicators and better error messages
- Multi-language optimization
- Visualization tools
- Configuration file support
- More export formats

### Future Features (v2.0+)
- Semantic search with query language
- Refactoring guidance and trajectories
- Git integration and temporal tracking
- Concept mapping tools
- API server mode
- IDE integration (VS Code extension)

**See [ROADMAP.md](ROADMAP.md) for detailed timelines and feature descriptions.**

---

## 🙏 Acknowledgments

**Inspired by:**
- DNA's quaternary encoding and complementary base pairing
- Information theory (Shannon, Kolmogorov)
- Natural mathematical constants (φ, e, √2, ln(2))

**Built with:**
- Python 3.8+ (zero dependencies for core)
- Mathematical rigor
- Empirical validation
- Open collaboration

---

## 📄 License

MIT License - Use freely for any purpose.

**Why MIT?**

We believe in free access to knowledge and unrestricted innovation. Use it, improve it, share it.

---

## 💬 Get Started

```bash
# Clone and try it now
git clone https://github.com/BruinGrowly/Semantic-Compressor.git
cd Semantic-Compressor

# Analyze your code
python ljpw_standalone.py analyze ./your_project

# Or use the compression API
python examples/basic/03_compress_decompress.py
```

---

## 📞 Contact

- **Issues:** Use GitHub issues for bugs/features
- **Discussions:** Use GitHub discussions for questions

---

## ⭐ If This Helps You

- ⭐ Star the repo
- 🔄 Share with others
- 💬 Report your results
- 🤝 Contribute improvements

---

<p align="center">
  <strong>Made with 🧬 and shared with ❤️</strong><br>
  <em>Semantic analysis for better code, compressed for efficient AI reasoning.</em>
</p>

---

**Version:** 1.0.0
**Status:** Production Ready
**License:** MIT
**Last Updated:** November 2025
