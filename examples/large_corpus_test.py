#!/usr/bin/env python3
"""
Large Corpus Ingestion Test for LJPW Semantic Compiler
Processes massive amounts of text to test compression performance at scale
"""

# Import LJPW components
import importlib.util
import math
import os
import random
import string
import time
from typing import Any, Dict, List, Tuple


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load pipeline
pipeline_mod = load_module("ljpw_pipeline", "ljpw_pipeline.py")
LJPWPipeline = pipeline_mod.LJPWPipeline

# ============================================================================
# LARGE CORPUS GENERATION
# ============================================================================


class CorpusGenerator:
    """Generate diverse, realistic code corpus at scale"""

    def __init__(self):
        self.templates = self._build_templates()
        self.code_patterns = self._build_code_patterns()

    def _build_templates(self) -> Dict[str, List[str]]:
        """Build realistic code templates"""
        return {
            "classes": [
                """
class {name}:
    '''{description}'''
    
    def __init__(self, {params}):
        {validations}
        {initializations}
    
    def {method_name}(self, {method_params}) -> {return_type}:
        '''{method_description}'''
        try:
            {method_body}
        except {exception_type} as e:
            {error_handling}
            {raise_or_return}
        return {return_value}
    
    def validate_{name}(self, data: Any) -> bool:
        '''Validate {name} data'''
        if not isinstance(data, {expected_type}):
            raise TypeError(f"Expected {expected_type}, got {{type(data)}}")
        {validation_logic}
        return True
    
    def {utility_method}(self, {utility_params}) -> Any:
        '''Utility method for {utility_purpose}'''
        {utility_body}
        return {utility_return}
""",
            ],
            "functions": [
                """
def {name}({params}) -> {return_type}:
    '''{description}
    
    Args:
        {arg_descriptions}
    
    Returns:
        {return_description}
    
    Raises:
        {exceptions}
    
    Complexity:
        Time: O({time_complexity})
        Space: O({space_complexity})
    '''
    # Input validation
    {validations}
    
    # Main logic
    {main_logic}
    
    # Result processing
    {result_processing}
    
    return {return_value}
""",
            ],
            "algorithms": [
                """
def {algorithm_name}({params}) -> {return_type}:
    '''{algorithm_description}
    
    {algorithm_details}
    '''
    # {algorithm_type} algorithm implementation
    {initialization}
    
    {loop_structure}
        {loop_body}
        {update_logic}
    
    {final_processing}
    return {result}
""",
            ],
            "interfaces": [
                """
from abc import ABC, abstractmethod
from typing import {type_imports}

class {interface_name}(ABC):
    '''{interface_description}'''
    
    @abstractmethod
    def {method_name}(self, {method_params}) -> {return_type}:
        '''{method_description}'''
        pass
    
    @abstractmethod
    def {method_name_2}(self, {method_params_2}) -> {return_type_2}:
        '''{method_description_2}'''
        pass
    
    {additional_methods}
""",
            ],
            "data_structures": [
                """
@dataclass
class {class_name}:
    '''{class_description}'''
    
    {fields}
    
    def __post_init__(self):
        '''Validate invariants'''
        {invariant_checks}
    
    def {method_name}(self, {method_params}) -> {return_type}:
        '''{method_description}'''
        {method_body}
    
    def __str__(self) -> str:
        return f"{class_name}({string_fields})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, {class_name}):
            return False
        {equality_logic}
        return True
    
    def {comparator_method}(self, other) -> bool:
        '''Comparison for sorting'''
        {comparison_logic}
""",
            ],
        }

    def _build_code_patterns(self) -> Dict[str, List[str]]:
        """Build realistic code patterns"""
        return {
            "class_names": [
                "DataProcessor",
                "CacheManager",
                "AuthHandler",
                "QueryBuilder",
                "EventEmitter",
                "ConfigValidator",
                "StateController",
                "ServiceRegistry",
                "ConnectionPool",
                "TaskScheduler",
                "ResourceManager",
                "ErrorHandler",
            ],
            "function_names": [
                "process_data",
                "validate_input",
                "compute_hash",
                "fetch_resource",
                "parse_response",
                "transform_format",
                "filter_results",
                "aggregate_data",
                "optimize_performance",
                "synchronize_state",
                "serialize_object",
                "deserialize_data",
            ],
            "algorithm_names": [
                "binary_search",
                "quick_sort",
                "merge_sort",
                "heap_sort",
                "depth_first_search",
                "breadth_first_search",
                "dijkstra",
                "bellman_ford",
                "k_means_clustering",
                "linear_regression",
                "gradient_descent",
                "newton_method",
            ],
            "variable_names": [
                "data",
                "result",
                "config",
                "params",
                "options",
                "metadata",
                "response",
                "request",
                "headers",
                "payload",
                "session",
                "context",
            ],
            "error_types": [
                "ValueError",
                "TypeError",
                "KeyError",
                "IndexError",
                "ConnectionError",
                "TimeoutError",
                "AuthenticationError",
                "ValidationError",
                "ConfigurationError",
                "RuntimeError",
            ],
        }

    def generate_realistic_code(self, complexity_level: str = "medium") -> str:
        """Generate realistic code based on complexity"""
        if complexity_level == "simple":
            return self._generate_simple_code()
        elif complexity_level == "medium":
            return self._generate_medium_code()
        elif complexity_level == "complex":
            return self._generate_complex_code()
        else:
            return self._generate_medium_code()

    def _generate_simple_code(self) -> str:
        """Generate simple function/class"""
        template = random.choice(self.templates["functions"])

        return template.format(
            name=random.choice(self.code_patterns["function_names"]),
            params="data: List[Any], config: Dict[str, Any]",
            return_type="List[Any]",
            description="Process and transform data",
            arg_descriptions="data: Input data to process\nconfig: Configuration options",
            return_description="Processed data",
            exceptions="ValueError: When data is invalid",
            time_complexity=random.choice(["n", "n log n", "n^2"]),
            space_complexity=random.choice(["1", "n", "n^2"]),
            validations=self._generate_validation_code(),
            main_logic=self._generate_processing_code(),
            result_processing=self._generate_result_code(),
            return_value="result",
        )

    def _generate_medium_code(self) -> str:
        """Generate medium complexity code"""
        template = random.choice(self.templates["classes"])

        return template.format(
            name=random.choice(self.code_patterns["class_names"]),
            description="Handles {name} operations with validation and error handling".format(
                name=random.choice(["data", "cache", "auth", "query", "events"]).lower()
            ),
            params="config: Dict[str, Any]",
            validations=self._generate_validation_code(),
            initializations=self._generate_initialization_code(),
            method_name=random.choice(["process", "handle", "execute", "perform"]),
            method_params="input_data: Any",
            return_type="Any",
            method_description="Execute the core operation",
            method_body=self._generate_processing_code(),
            exception_type=random.choice(self.code_patterns["error_types"]),
            error_handling=self._generate_error_handling_code(),
            raise_or_return="raise",
            return_value="result",
            expected_type="Dict[str, Any]",
            validation_logic='if not data:\n        raise ValueError("Data cannot be empty")',
            utility_method="get_metrics",
            utility_params="self",
            utility_purpose="performance tracking",
            utility_body="return self.metrics",
            utility_return="self.metrics",
        )

    def _generate_complex_code(self) -> str:
        """Generate complex algorithmic code"""
        template = random.choice(self.templates["algorithms"])

        return template.format(
            algorithm_name=random.choice(self.code_patterns["algorithm_names"]),
            algorithm_description="Efficient implementation of {name} algorithm".format(
                name=random.choice(["sorting", "searching", "graph", "optimization"])
            ),
            algorithm_details=self._generate_algorithm_details(),
            params="data: List[Comparable], target: Optional[Comparable] = None",
            return_type="Union[List[Comparable], int, None]",
            algorithm_type="Divide and conquer",
            initialization=self._generate_initialization_code(),
            loop_structure=self._generate_loop_structure(),
            loop_body=self._generate_loop_body(),
            update_logic=self._generate_update_logic(),
            final_processing=self._generate_final_processing(),
            result="result",
        )

    def _generate_validation_code(self) -> str:
        """Generate validation code patterns"""
        patterns = [
            """
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        if not data:
            return []""",
            """
        if not config:
            config = {}
        required_keys = ['timeout', 'retries']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config: {key}")""",
            """
        if input_data is None:
            raise ValueError("Input data cannot be None")
        if not hasattr(input_data, '__iter__'):
            raise TypeError("Input data must be iterable")""",
        ]
        return random.choice(patterns)

    def _generate_processing_code(self) -> str:
        """Generate main processing logic"""
        patterns = [
            """
        result = []
        for item in data:
            if self.validate_item(item):
                processed = self.transform_item(item, config)
                result.append(processed)
        return result""",
            """
        processed_data = []
        for index, element in enumerate(data):
            try:
                transformed = self.apply_transformation(element, config)
                if transformed:
                    processed_data.append(transformed)
            except Exception as e:
                self.handle_error(index, e)
                continue
        return processed_data""",
            """
        cache_key = self.generate_cache_key(data)
        if cached := self.cache.get(cache_key):
            return cached
        
        result = self.compute_result(data, config)
        self.cache.set(cache_key, result, timeout=config.get('ttl', 300))
        return result""",
        ]
        return random.choice(patterns)

    def _generate_error_handling_code(self) -> str:
        """Generate error handling patterns"""
        patterns = [
            """
        logger.error(f"Error processing {input_data}: {e}")
        if config.get('raise_on_error', True):
            raise
        return None""",
            """
        self.error_count += 1
        self.metrics.record_error(type(e).__name__)
        if self.error_count > config.get('max_errors', 10):
            raise RuntimeError(f"Too many errors: {self.error_count}")""",
            """
        self.fallback_handler.handle(input_data, e)
        return self.get_default_result(input_data)""",
        ]
        return random.choice(patterns)

    def _generate_initialization_code(self) -> str:
        """Generate initialization code"""
        patterns = [
            """
        self.config = config or {}
        self.cache = {}
        self.metrics = {'processed': 0, 'errors': 0}""",
            """
        self.validator = ConfigValidator(config)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.state = 'initialized'""",
            """
        self.pool = ConnectionPool(config.get('pool_size', 10))
        self.serializer = JSONSerializer()
        self.version = '1.0.0'""",
        ]
        return random.choice(patterns)

    def _generate_loop_structure(self) -> str:
        """Generate loop structures"""
        patterns = [
            """
    left, right = 0, len(data) - 1
    while left <= right:""",
            """
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):""",
            """
    while not self.is_sorted(data):
        made_changes = False""",
        ]
        return random.choice(patterns)

    def _generate_loop_body(self) -> str:
        """Generate loop body content"""
        patterns = [
            """
        if data[left] == target:
            return left
        elif data[left] < target:
            left += 1
        else:
            right -= 1""",
            """
        if data[i] > data[j]:
            data[i], data[j] = data[j], data[i]
            made_changes = True""",
            """
        if not self.compare(data[i], data[j]):
            self.swap(data[i], data[j])
            changes += 1""",
        ]
        return random.choice(patterns)

    def _generate_algorithm_details(self) -> str:
        """Generate algorithm documentation"""
        return """Uses divide-and-conquer strategy for optimal performance.
        Time complexity: O(n log n) in average case, O(n^2) worst case.
        Space complexity: O(log n) due to recursion stack."""

    def _generate_update_logic(self) -> str:
        """Generate update logic for loops"""
        patterns = [
            "        pass",
            "        # Update counters\n        self.operations += 1",
            "        # Check termination condition\n        if self.should_terminate(): break",
        ]
        return random.choice(patterns)

    def _generate_final_processing(self) -> str:
        """Generate final processing steps"""
        patterns = [
            "    result = data if target is None else left",
            "    return -1 if not found else data",
            "    self.validate_result(result)\n    return result",
        ]
        return random.choice(patterns)

    def _generate_result_code(self) -> str:
        """Generate result processing code"""
        patterns = [
            "        result = filtered_data",
            "        result = self.optimize_output(processed_data)",
            "        result = self.post_process(processed_data)",
        ]
        return random.choice(patterns)

    def generate_large_corpus(
        self, num_files: int, avg_lines_per_file: int
    ) -> List[Tuple[str, str]]:
        """Generate large corpus of realistic code"""
        print(f"Generating {num_files} files with avg {avg_lines_per_file} lines each...")

        corpus = []
        complexities = ["simple", "medium", "complex"]
        weights = [0.3, 0.5, 0.2]  # Distribution of complexity levels

        start_time = time.time()

        for i in range(num_files):
            # Choose complexity based on weights
            complexity = random.choices(complexities, weights=weights)[0]

            # Generate code
            code = self.generate_realistic_code(complexity)

            # Adjust line count by adding/removing content
            current_lines = len(code.split("\n"))
            if current_lines < avg_lines_per_file:
                # Add more content
                additional_content = self._generate_additional_code(
                    avg_lines_per_file - current_lines
                )
                code += "\n" + additional_content
            elif current_lines > avg_lines_per_file:
                # Truncate (not ideal but simple)
                lines = code.split("\n")[:avg_lines_per_file]
                code = "\n".join(lines)

            filename = f"generated_file_{i:04d}.py"
            corpus.append((filename, code))

            # Progress indicator
            if (i + 1) % max(1, num_files // 20) == 0:
                progress = (i + 1) / num_files * 100
                elapsed = time.time() - start_time
                eta = elapsed / (i + 1) * (num_files - i - 1)
                print(f"  Progress: {progress:.1f}% ({i+1}/{num_files}), ETA: {eta:.1f}s")

        print(f"Generated {len(corpus)} files in {time.time() - start_time:.1f}s")
        return corpus

    def _generate_additional_code(self, needed_lines: int) -> str:
        """Generate additional code to meet line requirements"""
        additional_patterns = [
            """

# Helper functions
def helper_function_1():
    '''Helper function for common operations'''
    return True

def helper_function_2(param: str) -> str:
    '''Another helper function'''
    return param.upper()

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
CACHE_SIZE = 1000

# Utility class
class UtilityMixin:
    '''Mixin class with utility methods'''
    
    def log_operation(self, operation: str) -> None:
        '''Log operation for debugging'''
        print(f"Operation: {operation}")
    
    def validate_config(self, config: dict) -> bool:
        '''Validate configuration parameters'''
        required_keys = ['host', 'port', 'timeout']
        return all(key in config for key in required_keys)
""",
            """

# Error definitions
class CustomError(Exception):
    '''Custom error class'''
    pass

class ValidationError(CustomError):
    '''Validation-specific error'''
    pass

# Type hints
from typing import Any, Dict, List, Optional, Union

# Configuration defaults
DEFAULT_CONFIG = {
    'debug': False,
    'timeout': 30,
    'retries': 3,
    'cache_enabled': True
}

# Performance metrics
class PerformanceTracker:
    '''Track performance metrics'''
    
    def __init__(self):
        self.start_time = None
        self.operations = 0
    
    def start(self):
        '''Start timing'''
        self.start_time = time.time()
    
    def record_operation(self):
        '''Record an operation'''
        self.operations += 1
    
    def get_stats(self) -> dict:
        '''Get performance statistics'''
        elapsed = time.time() - self.start_time if self.start_time else 0
        return {
            'elapsed_time': elapsed,
            'operations': self.operations,
            'ops_per_second': self.operations / elapsed if elapsed > 0 else 0
        }
""",
        ]

        pattern = random.choice(additional_patterns)
        lines = pattern.split("\n")

        # Adjust to exact line count needed
        if len(lines) < needed_lines:
            # Add simple lines
            extra_lines = needed_lines - len(lines)
            for i in range(extra_lines):
                lines.append(f"# Generated line {i+1}")
        elif len(lines) > needed_lines:
            lines = lines[:needed_lines]

        return "\n".join(lines)


# ============================================================================
# LARGE SCALE TEST
# ============================================================================


def run_large_scale_corpus_test(corpus_sizes: List[int], avg_lines: List[int]):
    """Run compression tests on increasingly large corpora"""

    print("=" * 80)
    print("LARGE SCALE CORPUS COMPRESSION TEST")
    print("Testing LJPW Semantic Compiler on Massive Text Corpora")
    print("=" * 80)

    generator = CorpusGenerator()
    pipeline = LJPWPipeline()

    results = []

    for size, lines in zip(corpus_sizes, avg_lines):
        print(f"\n{'='*60}")
        print(f"TESTING: {size} files, avg {lines} lines per file")
        print(f"{'='*60}")

        # Generate corpus
        print("\n1. GENERATING CORPUS")
        print("-" * 60)
        corpus = generator.generate_large_corpus(size, lines)

        # Calculate corpus statistics
        total_chars = sum(len(code) for _, code in corpus)
        total_lines = sum(len(code.split("\n")) for _, code in corpus)
        total_size_mb = total_chars / (1024 * 1024)

        print(f"\nCorpus Statistics:")
        print(f"  Files: {size:,}")
        print(f"  Total lines: {total_lines:,}")
        print(f"  Total characters: {total_chars:,}")
        print(f"  Total size: {total_size_mb:.2f} MB")
        print(f"  Avg lines/file: {total_lines/size:.1f}")
        print(f"  Avg size/file: {total_chars/size:,.0f} characters")

        # Run compression pipeline
        print(f"\n2. RUNNING LJPW COMPRESSION PIPELINE")
        print("-" * 60)

        start_time = time.time()

        try:
            pipeline_results = pipeline.analyze_codebase(
                corpus,
                generate_docs=False,  # Skip for speed in large tests
                generate_improvement_plan=False,
            )

            processing_time = time.time() - start_time

            # Extract metrics
            compression_ratio = pipeline_results["compression_ratio"]
            compressed_size = pipeline_results["statistics"]["compressed_size"]
            semantic_units = pipeline_results["statistics"]["semantic_units"]
            health_score = pipeline_results["statistics"]["health_score"]
            avg_ljpw = pipeline_results["statistics"]["average_ljpw"]

            # Calculate performance metrics
            throughput_files_per_sec = size / processing_time
            throughput_chars_per_sec = total_chars / processing_time
            throughput_lines_per_sec = total_lines / processing_time

            print(f"\n3. COMPRESSION RESULTS")
            print("-" * 60)
            print(f"Compression ratio: {compression_ratio:.1f}x")
            print(f"Original size: {total_size_mb:.2f} MB")
            print(f"Compressed size: {compressed_size:,} bytes ({compressed_size/1024:.1f} KB)")
            print(f"Semantic units: {semantic_units:,}")
            print(f"Space savings: {(1 - compressed_size/total_chars)*100:.1f}%")

            print(f"\n4. PERFORMANCE METRICS")
            print("-" * 60)
            print(f"Processing time: {processing_time:.2f} seconds")
            print(f"Throughput:")
            print(f"  Files/sec: {throughput_files_per_sec:.1f}")
            print(f"  Lines/sec: {throughput_lines_per_sec:.0f}")
            print(f"  Chars/sec: {throughput_chars_per_sec:,.0f}")

            print(f"\n5. QUALITY METRICS")
            print("-" * 60)
            print(f"Health score: {health_score:.1%}")
            L, J, P, W = avg_ljpw
            print(f"Average LJPW:")
            print(f"  Love (Safety):      {L:.3f}")
            print(f"  Justice (Structure): {J:.3f}")
            print(f"  Power (Performance): {P:.3f}")
            print(f"  Wisdom (Design):     {W:.3f}")

            # Store results
            results.append(
                {
                    "files": size,
                    "lines_per_file": lines,
                    "total_lines": total_lines,
                    "total_size_mb": total_size_mb,
                    "compression_ratio": compression_ratio,
                    "processing_time_sec": processing_time,
                    "throughput_files_per_sec": throughput_files_per_sec,
                    "health_score": health_score,
                    "space_savings_percent": (1 - compressed_size / total_chars) * 100,
                }
            )

            print(f"\n[SUCCESS] TEST COMPLETED SUCCESSFULLY")

        except Exception as e:
            print(f"\n[FAILED] TEST FAILED: {e}")
            import traceback

            traceback.print_exc()
            results.append({"files": size, "error": str(e)})

    # Summary
    print(f"\n{'='*80}")
    print("LARGE SCALE TEST SUMMARY")
    print("=" * 80)

    print(
        f"\n{'Files':<8} {'Lines':<8} {'Size(MB)':<10} {'Comp.Ratio':<12} {'Time(s)':<10} {'SpaceSave%':<12}"
    )
    print("-" * 70)

    for result in results:
        if "error" not in result:
            print(
                f"{result['files']:<8} {result['lines_per_file']:<8} {result['total_size_mb']:<10.1f} "
                f"{result['compression_ratio']:<12.1f} {result['processing_time_sec']:<10.2f} "
                f"{result['space_savings_percent']:<12.1f}"
            )
        else:
            print(f"{result['files']:<8} {'ERROR':<28} {result['error']}")

    # Find optimal compression point
    successful_results = [r for r in results if "error" not in r]
    if successful_results:
        best_compression = max(successful_results, key=lambda x: x["compression_ratio"])
        fastest_throughput = max(successful_results, key=lambda x: x["throughput_files_per_sec"])

        print(f"\n[TROPHY] OPTIMAL PERFORMERS:")
        print(
            f"Best Compression: {best_compression['files']} files "
            f"({best_compression['compression_ratio']:.1f}x ratio)"
        )
        print(
            f"Fastest Throughput: {fastest_throughput['files']} files "
            f"({fastest_throughput['throughput_files_per_sec']:.1f} files/sec)"
        )

    return results


# ============================================================================
# STRESS TEST
# ============================================================================


def run_stress_test():
    """Push the system to its limits"""
    print("\n" + "=" * 80)
    print("STRESS TEST - PUSHING LIMITS")
    print("=" * 80)

    # Extreme parameters
    stress_tests = [
        (1000, 50),  # Many small files
        (100, 500),  # Few large files
        (500, 200),  # Medium-large
        (2000, 25),  # Many tiny files
    ]

    return run_large_scale_corpus_test(
        corpus_sizes=[test[0] for test in stress_tests],
        avg_lines=[test[1] for test in stress_tests],
    )


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("LJPW LARGE CORPUS INGESTION TEST")
    print("Testing Semantic Compression on Massive Scale")

    # Run progressively larger tests
    test_sizes = [50, 100, 200, 500]
    avg_lines = [100, 100, 100, 100]

    results = run_large_scale_corpus_test(test_sizes, avg_lines)

    # Run stress test if basic tests pass
    if any("error" not in r for r in results):
        print("\n[ROCKET] RUNNING STRESS TEST")
        stress_results = run_stress_test()
        results.extend(stress_results)

    print("\n" + "=" * 80)
    print("ALL LARGE SCALE TESTS COMPLETED")
    print("=" * 80)
    print("LJPW Semantic Compiler successfully processed massive corpora!")
    print(f"Total test runs: {len([r for r in results if 'error' not in r])} successful")
