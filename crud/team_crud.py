"""
Team CRUD & Budget Management Operations
Demonstrates:
- Relational Foreign Keys (players.team_id -> teams.team_id)
- Aggregations and Real-time Purse Tracking
- SQL JOIN Queries

Used for:
- Boss Question 9: Show a team's purchased players
- Boss Question 10: Show remaining team budget
"""

from typing import List, Dict, Any, Optional
from database import get_connection, row_to_dict
from config import format_currency


def read_all_teams() -> List[Dict[str, Any]]:
    """Fetches all 10 IPL franchises with their current purse and squad count."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        t.team_id,
        t.team_name,
        t.short_code,
        t.primary_color,
        t.secondary_color,
        t.total_budget,
        t.remaining_budget,
        (t.total_budget - t.remaining_budget) AS spent_budget,
        t.max_squad_size,
        COUNT(p.player_id) AS current_squad_size
    FROM teams t
    LEFT JOIN players p ON t.team_id = p.team_id
    GROUP BY t.team_id
    ORDER BY t.team_id ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    teams: List[Dict[str, Any]] = []
    for r in rows:
        d = row_to_dict(r)
        d["total_budget_fmt"] = format_currency(d["total_budget"])
        d["remaining_budget_fmt"] = format_currency(d["remaining_budget"])
        d["spent_budget_fmt"] = format_currency(d["spent_budget"])
        teams.append(d)

    return teams


def get_team_by_id(team_id: int) -> Optional[Dict[str, Any]]:
    """Finds a team by its Primary Key (team_id)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teams WHERE team_id = ?;", (team_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row) if row else None


def get_team_by_code(short_code: str) -> Optional[Dict[str, Any]]:
    """Finds a team by its short code (e.g. 'CSK', 'MI', 'RCB')."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teams WHERE UPPER(short_code) = ?;", (short_code.strip().upper(),))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row) if row else None


def get_team_purchased_players(team_id_or_code: Any) -> Dict[str, Any]:
    """
    [Boss Question 9: Show a team's purchased players]
    Uses a SQL JOIN between 'teams' and 'players' on Foreign Key 'team_id'.
    Returns:
        dict: {
            'team': team_info_dict,
            'players': list_of_purchased_players,
            'total_spent': float,
            'remaining_budget': float
        }
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Determine whether lookup is by ID or Short Code
    if isinstance(team_id_or_code, int) or (isinstance(team_id_or_code, str) and team_id_or_code.isdigit()):
        team_id = int(team_id_or_code)
        cursor.execute("SELECT * FROM teams WHERE team_id = ?;", (team_id,))
    else:
        cursor.execute("SELECT * FROM teams WHERE UPPER(short_code) = ?;", (str(team_id_or_code).strip().upper(),))

    team_row = cursor.fetchone()
    if not team_row:
        conn.close()
        return {"team": None, "players": [], "total_spent": 0.0, "remaining_budget": 0.0}

    team = row_to_dict(team_row)

    # Relational SQL JOIN with Foreign Key
    query = """
    SELECT 
        p.player_id,
        p.name,
        p.role,
        p.country,
        p.base_price,
        p.sold_price,
        s.matches,
        s.runs,
        s.batting_avg,
        s.strike_rate,
        s.wickets,
        s.bowling_economy
    FROM players p
    LEFT JOIN player_stats s ON p.player_id = s.player_id
    WHERE p.team_id = ? AND p.status = 'Sold'
    ORDER BY p.sold_price DESC;
    """
    cursor.execute(query, (team["team_id"],))
    player_rows = cursor.fetchall()
    conn.close()

    players_list = [row_to_dict(r) for r in player_rows]
    total_spent = sum(p.get("sold_price", 0.0) for p in players_list)

    return {
        "team": team,
        "players": players_list,
        "total_spent": total_spent,
        "remaining_budget": team["remaining_budget"],
        "total_spent_fmt": format_currency(total_spent),
        "remaining_budget_fmt": format_currency(team["remaining_budget"]),
    }


def get_team_budget_overview() -> List[Dict[str, Any]]:
    """
    [Boss Question 10: Show remaining team budget]
    Returns budget summary across all 10 franchises.
    """
    return read_all_teams()


def update_team_budget(team_id: int, deduction_amount: float) -> bool:
    """
    Deducts auction bid amount from a team's remaining budget.
    Ensures team purse does not go negative.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT remaining_budget FROM teams WHERE team_id = ?;", (team_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False

        curr_budget = row["remaining_budget"]
        if curr_budget < deduction_amount:
            conn.close()
            return False  # Insufficient funds

        new_budget = curr_budget - deduction_amount
        cursor.execute("UPDATE teams SET remaining_budget = ? WHERE team_id = ?;", (new_budget, team_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
