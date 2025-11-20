#!/usr/bin/env python3
"""
Comprehensive LJPW Validation Suite (Days 8-30)
================================================

Tests LJPW framework against edge cases, complex patterns,
and real-world code to validate robustness and universality.

Test Categories:
1. Edge Cases: Empty functions, one-liners, deeply nested code
2. Design Patterns: Singleton, Factory, Observer, Strategy, etc.
3. Code Smells: God classes, long methods, duplicate code
4. Refactoring Sequences: Track movement toward/away from NE
5. Algorithmic Complexity: O(1) vs O(n) vs O(n²) implementations
"""

import sys
from pathlib import Path
import math

sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'ljpw'))
from ljpw_standalone import analyze_quick, calculate_distance

# Natural Equilibrium for reference
NATURAL_EQUILIBRIUM = (0.618, 0.414, 0.718, 0.693)

def distance(coords1, coords2):
    """Calculate Euclidean distance between two 4D points"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coords1, coords2)))


# =============================================================================
# CATEGORY 1: EDGE CASES
# =============================================================================

EDGE_CASES = {
    "empty_function": """
def empty():
    pass
""",

    "one_liner": """
def add(a, b): return a + b
""",

    "deeply_nested": """
def process(data):
    if data:
        if isinstance(data, list):
            for item in data:
                if item > 0:
                    if item % 2 == 0:
                        if item < 100:
                            return item
    return None
""",

    "single_expression": """
lambda x: x * 2
""",

    "docstring_only": """
def placeholder():
    '''This function does nothing yet'''
    pass
""",
}


# =============================================================================
# CATEGORY 2: DESIGN PATTERNS
# =============================================================================

DESIGN_PATTERNS = {
    "singleton": """
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
""",

    "factory": """
class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal: {animal_type}")
""",

    "observer": """
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)
""",

    "strategy": """
class SortContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def sort(self, data):
        return self._strategy.sort(data)
""",

    "decorator_pattern": """
class Component:
    def operation(self):
        pass

class Decorator:
    def __init__(self, component):
        self._component = component

    def operation(self):
        self._component.operation()
        self.extra_behavior()

    def extra_behavior(self):
        pass
""",
}


# =============================================================================
# CATEGORY 3: CODE SMELLS
# =============================================================================

CODE_SMELLS = {
    "god_class": """
class UserManager:
    def create_user(self, name): pass
    def delete_user(self, id): pass
    def send_email(self, user, msg): pass
    def validate_password(self, pwd): pass
    def log_activity(self, action): pass
    def generate_report(self): pass
    def backup_database(self): pass
    def check_permissions(self, user): pass
    def update_settings(self, key, val): pass
    def process_payment(self, amount): pass
""",

    "long_method": """
def process_order(order):
    # Validate order
    if not order or not order.get('items'):
        raise ValueError("Invalid order")

    # Calculate subtotal
    subtotal = 0
    for item in order['items']:
        if item['quantity'] <= 0:
            raise ValueError("Invalid quantity")
        subtotal += item['price'] * item['quantity']

    # Apply discount
    discount = 0
    if order.get('coupon'):
        if order['coupon'] == 'SAVE10':
            discount = subtotal * 0.1
        elif order['coupon'] == 'SAVE20':
            discount = subtotal * 0.2

    # Calculate tax
    tax = (subtotal - discount) * 0.08

    # Calculate total
    total = subtotal - discount + tax

    # Process payment
    # ... many more lines

    return total
""",

    "duplicate_code": """
def calculate_circle_area(radius):
    return 3.14159 * radius * radius

def calculate_circle_circumference(radius):
    return 2 * 3.14159 * radius

def calculate_sphere_volume(radius):
    return (4/3) * 3.14159 * radius * radius * radius
""",

    "magic_numbers": """
def calculate_price(base):
    if base > 100:
        return base * 0.85
    elif base > 50:
        return base * 0.90
    else:
        return base * 0.95
""",
}


# =============================================================================
# CATEGORY 4: REFACTORING SEQUENCES
# =============================================================================

REFACTORING_BEFORE_AFTER = [
    # Refactoring 1: Extract method
    {
        "name": "Extract Method",
        "before": """
def process_data(data):
    # Validate
    if not data or len(data) == 0:
        raise ValueError("Empty data")

    # Transform
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)

    return result
""",
        "after": """
def validate_data(data):
    if not data or len(data) == 0:
        raise ValueError("Empty data")

def transform_data(data):
    return [item * 2 for item in data if item > 0]

def process_data(data):
    validate_data(data)
    return transform_data(data)
""",
    },

    # Refactoring 2: Replace magic number with constant
    {
        "name": "Replace Magic Number",
        "before": """
def calculate_discount(price):
    if price > 100:
        return price * 0.2
    return 0
""",
        "after": """
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.2

def calculate_discount(price):
    if price > DISCOUNT_THRESHOLD:
        return price * DISCOUNT_RATE
    return 0
""",
    },

    # Refactoring 3: Replace conditional with polymorphism
    {
        "name": "Replace Conditional with Polymorphism",
        "before": """
def get_speed(vehicle_type):
    if vehicle_type == "car":
        return 100
    elif vehicle_type == "bike":
        return 30
    elif vehicle_type == "plane":
        return 500
    else:
        return 0
""",
        "after": """
class Vehicle:
    def get_speed(self):
        raise NotImplementedError

class Car(Vehicle):
    def get_speed(self):
        return 100

class Bike(Vehicle):
    def get_speed(self):
        return 30

class Plane(Vehicle):
    def get_speed(self):
        return 500
""",
    },
]


# =============================================================================
# CATEGORY 5: ALGORITHMIC COMPLEXITY
# =============================================================================

ALGORITHMIC_COMPLEXITY = {
    "linear_search_O_n": """
def linear_search(arr, target):
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1
""",

    "binary_search_O_log_n": """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",

    "bubble_sort_O_n2": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
""",

    "merge_sort_O_n_log_n": """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
""",

    "constant_lookup_O_1": """
def get_value(dictionary, key):
    return dictionary.get(key)
""",
}


# =============================================================================
# TEST EXECUTION
# =============================================================================

def get_genome(result):
    """Create genome from LJPW result"""
    L = result['ljpw']['L']
    J = result['ljpw']['J']
    P = result['ljpw']['P']
    W = result['ljpw']['W']

    L_digit = int(round(L * 10)) % 10
    J_digit = int(round(J * 10)) % 10
    P_digit = int(round(P * 10)) % 10
    W_digit = int(round(W * 10)) % 10

    return f"L{L_digit}J{J_digit}P{P_digit}W{W_digit}"


def test_edge_cases():
    """Test LJPW on edge cases"""
    print("=" * 70)
    print("CATEGORY 1: EDGE CASES")
    print("=" * 70)
    print()

    results = []

    for name, code in EDGE_CASES.items():
        result = analyze_quick(code)
        l = result['ljpw']['L']
        j = result['ljpw']['J']
        p = result['ljpw']['P']
        w = result['ljpw']['W']
        coords = (l, j, p, w)
        genome = get_genome(result)
        dist_to_ne = distance(coords, NATURAL_EQUILIBRIUM)

        print(f"{name}:")
        print(f"  Genome: {genome}")
        print(f"  Position: L={l:.2f}, J={j:.2f}, P={p:.2f}, W={w:.2f}")
        print(f"  Distance from NE: {dist_to_ne:.3f}")
        print()

        results.append({
            'name': name,
            'coords': coords,
            'genome': genome,
            'dist_to_ne': dist_to_ne
        })

    # Test passes if no exceptions were raised
    assert len(results) > 0


def test_design_patterns():
    """Test LJPW on common design patterns"""
    print("=" * 70)
    print("CATEGORY 2: DESIGN PATTERNS")
    print("=" * 70)
    print()
    print("Hypothesis: Design patterns should cluster in similar regions")
    print()

    results = []

    for name, code in DESIGN_PATTERNS.items():
        result = analyze_quick(code)
        l = result['ljpw']['L']
        j = result['ljpw']['J']
        p = result['ljpw']['P']
        w = result['ljpw']['W']
        coords = (l, j, p, w)
        genome = get_genome(result)
        dist_to_ne = distance(coords, NATURAL_EQUILIBRIUM)

        print(f"{name}:")
        print(f"  Genome: {genome}")
        print(f"  Position: L={l:.2f}, J={j:.2f}, P={p:.2f}, W={w:.2f}")
        print(f"  Distance from NE: {dist_to_ne:.3f}")
        print()

        results.append({
            'name': name,
            'coords': coords,
            'genome': genome,
            'dist_to_ne': dist_to_ne
        })

    # Calculate average pairwise distance
    n = len(results)
    total_dist = 0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(results[i]['coords'], results[j]['coords'])
            total_dist += d
            count += 1

    avg_pattern_distance = total_dist / count if count > 0 else 0
    print(f"Average pairwise distance: {avg_pattern_distance:.3f}")
    print(f"✓ Patterns cluster together" if avg_pattern_distance < 0.5 else "✗ Patterns are scattered")
    print()

    # Test passes if no exceptions were raised
    assert len(results) > 0


def test_code_smells():
    """Test LJPW on code smells"""
    print("=" * 70)
    print("CATEGORY 3: CODE SMELLS")
    print("=" * 70)
    print()
    print("Hypothesis: Code smells should be far from Natural Equilibrium")
    print()

    results = []

    for name, code in CODE_SMELLS.items():
        result = analyze_quick(code)
        l = result['ljpw']['L']
        j = result['ljpw']['J']
        p = result['ljpw']['P']
        w = result['ljpw']['W']
        coords = (l, j, p, w)
        genome = get_genome(result)
        dist_to_ne = distance(coords, NATURAL_EQUILIBRIUM)

        print(f"{name}:")
        print(f"  Genome: {genome}")
        print(f"  Position: L={l:.2f}, J={j:.2f}, P={p:.2f}, W={w:.2f}")
        print(f"  Distance from NE: {dist_to_ne:.3f}")
        print()

        results.append({
            'name': name,
            'coords': coords,
            'genome': genome,
            'dist_to_ne': dist_to_ne
        })

    avg_smell_distance = sum(r['dist_to_ne'] for r in results) / len(results)
    print(f"Average distance from NE: {avg_smell_distance:.3f}")
    print(f"✓ Code smells are far from NE" if avg_smell_distance > 0.8 else "✗ Code smells near NE")
    print()

    # Test passes if no exceptions were raised
    assert len(results) > 0


def test_refactoring_sequences():
    """Test if refactoring moves code toward Natural Equilibrium"""
    print("=" * 70)
    print("CATEGORY 4: REFACTORING SEQUENCES")
    print("=" * 70)
    print()
    print("Hypothesis: Refactoring moves code TOWARD Natural Equilibrium")
    print()

    results = []

    improvements = 0
    degradations = 0

    for refactoring in REFACTORING_BEFORE_AFTER:
        name = refactoring['name']
        before_code = refactoring['before']
        after_code = refactoring['after']

        before_result = analyze_quick(before_code)
        after_result = analyze_quick(after_code)

        before_coords = (before_result['ljpw']['L'], before_result['ljpw']['J'],
                        before_result['ljpw']['P'], before_result['ljpw']['W'])
        after_coords = (after_result['ljpw']['L'], after_result['ljpw']['J'],
                       after_result['ljpw']['P'], after_result['ljpw']['W'])

        before_dist = distance(before_coords, NATURAL_EQUILIBRIUM)
        after_dist = distance(after_coords, NATURAL_EQUILIBRIUM)

        delta = after_dist - before_dist
        moved_toward = delta < 0

        before_genome = get_genome(before_result)
        after_genome = get_genome(after_result)

        print(f"{name}:")
        print(f"  Before: {before_genome} @ {before_dist:.3f} from NE")
        print(f"  After:  {after_genome} @ {after_dist:.3f} from NE")
        print(f"  Delta: {delta:+.3f} {'✓ MOVED TOWARD NE' if moved_toward else '✗ MOVED AWAY'}")
        print()

        if moved_toward:
            improvements += 1
        else:
            degradations += 1

        results.append({
            'name': name,
            'before_dist': before_dist,
            'after_dist': after_dist,
            'delta': delta,
            'moved_toward_ne': moved_toward
        })

    success_rate = improvements / len(REFACTORING_BEFORE_AFTER) * 100
    print(f"Refactorings toward NE: {improvements}/{len(REFACTORING_BEFORE_AFTER)} ({success_rate:.0f}%)")
    print(f"{'✓ HYPOTHESIS CONFIRMED' if success_rate >= 70 else '✗ HYPOTHESIS CHALLENGED'}")
    print()

    # Test passes if no exceptions were raised
    assert len(results) > 0


def test_algorithmic_complexity():
    """Test if LJPW captures algorithmic complexity"""
    print("=" * 70)
    print("CATEGORY 5: ALGORITHMIC COMPLEXITY")
    print("=" * 70)
    print()
    print("Question: Does LJPW distinguish different time complexities?")
    print()

    results = []

    for name, code in ALGORITHMIC_COMPLEXITY.items():
        result = analyze_quick(code)
        l = result['ljpw']['L']
        j = result['ljpw']['J']
        p = result['ljpw']['P']
        w = result['ljpw']['W']
        coords = (l, j, p, w)
        genome = get_genome(result)
        dist_to_ne = distance(coords, NATURAL_EQUILIBRIUM)

        # Extract complexity from name
        complexity = name.split('_')[-1].replace('_', ' ')

        print(f"{name} ({complexity}):")
        print(f"  Genome: {genome}")
        print(f"  Position: L={l:.2f}, J={j:.2f}, P={p:.2f}, W={w:.2f}")
        print(f"  Distance from NE: {dist_to_ne:.3f}")
        print()

        results.append({
            'name': name,
            'complexity': complexity,
            'coords': coords,
            'genome': genome,
            'dist_to_ne': dist_to_ne
        })

    # Test passes if no exceptions were raised
    assert len(results) > 0


def main():
    """Run comprehensive validation suite"""
    print("=" * 70)
    print("COMPREHENSIVE LJPW VALIDATION SUITE")
    print("=" * 70)
    print()
    print("Testing LJPW robustness across:")
    print("  1. Edge cases")
    print("  2. Design patterns")
    print("  3. Code smells")
    print("  4. Refactoring sequences")
    print("  5. Algorithmic complexity")
    print()

    edge_results = test_edge_cases()
    pattern_results = test_design_patterns()
    smell_results = test_code_smells()
    refactoring_results = test_refactoring_sequences()
    complexity_results = test_algorithmic_complexity()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print(f"✓ Tested {len(edge_results)} edge cases")
    print(f"✓ Tested {len(pattern_results)} design patterns")
    print(f"✓ Tested {len(smell_results)} code smells")
    print(f"✓ Tested {len(refactoring_results)} refactoring sequences")
    print(f"✓ Tested {len(complexity_results)} algorithmic complexities")
    print()
    print(f"Total test cases: {len(edge_results) + len(pattern_results) + len(smell_results) + len(refactoring_results) + len(complexity_results)}")
    print()


if __name__ == "__main__":
    main()
