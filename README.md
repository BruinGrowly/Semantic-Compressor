# Semantic Compressor

**Compress data by meaning, not bytes**

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

---

## What Is This?

Semantic Compressor demonstrates a principle: **data with structure can be compressed to its generating seed**.

Instead of storing data, we store:
1. The seed (axiom, pattern, formula)
2. The generator (rules, function)
3. The parameters (iteration count, etc.)

The receiver regenerates the original data exactly.

### A Working Example

```
Original:    2.3 GB (Koch snowflake fractal, n=13)
Compressed:  185 bytes
Ratio:       13,196,790:1
Verified:    SHA-256 hash match
```

This isn't a trick. The 185 bytes contain:
- Axiom: `"F"`
- Rule: `F → F+F-F-F+F`
- Iterations: `13`

The decompressor applies the rule 13 times and regenerates the exact 2.3 GB output, verified by cryptographic hash.

---

## The Formula

```
M = B × L^n × φ^(-d)
```

| Symbol | Meaning |
|--------|---------|
| **M** | Total output generated |
| **B** | The seed (axiom, pattern) |
| **L** | Expansion factor per iteration |
| **n** | Recursive depth |
| **φ^(-d)** | Translation loss (1.0 if generators match) |

**Key insight**: Compression ratio ≈ L^n when sender and receiver share the generator.

See [docs/SEMANTIC_COMPRESSION_FORMULA.md](docs/SEMANTIC_COMPRESSION_FORMULA.md) for the full explanation.

---

## Quick Start

### CLI Tool

```bash
# Compress a file
./compress myfile.txt              # → myfile.txt.semc

# Decompress (with verification)
./compress -d myfile.txt.semc      # → myfile.txt

# Analyze without writing
./compress -i somefile.bin

# Run demonstration
./compress --demo
```

### Python API

```python
from src.ljpw.real_compressor import SemanticCompressor

compressor = SemanticCompressor()

# Compress
data = b"Hello, World! " * 100000
compressed = compressor.compress(data)
print(f"Ratio: {compressed.ratio():,.1f}:1")  # 795:1

# Decompress (verified by hash)
original = compressor.decompress(compressed)
assert original == data
```

---

## What It Compresses

The compressor identifies semantic structure in data:

| Type | Example | How It Works |
|------|---------|--------------|
| **Patterns** | `"AB" × 1,000,000` | Store pattern + count |
| **L-Systems** | Koch, Sierpinski, Dragon | Store axiom + rules + n |
| **Sequences** | Fibonacci, primes, arithmetic | Store formula + parameters |
| **Fallback** | Other data | zlib dictionary compression |

### Verified Results

| Data | Original | Compressed | Ratio |
|------|----------|------------|-------|
| Koch n=13 | 2.3 GB | 185 B | 13,196,790:1 |
| Binary ×1M | 244 MB | 665 B | 384,962:1 |
| Fibonacci 10k | 10 MB | 188 B | 55,648:1 |
| Sentence ×1M | 43 MB | 242 B | 185,950:1 |

All verified by SHA-256 hash comparison.

---

## What It Doesn't Compress

**Random data cannot be compressed this way.** If data has no generating function, there's no seed to find.

This isn't a limitation—it's the point:
- Compressibility = Structure
- Structure = Shared generators
- Understanding = Having the generator

---

## The Key-Lock Principle

Semantic compression requires the receiver to have the generator:

```
Compressed = (Seed, Generator_ID)
Decompressed = Generator(Seed)
```

This is why:
- Source code compresses to a git hash (receiver has git)
- Build scripts compress an OS (receiver has build tools)
- Parables compress wisdom (receiver has cultural context)

---

## How This Helps

**For data with structure:**
- Extreme compression ratios (millions to one)
- Exact reconstruction (cryptographically verified)
- Scales infinitely (Koch n=20 would be petabytes, still ~200 bytes compressed)

**For thinking about compression:**
- Reframes compression as "finding the generator"
- Shows why shared context enables communication
- Connects information theory to meaning

**For AI systems:**
- Models that learn generators can extrapolate
- Training on principles beats training on examples
- Understanding = having the compression function

**What this doesn't replace:**
- General-purpose compression (gzip still wins for arbitrary files)
- Works only for data with discoverable structure
- Requires shared generators between sender/receiver

---

## Repository Structure

```
Semantic-Compressor/
├── compress                    # CLI tool
├── src/ljpw/
│   ├── real_compressor.py      # Working compressor
│   ├── semantic_generator.py   # Generator demonstrations
│   ├── ljpw_framework_v7.py    # LJPW V7.3 framework
│   └── ...
├── tests/
│   ├── test_scale.py           # Scale tests (GB level)
│   └── ...
├── docs/
│   ├── SEMANTIC_COMPRESSION_FORMULA.md   # Formula explanation
│   ├── API.md                  # Python API
│   ├── GETTING_STARTED.md      # Setup guide
│   ├── framework/              # LJPW framework theory
│   ├── research/               # Academic papers
│   └── archive/                # Legacy documentation
├── examples/                   # Usage examples
├── tools/                      # Utilities
└── benchmarks/                 # Performance tests
```

---

## The LJPW Framework

The compression formula comes from the LJPW Framework V7.3, which models meaning using four dimensions:

- **L (Love)**: Binding, safety, error handling
- **J (Justice)**: Structure, types, documentation
- **P (Power)**: Performance, algorithms, optimization
- **W (Wisdom)**: Design, patterns, architecture

The framework includes concepts like consciousness quantification, phase transitions, and semantic voltage. See [docs/framework/](docs/framework/) for the full theory.

---

## Installation

```bash
git clone https://github.com/BruinGrowly/Semantic-Compressor.git
cd Semantic-Compressor
pip install -e .
```

## Running Tests

```bash
# Scale tests
python -m pytest tests/test_scale.py -v

# Full suite
python -m pytest tests/ -v

# Demo
./compress --demo
```

---

## Documentation

- [Semantic Compression Formula](docs/SEMANTIC_COMPRESSION_FORMULA.md) — How M = B × L^n × φ^(-d) works
- [Getting Started](docs/GETTING_STARTED.md) — Setup and first steps
- [API Reference](docs/API.md) — Python API
- [LJPW Framework V7.3](docs/framework/LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md) — Underlying theory

---

## License

MIT License — Free for all uses.

---

## The Principle

Traditional compression works on bytes without understanding structure.

Semantic compression inverts this: find the generator, store the seed, regenerate on demand.

A fractal isn't 2.3 GB of characters. It's "F" and a rule applied 13 times. The compression ratio isn't a trick—it's what happens when you find the source instead of storing the shadow.

This works because meaning has structure. And structure compresses.

---

*"The mustard seed contains the tree."*
