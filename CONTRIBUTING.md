# Contributing to Semantic Compressor

Thank you for your interest in contributing to Semantic Compressor! This document provides guidelines and instructions for contributing.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Code Style](#code-style)
7. [Pull Request Process](#pull-request-process)
8. [Reporting Bugs](#reporting-bugs)
9. [Suggesting Features](#suggesting-features)
10. [Questions](#questions)

---

## Code of Conduct

This project follows a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

**In short:**
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Prioritize project goals over personal preferences

---

## Getting Started

### First Time Contributors

Looking to contribute? Great! Here are some good starting points:

- 🐛 [Good First Issues](https://github.com/BruinGrowly/Semantic-Compressor/labels/good%20first%20issue)
- 📝 Documentation improvements
- ✅ Adding tests for uncovered code
- 🧪 Testing on different platforms/Python versions

### Project Overview

- **Language:** Python 3.7+
- **Core Concept:** Semantic code compression using LJPW framework
- **Key Files:**
  - `src/ljpw/ljpw_standalone.py` - Main analyzer
  - `tests/` - Test suite
  - `docs/` - Documentation

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Semantic-Compressor.git
cd Semantic-Compressor
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### 3. Install in Development Mode

```bash
# Install package with dev dependencies
pip install -e ".[dev]"

# This installs:
# - The package in editable mode
# - pytest, pytest-cov (testing)
# - black, isort (formatting)
# - flake8 (linting)
# - mypy (type checking)
```

### 4. Verify Installation

```bash
# Run tests to ensure everything works
pytest

# Try the CLI
ljpw help
```

---

## Making Changes

### 1. Create a Feature Branch

```bash
# Always create a new branch for your changes
git checkout -b feature/amazing-feature

# Use prefixes:
# - feature/ for new features
# - fix/ for bug fixes
# - docs/ for documentation
# - test/ for test improvements
# - refactor/ for code refactoring
```

### 2. Make Your Changes

Follow these guidelines:
- Keep changes focused (one feature/fix per PR)
- Add tests for new functionality
- Update documentation if needed
- Follow the existing code style
- Add docstrings to new functions/classes

### 3. Write Good Commit Messages

```bash
# Good commit message format:
# <type>: <subject>
# 
# <body>

# Example:
git commit -m "feat: add progress indicators for directory analysis

Added progress bar showing current file and percentage complete
when analyzing directories with multiple files."

# Types: feat, fix, docs, test, refactor, style, chore
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_ljpw_framework.py

# Run with coverage
pytest --cov=src/ljpw --cov-report=html

# View coverage report
open htmlcov/index.html  # On Mac
# or
xdg-open htmlcov/index.html  # On Linux
```

### Writing Tests

Add tests for any new functionality:

```python
# tests/test_new_feature.py
import pytest
from src.ljpw.ljpw_standalone import analyze_quick

def test_new_feature():
    """Test description"""
    code = "def example(): pass"
    result = analyze_quick(code)
    
    assert 'ljpw' in result
    assert result['health'] >= 0
```

**Test Guidelines:**
- ✅ Test edge cases (empty input, invalid input, etc.)
- ✅ Test error conditions
- ✅ Use descriptive test names
- ✅ Keep tests independent (no shared state)
- ✅ Mock external dependencies

---

## Code Style

We follow PEP 8 with some modifications:

### Formatting

```bash
# Format code with black
black src/ tests/ tools/

# Sort imports with isort
isort src/ tests/ tools/

# Check linting with flake8
flake8 src/ tests/ tools/
```

### Style Guidelines

1. **Line Length:** 100 characters (not 80)
2. **Quotes:** Use double quotes `"` for strings
3. **Imports:** Group by standard lib, third-party, local
4. **Type Hints:** Add type hints for function parameters and returns
5. **Docstrings:** Use Google-style docstrings

**Example:**

```python
from typing import Dict, List, Optional
import math
import re

def analyze_code(code: str, filename: str = "code") -> Dict[str, Any]:
    """
    Analyze code and return LJPW metrics.
    
    Args:
        code: Source code string to analyze
        filename: Optional filename for context
    
    Returns:
        Dictionary containing LJPW scores and health metrics
    
    Raises:
        ValueError: If code is None or invalid
    
    Example:
        >>> result = analyze_code("def hello(): pass")
        >>> print(result['health'])
        0.42
    """
    # Implementation
    pass
```

### Pre-commit Hooks

Optionally set up pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Now black, isort, and flake8 run automatically on commit
```

---

## Pull Request Process

### Before Submitting

1. ✅ All tests pass: `pytest`
2. ✅ Code is formatted: `black src/ tests/`
3. ✅ Imports are sorted: `isort src/ tests/`
4. ✅ Linting passes: `flake8 src/ tests/`
5. ✅ New code has tests
6. ✅ Documentation is updated

### Submitting PR

1. **Push your branch:**
   ```bash
   git push origin feature/amazing-feature
   ```

2. **Create Pull Request on GitHub**
   - Use a clear, descriptive title
   - Reference any related issues (#123)
   - Describe what changes you made and why
   - Add screenshots if relevant

3. **PR Template:**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Code refactoring
   
   ## Testing
   Describe how you tested these changes
   
   ## Checklist
   - [ ] Tests pass
   - [ ] Code formatted with black
   - [ ] Documentation updated
   - [ ] Commits follow convention
   ```

### Review Process

- Maintainers will review your PR within 48 hours
- Address any requested changes
- Once approved, maintainers will merge

---

## Reporting Bugs

### Before Reporting

1. Check if bug already reported in [Issues](https://github.com/BruinGrowly/Semantic-Compressor/issues)
2. Try to reproduce with latest version
3. Collect information about your environment

### Bug Report Template

```markdown
**Bug Description**
Clear description of what went wrong

**To Reproduce**
Steps to reproduce:
1. Run command: `ljpw analyze file.py`
2. With this input: ...
3. See error: ...

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened (include error messages)

**Environment**
- OS: [e.g., Ubuntu 22.04, Windows 11]
- Python version: [e.g., 3.11.2]
- Semantic Compressor version: [e.g., 2.0.0]

**Additional Context**
Any other relevant information
```

---

## Suggesting Features

We love feature ideas! Here's how to suggest one:

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How would you like this to work?

**Example Usage**
```python
# Show example of how feature would be used
result = new_feature(input)
```

**Alternatives Considered**
Other ways this could be implemented

**Additional Context**
Mockups, related projects, etc.
```

### Feature Discussion

- Features are discussed in Issues before implementation
- We consider: usefulness, complexity, maintenance burden
- See [ROADMAP.md](ROADMAP.md) for planned features

---

## Questions

### Where to Ask

- 💬 **Discussions:** General questions, ideas, brainstorming
- 🐛 **Issues:** Bug reports, feature requests
- 📖 **Docs:** Check documentation first

### Getting Help

- Read [Quick Reference](docs/QUICK_REFERENCE.md)
- Check [examples/](examples/) directory
- Review [test files](tests/) for usage examples

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in commits

---

## Development Tips

### Running Specific Examples

```bash
# Run examples to see how features work
python examples/basic/01_analyze_single_file.py
python examples/advanced/demo_iso_analysis.py
```

### Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pdb for interactive debugging
import pdb; pdb.set_trace()
```

### Performance Profiling

```python
# Profile code
python -m cProfile -o output.prof your_script.py

# View results
python -m pstats output.prof
```

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Thank You!

Your contributions make Semantic Compressor better for everyone. Whether it's code, documentation, bug reports, or feature ideas - every contribution matters!

**Questions?** Open an issue or discussion, we're happy to help!

---

*Last updated: November 29, 2025*
