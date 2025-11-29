from typing import List, Union


def calculate_total(items: List[Union[int, float]]) -> float:
    """
    Calculate the sum of numeric items.

    Args:
        items: List of numbers to sum

    Returns:
        Total sum of all items

    Raises:
        TypeError: If items is not a list or contains non-numeric values
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")

    if not items:
        return 0.0

    total = 0.0
    for item in items:
        if not isinstance(item, (int, float)):
            raise TypeError(f"Item {item} is not a number")
        total += item

    return total
