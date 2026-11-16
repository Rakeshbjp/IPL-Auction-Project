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

from typing import List, Dict, Any, Optional, Tuple
from database import get_connection, row_to_dict
from config import format_currency


def read_all_teams() -> List[Dict[str, Any]]:
    """Fetches all 10 IPL franchises with their purse, retentions, RTM cards, and squad counts."""
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
        t.retention_spend,
        t.retentions_count,
        t.rtm_cards,
        t.retained_names,
        t.min_squad_size,
        t.max_squad_size,
        t.max_overseas,
        COUNT(p.player_id) AS current_squad_size,
        SUM(CASE WHEN p.is_overseas = 1 THEN 1 ELSE 0 END) AS overseas_count
    FROM teams t
    LEFT JOIN players p ON t.team_id = p.team_id AND p.status = 'Sold'
    GROUP BY t.team_id
    ORDER BY t.team_id ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    teams: List[Dict[str, Any]] = []
    for r in rows:
        d = row_to_dict(r)
        d["overseas_count"] = d.get("overseas_count") or 0
        d["total_squad_size"] = d["current_squad_size"] + (d.get("retentions_count") or 0)
        d["is_squad_full"] = d["total_squad_size"] >= d["max_squad_size"]
        d["is_min_squad_met"] = d["total_squad_size"] >= d["min_squad_size"]
        d["is_overseas_full"] = d["overseas_count"] >= d["max_overseas"]

        d["total_budget_fmt"] = format_currency(d["total_budget"])
        d["remaining_budget_fmt"] = format_currency(d["remaining_budget"])
        d["spent_budget_fmt"] = format_currency(d["spent_budget"])
        d["retention_spend_fmt"] = format_currency(d.get("retention_spend", 0.0))
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


def retain_player_for_team(team_id: int, player_id: int, retention_price: Optional[float] = None) -> Tuple[bool, str]:
    """
    Retains a player for a franchise ahead of the auction:
    - Enforces maximum 6 retentions per team.
    - Determines retention cost (default: player's base price or tier).
    - Checks that franchise has sufficient purse.
    - Updates team retention spend, remaining budget, retentions count, retained names, and RTM cards.
    - Updates player status to 'Retained' under team_id.
    - Records player into team's dedicated squad table (e.g. rcb_players).
    """
    from database import get_connection, row_to_dict, record_player_in_team_table
    from auction.auction_engine import get_auction_mode

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Fetch team
        cursor.execute("SELECT * FROM teams WHERE team_id = ?;", (team_id,))
        team_row = cursor.fetchone()
        if not team_row:
            return False, "Franchise not found."
        team = row_to_dict(team_row)

        if team.get("retentions_count", 0) >= 6:
            return False, f"Maximum retention limit reached (Already 6/6 players retained for {team['short_code']})."

        # 2. Fetch player
        cursor.execute("""
        SELECT p.*, s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
               s.fours, s.sixes, s.wickets, s.bowling_economy, s.bowling_avg
        FROM players p
        LEFT JOIN player_stats s ON p.player_id = s.player_id
        WHERE p.player_id = ?;
        """, (player_id,))
        player_row = cursor.fetchone()
        if not player_row:
            return False, "Player not found."
        player = row_to_dict(player_row)

        # Cost: user provided, or player base price, or default slab
        cost = float(retention_price) if retention_price and float(retention_price) > 0 else float(player.get("base_price", 10_000_000.0))

        if team["remaining_budget"] < cost:
            return False, f"Insufficient purse: {team['short_code']} has {format_currency(team['remaining_budget'])} available, requires {format_currency(cost)}."

        # Update Team
        new_retentions_count = team.get("retentions_count", 0) + 1
        new_retention_spend = team.get("retention_spend", 0.0) + cost
        new_rem_budget = team["remaining_budget"] - cost

        existing_names = [n.strip() for n in team.get("retained_names", "").split(",") if n.strip()]
        if player["name"] not in existing_names:
            existing_names.append(player["name"])
        updated_names_str = ", ".join(existing_names)

        # Recalculate RTM cards based on mode
        mode = get_auction_mode()
        new_rtm = max(0, 6 - new_retentions_count) if mode == "mega" else 0

        cursor.execute("""
        UPDATE teams 
        SET retentions_count = ?,
            retention_spend = ?,
            remaining_budget = ?,
            retained_names = ?,
            rtm_cards = ?
        WHERE team_id = ?;
        """, (new_retentions_count, new_retention_spend, new_rem_budget, updated_names_str, new_rtm, team_id))

        # Update Player
        cursor.execute("""
        UPDATE players 
        SET status = 'Retained',
            team_id = ?,
            sold_price = ?
        WHERE player_id = ?;
        """, (team_id, cost, player_id))

        conn.commit()

        # Insert into dedicated squad table
        player["sold_price"] = cost
        record_player_in_team_table(team["short_code"], player)

        return True, f"Successfully retained {player['name']} for {team['team_name']} at {format_currency(cost)}! RTM cards: {new_rtm}."
    except Exception as e:
        conn.rollback()
        return False, f"Error retaining player: {e}"
    finally:
        conn.close()


def release_player_from_team(team_id: int, player_id: int) -> Tuple[bool, str]:
    """
    Releases a player (retained or auctioned) back into the available pool:
    - Refunds player's cost back to remaining_budget.
    - Updates retentions count and retained names if player was retained.
    - Recalculates RTM cards.
    - Sets player status to 'Available' and team_id to NULL.
    - Removes from team's dedicated squad table.
    """
    from database import get_connection, row_to_dict, remove_player_from_team_tables
    from auction.auction_engine import get_auction_mode

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM teams WHERE team_id = ?;", (team_id,))
        team_row = cursor.fetchone()
        if not team_row:
            return False, "Franchise not found."
        team = row_to_dict(team_row)

        cursor.execute("SELECT * FROM players WHERE player_id = ?;", (player_id,))
        player_row = cursor.fetchone()
        if not player_row:
            return False, "Player not found."
        player = row_to_dict(player_row)

        cost = float(player.get("sold_price", 0.0))
        is_retained = player.get("status") == "Retained" or player["name"] in team.get("retained_names", "")

        new_rem_budget = min(team["total_budget"], team["remaining_budget"] + cost)
        new_retentions_count = max(0, team.get("retentions_count", 0) - (1 if is_retained else 0))
        new_retention_spend = max(0.0, team.get("retention_spend", 0.0) - (cost if is_retained else 0.0))

        existing_names = [n.strip() for n in team.get("retained_names", "").split(",") if n.strip()]
        existing_names = [n for n in existing_names if n != player["name"]]
        updated_names_str = ", ".join(existing_names)

        mode = get_auction_mode()
        new_rtm = max(0, 6 - new_retentions_count) if mode == "mega" else 0

        cursor.execute("""
        UPDATE teams 
        SET retentions_count = ?,
            retention_spend = ?,
            remaining_budget = ?,
            retained_names = ?,
            rtm_cards = ?
        WHERE team_id = ?;
        """, (new_retentions_count, new_retention_spend, new_rem_budget, updated_names_str, new_rtm, team_id))

        cursor.execute("""
        UPDATE players 
        SET status = 'Available',
            team_id = NULL,
            sold_price = 0.0
        WHERE player_id = ?;
        """, (player_id,))

        cursor.execute("DELETE FROM auction_bids WHERE player_id = ? AND team_id = ?;", (player_id, team_id))

        conn.commit()

        # Remove from dedicated squad table
        remove_player_from_team_tables(player_id)

        return True, f"Released {player['name']} from {team['team_name']} back to Available Auction Pool. Refunded {format_currency(cost)}!"
    except Exception as e:
        conn.rollback()
        return False, f"Error releasing player: {e}"
    finally:
        conn.close()


def get_team_full_dossier(team_id_or_code: Any) -> Dict[str, Any]:
    """
    Returns complete franchise profile:
    - Team info, purse, budget, retentions, RTM cards
    - Retained players list
    - Picked in live auction players list
    - Eligible players available to retain
    """
    from database import get_connection, row_to_dict
    from crud.player_crud import read_all_players

    conn = get_connection()
    cursor = conn.cursor()

    if isinstance(team_id_or_code, int) or (isinstance(team_id_or_code, str) and team_id_or_code.isdigit()):
        cursor.execute("SELECT * FROM teams WHERE team_id = ?;", (int(team_id_or_code),))
    else:
        cursor.execute("SELECT * FROM teams WHERE UPPER(short_code) = ?;", (str(team_id_or_code).strip().upper(),))

    team_row = cursor.fetchone()
    if not team_row:
        conn.close()
        return {}

    team = row_to_dict(team_row)
    team_id = team["team_id"]

    # All players assigned to this team
    cursor.execute("""
    SELECT p.*, s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
           s.wickets, s.bowling_economy
    FROM players p
    LEFT JOIN player_stats s ON p.player_id = s.player_id
    WHERE p.team_id = ?
    ORDER BY p.sold_price DESC;
    """, (team_id,))
    assigned_rows = cursor.fetchall()
    conn.close()

    assigned_players = [row_to_dict(r) for r in assigned_rows]
    retained_names_list = [n.strip() for n in team.get("retained_names", "").split(",") if n.strip()]

    retained_players = []
    auction_picked_players = []

    for p in assigned_players:
        if p["status"] == "Retained" or p["name"] in retained_names_list:
            retained_players.append(p)
        else:
            auction_picked_players.append(p)

    total_squad = len(assigned_players) + len(retained_names_list) if not assigned_players else len(assigned_players)
    overseas_count = len([p for p in assigned_players if p.get("is_overseas") or p.get("country", "India") != "India"])

    all_players = read_all_players()
    available_to_retain = [p for p in all_players if p.get("status") == "Available"]

    return {
        "team": team,
        "retained_players": retained_players,
        "auction_picked_players": auction_picked_players,
        "available_to_retain": available_to_retain,
        "total_squad": total_squad,
        "overseas_count": overseas_count,
        "total_spent_fmt": format_currency(team["total_budget"] - team["remaining_budget"]),
        "remaining_budget_fmt": format_currency(team["remaining_budget"]),
        "retention_spend_fmt": format_currency(team.get("retention_spend", 0.0)),
    }
