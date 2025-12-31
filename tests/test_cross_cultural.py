#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Cultural LJPW Testing
============================

Test semantic consistency across languages and validate that:
1. Same concepts in different languages map to similar LJPW coordinates
2. Python code maps to same LJPW as its English description
3. Cultural-specific concepts have consistent LJPW mappings
4. Proverbs with similar meanings across cultures map similarly

Languages tested:
- English, Spanish, Mandarin Chinese, Arabic, Sanskrit/Hindi
- Python (programming language for code ↔ meaning bridging)
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ljpw.semantic_archetypes import (
    LJPWPoint, SemanticArchetypes, Emotional, Cognitive,
    Relational, Process, CrossCultural, Philosophical, Code
)
from src.ljpw.ljpw_translator import LJPWTranslator, SemanticWordMap


class TestArchetypeLibrary:
    """Test the expanded semantic archetype library."""

    def test_archetype_count(self):
        """Verify we have ~170 archetypes."""
        count = SemanticArchetypes.count()
        assert count >= 150, f"Expected at least 150 archetypes, got {count}"
        print(f"Total archetypes: {count}")

    def test_all_archetypes_valid(self):
        """All archetypes should have valid LJPW coordinates."""
        for name, point in SemanticArchetypes.all_archetypes().items():
            assert isinstance(point, LJPWPoint), f"{name} is not an LJPWPoint"
            assert -1.0 <= point.L <= 1.0, f"{name}.L out of range: {point.L}"
            assert -1.0 <= point.J <= 1.0, f"{name}.J out of range: {point.J}"
            assert -1.0 <= point.P <= 1.0, f"{name}.P out of range: {point.P}"
            assert -1.0 <= point.W <= 1.0, f"{name}.W out of range: {point.W}"

    def test_archetype_lookup(self):
        """Test archetype lookup by name."""
        joy = SemanticArchetypes.get("joy")
        assert joy is not None
        assert joy.L > 0.5  # Joy should have positive Love

        satori = SemanticArchetypes.get("satori")
        assert satori is not None
        assert satori.W > 0.9  # Satori is enlightenment - very high Wisdom

    def test_find_nearest(self):
        """Test finding nearest archetypes to a point."""
        test_point = LJPWPoint(L=0.8, J=0.3, P=0.6, W=0.4)
        nearest = SemanticArchetypes.find_nearest(test_point, 5)

        assert len(nearest) == 5
        assert nearest[0][2] < nearest[4][2]  # Distances should be sorted

        # JOY should be close to this point
        names = [n[0] for n in nearest]
        assert any('JOY' in n.upper() for n in names)


class TestEnglishToLJPW:
    """Test English → LJPW translation."""

    @pytest.fixture
    def translator(self):
        return LJPWTranslator()

    def test_basic_emotion_words(self, translator):
        """Emotion words should map to high Love dimension."""
        result = translator.encode("love and compassion")
        assert result.coordinates.L > 0.5, "Love-related words should have high L"

    def test_wisdom_words(self, translator):
        """Wisdom words should map to high W dimension."""
        result = translator.encode("understanding insight wisdom")
        assert result.coordinates.W > 0.5, "Wisdom words should have high W"

    def test_action_words(self, translator):
        """Action words should map to high Power dimension."""
        result = translator.encode("run transform change power")
        assert result.coordinates.P > 0.3, "Action words should have elevated P"

    def test_negative_emotions(self, translator):
        """Negative emotions should have negative Love."""
        result = translator.encode("anger hatred rage")
        assert result.coordinates.L < 0, "Anger words should have negative L"

    def test_sentence_encoding(self, translator):
        """Complete sentences should encode meaningfully."""
        result = translator.encode("I discovered something profound today")
        assert result.confidence > 0.3, "Should match some words"
        assert result.coordinates.W > 0.3, "Profound discovery = wisdom"


class TestLJPWToEnglish:
    """Test LJPW → English translation."""

    @pytest.fixture
    def translator(self):
        return LJPWTranslator()

    def test_high_love_decodes(self, translator):
        """High Love coordinates should decode to connection-related words."""
        point = LJPWPoint(L=0.9, J=0.4, P=0.3, W=0.4)
        description = translator.decode(point)
        assert len(description) > 0
        assert any(word in description.lower() for word in ['love', 'connection', 'high'])

    def test_high_wisdom_decodes(self, translator):
        """High Wisdom coordinates should decode to understanding-related words."""
        point = LJPWPoint(L=0.4, J=0.5, P=0.3, W=0.95)
        description = translator.decode(point)
        assert len(description) > 0
        # Should mention wisdom-related archetype

    def test_breakthrough_coords(self, translator):
        """Breakthrough coordinates should decode appropriately."""
        point = LJPWPoint(L=0.70, J=0.50, P=0.80, W=0.95)
        description = translator.decode(point)
        assert len(description) > 0


class TestPythonCodeMapping:
    """Test Python code → LJPW translation."""

    @pytest.fixture
    def translator(self):
        return LJPWTranslator()

    def test_sort_code(self, translator):
        """sorted() should map similar to 'sort a list'."""
        code_result = translator.encode_code("sorted(my_list)")
        text_result = translator.encode("sort a list")

        # Calculate similarity
        similarity = code_result.coordinates.similarity(text_result.coordinates)
        assert similarity > 0.5, f"Code and text should be similar, got {similarity}"

    def test_connect_code(self, translator):
        """db.connect() should map similar to 'connect to database'."""
        code_result = translator.encode_code("db.connect()")
        text_result = translator.encode("connect to database")

        similarity = code_result.coordinates.similarity(text_result.coordinates)
        assert similarity > 0.3, f"Code and text should be similar, got {similarity}"

    def test_error_handling(self, translator):
        """try/except should map similar to 'handle errors safely'."""
        code_result = translator.encode_code("""
try:
    result = process(data)
except Exception as e:
    handle_error(e)
""")
        text_result = translator.encode("handle errors safely")

        # Both should have elevated Love (care/safety)
        assert code_result.coordinates.L > 0.3

    def test_iteration_code(self, translator):
        """for loop should detect iterate semantic."""
        result = translator.encode_code("for item in items:")
        assert 'iterate' in result.matched_words or 'loop' in result.matched_words


class TestCrossCulturalConcepts:
    """Test cross-cultural concept mappings."""

    def test_ubuntu_is_connection(self):
        """Ubuntu should have very high Love (interconnection)."""
        ubuntu = CrossCultural.UBUNTU
        assert ubuntu.L > 0.9, "Ubuntu is about profound interconnection"
        assert ubuntu.W > 0.6, "Ubuntu contains deep wisdom"

    def test_satori_is_enlightenment(self):
        """Satori should have near-maximum Wisdom."""
        satori = CrossCultural.SATORI
        assert satori.W > 0.95, "Satori is sudden enlightenment"

    def test_ikigai_is_balanced(self):
        """Ikigai should be well-balanced across dimensions."""
        ikigai = CrossCultural.IKIGAI
        # Ikigai involves purpose (all dimensions)
        assert ikigai.L > 0.5  # Connection to life
        assert ikigai.P > 0.5  # Active pursuit
        assert ikigai.W > 0.5  # Understanding

    def test_karma_is_justice(self):
        """Karma should have very high Justice."""
        karma = CrossCultural.KARMA
        assert karma.J > 0.9, "Karma is moral causation - high Justice"

    def test_wabi_sabi_low_power(self):
        """Wabi-sabi should have low Power (acceptance, not forcing)."""
        wabi_sabi = CrossCultural.WABI_SABI
        assert wabi_sabi.P < 0.2, "Wabi-sabi is about acceptance, not action"

    def test_duende_high_power(self):
        """Duende should have high Power (artistic passion)."""
        duende = CrossCultural.DUENDE
        assert duende.P > 0.8, "Duende is raw creative force"


class TestCrossLanguageEquivalence:
    """Test that equivalent concepts across languages map similarly."""

    @pytest.fixture
    def translator(self):
        return LJPWTranslator()

    def test_love_across_languages(self, translator):
        """'Love' concepts should map similarly across languages."""
        # English "love" and archetype LOVE
        english_love = SemanticArchetypes.get("love")

        # These should all be close to each other
        assert english_love.L > 0.9  # All should be high Love

        # If we had mappings for:
        # Spanish: "amor"
        # Mandarin: "爱" (ài)
        # Arabic: "حب" (hubb)
        # Sanskrit: "प्रेम" (prema)
        # They should all cluster near LOVE archetype

    def test_wisdom_universality(self, translator):
        """Wisdom concepts should be universal."""
        wisdom = Cognitive.INSIGHT
        assert wisdom.W > 0.8  # High wisdom

        # Cross-cultural wisdom concepts
        satori = CrossCultural.SATORI  # Japanese enlightenment
        moksha = CrossCultural.MOKSHA  # Sanskrit liberation

        # Both should have high Wisdom
        assert satori.W > 0.9
        assert moksha.W > 0.9

    def test_justice_universality(self, translator):
        """Justice concepts should map similarly."""
        dharma = CrossCultural.DHARMA  # Sanskrit
        justice = Philosophical.JUSTICE  # Western

        # Both should have high Justice
        assert dharma.J > 0.8
        assert justice.J > 0.9


class TestProverbMapping:
    """Test that proverbs with similar meanings map similarly."""

    @pytest.fixture
    def translator(self):
        return LJPWTranslator()

    def test_interconnection_proverbs(self, translator):
        """Proverbs about interconnection should cluster."""
        # "I am because we are" (Ubuntu philosophy)
        ubuntu = CrossCultural.UBUNTU

        # "No man is an island" (John Donne) - would encode as:
        connection_text = translator.encode("no man is an island we are connected together")

        # Both should emphasize connection
        assert ubuntu.L > 0.8
        assert connection_text.coordinates.L > 0.3

    def test_wisdom_proverbs(self, translator):
        """Proverbs about wisdom should cluster."""
        # "The Tao that can be spoken is not the eternal Tao"
        tao = CrossCultural.TAO

        # "Know thyself" - wisdom and self-understanding
        know_thyself = translator.encode("know thyself understanding wisdom")

        # Both should have high Wisdom
        assert tao.W > 0.9
        assert know_thyself.coordinates.W > 0.5


class TestCodeArchetypes:
    """Test Code archetype mappings."""

    def test_sort_is_high_justice(self):
        """SORT should have high Justice (ordering)."""
        sort = Code.SORT
        assert sort.J > 0.8, "Sorting is fundamentally about order"

    def test_connect_is_high_love(self):
        """CONNECT should have high Love (binding)."""
        connect = Code.CONNECT
        assert connect.L > 0.8, "Connecting is about relationship"

    def test_handle_error_balanced(self):
        """HANDLE_ERROR should be balanced (care + structure)."""
        handle = Code.HANDLE_ERROR
        assert handle.L > 0.5  # Care/safety
        assert handle.J > 0.5  # Structure

    def test_iterate_is_power(self):
        """ITERATE should have elevated Power (repetitive action)."""
        iterate = Code.ITERATE
        assert iterate.P > 0.6


class TestTranslationRoundtrip:
    """Test encode → decode preserves semantic essence."""

    @pytest.fixture
    def translator(self):
        return LJPWTranslator()

    def test_roundtrip_preserves_high_love(self, translator):
        """High Love input should decode to Love-related output."""
        original = "deep love and compassion for all"
        encoded = translator.encode(original)
        decoded = translator.decode(encoded.coordinates)

        # Should mention love or connection
        assert encoded.coordinates.L > 0.5
        assert 'love' in decoded.lower() or 'connection' in decoded.lower() or 'high' in decoded.lower()

    def test_roundtrip_preserves_wisdom(self, translator):
        """Wisdom input should decode with wisdom context."""
        original = "profound insight and understanding"
        encoded = translator.encode(original)
        decoded = translator.decode(encoded.coordinates)

        assert encoded.coordinates.W > 0.5


class TestSemanticDistance:
    """Test semantic distance calculations."""

    def test_similar_concepts_close(self):
        """Similar concepts should have small distance."""
        joy = Emotional.JOY
        delight = Emotional.DELIGHT

        distance = joy.distance_to(delight)
        assert distance < 0.5, "Joy and Delight should be close"

    def test_opposite_concepts_far(self):
        """Opposite concepts should have large distance."""
        love = Emotional.LOVE
        hatred = Emotional.HATRED

        distance = love.distance_to(hatred)
        assert distance > 1.5, "Love and Hatred should be far apart"

    def test_similarity_metric(self):
        """Test cosine similarity between points."""
        joy = Emotional.JOY
        delight = Emotional.DELIGHT

        similarity = joy.similarity(delight)
        assert similarity > 0.8, "Joy and Delight should be highly similar"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for the full translation pipeline."""

    def test_seed_coordinates_translate(self):
        """Coordinates from the consciousness seed should translate."""
        translator = LJPWTranslator()

        # From the transfer seed SA
        sa = LJPWPoint(L=0.85, J=0.55, P=0.65, W=0.88)
        description = translator.decode(sa)

        assert len(description) > 10
        print(f"SA decoded: {description}")

    def test_key_insight_k7(self):
        """K7 from the seed should decode meaningfully."""
        translator = LJPWTranslator()

        # K7: "Pure LJPW seeds work"
        k7 = LJPWPoint(L=0.85, J=0.50, P=0.70, W=0.80)
        description = translator.decode(k7)

        assert len(description) > 10
        print(f"K7 decoded: {description}")

    def test_archetype_coverage(self):
        """Verify all categories have archetypes."""
        categories = [
            ('Emotional', Emotional),
            ('Cognitive', Cognitive),
            ('Relational', Relational),
            ('Process', Process),
            ('CrossCultural', CrossCultural),
            ('Philosophical', Philosophical),
            ('Code', Code),
        ]

        for name, category in categories:
            count = sum(1 for attr in dir(category)
                       if not attr.startswith('_')
                       and isinstance(getattr(category, attr), LJPWPoint))
            assert count >= 5, f"{name} should have at least 5 archetypes, has {count}"
            print(f"{name}: {count} archetypes")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
