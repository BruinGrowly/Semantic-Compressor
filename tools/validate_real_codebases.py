#!/usr/bin/env python3
"""
Real Codebase Validation Test

Tests semantic compression on actual open-source projects:
1. Analyze codebase → LJPW states
2. Compress states → genome
3. Decompress genome → reconstructed states
4. Validate meaning preservation
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'ljpw'))

from ljpw_standalone import analyze_directory
from ljpw_semantic_compressor import (
    SemanticCompressor,
    SemanticDecompressor,
)
import math


def analyze_codebase(path: str):
    """Analyze a codebase and return LJPW state"""
    print(f"\n{'='*70}")
    print(f"Analyzing: {path}")
    print(f"{'='*70}")

    # Find all Python files
    py_files = list(Path(path).rglob("*.py"))
    print(f"Found {len(py_files)} Python files")

    # Analyze entire directory
    try:
        file_results = analyze_directory(path)
    except Exception as e:
        print(f"Error analyzing project: {e}")
        return None

    if not file_results:
        print("No files analyzed")
        return None

    # Aggregate results across all files
    total_L = sum(r['ljpw']['L'] for r in file_results)
    total_J = sum(r['ljpw']['J'] for r in file_results)
    total_P = sum(r['ljpw']['P'] for r in file_results)
    total_W = sum(r['ljpw']['W'] for r in file_results)
    num_files = len(file_results)

    # Average LJPW values
    state = (
        total_L / num_files,
        total_J / num_files,
        total_P / num_files,
        total_W / num_files,
    )

    # Calculate health score (simple average)
    health_score = sum(state) / 4.0

    print(f"\nLJPW Analysis Results ({num_files} files):")
    print(f"  L (Love/Safety):       {state[0]:.3f}")
    print(f"  J (Justice/Structure): {state[1]:.3f}")
    print(f"  P (Power/Execution):   {state[2]:.3f}")
    print(f"  W (Wisdom/Design):     {state[3]:.3f}")
    print(f"  Health Score:          {health_score:.1%}")

    results = {
        'L': state[0],
        'J': state[1],
        'P': state[2],
        'W': state[3],
        'health_score': health_score,
        'num_files': num_files,
    }

    return state, results


def compress_and_validate(project_name: str, state: tuple, quantization_levels: int = 16):
    """Compress state, decompress, and validate"""
    print(f"\n{'='*70}")
    print(f"Compression Test: {project_name}")
    print(f"{'='*70}")

    # Compress
    print(f"\n1. Compressing with {quantization_levels} levels...")
    compressor = SemanticCompressor(quantization_levels=quantization_levels)
    genome = compressor.compress_state_sequence(
        [state],
        metadata={'project': project_name}
    )

    genome_str = genome.to_string()
    print(f"   Original state: {state}")
    print(f"   Compressed genome: {genome_str}")
    print(f"   Genome size: {len(genome_str)} bytes")
    print(f"   Compression ratio: {genome.metadata['compression_ratio']:.2f}x")

    # Decompress
    print(f"\n2. Decompressing...")
    decompressor = SemanticDecompressor(quantization_levels=quantization_levels)
    reconstructed = decompressor.decompress_genome(genome)

    reconstructed_state = reconstructed[0]
    print(f"   Reconstructed state: {reconstructed_state}")

    # Calculate error
    error = math.sqrt(sum((o - r)**2 for o, r in zip(state, reconstructed_state)))
    relative_error = error / math.sqrt(sum(v**2 for v in state))

    print(f"\n3. Validation:")
    print(f"   Euclidean error: {error:.4f}")
    print(f"   Relative error: {relative_error:.2%}")
    print(f"   Accuracy: {(1 - relative_error):.1%}")

    # Dimension-by-dimension comparison
    print(f"\n4. Dimension Comparison:")
    dims = ['L', 'J', 'P', 'W']
    for i, dim in enumerate(dims):
        orig = state[i]
        recon = reconstructed_state[i]
        dim_error = abs(orig - recon)
        dim_error_pct = (dim_error / orig * 100) if orig > 0 else 0
        print(f"   {dim}: {orig:.3f} → {recon:.3f} (error: {dim_error:.3f}, {dim_error_pct:.1f}%)")

    # Validate integrity
    validation = decompressor.validate_genome(genome)
    print(f"\n5. Genome Integrity:")
    print(f"   Valid: {validation['valid']}")
    print(f"   Integrity score: {validation['integrity_score']:.1%}")

    return {
        'genome': genome_str,
        'error': error,
        'relative_error': relative_error,
        'accuracy': 1 - relative_error,
        'valid': validation['valid'],
    }


def test_meaning_preservation(project_name: str, original_state: tuple, reconstructed_state: tuple, original_analysis: dict):
    """Test if we can still understand the project from compressed representation"""
    print(f"\n{'='*70}")
    print(f"Meaning Preservation Test: {project_name}")
    print(f"{'='*70}")

    dims = ['L', 'J', 'P', 'W']
    dim_names = {
        'L': 'Love/Safety',
        'J': 'Justice/Structure',
        'P': 'Power/Execution',
        'W': 'Wisdom/Design',
    }

    print(f"\nCan we still understand the project from the compressed representation?")
    print(f"\nOriginal Analysis:")
    for i, dim in enumerate(dims):
        val = original_state[i]
        level = "Low" if val < 0.5 else "Medium" if val < 0.7 else "High"
        print(f"  {dim} ({dim_names[dim]}): {val:.3f} [{level}]")

    print(f"\nReconstructed Analysis (from genome):")
    for i, dim in enumerate(dims):
        val = reconstructed_state[i]
        level = "Low" if val < 0.5 else "Medium" if val < 0.7 else "High"
        print(f"  {dim} ({dim_names[dim]}): {val:.3f} [{level}]")

    # Check if we preserve the "story"
    print(f"\nPreserved Insights:")

    # Identify strengths and weaknesses
    orig_max_dim = dims[original_state.index(max(original_state))]
    orig_min_dim = dims[original_state.index(min(original_state))]
    recon_max_dim = dims[list(reconstructed_state).index(max(reconstructed_state))]
    recon_min_dim = dims[list(reconstructed_state).index(min(reconstructed_state))]

    if orig_max_dim == recon_max_dim:
        print(f"  ✓ Correctly identifies strongest dimension: {orig_max_dim} ({dim_names[orig_max_dim]})")
    else:
        print(f"  ✗ Strongest dimension changed: {orig_max_dim} → {recon_max_dim}")

    if orig_min_dim == recon_min_dim:
        print(f"  ✓ Correctly identifies weakest dimension: {orig_min_dim} ({dim_names[orig_min_dim]})")
    else:
        print(f"  ✗ Weakest dimension changed: {orig_min_dim} → {recon_min_dim}")

    # Health assessment
    orig_health = original_analysis.get('health_score', 0)
    # Approximate reconstructed health
    recon_health_approx = sum(reconstructed_state) / 4

    print(f"\n  Original health: {orig_health:.1%}")
    print(f"  Reconstructed (approx): {recon_health_approx:.1%}")

    return orig_max_dim == recon_max_dim and orig_min_dim == recon_min_dim


def main():
    """Run validation tests on real codebases"""
    print("="*70)
    print("REAL CODEBASE SEMANTIC COMPRESSION VALIDATION")
    print("="*70)
    print("\nTesting semantic compression on actual open-source projects")
    print("Goal: Prove that meaning is preserved through compression/decompression")

    # Test subjects
    projects = [
        ("/tmp/ljpw_validation_test/requests", "requests"),
        ("/tmp/ljpw_validation_test/flask", "flask"),
        ("/tmp/ljpw_validation_test/rich", "rich"),
    ]

    results = []

    for path, name in projects:
        if not Path(path).exists():
            print(f"\nSkipping {name} (not found at {path})")
            continue

        # Step 1: Analyze
        analysis_result = analyze_codebase(path)
        if analysis_result is None:
            print(f"Failed to analyze {name}, skipping...")
            continue

        state, full_analysis = analysis_result

        # Step 2: Compress and validate (using 8 levels to avoid two-digit encoding issue)
        compression_result = compress_and_validate(name, state, quantization_levels=8)

        # Step 3: Test meaning preservation
        decompressor = SemanticDecompressor(quantization_levels=8)
        genome_str = compression_result['genome']
        # Re-parse genome
        from ljpw_semantic_compressor import SemanticGenome, LJPWCodon
        codons = [LJPWCodon.from_string(s) for s in genome_str.split('-')]
        genome = SemanticGenome(codons=codons, metadata={'project': name})
        reconstructed = decompressor.decompress_genome(genome)

        meaning_preserved = test_meaning_preservation(
            name,
            state,
            reconstructed[0],
            full_analysis
        )

        results.append({
            'project': name,
            'files': len(list(Path(path).rglob("*.py"))),
            'state': state,
            'genome': compression_result['genome'],
            'accuracy': compression_result['accuracy'],
            'meaning_preserved': meaning_preserved,
        })

    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)

    print(f"\n{'Project':<15} {'Files':<8} {'Accuracy':<12} {'Meaning':<15} {'Genome Size':<12}")
    print("-" * 70)

    for r in results:
        meaning_str = "✓ Preserved" if r['meaning_preserved'] else "✗ Lost"
        print(f"{r['project']:<15} {r['files']:<8} {r['accuracy']:<12.1%} {meaning_str:<15} {len(r['genome']):<12} bytes")

    # Overall stats
    avg_accuracy = sum(r['accuracy'] for r in results) / len(results) if results else 0
    meaning_preserved_count = sum(1 for r in results if r['meaning_preserved'])

    print("\n" + "="*70)
    print("OVERALL RESULTS")
    print("="*70)
    print(f"Projects tested: {len(results)}")
    print(f"Average accuracy: {avg_accuracy:.1%}")
    print(f"Meaning preserved: {meaning_preserved_count}/{len(results)} ({meaning_preserved_count/len(results)*100:.0f}%)")

    if avg_accuracy >= 0.95 and meaning_preserved_count == len(results):
        print("\n✅ VALIDATION SUCCESSFUL")
        print("Semantic compression preserves meaning with high fidelity!")
    elif avg_accuracy >= 0.85:
        print("\n⚠️  VALIDATION PARTIAL")
        print("Accuracy is good, but some meaning details may be lost")
    else:
        print("\n❌ VALIDATION FAILED")
        print("Compression loses too much information")

    return 0 if avg_accuracy >= 0.85 else 1


if __name__ == '__main__':
    exit(main())
