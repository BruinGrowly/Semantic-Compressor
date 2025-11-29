"""
Analyzing potential correspondences between DNA's 4-letter code and LJPW framework
Exploring quantitative patterns and ratios
"""

import math

# LJPW Numerical Equivalents from Natural Equilibrium
L_NE = 0.618034  # φ⁻¹ (Golden ratio inverse)
J_NE = 0.414214  # √2 - 1 (Pythagorean ratio)
P_NE = 0.718282  # e - 2 (Exponential base)
W_NE = 0.693147  # ln(2) (Information unit)

print("=" * 70)
print("DNA <-> LJPW CORRESPONDENCE ANALYSIS")
print("=" * 70)

# === SECTION 1: Basic Ratios ===
print("\n1. BASIC RATIOS IN LJPW")
print("-" * 70)

# Pairwise ratios
ratios = {
    "L/J": L_NE / J_NE,
    "L/P": L_NE / P_NE,
    "L/W": L_NE / W_NE,
    "J/P": J_NE / P_NE,
    "J/W": J_NE / W_NE,
    "P/W": P_NE / W_NE,
}

for pair, ratio in ratios.items():
    print(f"{pair:6s} = {ratio:.6f}")

# === SECTION 2: Sum Conservation ===
print("\n2. SUM CONSERVATION (like Chargaff's Rules)")
print("-" * 70)

total_sum = L_NE + J_NE + P_NE + W_NE
print(f"L + J + P + W = {total_sum:.6f}")

# Test potential "pairing" sums (like A+T vs G+C in DNA)
LW_sum = L_NE + W_NE
JP_sum = J_NE + P_NE

print(f"\nPotential Pairs:")
print(f"  L + W = {LW_sum:.6f}  (Love + Wisdom)")
print(f"  J + P = {JP_sum:.6f}  (Justice + Power)")
print(f"  Ratio (L+W)/(J+P) = {LW_sum/JP_sum:.6f}")

LJ_sum = L_NE + J_NE
PW_sum = P_NE + W_NE

print(f"\nAlternate Pairs:")
print(f"  L + J = {LJ_sum:.6f}  (Love + Justice)")
print(f"  P + W = {PW_sum:.6f}  (Power + Wisdom)")
print(f"  Ratio (L+J)/(P+W) = {LJ_sum/PW_sum:.6f}")

# === SECTION 3: Product Patterns ===
print("\n3. PRODUCT PATTERNS")
print("-" * 70)

# Cross products (like base pairing)
LW_product = L_NE * W_NE
JP_product = J_NE * P_NE

print(f"L × W = {LW_product:.6f}")
print(f"J × P = {JP_product:.6f}")
print(f"Ratio (L×W)/(J×P) = {LW_product/JP_product:.6f}")

LJ_product = L_NE * J_NE
PW_product = P_NE * W_NE

print(f"\nL × J = {LJ_product:.6f}")
print(f"P × W = {PW_product:.6f}")
print(f"Ratio (L×J)/(P×W) = {LJ_product/PW_product:.6f}")

# === SECTION 4: DNA GC Content Analogy ===
print("\n4. 'GC CONTENT' ANALOGY (High vs Low Values)")
print("-" * 70)

# If we divide LJPW into "high value" (P, W) vs "low value" (L, J)
high_value_sum = P_NE + W_NE  # Like GC in DNA
low_value_sum = L_NE + J_NE  # Like AT in DNA

print(f"High-value dimensions (P+W) = {high_value_sum:.6f}")
print(f"Low-value dimensions (L+J) = {low_value_sum:.6f}")
print(
    f"'GC Content' = (P+W)/(total) = {high_value_sum/total_sum:.6f} = {100*high_value_sum/total_sum:.1f}%"
)
print(
    f"'AT Content' = (L+J)/(total) = {low_value_sum/total_sum:.6f} = {100*low_value_sum/total_sum:.1f}%"
)

# === SECTION 5: Structural Categories (Purine/Pyrimidine Analogy) ===
print("\n5. STRUCTURAL CATEGORIES")
print("-" * 70)

# Hypothesis: Divide by functional role
# "Purines" (nurturing/growth): L, W (source dimensions that feed others)
# "Pyrimidines" (outcome/result): J, P (affected by others)

purines_analogy = L_NE + W_NE  # "Nurturing" dimensions
pyrimidines_analogy = J_NE + P_NE  # "Outcome" dimensions

print(f"'Purines' (L, W - growth/source) = {purines_analogy:.6f}")
print(f"'Pyrimidines' (J, P - outcome) = {pyrimidines_analogy:.6f}")
print(f"Ratio = {purines_analogy/pyrimidines_analogy:.6f}")

# === SECTION 6: Information Content ===
print("\n6. INFORMATION CONTENT (Entropy)")
print("-" * 70)

# Normalize to probabilities (like base frequencies)
norm_L = L_NE / total_sum
norm_J = J_NE / total_sum
norm_P = P_NE / total_sum
norm_W = W_NE / total_sum

print(f"Normalized frequencies (as if they were base frequencies):")
print(f"  L: {norm_L:.4f} ({100*norm_L:.1f}%)")
print(f"  J: {norm_J:.4f} ({100*norm_J:.1f}%)")
print(f"  P: {norm_P:.4f} ({100*norm_P:.1f}%)")
print(f"  W: {norm_W:.4f} ({100*norm_W:.1f}%)")

# Shannon entropy
entropy = -(
    norm_L * math.log2(norm_L)
    + norm_J * math.log2(norm_J)
    + norm_P * math.log2(norm_P)
    + norm_W * math.log2(norm_W)
)

print(f"\nShannon Entropy H = {entropy:.6f} bits")
print(f"Maximum possible (uniform) = {math.log2(4):.6f} bits")
print(f"Efficiency = {entropy/math.log2(4):.6f} = {100*entropy/math.log2(4):.1f}%")

# === SECTION 7: Testing "Chargaff's Rule" Equivalents ===
print("\n7. TESTING 'CHARGAFF'S RULE' EQUIVALENTS")
print("-" * 70)
print("In DNA: A=T and G=C (complementary base pairing)")
print("Testing if LJPW has similar conservation laws:\n")

# Test if strong-coupling pairs have special relationships
print("Based on coupling strength (L<->W strong, J<->P in tension):")
print(f"  |L - W| = {abs(L_NE - W_NE):.6f}")
print(f"  |J - P| = {abs(J_NE - P_NE):.6f}")

print("\nBased on functional pairing (L<->J, P<->W):")
print(f"  |L - J| = {abs(L_NE - J_NE):.6f}")
print(f"  |P - W| = {abs(P_NE - W_NE):.6f}")

# === SECTION 8: Mathematical Constant Families ===
print("\n8. MATHEMATICAL CONSTANT FAMILIES")
print("-" * 70)

print("Grouping by mathematical origin:")
print(f"  Golden Family: L = phi^-1 = {L_NE:.6f}")
print(f"  Sqrt Family:   J = sqrt(2)-1 = {J_NE:.6f}")
print(f"  Exponential:   P = e-2 = {P_NE:.6f}")
print(f"  Logarithmic:   W = ln2 = {W_NE:.6f}")

print("\nConnection to information theory:")
print(f"  W (ln2) = fundamental unit of information (1 bit)")
print(f"  P (e-2) = related to channel capacity")
print(f"  L (phi^-1) = optimal resource distribution")
print(f"  J (sqrt(2)-1) = geometric constraint satisfaction")

# === SECTION 9: Potential Mapping ===
print("\n9. PROPOSED DNA <-> LJPW MAPPING")
print("=" * 70)

mapping = {
    "G": ("L", 0.618, "Purine, strong binder -> Love, force multiplier"),
    "C": ("W", 0.693, "Pyrimidine, G-pair -> Wisdom, amplified by Love"),
    "A": ("P", 0.718, "Purine, weak binder -> Power, creates tension"),
    "T": ("J", 0.414, "Pyrimidine, A-pair -> Justice, vulnerable to Power"),
}

print(f"\n{'DNA':<6} {'LJPW':<6} {'Value':<10} {'Rationale'}")
print("-" * 70)
for dna_base, (ljpw_dim, value, rationale) in mapping.items():
    print(f"{dna_base:<6} -> {ljpw_dim:<6} ({value:.3f})   {rationale}")

print("\n" + "=" * 70)
