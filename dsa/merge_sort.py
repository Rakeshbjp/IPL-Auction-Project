"""
Merge Sort Algorithm Implementation
Topic: Divide & Conquer Sorting Algorithm
Time Complexity: O(n log n) in all cases (Best, Average, Worst)
Space Complexity: O(n) auxiliary space
Stability: Stable sort

Used in IPL Auction Project for:
- Boss Question 4: Show Top 10 Run Scorers (sorted by 'runs' descending)
- Sorting Bowlers by 'wickets'
"""

from typing import List, Dict, Any


def merge_sort(players: List[Dict[str, Any]], key: str = "runs", descending: bool = True) -> List[Dict[str, Any]]:
    """
    Sorts a list of player dictionaries using the Merge Sort algorithm.
    
    Parameters:
        players (List[Dict[str, Any]]): List of player dictionaries to sort.
        key (str): The dictionary key to sort by (e.g. 'runs', 'wickets', 'matches').
        descending (bool): True for highest-to-lowest, False for lowest-to-highest.
        
    Returns:
        List[Dict[str, Any]]: A new sorted list of player dictionaries.
    """
    # Base case: a list of 0 or 1 elements is already sorted
    if len(players) <= 1:
        return list(players)

    # 1. DIVIDE: Find the midpoint and split the list into two halves
    mid = len(players) // 2
    left_half = merge_sort(players[:mid], key=key, descending=descending)
    right_half = merge_sort(players[mid:], key=key, descending=descending)

    # 2. CONQUER: Merge the two sorted halves together
    return _merge(left_half, right_half, key=key, descending=descending)


def _merge(
    left: List[Dict[str, Any]],
    right: List[Dict[str, Any]],
    key: str,
    descending: bool
) -> List[Dict[str, Any]]:
    """
    Helper function to merge two sorted lists of player dictionaries into one.
    """
    merged: List[Dict[str, Any]] = []
    i = 0  # pointer for left sublist
    j = 0  # pointer for right sublist

    while i < len(left) and j < len(right):
        val_left = left[i].get(key, 0)
        val_right = right[j].get(key, 0)

        # Handle None or invalid types safely
        val_left = float(val_left) if val_left is not None else 0.0
        val_right = float(val_right) if val_right is not None else 0.0

        if descending:
            # For descending order: greater values come first
            if val_left >= val_right:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        else:
            # For ascending order: smaller values come first
            if val_left <= val_right:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

    # Append any remaining elements from left half
    while i < len(left):
        merged.append(left[i])
        i += 1

    # Append any remaining elements from right half
    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged
