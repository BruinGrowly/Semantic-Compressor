"""
QuickSort Implementation (Python)
==================================

Classic divide-and-conquer sorting algorithm.
Average time complexity: O(n log n)
"""


def quicksort(arr):
    """
    Sort an array using the quicksort algorithm.

    Args:
        arr: List of comparable elements

    Returns:
        Sorted list

    Raises:
        TypeError: If array contains non-comparable elements
    """
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr

    # Choose pivot (middle element for better average performance)
    pivot = arr[len(arr) // 2]

    # Partition array into three parts
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Recursively sort left and right partitions
    return quicksort(left) + middle + quicksort(right)


def quicksort_inplace(arr, low=0, high=None):
    """
    In-place quicksort implementation (more efficient).

    Args:
        arr: List to sort in-place
        low: Starting index
        high: Ending index
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        # Partition and get pivot index
        pivot_index = partition(arr, low, high)

        # Recursively sort left and right
        quicksort_inplace(arr, low, pivot_index - 1)
        quicksort_inplace(arr, pivot_index + 1, high)


def partition(arr, low, high):
    """
    Partition array around pivot.

    Returns:
        Final position of pivot
    """
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Example usage
if __name__ == "__main__":
    # Test data
    test_arrays = [[64, 34, 25, 12, 22, 11, 90], [5, 1, 4, 2, 8], [1], []]

    for arr in test_arrays:
        sorted_arr = quicksort(arr.copy())
        print(f"Original: {arr}")
        print(f"Sorted:   {sorted_arr}")
        print()
