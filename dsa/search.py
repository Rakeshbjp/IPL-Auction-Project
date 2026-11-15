"""
Search and Filtering Utilities
Topics: Lists, Dictionaries, Loops, Linear Search & Hash Indexing

Used in IPL Auction Project for:
- Boss Question 2: Show only bowlers (or batsmen, allrounders, wicketkeepers)
- Boss Question 3: Find Virat Kohli (search any player by full or partial name)
"""

from typing import List, Dict, Any, Optional


def find_player_by_name_in_list(players: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Searches a list of player dictionaries by name using loops and string comparison.
    Performs case-insensitive substring matching.
    
    Parameters:
        players (List[Dict[str, Any]]): List of player dictionaries.
        query (str): Search string (e.g., 'Virat', 'Kohli', 'Bumrah').
        
    Returns:
        List[Dict[str, Any]]: Matching players list.
    """
    query_clean = query.strip().lower()
    matches: List[Dict[str, Any]] = []

    # Demonstrates Python 'for' loop over player list
    for player in players:
        player_name = player.get("name", "").lower()
        if query_clean in player_name:
            matches.append(player)

    return matches


def build_player_dict_index(players: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    Builds a dictionary hash index from player_id -> player dictionary.
    Demonstrates O(1) dictionary key-value lookups.
    """
    index: Dict[int, Dict[str, Any]] = {}
    for player in players:
        pid = player.get("player_id")
        if pid:
            index[pid] = player
    return index


def filter_players_by_role(players: List[Dict[str, Any]], role: str) -> List[Dict[str, Any]]:
    """
    Filters player dictionaries by role (e.g., 'Bowler', 'Batsman', 'Allrounder', 'Wicketkeeper').
    Demonstrates filtering with Python loops and conditional statements.
    """
    role_clean = role.strip().lower()
    filtered: List[Dict[str, Any]] = []

    for player in players:
        player_role = player.get("role", "").strip().lower()
        if role_clean == player_role or (role_clean in player_role):
            filtered.append(player)

    return filtered
