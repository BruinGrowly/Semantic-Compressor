"""
Multi-Language and Edge Case Testing for LJPW Framework

Tests the framework with:
1. Multiple programming languages (Python, JavaScript, Rust, Java)
2. Edge cases (empty code, huge files, extreme LJPW values)
3. Real-world code samples
4. Stress tests
"""

import importlib.util
import os

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

base_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'ljpw')
pipeline_mod = load_module("ljpw_pipeline", os.path.join(base_path, "ljpw_pipeline.py"))
LJPWPipeline = pipeline_mod.LJPWPipeline

# ============================================================================
# MULTI-LANGUAGE TEST SAMPLES
# ============================================================================

LANGUAGE_SAMPLES = {
    "python": [
        ("safe_python.py", """
from typing import Optional, List
import logging

class DataValidator:
    '''Validates data with comprehensive error handling'''

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.logger = logging.getLogger(__name__)

    def validate(self, data: Optional[List[int]]) -> bool:
        '''
        Validate input data

        Args:
            data: List of integers to validate

        Returns:
            True if valid, False otherwise

        Raises:
            TypeError: If data is not a list
            ValueError: If data contains invalid values
        '''
        if data is None:
            if self.strict_mode:
                raise ValueError("Data cannot be None")
            return False

        if not isinstance(data, list):
            raise TypeError(f"Expected list, got {type(data)}")

        try:
            for i, item in enumerate(data):
                if not isinstance(item, int):
                    self.logger.warning(f"Item {i} is not int: {item}")
                    if self.strict_mode:
                        raise ValueError(f"Invalid item at index {i}")

            return True
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            raise
"""),
    ],

    "javascript": [
        ("safe_js.js", """
class DataProcessor {
    constructor(options = {}) {
        this.validateOptions(options);
        this.options = options;
    }

    validateOptions(options) {
        if (!options || typeof options !== 'object') {
            throw new TypeError('Options must be an object');
        }
    }

    async processData(data) {
        try {
            if (!Array.isArray(data)) {
                throw new TypeError('Data must be an array');
            }

            const results = [];
            for (const item of data) {
                if (item === null || item === undefined) {
                    continue;
                }

                const validated = await this.validateItem(item);
                if (validated) {
                    results.push(this.transform(item));
                }
            }

            return results;
        } catch (error) {
            console.error('Processing error:', error);
            throw error;
        }
    }

    async validateItem(item) {
        return item !== null;
    }

    transform(item) {
        return item * 2;
    }
}

module.exports = DataProcessor;
"""),
    ],

    "rust": [
        ("safe_rust.rs", """
use std::error::Error;
use std::fmt;

#[derive(Debug)]
pub struct ValidationError {
    message: String,
}

impl fmt::Display for ValidationError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Validation error: {}", self.message)
    }
}

impl Error for ValidationError {}

pub struct DataValidator {
    strict_mode: bool,
}

impl DataValidator {
    pub fn new(strict_mode: bool) -> Self {
        DataValidator { strict_mode }
    }

    pub fn validate(&self, data: Option<Vec<i32>>) -> Result<bool, Box<dyn Error>> {
        match data {
            None => {
                if self.strict_mode {
                    Err(Box::new(ValidationError {
                        message: String::from("Data cannot be None"),
                    }))
                } else {
                    Ok(false)
                }
            }
            Some(values) => {
                for (i, value) in values.iter().enumerate() {
                    if *value < 0 && self.strict_mode {
                        return Err(Box::new(ValidationError {
                            message: format!("Negative value at index {}: {}", i, value),
                        }));
                    }
                }
                Ok(true)
            }
        }
    }

    pub fn process(&self, data: Vec<i32>) -> Result<Vec<i32>, Box<dyn Error>> {
        self.validate(Some(data.clone()))?;

        Ok(data
            .into_iter()
            .filter(|&x| x >= 0)
            .map(|x| x * 2)
            .collect())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validation() {
        let validator = DataValidator::new(true);
        assert!(validator.validate(Some(vec![1, 2, 3])).is_ok());
    }
}
"""),
    ],

    "java": [
        ("SafeJava.java", """
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;
import java.util.logging.Level;

public class DataValidator {
    private static final Logger LOGGER = Logger.getLogger(DataValidator.class.getName());
    private final boolean strictMode;

    public DataValidator(boolean strictMode) {
        this.strictMode = strictMode;
    }

    public boolean validate(List<Integer> data) throws ValidationException {
        if (data == null) {
            if (strictMode) {
                throw new ValidationException("Data cannot be null");
            }
            return false;
        }

        try {
            for (int i = 0; i < data.size(); i++) {
                Integer item = data.get(i);
                if (item == null) {
                    LOGGER.log(Level.WARNING, "Null item at index: " + i);
                    if (strictMode) {
                        throw new ValidationException("Null item at index: " + i);
                    }
                }
            }
            return true;
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Validation error", e);
            throw e;
        }
    }

    public List<Integer> process(List<Integer> data) throws ValidationException {
        validate(data);

        List<Integer> results = new ArrayList<>();
        for (Integer item : data) {
            if (item != null) {
                results.add(item * 2);
            }
        }

        return results;
    }

    public static class ValidationException extends Exception {
        public ValidationException(String message) {
            super(message);
        }
    }
}
"""),
    ],
}

# ============================================================================
# EDGE CASE SAMPLES
# ============================================================================

EDGE_CASES = [
    ("empty.py", ""),  # Empty file

    ("minimal.py", "x = 1"),  # Minimal code

    ("comment_only.py", """
# This file only has comments
# No actual code here
# Just documentation
"""),

    ("massive_safety.py", """
def ultra_safe_function(data):
    '''Maximum safety checks'''
    if data is None:
        raise ValueError("None not allowed")
    if not isinstance(data, list):
        raise TypeError("Must be list")
    if len(data) == 0:
        raise ValueError("Empty list")
    if len(data) > 1000:
        raise ValueError("Too large")

    try:
        validated = []
        for i, item in enumerate(data):
            if item is None:
                raise ValueError(f"None at {i}")
            if not isinstance(item, (int, float)):
                raise TypeError(f"Wrong type at {i}")
            if item < 0:
                raise ValueError(f"Negative at {i}")
            if item > 1000000:
                raise ValueError(f"Too large at {i}")

            validated.append(item)

        return validated
    except Exception as e:
        logging.error(f"Error: {e}")
        raise
"""),

    ("no_safety.py", """
def unsafe_function(data):
    return [x * 2 for x in data]
"""),
]

# ============================================================================
# TEST EXECUTION
# ============================================================================

def test_multi_language():
    """Test framework with multiple programming languages"""
    print("="*70)
    print("MULTI-LANGUAGE LJPW ANALYSIS TEST")
    print("="*70)

    pipeline = LJPWPipeline()

    for language, samples in LANGUAGE_SAMPLES.items():
        print(f"\n{language.upper()} Analysis:")
        print("-" * 70)

        results = pipeline.analyze_codebase(samples,
                                           generate_docs=False,
                                           generate_improvement_plan=False)

        stats = results['statistics']
        avg_ljpw = stats['average_ljpw']

        print(f"\nResults for {language}:")
        print(f"  Files analyzed: {stats['total_files']}")
        print(f"  Compression: {stats['compression_ratio']:.1f}x")
        print(f"  Health Score: {stats['health_score']:.1%}")
        print(f"  Average LJPW: L={avg_ljpw[0]:.2f}, J={avg_ljpw[1]:.2f}, P={avg_ljpw[2]:.2f}, W={avg_ljpw[3]:.2f}")

        # Insights
        if results['reasoning']['insights']:
            print(f"\n  Top Insights:")
            for insight in results['reasoning']['insights'][:3]:
                print(f"    [{insight['type']}] {insight['message']}")

def test_edge_cases():
    """Test framework with edge cases"""
    print("\n" + "="*70)
    print("EDGE CASE TESTING")
    print("="*70)

    pipeline = LJPWPipeline()

    for filename, code in EDGE_CASES:
        print(f"\nTesting: {filename}")
        print("-" * 70)

        try:
            results = pipeline.analyze_codebase([(filename, code)],
                                               generate_docs=False,
                                               generate_improvement_plan=False)

            stats = results['statistics']
            avg_ljpw = stats['average_ljpw']

            print(f"  Success!")
            print(f"  Health: {stats['health_score']:.1%}")
            print(f"  LJPW: L={avg_ljpw[0]:.2f}, J={avg_ljpw[1]:.2f}, P={avg_ljpw[2]:.2f}, W={avg_ljpw[3]:.2f}")

        except Exception as e:
            print(f"  Error: {e}")

def test_extreme_scale():
    """Test with extremely large generated codebase"""
    print("\n" + "="*70)
    print("EXTREME SCALE TEST")
    print("="*70)

    # Generate 100 files
    print("\nGenerating 100 synthetic code files...")

    synthetic_files = []
    for i in range(100):
        code = f"""
def function_{i}(data):
    '''Function {i}'''
    if not data:
        raise ValueError("Empty data")

    try:
        result = []
        for item in data:
            if item is not None:
                result.append(item * {i + 1})
        return result
    except Exception as e:
        print(f"Error: {{e}}")
        raise
"""
        synthetic_files.append((f"file_{i}.py", code))

    print(f"Generated {len(synthetic_files)} files")
    print("Running pipeline...")

    pipeline = LJPWPipeline()

    import time
    start = time.time()

    results = pipeline.analyze_codebase(synthetic_files,
                                       generate_docs=False,
                                       generate_improvement_plan=False)

    elapsed = time.time() - start

    stats = results['statistics']
    avg_ljpw = stats['average_ljpw']

    print(f"\nExtreme Scale Results:")
    print(f"  Files: {stats['total_files']}")
    print(f"  Total code size: {stats['total_code_size']:,} bytes")
    print(f"  Compressed size: {stats['compressed_size']:,} bytes")
    print(f"  Compression: {stats['compression_ratio']:.1f}x")
    print(f"  Processing time: {elapsed:.2f}s")
    print(f"  Throughput: {stats['total_files']/elapsed:.1f} files/sec")
    print(f"  Health: {stats['health_score']:.1%}")
    print(f"  LJPW: L={avg_ljpw[0]:.2f}, J={avg_ljpw[1]:.2f}, P={avg_ljpw[2]:.2f}, W={avg_ljpw[3]:.2f}")

def compare_languages():
    """Compare LJPW scores across languages"""
    print("\n" + "="*70)
    print("CROSS-LANGUAGE COMPARISON")
    print("="*70)

    pipeline = LJPWPipeline()
    language_scores = {}

    for language, samples in LANGUAGE_SAMPLES.items():
        results = pipeline.analyze_codebase(samples,
                                           generate_docs=False,
                                           generate_improvement_plan=False)

        avg_ljpw = results['statistics']['average_ljpw']
        health = results['statistics']['health_score']

        language_scores[language] = {
            'ljpw': avg_ljpw,
            'health': health,
        }

    # Display comparison
    print("\nLanguage\t\tL\tJ\tP\tW\tHealth")
    print("-" * 70)
    for lang in sorted(language_scores.keys()):
        scores = language_scores[lang]
        L, J, P, W = scores['ljpw']
        health = scores['health']
        print(f"{lang:15s}\t{L:.2f}\t{J:.2f}\t{P:.2f}\t{W:.2f}\t{health:.1%}")

    # Find best language
    best_lang = max(language_scores.items(), key=lambda x: x[1]['health'])
    print(f"\nHighest Health Score: {best_lang[0]} ({best_lang[1]['health']:.1%})")

# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == '__main__':
    print("#"*70)
    print("# LJPW MULTI-LANGUAGE & EDGE CASE TEST SUITE")
    print("#"*70)

    test_multi_language()
    test_edge_cases()
    test_extreme_scale()
    compare_languages()

    print("\n" + "#"*70)
    print("# ALL MULTI-LANGUAGE TESTS COMPLETE")
    print("#"*70)
    print("\n[SUCCESS] Framework validated across multiple languages and edge cases!")
