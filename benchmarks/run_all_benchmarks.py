#!/usr/bin/env python3
"""
LJPW Comprehensive Benchmark Suite
Runs all benchmarks and generates report

Usage:
    python run_all_benchmarks.py           # Full suite
    python run_all_benchmarks.py --quick   # Quick smoke test
    python run_all_benchmarks.py --report  # Generate report only
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path for src module imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ljpw.ljpw_semantic_compressor import SemanticCompressor, SemanticDecompressor
from src.ljpw.ljpw_standalone import SimpleCodeAnalyzer, analyze_directory, analyze_file


class BenchmarkSuite:
    """Comprehensive benchmark suite for LJPW"""

    def __init__(self, quick_mode=False):
        self.quick_mode = quick_mode
        self.results = {"timestamp": datetime.now().isoformat(), "version": "1.0", "benchmarks": {}}

    def run_all(self):
        """Run all benchmarks"""
        print("=" * 70)
        print("LJPW Benchmark Suite v1.0")
        print("=" * 70)
        print(f"Mode: {'Quick' if self.quick_mode else 'Full'}")
        print(f"Started: {self.results['timestamp']}")
        print()

        benchmarks = [
            ("compression_ratio", self.benchmark_compression_ratio),
            ("performance", self.benchmark_performance),
            ("accuracy", self.benchmark_accuracy),
            ("edge_cases", self.benchmark_edge_cases),
            ("multi_language", self.benchmark_multi_language),
        ]

        for name, func in benchmarks:
            print(f"Running: {name}...")
            start = time.time()
            try:
                result = func()
                duration = time.time() - start
                self.results["benchmarks"][name] = {
                    "status": "PASS",
                    "duration": duration,
                    "results": result,
                }
                print(f"  ✓ {name}: PASS ({duration:.2f}s)")
            except Exception as e:
                duration = time.time() - start
                self.results["benchmarks"][name] = {
                    "status": "FAIL",
                    "duration": duration,
                    "error": str(e),
                }
                print(f"  ✗ {name}: FAIL - {e}")
            print()

        self.save_results()
        self.print_summary()

    def benchmark_compression_ratio(self):
        """Test compression ratios across different code types"""
        compressor = SemanticCompressor()

        test_cases = [
            {
                "name": "simple_script",
                "code": 'def hello(): print("hi")',
                "expected_ratio": 50,  # Rough estimate
            },
            {
                "name": "medium_function",
                "code": self._generate_medium_code(),
                "expected_ratio": 500,
            },
        ]

        if not self.quick_mode:
            # Add Django test if file exists
            django_file = Path(__file__).parent.parent / "django_query.py"
            if django_file.exists():
                with open(django_file) as f:
                    test_cases.append(
                        {
                            "name": "django_orm",
                            "code": f.read(),
                            "expected_ratio": 50000,
                        }
                    )

        results = {}
        for case in test_cases:
            code = case["code"]
            original_size = len(code.encode("utf-8"))

            # Analyze and compress
            analyzer = SimpleCodeAnalyzer()
            analysis = analyzer.analyze(code)
            ljpw = analysis["ljpw"]

            # Create state and compress
            state = [(ljpw["L"], ljpw["J"], ljpw["P"], ljpw["W"])]
            genome = compressor.compress_state_sequence(state)

            compressed_size = len(genome.to_string().encode("utf-8"))
            ratio = original_size / max(compressed_size, 1)

            results[case["name"]] = {
                "original_bytes": original_size,
                "compressed_bytes": compressed_size,
                "ratio": ratio,
                "expected_ratio": case["expected_ratio"],
                "passes": ratio >= case["expected_ratio"] * 0.5,  # 50% tolerance
            }

        return results

    def benchmark_performance(self):
        """Test processing speed"""
        analyzer = SimpleCodeAnalyzer()

        test_cases = [
            ("small", "def f(): pass", 100 if not self.quick_mode else 10),
            ("medium", self._generate_medium_code(), 50 if not self.quick_mode else 5),
            ("large", self._generate_medium_code() * 10, 10 if not self.quick_mode else 1),
        ]

        results = {}
        for name, code, iterations in test_cases:
            times = []
            for _ in range(iterations):
                start = time.perf_counter()
                analyzer.analyze(code)
                duration = time.perf_counter() - start
                times.append(duration)

            avg_time = sum(times) / len(times)
            results[name] = {
                "avg_time_ms": avg_time * 1000,
                "iterations": iterations,
                "throughput": 1 / avg_time if avg_time > 0 else float("inf"),
            }

        return results

    def benchmark_accuracy(self):
        """Test semantic preservation accuracy"""
        compressor = SemanticCompressor()
        decompressor = SemanticDecompressor()

        # Test round-trip accuracy
        test_states = [
            (0.6, 0.4, 0.7, 0.7),
            (0.3, 0.5, 0.9, 0.4),
            (0.618, 0.414, 0.718, 0.693),  # Natural Equilibrium
        ]

        errors = []
        for original in test_states:
            genome = compressor.compress_state_sequence([original])
            reconstructed = decompressor.decompress_genome(genome)

            if reconstructed:
                recon = reconstructed[0]
                error = sum((o - r) ** 2 for o, r in zip(original, recon)) ** 0.5
                errors.append(error)

        avg_error = sum(errors) / len(errors) if errors else 0

        return {
            "round_trip_tests": len(test_states),
            "avg_reconstruction_error": avg_error,
            "max_error": max(errors) if errors else 0,
            "accuracy_percent": (1 - avg_error) * 100,
        }

    def benchmark_edge_cases(self):
        """Test edge case handling"""
        analyzer = SimpleCodeAnalyzer()

        edge_cases = [
            ("empty", ""),
            ("whitespace_only", "   \n\n   "),
            ("comments_only", "# comment\n# another"),
            ("unicode", "def 函数(): pass"),
            ("very_long_line", "x = " + "a" * 1000),
        ]

        results = {}
        for name, code in edge_cases:
            try:
                result = analyzer.analyze(code, name)
                results[name] = {
                    "status": "handled",
                    "health": result.get("health", 0),
                    "has_insights": len(result.get("insights", [])) > 0,
                }
            except Exception as e:
                results[name] = {"status": "error", "error": str(e)}

        return results

    def benchmark_multi_language(self):
        """Test multi-language support"""
        analyzer = SimpleCodeAnalyzer()

        languages = {
            "python": 'def hello(): print("hi")',
            "javascript": 'function hello() { console.log("hi"); }',
            "rust": 'fn main() { println!("hi"); }',
            "java": "public class Hello { public static void main(String[] args) {} }",
        }

        results = {}
        for lang, code in languages.items():
            analysis = analyzer.analyze(code, f"test.{lang}")
            results[lang] = {
                "ljpw": analysis["ljpw"],
                "health": analysis["health"],
                "analyzed": True,
            }

        return results

    def _generate_medium_code(self):
        """Generate medium-sized test code"""
        return '''
def process_data(data: list) -> list:
    """
    Process input data with validation and error handling.

    Args:
        data: List of items to process

    Returns:
        Processed list

    Raises:
        ValueError: If data is invalid
    """
    if not data:
        raise ValueError("Data cannot be empty")

    try:
        result = []
        for item in data:
            if isinstance(item, (int, float)):
                result.append(item * 2)
            else:
                result.append(str(item))
        return result
    except Exception as e:
        logging.error(f"Processing failed: {e}")
        raise

class DataProcessor:
    """Advanced data processor with caching"""

    def __init__(self, cache_size=100):
        self.cache = {}
        self.cache_size = cache_size

    def process(self, data):
        """Process with caching"""
        key = hash(str(data))
        if key in self.cache:
            return self.cache[key]

        result = process_data(data)

        if len(self.cache) >= self.cache_size:
            self.cache.pop(next(iter(self.cache)))

        self.cache[key] = result
        return result
'''

    def save_results(self):
        """Save results to file"""
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)

        # Save JSON
        results_file = results_dir / "benchmark_results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"Results saved to: {results_file}")

        # Append to history
        history_file = results_dir / "benchmark_history.csv"
        if not history_file.exists():
            with open(history_file, "w") as f:
                f.write("timestamp,benchmark,metric,value\n")

        with open(history_file, "a") as f:
            ts = self.results["timestamp"]
            for bench_name, bench_data in self.results["benchmarks"].items():
                status = bench_data["status"]
                duration = bench_data["duration"]
                f.write(f"{ts},{bench_name},status,{status}\n")
                f.write(f"{ts},{bench_name},duration,{duration}\n")

    def print_summary(self):
        """Print benchmark summary"""
        print()
        print("=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70)

        total = len(self.results["benchmarks"])
        passed = sum(1 for b in self.results["benchmarks"].values() if b["status"] == "PASS")
        failed = total - passed

        print(f"Total benchmarks: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print()

        if failed > 0:
            print("Failed benchmarks:")
            for name, data in self.results["benchmarks"].items():
                if data["status"] == "FAIL":
                    print(f"  - {name}: {data.get('error', 'Unknown error')}")
        else:
            print("All benchmarks passed! 🎉")

        print()
        print(f"Results saved to: benchmarks/results/benchmark_results.json")
        print("=" * 70)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run LJPW benchmarks")
    parser.add_argument("--quick", action="store_true", help="Quick smoke test")
    parser.add_argument("--report", action="store_true", help="Generate report only")

    args = parser.parse_args()

    if args.report:
        # Just print existing results
        results_file = Path(__file__).parent / "results" / "benchmark_results.json"
        if results_file.exists():
            with open(results_file) as f:
                results = json.load(f)
            print(json.dumps(results, indent=2))
        else:
            print("No results found. Run benchmarks first.")
        return

    suite = BenchmarkSuite(quick_mode=args.quick)
    suite.run_all()


if __name__ == "__main__":
    main()
