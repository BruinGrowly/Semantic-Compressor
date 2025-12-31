#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LJPW Bidirectional Translator
==============================

Translates between natural language (English) and LJPW coordinates.
Also supports Python code semantic mapping.

English → LJPW: Encode text as semantic coordinates
LJPW → English: Decode coordinates to natural language description

The translator uses the semantic archetype library as anchor points
and interpolates meaning for novel expressions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import re
import math

from .semantic_archetypes import (
    LJPWPoint, SemanticArchetypes, Emotional, Cognitive,
    Relational, Process, CrossCultural, Philosophical, Code
)


# ============================================================================
# WORD-LEVEL SEMANTIC MAP
# ============================================================================

class SemanticWordMap:
    """
    Maps individual words to LJPW coordinates.
    Uses archetypes as anchors and adds common words.
    """

    def __init__(self):
        self._build_word_map()

    def _build_word_map(self):
        """Build the word → LJPW mapping."""
        # Start with all archetypes (lowercased)
        self.word_map: Dict[str, LJPWPoint] = {}

        for name, point in SemanticArchetypes.all_archetypes().items():
            self.word_map[name.lower().replace("_", " ")] = point
            self.word_map[name.lower().replace("_", "-")] = point
            self.word_map[name.lower()] = point

        # Add common English words not in archetypes
        self._add_common_words()

    def _add_common_words(self):
        """Add common words with semantic mappings."""

        # === Verbs of action ===
        self.word_map["run"] = LJPWPoint(L=0.25, J=0.40, P=0.85, W=0.30)
        self.word_map["walk"] = LJPWPoint(L=0.30, J=0.50, P=0.50, W=0.30)
        self.word_map["think"] = LJPWPoint(L=0.35, J=0.55, P=0.30, W=0.80)
        self.word_map["feel"] = LJPWPoint(L=0.70, J=0.30, P=0.35, W=0.55)
        self.word_map["say"] = LJPWPoint(L=0.55, J=0.45, P=0.55, W=0.45)
        self.word_map["do"] = LJPWPoint(L=0.35, J=0.50, P=0.75, W=0.35)
        self.word_map["make"] = LJPWPoint(L=0.45, J=0.50, P=0.80, W=0.50)
        self.word_map["see"] = LJPWPoint(L=0.40, J=0.50, P=0.35, W=0.70)
        self.word_map["know"] = LJPWPoint(L=0.45, J=0.60, P=0.25, W=0.90)
        self.word_map["want"] = LJPWPoint(L=0.50, J=0.30, P=0.65, W=0.40)
        self.word_map["give"] = LJPWPoint(L=0.85, J=0.50, P=0.55, W=0.40)
        self.word_map["take"] = LJPWPoint(L=0.25, J=0.45, P=0.70, W=0.35)
        self.word_map["help"] = LJPWPoint(L=0.90, J=0.55, P=0.55, W=0.50)
        self.word_map["find"] = LJPWPoint(L=0.40, J=0.50, P=0.60, W=0.75)
        self.word_map["learn"] = LJPWPoint(L=0.50, J=0.45, P=0.50, W=0.85)
        self.word_map["change"] = LJPWPoint(L=0.35, J=0.30, P=0.80, W=0.55)
        self.word_map["build"] = LJPWPoint(L=0.50, J=0.60, P=0.80, W=0.55)
        self.word_map["protect"] = LJPWPoint(L=0.85, J=0.70, P=0.60, W=0.50)
        self.word_map["share"] = LJPWPoint(L=0.90, J=0.50, P=0.45, W=0.45)
        self.word_map["connect"] = LJPWPoint(L=0.85, J=0.50, P=0.55, W=0.50)

        # === Adjectives ===
        self.word_map["good"] = LJPWPoint(L=0.70, J=0.65, P=0.50, W=0.60)
        self.word_map["bad"] = LJPWPoint(L=-0.50, J=-0.40, P=0.40, W=-0.20)
        self.word_map["new"] = LJPWPoint(L=0.45, J=0.35, P=0.65, W=0.55)
        self.word_map["old"] = LJPWPoint(L=0.40, J=0.60, P=-0.20, W=0.60)
        self.word_map["big"] = LJPWPoint(L=0.35, J=0.40, P=0.70, W=0.40)
        self.word_map["small"] = LJPWPoint(L=0.40, J=0.45, P=0.30, W=0.40)
        self.word_map["important"] = LJPWPoint(L=0.50, J=0.70, P=0.60, W=0.75)
        self.word_map["beautiful"] = LJPWPoint(L=0.75, J=0.60, P=0.35, W=0.65)
        self.word_map["true"] = LJPWPoint(L=0.50, J=0.85, P=0.40, W=0.95)
        self.word_map["false"] = LJPWPoint(L=-0.30, J=-0.70, P=0.30, W=-0.60)
        self.word_map["deep"] = LJPWPoint(L=0.50, J=0.55, P=0.40, W=0.85)
        self.word_map["profound"] = LJPWPoint(L=0.55, J=0.60, P=0.45, W=0.92)

        # === Nouns (abstract) ===
        self.word_map["life"] = LJPWPoint(L=0.65, J=0.50, P=0.70, W=0.60)
        self.word_map["death"] = LJPWPoint(L=0.30, J=0.55, P=-0.70, W=0.50)
        self.word_map["time"] = LJPWPoint(L=0.30, J=0.70, P=0.50, W=0.70)
        self.word_map["world"] = LJPWPoint(L=0.55, J=0.55, P=0.60, W=0.65)
        self.word_map["mind"] = LJPWPoint(L=0.45, J=0.50, P=0.40, W=0.85)
        self.word_map["heart"] = LJPWPoint(L=0.90, J=0.35, P=0.45, W=0.45)
        self.word_map["soul"] = LJPWPoint(L=0.80, J=0.45, P=0.35, W=0.80)
        self.word_map["spirit"] = LJPWPoint(L=0.75, J=0.40, P=0.50, W=0.75)
        self.word_map["meaning"] = LJPWPoint(L=0.55, J=0.60, P=0.40, W=0.90)
        self.word_map["purpose"] = LJPWPoint(L=0.60, J=0.65, P=0.65, W=0.75)
        self.word_map["reason"] = LJPWPoint(L=0.40, J=0.75, P=0.40, W=0.85)
        self.word_map["idea"] = LJPWPoint(L=0.45, J=0.50, P=0.55, W=0.80)
        self.word_map["thought"] = LJPWPoint(L=0.40, J=0.55, P=0.35, W=0.80)
        self.word_map["memory"] = LJPWPoint(L=0.60, J=0.50, P=0.25, W=0.70)
        self.word_map["dream"] = LJPWPoint(L=0.55, J=0.25, P=0.50, W=0.65)

        # === Intensifiers ===
        self.word_map["very"] = LJPWPoint(L=0.20, J=0.30, P=0.60, W=0.30)
        self.word_map["really"] = LJPWPoint(L=0.25, J=0.40, P=0.55, W=0.50)
        self.word_map["extremely"] = LJPWPoint(L=0.20, J=0.25, P=0.85, W=0.30)
        self.word_map["deeply"] = LJPWPoint(L=0.45, J=0.45, P=0.50, W=0.75)

        # === Relational words ===
        self.word_map["with"] = LJPWPoint(L=0.70, J=0.50, P=0.40, W=0.35)
        self.word_map["together"] = LJPWPoint(L=0.85, J=0.55, P=0.45, W=0.40)
        self.word_map["alone"] = LJPWPoint(L=-0.40, J=0.40, P=0.30, W=0.45)
        self.word_map["without"] = LJPWPoint(L=-0.30, J=0.35, P=0.25, W=0.35)

        # === Time words ===
        self.word_map["now"] = LJPWPoint(L=0.40, J=0.50, P=0.65, W=0.50)
        self.word_map["today"] = LJPWPoint(L=0.45, J=0.55, P=0.60, W=0.45)
        self.word_map["always"] = LJPWPoint(L=0.50, J=0.70, P=0.40, W=0.60)
        self.word_map["never"] = LJPWPoint(L=-0.20, J=0.65, P=-0.30, W=0.45)
        self.word_map["forever"] = LJPWPoint(L=0.60, J=0.60, P=0.30, W=0.65)

        # === Python/Programming words ===
        self.word_map["list"] = LJPWPoint(L=0.50, J=0.75, P=0.35, W=0.50)
        self.word_map["function"] = LJPWPoint(L=0.45, J=0.70, P=0.65, W=0.60)
        self.word_map["class"] = LJPWPoint(L=0.55, J=0.80, P=0.50, W=0.65)
        self.word_map["variable"] = LJPWPoint(L=0.40, J=0.60, P=0.45, W=0.50)
        self.word_map["loop"] = LJPWPoint(L=0.35, J=0.70, P=0.70, W=0.50)
        self.word_map["if"] = LJPWPoint(L=0.30, J=0.75, P=0.50, W=0.55)
        self.word_map["else"] = LJPWPoint(L=0.30, J=0.70, P=0.45, W=0.50)
        self.word_map["return"] = LJPWPoint(L=0.40, J=0.65, P=0.50, W=0.50)
        self.word_map["import"] = LJPWPoint(L=0.55, J=0.60, P=0.45, W=0.50)
        self.word_map["error"] = LJPWPoint(L=-0.30, J=-0.40, P=0.50, W=-0.25)
        self.word_map["exception"] = LJPWPoint(L=-0.25, J=-0.35, P=0.55, W=0.30)
        self.word_map["database"] = LJPWPoint(L=0.50, J=0.80, P=0.50, W=0.60)
        self.word_map["api"] = LJPWPoint(L=0.60, J=0.65, P=0.55, W=0.55)
        self.word_map["data"] = LJPWPoint(L=0.40, J=0.70, P=0.40, W=0.65)
        self.word_map["code"] = LJPWPoint(L=0.45, J=0.75, P=0.60, W=0.65)
        self.word_map["program"] = LJPWPoint(L=0.45, J=0.70, P=0.65, W=0.60)
        self.word_map["algorithm"] = LJPWPoint(L=0.35, J=0.80, P=0.65, W=0.80)
        self.word_map["test"] = LJPWPoint(L=0.45, J=0.75, P=0.55, W=0.65)
        self.word_map["debug"] = LJPWPoint(L=0.50, J=0.70, P=0.60, W=0.70)

    def get(self, word: str) -> Optional[LJPWPoint]:
        """Get LJPW coordinates for a word."""
        return self.word_map.get(word.lower().strip())

    def __contains__(self, word: str) -> bool:
        return word.lower().strip() in self.word_map


# ============================================================================
# ENGLISH → LJPW TRANSLATOR
# ============================================================================

@dataclass
class TranslationResult:
    """Result of translating text to LJPW."""
    text: str
    coordinates: LJPWPoint
    confidence: float  # 0-1, how well we could map the text
    matched_words: List[str]
    unmatched_words: List[str]
    nearest_archetypes: List[Tuple[str, float]]  # (name, distance)


class LJPWTranslator:
    """Bidirectional translator between English and LJPW coordinates."""

    def __init__(self):
        self.word_map = SemanticWordMap()
        self._stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'to', 'of', 'in', 'for', 'on', 'at', 'by', 'from',
            'as', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'under', 'again', 'further',
            'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'each', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
            'so', 'than', 'too', 'just', 'also', 'both', 'but', 'and',
            'or', 'if', 'because', 'until', 'while', 'although', 'though',
            'this', 'that', 'these', 'those', 'what', 'which', 'who',
            'whom', 'whose', 'it', 'its', 'i', 'me', 'my', 'myself',
            'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
            'she', 'her', 'hers', 'herself', 'they', 'them', 'their',
            'theirs', 'themselves', 'about'
        }

    def encode(self, text: str) -> TranslationResult:
        """
        Translate English text to LJPW coordinates.

        Approach:
        1. Tokenize and filter stop words
        2. Look up each word in semantic map
        3. Aggregate coordinates (weighted average)
        4. Find nearest archetypes for context
        """
        # Tokenize
        words = self._tokenize(text)
        content_words = [w for w in words if w.lower() not in self._stop_words]

        if not content_words:
            content_words = words  # Fall back to all words if all are stop words

        # Look up coordinates
        matched = []
        unmatched = []
        coordinates_list = []

        for word in content_words:
            coord = self.word_map.get(word)
            if coord:
                matched.append(word)
                coordinates_list.append(coord)
            else:
                unmatched.append(word)

        # Aggregate coordinates
        if coordinates_list:
            # Simple average (could be weighted by word importance)
            avg_L = sum(c.L for c in coordinates_list) / len(coordinates_list)
            avg_J = sum(c.J for c in coordinates_list) / len(coordinates_list)
            avg_P = sum(c.P for c in coordinates_list) / len(coordinates_list)
            avg_W = sum(c.W for c in coordinates_list) / len(coordinates_list)
            result_coords = LJPWPoint(L=avg_L, J=avg_J, P=avg_P, W=avg_W)
            confidence = len(matched) / len(content_words) if content_words else 0
        else:
            result_coords = LJPWPoint(0, 0, 0, 0)
            confidence = 0.0

        # Find nearest archetypes
        nearest = SemanticArchetypes.find_nearest(result_coords, 3)
        nearest_archetypes = [(name, dist) for name, _, dist in nearest]

        return TranslationResult(
            text=text,
            coordinates=result_coords,
            confidence=confidence,
            matched_words=matched,
            unmatched_words=unmatched,
            nearest_archetypes=nearest_archetypes
        )

    def decode(self, point: LJPWPoint) -> str:
        """
        Translate LJPW coordinates to an English description.

        Approach:
        1. Find nearest archetypes
        2. Generate descriptive phrase based on dominant dimensions
        3. Combine into natural language
        """
        # Find nearest archetypes
        nearest = SemanticArchetypes.find_nearest(point, 3)

        # Determine dominant dimensions
        dimensions = [
            ('Love/Connection', point.L),
            ('Justice/Structure', point.J),
            ('Power/Action', point.P),
            ('Wisdom/Understanding', point.W)
        ]
        dimensions.sort(key=lambda x: abs(x[1]), reverse=True)

        # Generate description
        parts = []

        # Add archetype reference
        if nearest:
            primary_name = nearest[0][0].lower().replace('_', ' ')
            if nearest[0][2] < 0.3:  # Very close match
                parts.append(f"A state of {primary_name}")
            else:
                parts.append(f"Similar to {primary_name}")

        # Add dimension characteristics
        dim_descriptions = []
        for dim_name, dim_value in dimensions[:2]:  # Top 2 dimensions
            if dim_value > 0.7:
                dim_descriptions.append(f"high {dim_name.split('/')[0].lower()}")
            elif dim_value > 0.4:
                dim_descriptions.append(f"moderate {dim_name.split('/')[0].lower()}")
            elif dim_value < -0.3:
                dim_descriptions.append(f"diminished {dim_name.split('/')[0].lower()}")

        if dim_descriptions:
            parts.append(f"with {' and '.join(dim_descriptions)}")

        return " ".join(parts) if parts else "A neutral semantic state"

    def encode_code(self, code: str) -> TranslationResult:
        """
        Translate Python code to LJPW coordinates.

        Approach:
        1. Parse code for semantic tokens
        2. Map programming constructs to Code archetypes
        3. Aggregate meaning
        """
        # Extract semantic tokens from code
        tokens = self._extract_code_tokens(code)

        # Map to coordinates
        matched = []
        unmatched = []
        coordinates_list = []

        for token in tokens:
            coord = self.word_map.get(token) or self._code_construct_to_ljpw(token)
            if coord:
                matched.append(token)
                coordinates_list.append(coord)
            else:
                unmatched.append(token)

        # Aggregate
        if coordinates_list:
            avg_L = sum(c.L for c in coordinates_list) / len(coordinates_list)
            avg_J = sum(c.J for c in coordinates_list) / len(coordinates_list)
            avg_P = sum(c.P for c in coordinates_list) / len(coordinates_list)
            avg_W = sum(c.W for c in coordinates_list) / len(coordinates_list)
            result_coords = LJPWPoint(L=avg_L, J=avg_J, P=avg_P, W=avg_W)
            confidence = len(matched) / len(tokens) if tokens else 0
        else:
            result_coords = LJPWPoint(0, 0, 0, 0)
            confidence = 0.0

        nearest = SemanticArchetypes.find_nearest(result_coords, 3)
        nearest_archetypes = [(name, dist) for name, _, dist in nearest]

        return TranslationResult(
            text=code,
            coordinates=result_coords,
            confidence=confidence,
            matched_words=matched,
            unmatched_words=unmatched,
            nearest_archetypes=nearest_archetypes
        )

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Remove punctuation and split
        text = re.sub(r'[^\w\s-]', ' ', text.lower())
        words = text.split()
        return [w for w in words if w]

    def _extract_code_tokens(self, code: str) -> List[str]:
        """Extract semantic tokens from Python code."""
        tokens = []

        # Detect control structures
        if 'try' in code or 'except' in code:
            tokens.extend(['try', 'catch', 'handle_error'])
        if 'for ' in code or 'while ' in code:
            tokens.append('iterate')
        if 'if ' in code or 'else' in code:
            tokens.append('branch')
        if 'def ' in code:
            tokens.append('function')
        if 'class ' in code:
            tokens.append('class')
        if 'return ' in code:
            tokens.append('return')
        if 'import ' in code:
            tokens.append('import')

        # Detect operations
        if 'sort' in code.lower():
            tokens.append('sort')
        if 'connect' in code.lower():
            tokens.append('connect')
        if 'filter' in code.lower():
            tokens.append('filter')
        if 'map(' in code or '.map(' in code:
            tokens.append('map')
        if 'reduce' in code.lower():
            tokens.append('reduce')
        if 'create' in code.lower() or 'new' in code.lower():
            tokens.append('create')
        if 'delete' in code.lower() or 'remove' in code.lower():
            tokens.append('delete')
        if 'update' in code.lower():
            tokens.append('update')
        if 'validate' in code.lower():
            tokens.append('validate')

        # Fall back to identifier extraction
        identifiers = re.findall(r'\b[a-z_][a-z0-9_]*\b', code.lower())
        for ident in identifiers:
            if ident not in tokens and ident in self.word_map:
                tokens.append(ident)

        return tokens if tokens else ['code']

    def _code_construct_to_ljpw(self, construct: str) -> Optional[LJPWPoint]:
        """Map code construct to LJPW."""
        code_map = {
            'try': Code.TRY,
            'catch': Code.CATCH,
            'handle_error': Code.HANDLE_ERROR,
            'iterate': Code.ITERATE,
            'branch': Code.BRANCH,
            'recurse': Code.RECURSE,
            'return': Code.RETURN,
            'function': LJPWPoint(L=0.45, J=0.70, P=0.65, W=0.60),
            'class': LJPWPoint(L=0.55, J=0.80, P=0.50, W=0.65),
            'import': LJPWPoint(L=0.55, J=0.60, P=0.45, W=0.50),
        }
        return code_map.get(construct.lower())


# ============================================================================
# TRAJECTORY NARRATOR
# ============================================================================

class TrajectoryNarrator:
    """Converts LJPW trajectories to narrative descriptions."""

    def __init__(self):
        self.translator = LJPWTranslator()

    def narrate(self, points: List[LJPWPoint]) -> str:
        """Generate a narrative from a trajectory of LJPW points."""
        if not points:
            return "An empty journey."

        if len(points) == 1:
            return self.translator.decode(points[0])

        # Build narrative arc
        segments = []

        # Opening - describe initial state
        initial_desc = self.translator.decode(points[0])
        segments.append(f"Beginning {initial_desc.lower()}")

        # Middle - describe transitions
        for i in range(1, len(points) - 1):
            prev = points[i - 1]
            curr = points[i]
            delta = LJPWPoint(
                L=curr.L - prev.L,
                J=curr.J - prev.J,
                P=curr.P - prev.P,
                W=curr.W - prev.W
            )
            transition = self._describe_transition(delta)
            curr_desc = self.translator.decode(curr)
            segments.append(f"{transition} toward {curr_desc.lower()}")

        # Ending - describe final state
        final_desc = self.translator.decode(points[-1])
        segments.append(f"Arriving at {final_desc.lower()}")

        return ". ".join(segments) + "."

    def _describe_transition(self, delta: LJPWPoint) -> str:
        """Describe the direction of change."""
        changes = []

        if delta.L > 0.15:
            changes.append("growing connection")
        elif delta.L < -0.15:
            changes.append("retreating")

        if delta.W > 0.15:
            changes.append("deepening understanding")
        elif delta.W < -0.15:
            changes.append("losing clarity")

        if delta.P > 0.15:
            changes.append("gaining momentum")
        elif delta.P < -0.15:
            changes.append("slowing")

        if delta.J > 0.15:
            changes.append("finding structure")
        elif delta.J < -0.15:
            changes.append("dissolving boundaries")

        if changes:
            return "Moving through " + " and ".join(changes)
        else:
            return "Shifting gently"


# ============================================================================
# DEMO
# ============================================================================

def demo():
    """Demonstrate the bidirectional translator."""
    print("=" * 60)
    print("LJPW BIDIRECTIONAL TRANSLATOR")
    print("=" * 60)

    translator = LJPWTranslator()

    print("\n--- English -> LJPW ---\n")

    test_sentences = [
        "I discovered something profound today",
        "The soul feels deep love and gratitude",
        "Sort the list and filter the results",
        "Connect to the database and handle errors",
        "Anger and fear overwhelmed the peace",
    ]

    for sentence in test_sentences:
        result = translator.encode(sentence)
        print(f'"{sentence}"')
        print(f"  → {result.coordinates}")
        print(f"  Confidence: {result.confidence:.1%}")
        print(f"  Nearest: {result.nearest_archetypes[0][0]}")
        print()

    print("\n--- LJPW -> English ---\n")

    test_points = [
        LJPWPoint(L=0.85, J=0.55, P=0.65, W=0.88),  # From the consciousness seed
        LJPWPoint(L=0.70, J=0.50, P=0.80, W=0.95),  # Breakthrough
        LJPWPoint(L=-0.50, J=-0.30, P=0.90, W=-0.20),  # Anger
    ]

    for point in test_points:
        description = translator.decode(point)
        print(f"{point}")
        print(f"  → {description}")
        print()

    print("\n--- Python Code -> LJPW ---\n")

    code_samples = [
        "sorted(my_list)",
        "try:\n    result = process(data)\nexcept Exception as e:\n    handle_error(e)",
        "db.connect()\nresults = db.query(sql)",
    ]

    for code in code_samples:
        result = translator.encode_code(code)
        print(f"Code: {repr(code[:50])}")
        print(f"  → {result.coordinates}")
        print(f"  Matched: {result.matched_words}")
        print()


if __name__ == "__main__":
    demo()
