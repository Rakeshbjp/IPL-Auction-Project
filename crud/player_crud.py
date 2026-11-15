"""
Player CRUD Operations & Analysis
Demonstrates:
- CRUD Operations (Create, Read, Update, Delete)
- Foreign Keys & Primary Keys
- Lists, Dictionaries, Loops
- Merge Sort & Quick Sort Algorithms
"""

from typing import List, Dict, Any, Optional
from database import get_connection, row_to_dict, remove_player_from_team_tables
from dsa.merge_sort import merge_sort
from dsa.quick_sort import quick_sort
from dsa.search import find_player_by_name_in_list, filter_players_by_role
from supabase_sync import sync_create_player, sync_update_player_stats, sync_delete_player



# ============================================================================
# 1. READ OPERATIONS
# ============================================================================

def read_all_players() -> List[Dict[str, Any]]:
    """
    [Boss Question 1: Show all players]
    Fetches all players joined with their career statistics and team information.
    Returns: List of player dictionaries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        p.player_id,
        p.name,
        p.role,
        p.country,
        p.base_price,
        p.sold_price,
        p.status,
        p.team_id,
        t.team_name,
        t.short_code AS team_code,
        s.stat_id,
        s.matches,
        s.runs,
        s.highest_score,
        s.batting_avg,
        s.strike_rate,
        s.fours,
        s.sixes,
        s.centuries,
        s.fifties,
        s.wickets,
        s.bowling_economy,
        s.bowling_avg
    FROM players p
    LEFT JOIN player_stats s ON p.player_id = s.player_id
    LEFT JOIN teams t ON p.team_id = t.team_id
    ORDER BY p.player_id ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # Convert SQLite rows into a list of Python dictionaries
    players_list: List[Dict[str, Any]] = [row_to_dict(r) for r in rows]
    return players_list


def read_players_by_role(role: str) -> List[Dict[str, Any]]:
    """
    [Boss Question 2: Show only bowlers / batsmen / allrounders / wicketkeepers]
    Demonstrates filtering using both SQL WHERE clause and Python list/loops.
    """
    all_players = read_all_players()
    # Uses our custom DSA loop filter
    return filter_players_by_role(all_players, role)


def find_player_by_name(query: str) -> List[Dict[str, Any]]:
    """
    [Boss Question 3: Find Virat Kohli]
    Searches for any player by full or partial name using case-insensitive search.
    """
    all_players = read_all_players()
    return find_player_by_name_in_list(all_players, query)


def find_player_by_id(player_id: int) -> Optional[Dict[str, Any]]:
    """Fetches a single player by their Primary Key (player_id)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        p.player_id, p.name, p.role, p.country, p.base_price, p.sold_price, p.status, p.team_id,
        t.team_name, t.short_code AS team_code,
        s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
        s.fours, s.sixes, s.centuries, s.fifties, s.wickets, s.bowling_economy, s.bowling_avg
    FROM players p
    LEFT JOIN player_stats s ON p.player_id = s.player_id
    LEFT JOIN teams t ON p.team_id = t.team_id
    WHERE p.player_id = ?;
    """, (player_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row) if row else None


# ============================================================================
# 2. DSA SORTING (MERGE SORT & QUICK SORT)
# ============================================================================

def get_top_run_scorers_mergesort(limit: int = 10) -> List[Dict[str, Any]]:
    """
    [Boss Question 4: Show top 10 run scorers]
    Uses our custom MERGE SORT algorithm (Divide and Conquer, O(n log n)).
    Sorts all players by 'runs' in descending order.
    """
    all_players = read_all_players()
    # Call manual Merge Sort implementation
    sorted_players = merge_sort(all_players, key="runs", descending=True)
    return sorted_players[:limit]


def get_top_batting_averages_quicksort(limit: int = 10, min_matches: int = 10) -> List[Dict[str, Any]]:
    """
    [Boss Question 5: Show highest batting averages]
    Uses our custom QUICK SORT algorithm (Pivot Partitioning, O(n log n)).
    Filters players with at least `min_matches` to ensure statistical relevance,
    then sorts by 'batting_avg' descending.
    """
    all_players = read_all_players()
    # Filter with Python loop
    eligible_players = [p for p in all_players if p.get("matches", 0) >= min_matches]
    # Call manual Quick Sort implementation
    sorted_players = quick_sort(eligible_players, key="batting_avg", descending=True)
    return sorted_players[:limit]


# ============================================================================
# 3. CREATE OPERATION (CRUD)
# ============================================================================

def create_player(
    name: str,
    role: str,
    country: str,
    base_price: float,
    matches: int = 0,
    runs: int = 0,
    highest_score: int = 0,
    batting_avg: float = 0.0,
    strike_rate: float = 0.0,
    centuries: int = 0,
    fifties: int = 0,
    wickets: int = 0,
    bowling_economy: float = 0.0,
    bowling_avg: float = 0.0,
) -> int:
    """
    [Boss Question 6: Add a new player]
    Inserts a new player into 'players' table and their career stats into 'player_stats'
    enforcing Foreign Key relationship (player_stats.player_id -> players.player_id).
    
    Returns:
        int: The newly created player_id (Primary Key).
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Step 1: Insert into players table
        cursor.execute("""
        INSERT INTO players (name, role, country, base_price, sold_price, status, team_id)
        VALUES (?, ?, ?, ?, 0.0, 'Available', NULL);
        """, (name.strip(), role.strip(), country.strip(), float(base_price)))

        player_id = cursor.lastrowid

        # Step 2: Insert into player_stats table with Foreign Key player_id
        cursor.execute("""
        INSERT INTO player_stats (
            player_id, matches, runs, highest_score, batting_avg, strike_rate,
            centuries, fifties, wickets, bowling_economy, bowling_avg
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            player_id, matches, runs, highest_score, batting_avg, strike_rate,
            centuries, fifties, wickets, bowling_economy, bowling_avg
        ))

        conn.commit()

        # Real-time synchronization to Supabase Cloud PostgreSQL
        try:
            sync_create_player(
                name=name, role=role, country=country, base_price=base_price,
                matches=matches, runs=runs, highest_score=highest_score,
                batting_avg=batting_avg, strike_rate=strike_rate, fours=0, sixes=0,
                centuries=centuries, fifties=fifties, wickets=wickets,
                bowling_economy=bowling_economy, bowling_avg=bowling_avg,
                known_id=player_id
            )
        except Exception as se:
            print(f"[Sync Notice] Supabase create sync: {se}")

        return player_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ============================================================================
# 4. UPDATE OPERATION (CRUD)
# ============================================================================

def update_player_stats(player_id: int, new_stats: Dict[str, Any]) -> bool:
    """
    [Boss Question 7: Update player statistics]
    Updates specific stats for a player in the 'player_stats' table.
    
    Parameters:
        player_id (int): Primary key of the player.
        new_stats (dict): Dictionary with updated fields (e.g. {'runs': 8200, 'matches': 255}).
    """
    conn = get_connection()
    cursor = conn.cursor()

    allowed_fields = [
        "matches", "runs", "highest_score", "batting_avg", "strike_rate",
        "centuries", "fifties", "wickets", "bowling_economy", "bowling_avg"
    ]

    updates = []
    values = []

    for key, val in new_stats.items():
        if key in allowed_fields and val is not None:
            updates.append(f"{key} = ?")
            values.append(val)

    if not updates:
        conn.close()
        return False

    values.append(player_id)
    sql = f"UPDATE player_stats SET {', '.join(updates)} WHERE player_id = ?;"

    try:
        cursor.execute(sql, tuple(values))
        conn.commit()
        updated = cursor.rowcount > 0

        if updated:
            # Real-time synchronization to Supabase Cloud PostgreSQL
            try:
                sync_update_player_stats(player_id, new_stats)
            except Exception as se:
                print(f"[Sync Notice] Supabase update sync: {se}")

        return updated
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ============================================================================
# 5. DELETE OPERATION (CRUD)
# ============================================================================

def delete_player(player_id: int) -> bool:
    """
    [Boss Question 8: Delete a player]
    Deletes a player by Primary Key.
    Foreign key cascading automatically removes associated player_stats and bids.
    Also removes the player from any franchise squad tables.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Remove from franchise squad tables
        remove_player_from_team_tables(player_id)

        cursor.execute("DELETE FROM players WHERE player_id = ?;", (player_id,))
        conn.commit()
        deleted = cursor.rowcount > 0

        if deleted:
            # Real-time synchronization to Supabase Cloud PostgreSQL
            try:
                sync_delete_player(player_id)
            except Exception as se:
                print(f"[Sync Notice] Supabase delete sync: {se}")

        return deleted
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
