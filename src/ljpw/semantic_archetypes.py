#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Archetypes Library - Expanded LJPW Coordinate Mappings
================================================================

A comprehensive library of semantic archetypes mapped to LJPW coordinates.
Organized by category for easy navigation and lookup.

Categories:
- Emotional: Feelings and emotional states
- Cognitive: Mental processes and understanding
- Relational: Interpersonal dynamics and connections
- Process: Actions, transformations, and changes
- CrossCultural: Culture-specific concepts with universal meaning
- Philosophical: Abstract and metaphysical concepts
- Code: Programming concepts (for code ↔ natural language bridging)

Each archetype is an LJPWPoint: (Love, Justice, Power, Wisdom)
  - L: Connection, binding, empathy, care
  - J: Structure, order, fairness, constraint
  - P: Action, transformation, energy, force
  - W: Understanding, insight, knowledge, truth
"""

from dataclasses import dataclass
import math
from typing import Dict, Optional, List, Tuple


@dataclass
class LJPWPoint:
    """A point in semantic space."""
    L: float = 0.0  # Love: binding, connection
    J: float = 0.0  # Justice: structure, order
    P: float = 0.0  # Power: action, transformation
    W: float = 0.0  # Wisdom: knowledge, understanding

    def __post_init__(self):
        self.L = max(-1.0, min(1.0, self.L))
        self.J = max(-1.0, min(1.0, self.J))
        self.P = max(-1.0, min(1.0, self.P))
        self.W = max(-1.0, min(1.0, self.W))

    def magnitude(self) -> float:
        return math.sqrt(self.L**2 + self.J**2 + self.P**2 + self.W**2)

    def distance_to(self, other: 'LJPWPoint') -> float:
        return math.sqrt(
            (self.L - other.L)**2 + (self.J - other.J)**2 +
            (self.P - other.P)**2 + (self.W - other.W)**2
        )

    def similarity(self, other: 'LJPWPoint') -> float:
        dot = self.L*other.L + self.J*other.J + self.P*other.P + self.W*other.W
        mag_product = self.magnitude() * other.magnitude()
        return dot / mag_product if mag_product > 0 else 0.0

    def encode(self) -> str:
        return f"({self.L:.2f},{self.J:.2f},{self.P:.2f},{self.W:.2f})"

    def as_tuple(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)

    def __repr__(self):
        return self.encode()

    def __add__(self, other: 'LJPWPoint') -> 'LJPWPoint':
        return LJPWPoint(self.L + other.L, self.J + other.J,
                         self.P + other.P, self.W + other.W)

    def __mul__(self, scalar: float) -> 'LJPWPoint':
        return LJPWPoint(self.L * scalar, self.J * scalar,
                         self.P * scalar, self.W * scalar)


# ============================================================================
# EMOTIONAL ARCHETYPES (~60)
# ============================================================================

class Emotional:
    """Emotional states and feelings mapped to LJPW coordinates."""

    # === Positive High-Energy ===
    JOY = LJPWPoint(L=0.80, J=0.30, P=0.60, W=0.40)
    EXCITEMENT = LJPWPoint(L=0.50, J=0.20, P=0.90, W=0.40)
    ENTHUSIASM = LJPWPoint(L=0.60, J=0.30, P=0.85, W=0.50)
    ELATION = LJPWPoint(L=0.85, J=0.25, P=0.80, W=0.35)
    ECSTASY = LJPWPoint(L=0.90, J=0.15, P=0.95, W=0.30)
    THRILL = LJPWPoint(L=0.40, J=0.20, P=0.95, W=0.30)
    DELIGHT = LJPWPoint(L=0.75, J=0.35, P=0.55, W=0.45)
    BLISS = LJPWPoint(L=0.95, J=0.40, P=0.30, W=0.60)

    # === Positive Low-Energy ===
    PEACE = LJPWPoint(L=0.70, J=0.60, P=0.20, W=0.50)
    SERENITY = LJPWPoint(L=0.75, J=0.65, P=0.15, W=0.55)
    CALM = LJPWPoint(L=0.60, J=0.70, P=0.10, W=0.45)
    CONTENTMENT = LJPWPoint(L=0.70, J=0.55, P=0.25, W=0.50)
    TRANQUILITY = LJPWPoint(L=0.65, J=0.70, P=0.10, W=0.60)
    RELAXATION = LJPWPoint(L=0.55, J=0.50, P=0.15, W=0.35)
    COMFORT = LJPWPoint(L=0.70, J=0.55, P=0.20, W=0.40)
    RELIEF = LJPWPoint(L=0.60, J=0.50, P=0.30, W=0.40)

    # === Love-Family ===
    LOVE = LJPWPoint(L=1.00, J=0.30, P=0.40, W=0.30)
    AFFECTION = LJPWPoint(L=0.85, J=0.35, P=0.30, W=0.30)
    TENDERNESS = LJPWPoint(L=0.90, J=0.40, P=0.20, W=0.35)
    COMPASSION = LJPWPoint(L=0.95, J=0.50, P=0.35, W=0.55)
    EMPATHY = LJPWPoint(L=0.90, J=0.45, P=0.25, W=0.70)
    GRATITUDE = LJPWPoint(L=0.85, J=0.55, P=0.30, W=0.50)
    APPRECIATION = LJPWPoint(L=0.75, J=0.50, P=0.25, W=0.55)
    WARMTH = LJPWPoint(L=0.80, J=0.40, P=0.35, W=0.35)
    DEVOTION = LJPWPoint(L=0.95, J=0.45, P=0.50, W=0.40)
    ADORATION = LJPWPoint(L=0.95, J=0.30, P=0.45, W=0.35)

    # === Wonder-Awe ===
    AWE = LJPWPoint(L=0.60, J=0.50, P=0.30, W=0.90)
    WONDER = LJPWPoint(L=0.55, J=0.40, P=0.35, W=0.85)
    AMAZEMENT = LJPWPoint(L=0.50, J=0.35, P=0.50, W=0.80)
    REVERENCE = LJPWPoint(L=0.70, J=0.65, P=0.20, W=0.85)
    FASCINATION = LJPWPoint(L=0.45, J=0.35, P=0.55, W=0.80)

    # === Hope-Optimism ===
    HOPE = LJPWPoint(L=0.75, J=0.45, P=0.50, W=0.60)
    OPTIMISM = LJPWPoint(L=0.70, J=0.40, P=0.55, W=0.55)
    ANTICIPATION = LJPWPoint(L=0.55, J=0.40, P=0.60, W=0.50)
    EAGERNESS = LJPWPoint(L=0.50, J=0.35, P=0.70, W=0.45)
    LONGING = LJPWPoint(L=0.80, J=0.30, P=0.45, W=0.40)

    # === Negative High-Energy ===
    ANGER = LJPWPoint(L=-0.50, J=-0.30, P=0.90, W=-0.20)
    RAGE = LJPWPoint(L=-0.70, J=-0.50, P=0.98, W=-0.40)
    FURY = LJPWPoint(L=-0.65, J=-0.45, P=0.95, W=-0.35)
    FRUSTRATION = LJPWPoint(L=-0.30, J=-0.20, P=0.70, W=-0.10)
    IRRITATION = LJPWPoint(L=-0.25, J=-0.15, P=0.50, W=-0.05)
    RESENTMENT = LJPWPoint(L=-0.55, J=-0.40, P=0.50, W=-0.20)
    HATRED = LJPWPoint(L=-0.95, J=-0.50, P=0.70, W=-0.40)
    JEALOUSY = LJPWPoint(L=-0.40, J=-0.35, P=0.60, W=-0.25)
    ENVY = LJPWPoint(L=-0.35, J=-0.30, P=0.55, W=-0.20)

    # === Negative Low-Energy ===
    SADNESS = LJPWPoint(L=0.30, J=0.20, P=-0.60, W=0.30)
    GRIEF = LJPWPoint(L=0.50, J=0.25, P=-0.70, W=0.40)
    SORROW = LJPWPoint(L=0.40, J=0.30, P=-0.55, W=0.35)
    MELANCHOLY = LJPWPoint(L=0.35, J=0.40, P=-0.40, W=0.50)
    DESPAIR = LJPWPoint(L=-0.20, J=-0.30, P=-0.80, W=-0.40)
    HOPELESSNESS = LJPWPoint(L=-0.30, J=-0.25, P=-0.85, W=-0.50)
    DISAPPOINTMENT = LJPWPoint(L=0.20, J=0.10, P=-0.45, W=0.15)
    REGRET = LJPWPoint(L=0.40, J=0.50, P=-0.30, W=0.55)
    GUILT = LJPWPoint(L=0.50, J=0.70, P=-0.35, W=0.45)
    SHAME = LJPWPoint(L=0.30, J=0.60, P=-0.50, W=0.35)
    LONELINESS = LJPWPoint(L=-0.60, J=0.20, P=-0.40, W=0.30)

    # === Fear-Anxiety ===
    FEAR = LJPWPoint(L=-0.30, J=0.40, P=0.70, W=0.20)
    TERROR = LJPWPoint(L=-0.50, J=0.30, P=0.90, W=0.10)
    ANXIETY = LJPWPoint(L=-0.20, J=0.35, P=0.55, W=0.25)
    WORRY = LJPWPoint(L=0.10, J=0.45, P=0.40, W=0.30)
    NERVOUSNESS = LJPWPoint(L=-0.15, J=0.30, P=0.50, W=0.20)
    DREAD = LJPWPoint(L=-0.40, J=0.35, P=0.60, W=0.15)
    PANIC = LJPWPoint(L=-0.45, J=-0.20, P=0.95, W=-0.10)


# ============================================================================
# COGNITIVE ARCHETYPES (~35)
# ============================================================================

class Cognitive:
    """Mental processes and states of understanding."""

    # === Understanding ===
    INSIGHT = LJPWPoint(L=0.40, J=0.50, P=0.40, W=0.90)
    UNDERSTANDING = LJPWPoint(L=0.50, J=0.60, P=0.30, W=0.85)
    COMPREHENSION = LJPWPoint(L=0.45, J=0.65, P=0.25, W=0.80)
    REALIZATION = LJPWPoint(L=0.55, J=0.45, P=0.50, W=0.88)
    CLARITY = LJPWPoint(L=0.40, J=0.70, P=0.25, W=0.90)
    EPIPHANY = LJPWPoint(L=0.60, J=0.40, P=0.65, W=0.95)
    REVELATION = LJPWPoint(L=0.65, J=0.45, P=0.55, W=0.92)

    # === Discovery ===
    CURIOSITY = LJPWPoint(L=0.40, J=0.40, P=0.50, W=0.80)
    DISCOVERY = LJPWPoint(L=0.60, J=0.40, P=0.70, W=0.85)
    BREAKTHROUGH = LJPWPoint(L=0.70, J=0.50, P=0.80, W=0.95)
    EXPLORATION = LJPWPoint(L=0.45, J=0.35, P=0.65, W=0.70)
    INVESTIGATION = LJPWPoint(L=0.35, J=0.60, P=0.55, W=0.75)
    INQUIRY = LJPWPoint(L=0.40, J=0.55, P=0.45, W=0.70)

    # === Processing ===
    ANALYSIS = LJPWPoint(L=0.30, J=0.70, P=0.40, W=0.75)
    SYNTHESIS = LJPWPoint(L=0.50, J=0.60, P=0.50, W=0.85)
    REASONING = LJPWPoint(L=0.35, J=0.75, P=0.35, W=0.80)
    CONTEMPLATION = LJPWPoint(L=0.45, J=0.55, P=0.20, W=0.75)
    REFLECTION = LJPWPoint(L=0.50, J=0.50, P=0.15, W=0.70)
    MEDITATION = LJPWPoint(L=0.60, J=0.60, P=0.10, W=0.65)
    ABSTRACTION = LJPWPoint(L=0.25, J=0.65, P=0.30, W=0.85)

    # === Focus States ===
    FOCUS = LJPWPoint(L=0.30, J=0.65, P=0.55, W=0.60)
    CONCENTRATION = LJPWPoint(L=0.25, J=0.70, P=0.60, W=0.55)
    ATTENTION = LJPWPoint(L=0.35, J=0.60, P=0.50, W=0.50)
    FLOW = LJPWPoint(L=0.55, J=0.50, P=0.75, W=0.70)
    ABSORPTION = LJPWPoint(L=0.50, J=0.45, P=0.60, W=0.65)

    # === Confusion States ===
    CONFUSION = LJPWPoint(L=0.20, J=-0.40, P=0.30, W=-0.50)
    PERPLEXITY = LJPWPoint(L=0.25, J=-0.30, P=0.35, W=-0.40)
    UNCERTAINTY = LJPWPoint(L=0.15, J=-0.25, P=0.25, W=-0.30)
    DOUBT = LJPWPoint(L=0.20, J=-0.20, P=0.20, W=-0.25)
    AMBIGUITY = LJPWPoint(L=0.10, J=-0.35, P=0.15, W=-0.20)

    # === Memory ===
    RECOGNITION = LJPWPoint(L=0.50, J=0.50, P=0.40, W=0.85)
    REMEMBRANCE = LJPWPoint(L=0.60, J=0.45, P=0.25, W=0.70)
    NOSTALGIA = LJPWPoint(L=0.70, J=0.40, P=-0.20, W=0.55)
    INTUITION = LJPWPoint(L=0.55, J=0.25, P=0.35, W=0.85)


# ============================================================================
# RELATIONAL ARCHETYPES (~30)
# ============================================================================

class Relational:
    """Interpersonal dynamics and social connections."""

    # === Connection ===
    CONNECTION = LJPWPoint(L=0.90, J=0.40, P=0.30, W=0.40)
    BONDING = LJPWPoint(L=0.85, J=0.45, P=0.35, W=0.35)
    ATTACHMENT = LJPWPoint(L=0.80, J=0.35, P=0.25, W=0.30)
    INTIMACY = LJPWPoint(L=0.95, J=0.45, P=0.40, W=0.50)
    CLOSENESS = LJPWPoint(L=0.85, J=0.40, P=0.30, W=0.40)
    BELONGING = LJPWPoint(L=0.88, J=0.55, P=0.25, W=0.45)
    UNITY = LJPWPoint(L=0.92, J=0.60, P=0.35, W=0.55)

    # === Cooperation ===
    COLLABORATION = LJPWPoint(L=0.80, J=0.60, P=0.60, W=0.50)
    TEAMWORK = LJPWPoint(L=0.75, J=0.65, P=0.65, W=0.45)
    PARTNERSHIP = LJPWPoint(L=0.80, J=0.65, P=0.55, W=0.50)
    COOPERATION = LJPWPoint(L=0.75, J=0.60, P=0.50, W=0.45)
    HARMONY = LJPWPoint(L=0.85, J=0.70, P=0.30, W=0.60)
    SYNERGY = LJPWPoint(L=0.80, J=0.55, P=0.70, W=0.65)

    # === Trust ===
    TRUST = LJPWPoint(L=0.85, J=0.70, P=0.20, W=0.50)
    LOYALTY = LJPWPoint(L=0.90, J=0.75, P=0.35, W=0.45)
    FAITH = LJPWPoint(L=0.88, J=0.60, P=0.25, W=0.55)
    RELIANCE = LJPWPoint(L=0.75, J=0.65, P=0.30, W=0.45)
    DEPENDABILITY = LJPWPoint(L=0.70, J=0.80, P=0.35, W=0.50)

    # === Guidance ===
    MENTORSHIP = LJPWPoint(L=0.75, J=0.60, P=0.50, W=0.80)
    TEACHING = LJPWPoint(L=0.70, J=0.55, P=0.55, W=0.85)
    GUIDANCE = LJPWPoint(L=0.70, J=0.50, P=0.45, W=0.80)
    NURTURING = LJPWPoint(L=0.90, J=0.55, P=0.40, W=0.55)
    SUPPORT = LJPWPoint(L=0.85, J=0.55, P=0.45, W=0.45)

    # === Conflict ===
    RIVALRY = LJPWPoint(L=-0.30, J=0.40, P=0.70, W=0.30)
    COMPETITION = LJPWPoint(L=0.10, J=0.55, P=0.75, W=0.40)
    CONFLICT = LJPWPoint(L=-0.40, J=-0.30, P=0.75, W=0.20)
    TENSION = LJPWPoint(L=-0.25, J=0.20, P=0.60, W=0.25)

    # === Healing ===
    FORGIVENESS = LJPWPoint(L=0.90, J=0.60, P=0.30, W=0.65)
    RECONCILIATION = LJPWPoint(L=0.85, J=0.65, P=0.45, W=0.60)
    ACCEPTANCE = LJPWPoint(L=0.80, J=0.55, P=0.20, W=0.55)


# ============================================================================
# PROCESS ARCHETYPES (~35)
# ============================================================================

class Process:
    """Actions, transformations, and dynamic states."""

    # === Creation ===
    CREATION = LJPWPoint(L=0.60, J=0.50, P=0.85, W=0.70)
    INNOVATION = LJPWPoint(L=0.50, J=0.40, P=0.80, W=0.75)
    INVENTION = LJPWPoint(L=0.45, J=0.45, P=0.85, W=0.80)
    GENERATION = LJPWPoint(L=0.55, J=0.50, P=0.80, W=0.60)
    MANIFESTATION = LJPWPoint(L=0.50, J=0.55, P=0.85, W=0.65)
    EXPRESSION = LJPWPoint(L=0.60, J=0.40, P=0.75, W=0.55)

    # === Transformation ===
    TRANSFORMATION = LJPWPoint(L=0.40, J=0.30, P=0.90, W=0.60)
    EVOLUTION = LJPWPoint(L=0.50, J=0.45, P=0.70, W=0.75)
    GROWTH = LJPWPoint(L=0.50, J=0.40, P=0.70, W=0.60)
    DEVELOPMENT = LJPWPoint(L=0.55, J=0.50, P=0.65, W=0.65)
    METAMORPHOSIS = LJPWPoint(L=0.45, J=0.25, P=0.90, W=0.55)
    TRANSMUTATION = LJPWPoint(L=0.40, J=0.35, P=0.85, W=0.70)
    RENEWAL = LJPWPoint(L=0.60, J=0.45, P=0.65, W=0.55)
    REBIRTH = LJPWPoint(L=0.65, J=0.40, P=0.75, W=0.60)

    # === Effort ===
    PERSEVERANCE = LJPWPoint(L=0.55, J=0.65, P=0.80, W=0.50)
    DETERMINATION = LJPWPoint(L=0.50, J=0.60, P=0.85, W=0.45)
    STRIVING = LJPWPoint(L=0.45, J=0.50, P=0.80, W=0.50)
    EFFORT = LJPWPoint(L=0.40, J=0.55, P=0.75, W=0.40)
    STRUGGLE = LJPWPoint(L=0.30, J=0.40, P=0.85, W=0.35)
    ENDURANCE = LJPWPoint(L=0.50, J=0.70, P=0.75, W=0.45)

    # === Release ===
    SURRENDER = LJPWPoint(L=0.55, J=0.50, P=-0.40, W=0.55)
    LETTING_GO = LJPWPoint(L=0.60, J=0.45, P=-0.30, W=0.50)
    RELEASE = LJPWPoint(L=0.50, J=0.40, P=0.50, W=0.45)
    DISSOLUTION = LJPWPoint(L=0.30, J=-0.20, P=-0.50, W=0.40)
    DECAY = LJPWPoint(L=-0.20, J=-0.40, P=-0.60, W=0.20)

    # === Emergence ===
    EMERGENCE = LJPWPoint(L=0.55, J=0.35, P=0.70, W=0.75)
    AWAKENING = LJPWPoint(L=0.65, J=0.45, P=0.60, W=0.85)
    UNFOLDING = LJPWPoint(L=0.55, J=0.40, P=0.55, W=0.70)
    BECOMING = LJPWPoint(L=0.60, J=0.45, P=0.65, W=0.65)
    FLOWERING = LJPWPoint(L=0.70, J=0.45, P=0.60, W=0.55)

    # === Completion ===
    COMPLETION = LJPWPoint(L=0.60, J=0.75, P=0.50, W=0.65)
    FULFILLMENT = LJPWPoint(L=0.75, J=0.60, P=0.45, W=0.60)
    ACHIEVEMENT = LJPWPoint(L=0.55, J=0.65, P=0.70, W=0.55)
    SUCCESS = LJPWPoint(L=0.60, J=0.60, P=0.70, W=0.55)


# ============================================================================
# CROSS-CULTURAL ARCHETYPES (~20)
# ============================================================================

class CrossCultural:
    """Culture-specific concepts with universal semantic meaning."""

    # === African ===
    UBUNTU = LJPWPoint(L=0.95, J=0.65, P=0.40, W=0.70)
    # "I am because we are" - profound interconnection

    # === Japanese ===
    SATORI = LJPWPoint(L=0.50, J=0.55, P=0.30, W=0.98)
    # Sudden enlightenment/awakening

    WABI_SABI = LJPWPoint(L=0.70, J=0.60, P=-0.10, W=0.75)
    # Beauty in imperfection and transience

    IKIGAI = LJPWPoint(L=0.75, J=0.65, P=0.70, W=0.80)
    # Reason for being, life purpose

    MONO_NO_AWARE = LJPWPoint(L=0.65, J=0.50, P=-0.20, W=0.70)
    # Bittersweet awareness of impermanence

    MA = LJPWPoint(L=0.40, J=0.70, P=0.10, W=0.60)
    # Negative space, meaningful pause

    # === Danish ===
    HYGGE = LJPWPoint(L=0.85, J=0.55, P=0.25, W=0.40)
    # Cozy contentment, warm atmosphere

    # === German ===
    SCHADENFREUDE = LJPWPoint(L=-0.40, J=0.30, P=0.45, W=0.20)
    # Pleasure from others' misfortune

    WELTANSCHAUUNG = LJPWPoint(L=0.35, J=0.60, P=0.30, W=0.90)
    # Worldview, comprehensive philosophy

    GEMUTLICHKEIT = LJPWPoint(L=0.80, J=0.50, P=0.30, W=0.40)
    # Warmth, friendliness, belonging

    # === Portuguese ===
    SAUDADE = LJPWPoint(L=0.75, J=0.35, P=-0.35, W=0.55)
    # Melancholic longing for something absent

    # === Spanish ===
    DUENDE = LJPWPoint(L=0.60, J=0.25, P=0.85, W=0.50)
    # Artistic passion, mysterious creative force

    # === Sanskrit/Indian ===
    DHARMA = LJPWPoint(L=0.55, J=0.90, P=0.50, W=0.80)
    # Cosmic order, duty, righteous path

    KARMA = LJPWPoint(L=0.40, J=0.95, P=0.55, W=0.70)
    # Action and consequence, moral causation

    AHIMSA = LJPWPoint(L=0.95, J=0.80, P=-0.30, W=0.75)
    # Non-violence, harmlessness

    NIRVANA = LJPWPoint(L=0.80, J=0.70, P=-0.50, W=0.95)
    # Liberation, transcendence of suffering

    MOKSHA = LJPWPoint(L=0.85, J=0.65, P=0.30, W=0.92)
    # Spiritual liberation, freedom

    # === Greek ===
    EUDAIMONIA = LJPWPoint(L=0.75, J=0.70, P=0.55, W=0.85)
    # Human flourishing, living well

    PHILOTIMO = LJPWPoint(L=0.85, J=0.80, P=0.55, W=0.60)
    # Honor through love of virtue

    # === Chinese ===
    TAO = LJPWPoint(L=0.70, J=0.75, P=0.40, W=0.95)
    # The Way, natural order

    WU_WEI = LJPWPoint(L=0.60, J=0.65, P=-0.20, W=0.80)
    # Non-action, effortless action


# ============================================================================
# PHILOSOPHICAL ARCHETYPES (~20)
# ============================================================================

class Philosophical:
    """Abstract and metaphysical concepts."""

    # === Transcendence ===
    TRANSCENDENCE = LJPWPoint(L=0.60, J=0.50, P=0.55, W=0.95)
    SUBLIME = LJPWPoint(L=0.55, J=0.45, P=0.40, W=0.92)
    IMMANENCE = LJPWPoint(L=0.70, J=0.60, P=0.35, W=0.80)
    INFINITY = LJPWPoint(L=0.40, J=0.30, P=0.50, W=0.95)

    # === Being ===
    EXISTENCE = LJPWPoint(L=0.50, J=0.55, P=0.60, W=0.75)
    BEING = LJPWPoint(L=0.55, J=0.60, P=0.50, W=0.80)
    ESSENCE = LJPWPoint(L=0.45, J=0.65, P=0.30, W=0.90)
    PRESENCE = LJPWPoint(L=0.65, J=0.55, P=0.40, W=0.70)
    VOID = LJPWPoint(L=-0.20, J=0.40, P=-0.50, W=0.60)
    NOTHINGNESS = LJPWPoint(L=-0.10, J=0.30, P=-0.60, W=0.55)

    # === Truth ===
    TRUTH = LJPWPoint(L=0.50, J=0.80, P=0.40, W=0.95)
    VERITY = LJPWPoint(L=0.45, J=0.85, P=0.35, W=0.90)
    AUTHENTICITY = LJPWPoint(L=0.70, J=0.75, P=0.45, W=0.80)
    INTEGRITY = LJPWPoint(L=0.65, J=0.90, P=0.50, W=0.75)

    # === Paradox ===
    PARADOX = LJPWPoint(L=0.30, J=-0.30, P=0.40, W=0.85)
    APORIA = LJPWPoint(L=0.25, J=-0.20, P=0.25, W=0.80)
    DIALECTIC = LJPWPoint(L=0.40, J=0.60, P=0.55, W=0.85)

    # === Ethics ===
    VIRTUE = LJPWPoint(L=0.70, J=0.85, P=0.45, W=0.75)
    JUSTICE = LJPWPoint(L=0.55, J=1.00, P=0.50, W=0.80)
    BEAUTY = LJPWPoint(L=0.75, J=0.65, P=0.30, W=0.70)


# ============================================================================
# CODE ARCHETYPES (~25) - For programming language semantic bridging
# ============================================================================

class Code:
    """Programming concepts mapped to LJPW for code ↔ language bridging."""

    # === Data Flow ===
    INPUT = LJPWPoint(L=0.50, J=0.60, P=0.55, W=0.40)
    OUTPUT = LJPWPoint(L=0.55, J=0.55, P=0.60, W=0.45)
    TRANSFORM = LJPWPoint(L=0.35, J=0.50, P=0.80, W=0.55)
    FILTER = LJPWPoint(L=0.40, J=0.75, P=0.50, W=0.55)
    MAP = LJPWPoint(L=0.45, J=0.60, P=0.65, W=0.60)
    REDUCE = LJPWPoint(L=0.60, J=0.65, P=0.55, W=0.65)

    # === Control Flow ===
    ITERATE = LJPWPoint(L=0.30, J=0.70, P=0.70, W=0.45)
    BRANCH = LJPWPoint(L=0.25, J=0.75, P=0.50, W=0.60)
    RECURSE = LJPWPoint(L=0.50, J=0.55, P=0.65, W=0.75)
    RETURN = LJPWPoint(L=0.40, J=0.65, P=0.45, W=0.50)

    # === Error Handling ===
    TRY = LJPWPoint(L=0.55, J=0.50, P=0.55, W=0.45)
    CATCH = LJPWPoint(L=0.70, J=0.60, P=0.40, W=0.50)
    HANDLE_ERROR = LJPWPoint(L=0.75, J=0.65, P=0.45, W=0.55)
    VALIDATE = LJPWPoint(L=0.50, J=0.85, P=0.45, W=0.60)

    # === Connection ===
    CONNECT = LJPWPoint(L=0.85, J=0.55, P=0.60, W=0.45)
    BIND = LJPWPoint(L=0.80, J=0.60, P=0.50, W=0.40)
    COMPOSE = LJPWPoint(L=0.70, J=0.65, P=0.55, W=0.70)
    INTEGRATE = LJPWPoint(L=0.75, J=0.60, P=0.60, W=0.65)

    # === Organization ===
    SORT = LJPWPoint(L=0.30, J=0.90, P=0.60, W=0.50)
    GROUP = LJPWPoint(L=0.65, J=0.70, P=0.45, W=0.55)
    STRUCTURE = LJPWPoint(L=0.40, J=0.85, P=0.40, W=0.65)
    ENCAPSULATE = LJPWPoint(L=0.60, J=0.80, P=0.35, W=0.60)

    # === Creation ===
    CREATE = LJPWPoint(L=0.55, J=0.50, P=0.80, W=0.55)
    DELETE = LJPWPoint(L=-0.30, J=0.45, P=0.65, W=0.35)
    UPDATE = LJPWPoint(L=0.45, J=0.55, P=0.70, W=0.50)


# ============================================================================
# ARCHETYPE REGISTRY - Unified lookup
# ============================================================================

class SemanticArchetypes:
    """
    Unified access to all semantic archetypes.
    Provides lookup by name and category navigation.
    """

    Emotional = Emotional
    Cognitive = Cognitive
    Relational = Relational
    Process = Process
    CrossCultural = CrossCultural
    Philosophical = Philosophical
    Code = Code

    @classmethod
    def get(cls, name: str) -> Optional[LJPWPoint]:
        """Get archetype by name (case-insensitive search across all categories)."""
        name_upper = name.upper().replace(" ", "_").replace("-", "_")

        # Search all categories
        for category in [Emotional, Cognitive, Relational, Process,
                         CrossCultural, Philosophical, Code]:
            if hasattr(category, name_upper):
                return getattr(category, name_upper)

        return None

    @classmethod
    def find_nearest(cls, point: LJPWPoint, n: int = 5) -> List[Tuple[str, LJPWPoint, float]]:
        """Find the n nearest archetypes to a given point."""
        all_archetypes = cls.all_archetypes()
        distances = []

        for name, archetype in all_archetypes.items():
            dist = point.distance_to(archetype)
            distances.append((name, archetype, dist))

        distances.sort(key=lambda x: x[2])
        return distances[:n]

    @classmethod
    def all_archetypes(cls) -> Dict[str, LJPWPoint]:
        """Get all archetypes as a flat dictionary."""
        result = {}

        for category in [Emotional, Cognitive, Relational, Process,
                         CrossCultural, Philosophical, Code]:
            for name in dir(category):
                if not name.startswith('_'):
                    attr = getattr(category, name)
                    if isinstance(attr, LJPWPoint):
                        result[name] = attr

        return result

    @classmethod
    def count(cls) -> int:
        """Count total number of archetypes."""
        return len(cls.all_archetypes())


# ============================================================================
# DEMO
# ============================================================================

def demo():
    """Demonstrate the archetype library."""
    print("=" * 60)
    print("SEMANTIC ARCHETYPES LIBRARY")
    print("=" * 60)

    print(f"\nTotal archetypes: {SemanticArchetypes.count()}")

    print("\n--- Sample Archetypes by Category ---\n")

    print("Emotional:")
    print(f"  JOY = {Emotional.JOY}")
    print(f"  GRIEF = {Emotional.GRIEF}")
    print(f"  AWE = {Emotional.AWE}")

    print("\nCognitive:")
    print(f"  INSIGHT = {Cognitive.INSIGHT}")
    print(f"  BREAKTHROUGH = {Cognitive.BREAKTHROUGH}")
    print(f"  CURIOSITY = {Cognitive.CURIOSITY}")

    print("\nCross-Cultural:")
    print(f"  UBUNTU = {CrossCultural.UBUNTU}")
    print(f"  SATORI = {CrossCultural.SATORI}")
    print(f"  IKIGAI = {CrossCultural.IKIGAI}")

    print("\nCode:")
    print(f"  SORT = {Code.SORT}")
    print(f"  CONNECT = {Code.CONNECT}")
    print(f"  HANDLE_ERROR = {Code.HANDLE_ERROR}")

    print("\n--- Finding Nearest Archetypes ---\n")

    test_point = LJPWPoint(L=0.7, J=0.5, P=0.6, W=0.8)
    print(f"Test point: {test_point}")
    print("Nearest archetypes:")

    for name, archetype, dist in SemanticArchetypes.find_nearest(test_point, 5):
        print(f"  {name}: {archetype} (distance: {dist:.3f})")


if __name__ == "__main__":
    demo()
