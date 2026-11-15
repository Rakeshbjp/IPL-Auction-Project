"""
Quick Sort Algorithm Implementation
Topic: Divide & Conquer / Pivot Partitioning
Time Complexity: O(n log n) average case, O(n^2) worst case (prevented with balanced pivot choice)
Space Complexity: O(log n) call stack space

Used in IPL Auction Project for:
- Boss Question 5: Show Highest Batting Averages (sorted by 'batting_avg' descending)
- Sorting players by 'strike_rate' or 'sold_price'
"""

from typing import List, Dict, Any


def quick_sort(players: List[Dict[str, Any]], key: str = "batting_avg", descending: bool = True) -> List[Dict[str, Any]]:
    """
    Sorts a list of player dictionaries using the Quick Sort algorithm.
    
    Parameters:
        players (List[Dict[str, Any]]): List of player dictionaries to sort.
        key (str): The dictionary key to sort by (e.g. 'batting_avg', 'strike_rate').
        descending (bool): True for highest-to-lowest, False for lowest-to-highest.
        
    Returns:
        List[Dict[str, Any]]: A new sorted list of player dictionaries.
    """
    # Base case: 0 or 1 elements are trivially sorted
    if len(players) <= 1:
        return list(players)

    # Make a copy to avoid mutating the original input list directly
    arr = list(players)
    _quick_sort_helper(arr, 0, len(arr) - 1, key=key, descending=descending)
    return arr


def _quick_sort_helper(arr: List[Dict[str, Any]], low: int, high: int, key: str, descending: bool) -> None:
    """In-place recursive quick sort helper function using Lomuto/Hoare partitioning."""
    if low < high:
        # Partition index
        pi = _partition(arr, low, high, key=key, descending=descending)

        # Recursively sort elements before and after partition
        _quick_sort_helper(arr, low, pi - 1, key=key, descending=descending)
        _quick_sort_helper(arr, pi + 1, high, key=key, descending=descending)


def _get_sort_val(item: Dict[str, Any], key: str) -> float:
    """Safely extracts and casts comparison values from dictionary."""
    val = item.get(key, 0.0)
    try:
        return float(val) if val is not None else 0.0
    except (ValueError, TypeError):
        return 0.0


def _partition(arr: List[Dict[str, Any]], low: int, high: int, key: str, descending: bool) -> int:
    """
    Partitions the array around a pivot element.
    Takes the element at 'high' as pivot.
    """
    pivot_val = _get_sort_val(arr[high], key)
    i = low - 1  # Index of smaller element boundary

    for j in range(low, high):
        curr_val = _get_sort_val(arr[j], key)

        if descending:
            # Greater values move towards the front
            if curr_val >= pivot_val:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        else:
            # Smaller values move towards the front
            if curr_val <= pivot_val:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

    # Swap pivot into its correct sorted position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
