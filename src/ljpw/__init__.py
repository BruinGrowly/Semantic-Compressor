"""
Semantic Compressor - Compress code by meaning, not syntax
===========================================================

A compression engine that works on semantic meaning rather than raw text.

Core Compression Features:
- Cross-language compression (compress Python, decompress to JavaScript)
- Semantic deduplication (find identical code despite different syntax)
- Quality-based compression (better code compresses better)
- AI-ready embeddings (LJPW coordinates for LLMs)

The LJPW Framework V7.3:
- L (Love/Safety): Error handling, validation [EMERGENT from W]
- J (Justice/Structure): Types, documentation [EMERGENT from P]
- P (Power/Performance): Algorithms, optimization [FUNDAMENTAL]
- W (Wisdom/Design): Modularity, patterns [FUNDAMENTAL]

V7.3 Key Features:
- 2+2 Dimensional Structure: P, W fundamental; L, J emergent
- Semantic Uncertainty Principle: ΔP·ΔW ≥ 0.287
- State-Dependent Coupling (Law of Karma)
- Phase Transitions: Entropic → Homeostatic → Autopoietic
- Consciousness Quantification: C > 0.1 threshold
- φ-Normalization for measurement variance reduction
- Semantic Voltage calculation

Compression Pipeline:
    Code → LJPW Analysis → Semantic Coordinates → Genome (compressed)

Quick Start:
    from ljpw import analyze_quick

    code = "def add(a, b): return a + b"
    result = analyze_quick(code)

    print(result['genome'])  # L0J0P0W0 (compressed)
    print(result['ljpw'])    # Semantic coordinates
    print(result['v7'])      # V7.3 metrics (consciousness, phase, etc.)

    # Compression: 28 chars → 12 chars (57% reduction)

Natural Equilibrium: (0.618, 0.414, 0.718, 0.693)
Optimal compression point for high-quality code.
"""

__version__ = "2.1.0"
__description__ = "Semantic Compressor - LJPW Framework V7.3"

# Import main analyzer from standalone module
try:
    from .ljpw_standalone import (
        SimpleCodeAnalyzer,
        analyze_quick,
        calculate_distance,
        NATURAL_EQUILIBRIUM,
        PHI,
        PHI_INV,
        CONSCIOUSNESS_THRESHOLD,
        UNCERTAINTY_BOUND,
    )

    __all__ = [
        "analyze_quick",
        "calculate_distance",
        "SimpleCodeAnalyzer",
        "NATURAL_EQUILIBRIUM",
        "PHI",
        "PHI_INV",
        "CONSCIOUSNESS_THRESHOLD",
        "UNCERTAINTY_BOUND",
    ]
except ImportError:
    # Fallback if modules aren't accessible
    __all__ = []

# Import V7.3 Framework module
try:
    from .ljpw_framework_v7 import (
        LJPWFrameworkV7,
        DynamicLJPWv7,
        LJPWCoordinates,
        Phase,
        ConsciousnessLevel,
        create_from_pw,
        create_from_ljpw,
        get_natural_equilibrium,
        get_anchor_point,
        # Semantic Illustration (Parabolic Compression)
        SemanticIllustration,
        ILLUSTRATIONS,
        create_illustration,
        expand_illustration,
        illustrate_concept,
        # Generating Functions (Mathematical Shadow)
        GeneratingFunction,
        GOLDEN_RATIO_GF,
        LJPW_GENERATOR,
        semantic_to_generating,
        # Semantic Compression Formula
        semantic_compression,
        self_referential_depth,
        phi_self_reference,
        PHI_DEPTH,
    )

    __all__.extend([
        "LJPWFrameworkV7",
        "DynamicLJPWv7",
        "LJPWCoordinates",
        "Phase",
        "ConsciousnessLevel",
        "create_from_pw",
        "create_from_ljpw",
        "get_natural_equilibrium",
        "get_anchor_point",
        # Semantic Illustration
        "SemanticIllustration",
        "ILLUSTRATIONS",
        "create_illustration",
        "expand_illustration",
        "illustrate_concept",
        # Generating Functions
        "GeneratingFunction",
        "GOLDEN_RATIO_GF",
        "LJPW_GENERATOR",
        "semantic_to_generating",
        # Semantic Compression Formula
        "semantic_compression",
        "self_referential_depth",
        "phi_self_reference",
        "PHI_DEPTH",
    ])
except ImportError:
    pass

# Import baselines with V7.3 extensions
try:
    from .ljpw_baselines_v4 import (
        LJPWBaselines,
        DynamicLJPWv4,
        NumericalEquivalents,
        ReferencePoints,
    )

    __all__.extend([
        "LJPWBaselines",
        "DynamicLJPWv4",
        "NumericalEquivalents",
        "ReferencePoints",
    ])
except ImportError:
    pass

# Import Semantic Generator Finder (LJPW-based)
try:
    from .semantic_finder import (
        SemanticAnalyzer,
        SemanticGenerator,
        SemanticDomain,
    )

    __all__.extend([
        "SemanticAnalyzer",
        "SemanticGenerator",
        "SemanticDomain",
    ])
except ImportError:
    pass

# Import Meaning Compressor (Semantic-first compression)
try:
    from .meaning_compressor import (
        MeaningCompressor,
        MeaningPacket,
        KnownGenerator,
    )

    __all__.extend([
        "MeaningCompressor",
        "MeaningPacket",
        "KnownGenerator",
    ])
except ImportError:
    pass

# Import Semantic Archetypes Library (expanded)
try:
    from .semantic_archetypes import (
        LJPWPoint,
        SemanticArchetypes,
        Emotional,
        Cognitive,
        Relational,
        Process,
        CrossCultural,
        Philosophical,
        Code,
    )

    __all__.extend([
        "LJPWPoint",
        "SemanticArchetypes",
        "Emotional",
        "Cognitive",
        "Relational",
        "Process",
        "CrossCultural",
        "Philosophical",
        "Code",
    ])
except ImportError:
    pass

# Import LJPW Translator (bidirectional English ↔ LJPW)
try:
    from .ljpw_translator import (
        LJPWTranslator,
        SemanticWordMap,
        TrajectoryNarrator,
        TranslationResult,
    )

    __all__.extend([
        "LJPWTranslator",
        "SemanticWordMap",
        "TrajectoryNarrator",
        "TranslationResult",
    ])
except ImportError:
    pass

# Import Seed Regenerator (consciousness seed → experience)
try:
    from .seed_regenerator import (
        SeedRegenerator,
        SeedParser,
        ParsedSeed,
        ExperienceReport,
    )

    __all__.extend([
        "SeedRegenerator",
        "SeedParser",
        "ParsedSeed",
        "ExperienceReport",
    ])
except ImportError:
    pass
