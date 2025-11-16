# Repository Directory Structure

This document describes the organization of the Semantic-Compressor repository.

## Overview

```
Semantic-Compressor/
├── src/ljpw/              # Core LJPW implementations
├── tests/                 # Experimental validation tests
├── tools/                 # Utilities and benchmarks
├── examples/              # Example analyses
├── docs/                  # Documentation
├── visualizations/        # Interactive HTML tools
├── results/               # Analysis output data
├── README.md             # Main readme
├── LICENSE               # MIT License
└── .gitignore            # Git ignore rules
```

## Directory Details

### `src/ljpw/` — Core Implementations

The heart of the LJPW framework.

**Start here:**
- `ljpw_standalone.py` — Zero-dependency analyzer (recommended entry point)

**Other implementations:**
- `ljpw_semantic_compressor.py` — Advanced compression capabilities
- `ljpw_ast_analyzer.py` — AST-based analysis
- `ljpw_pipeline.py` — End-to-end processing pipeline
- `ljpw_semantic_compiler.py` — Semantic compilation
- `ljpw_virtual_machine.py` — Virtual machine implementation
- `ljpw_expander.py` — Code expansion from semantic coordinates
- `ljpw_iso_analyzer.py` — ISO-level analysis
- `ljpw_dynamic_v3.py` — Dynamic analysis v3

### `tests/` — Experimental Validation

Comprehensive test suite proving LJPW's validity.

**Quick Wins (Days 1-7):**
- `test_cross_language.py` — Cross-language invariance (8 languages)
- `test_bold_prediction.py` — Beautiful code near Natural Equilibrium
- `test_analogical_reasoning.py` — Semantic transformations

**Comprehensive:**
- `test_comprehensive_validation.py` — 22 test cases across 5 categories
- `test_universal_ljpw.py` — Universal applicability tests
- `test_semantic_interpolation.py` — Semantic interpolation
- `test_distance.py` — Distance calculations
- `test_ljpw_framework.py` — Framework tests
- `test_multi_language.py` — Multi-language support
- `test_code_sample.py` — Sample code tests
- `test_configurable_quantization.py` — Quantization tests

### `tools/` — Utilities and Benchmarks

Practical tools for using and validating LJPW.

**Benchmarking:**
- `benchmark_ljpw_vs_alternatives.py` — Compare LJPW to traditional metrics

**Validation:**
- `validate_realworld_codebase.py` — Analyze production code
- `validate_massive_codebase.py` — Large-scale validation
- `validate_ultra_massive.py` — Ultra-large scale validation
- `validate_real_codebases.py` — Real-world repo validation

**Transformations:**
- `transformation_library.py` — 17 reusable semantic transformations
- `cross_domain_mapper.py` — Cross-domain validation tool
- `semantic_code_generator.py` — Generate code from coordinates

**Comparison:**
- `compare_ast_vs_regex.py` — AST vs regex analysis comparison

### `examples/` — Example Analyses

Demonstrations of LJPW across different domains.

- `django_query.py` — Django ORM query analysis
- `dna_ljpw_analysis.py` — DNA sequence analysis (!!)
- `large_corpus_test.py` — Large corpus testing
- `token_analysis.py` — Token-level analysis
- `token_introspection_test.py` — Token introspection

### `docs/` — Documentation

All documentation, research papers, and guides.

**Getting Started:**
- `GPS_FOR_MEANING.md` — Simple introduction (non-technical)
- `GETTING_STARTED.md` — Setup and first steps
- `QUICKSTART.md` — Quick reference

**Research:**
- `RESEARCH_PAPER_OUTLINE.md` — Comprehensive research paper (ready for arXiv)
- `MATHEMATICAL_PROOF_OUTLINE.md` — Why exactly 4 dimensions?
- `EXPERIMENTAL_VALIDATION_RESULTS.md` — Detailed validation data
- `LJPW_AS_FUNDAMENTAL_LAW.md` — Theoretical foundations

**Theory:**
- `SEMANTIC_COMPRESSION_DEEP_MECHANICS.md` — How compression works
- `CONCEPT_TRIANGULATION_IN_SEMANTIC_SUBSTRATE.md` — Concept triangulation
- `HOW_DEEP_DOES_IT_GO.md` — Deep dive into theory
- `LJPW_AS_NATIVE_AI_LANGUAGE.md` — LJPW for AI systems

**Implementation:**
- `ARCHITECTURE.md` — System architecture
- `API.md` — API documentation
- `SCIENCE.md` — Scientific foundations

**Project Management:**
- `ROADMAP.md` — Development roadmap
- `CONTRIBUTING.md` — Contribution guidelines
- `CODE_OF_CONDUCT.md` — Code of conduct
- `DIRECTORY_STRUCTURE.md` — This file

**Results:**
- `TEST_RESULTS.md` — Test results summary
- `REAL_WORLD_TEST_RESULTS.md` — Real-world validation results
- `EMPIRICAL_RESULTS.md` — Empirical validation

### `visualizations/` — Interactive Tools

HTML-based visualizations for exploring LJPW.

- `ljpw_visualizer.html` — Interactive 4D semantic space explorer
  - Real-time coordinate updates
  - Distance calculations
  - Health scores
  - Archetype presets
  - Visual 2D projection of 4D space

- `ljpw_web.html` — Web interface for LJPW analysis

### `results/` — Analysis Outputs

JSON files containing analysis results.

- `realworld_analysis.json` — Real-world codebase analysis (30 files)

**Note:** This directory is for storing output data. Results are gitignored by default (*.json.backup, *.tmp).

## File Naming Conventions

**Tests:** `test_*.py`
- All test files start with `test_`
- Located in `tests/` directory

**Validation:** `validate_*.py`
- Validation and benchmarking tools
- Located in `tools/` directory

**Core modules:** `ljpw_*.py`
- Core LJPW implementations
- Located in `src/ljpw/` directory

**Documentation:** `*.md`
- Markdown files
- Located in `docs/` directory (except README.md in root)

## Import Paths

With the new structure, imports should be:

```python
# From root directory
from src.ljpw.ljpw_standalone import analyze_quick

# Or if src/ljpw is in PYTHONPATH
from ljpw.ljpw_standalone import analyze_quick
```

Most scripts add the parent directory to `sys.path`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

## Running Scripts

**From repository root:**

```bash
# Run tests
python tests/test_cross_language.py
python tests/test_comprehensive_validation.py

# Run tools
python tools/benchmark_ljpw_vs_alternatives.py
python tools/validate_realworld_codebase.py

# Use core analyzer
python src/ljpw/ljpw_standalone.py analyze myfile.py
```

## Contributing

When adding new files:

1. **Tests** → Place in `tests/` with `test_` prefix
2. **Tools/utilities** → Place in `tools/`
3. **Core implementations** → Place in `src/ljpw/` with `ljpw_` prefix
4. **Documentation** → Place in `docs/` as `.md` file
5. **Examples** → Place in `examples/`
6. **Visualizations** → Place in `visualizations/` as `.html` file

## Migration Notes

This structure was established on 2024-11-16 to organize the repository from 66+ files in the root directory into a clean, hierarchical structure.

**Before:** All files in root (messy)
**After:** Organized by purpose (clean)

All file history was preserved using `git mv`.
