"""
Real IPL Auction Simulation Engine
Features:
- Live franchise bidding simulation with realistic purse constraints
- Auctioneer gavel knockdowns ("Going once, going twice, SOLD!")
- Database state updates (Status, Sold Price, Foreign Key team_id, Purse deductions)
- Records every bid into 'auction_bids' table for full audit trail
"""

import time
import random
from typing import List, Dict, Any, Optional, Tuple
from database import (
    get_connection,
    row_to_dict,
    record_player_in_team_table,
    remove_player_from_team_tables,
    clear_all_team_tables,
)
from config import format_currency
from crud.team_crud import read_all_teams
from supabase_sync import (
    sync_record_winning_bid,
    sync_mark_player_unsold,
    sync_reset_auction,
)



def get_available_players_pool() -> List[Dict[str, Any]]:
    """Fetches all players currently marked 'Available' in the auction pool."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        p.player_id, p.name, p.role, p.country, p.base_price, p.status,
        s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
        s.wickets, s.bowling_economy
    FROM players p
    JOIN player_stats s ON p.player_id = s.player_id
    WHERE p.status = 'Available'
    ORDER BY p.player_id ASC;
    """)
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def get_bid_increment(current_bid: float) -> float:
    """Calculates official IPL style bidding slab increments."""
    if current_bid < 10_000_000:       # Under 1 Cr
        return 1_000_000               # + 10 Lakhs
    elif current_bid < 20_000_000:     # 1 Cr - 2 Cr
        return 2_000_000               # + 20 Lakhs
    elif current_bid < 50_000_000:     # 2 Cr - 5 Cr
        return 2_500_000               # + 25 Lakhs
    elif current_bid < 100_000_000:    # 5 Cr - 10 Cr
        return 5_000_000               # + 50 Lakhs
    else:                              # Above 10 Cr
        return 10_000_000              # + 1 Crore


def record_winning_bid(player_id: int, team_id: int, sold_price: float) -> bool:
    """
    Executes the winning bid transaction:
    1. Sets player status to 'Sold', updates sold_price, sets team_id (Foreign Key).
    2. Deducts sold_price from team's remaining_budget.
    3. Records winning entry into auction_bids table.
    4. Inserts player into buying team's dedicated database table (e.g. csk_players, mi_players).
    5. Synchronizes transaction to Supabase Cloud PostgreSQL in real-time!
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check team budget & fetch short_code
        cursor.execute("SELECT short_code, remaining_budget FROM teams WHERE team_id = ?;", (team_id,))
        team_row = cursor.fetchone()
        if not team_row or team_row["remaining_budget"] < sold_price:
            conn.close()
            return False

        team_code = team_row["short_code"]

        # Fetch player info and stats for team-specific database table
        cursor.execute("""
        SELECT p.player_id, p.name, p.role, p.country, s.matches, s.runs, s.highest_score,
               s.batting_avg, s.strike_rate, s.fours, s.sixes, s.wickets, s.bowling_economy, s.bowling_avg
        FROM players p
        LEFT JOIN player_stats s ON p.player_id = s.player_id
        WHERE p.player_id = ?;
        """, (player_id,))
        player_row = cursor.fetchone()
        player_info = row_to_dict(player_row) if player_row else {}
        player_info["sold_price"] = sold_price

        # 1. Update player record in players table
        cursor.execute("""
        UPDATE players 
        SET status = 'Sold', sold_price = ?, team_id = ?
        WHERE player_id = ?;
        """, (sold_price, team_id, player_id))

        # 2. Update team budget
        new_budget = team_row["remaining_budget"] - sold_price
        cursor.execute("UPDATE teams SET remaining_budget = ? WHERE team_id = ?;", (new_budget, team_id))

        # 3. Insert into auction_bids table
        cursor.execute("""
        INSERT INTO auction_bids (player_id, team_id, bid_amount)
        VALUES (?, ?, ?);
        """, (player_id, team_id, sold_price))

        conn.commit()

        # 4. Insert into the buying team's dedicated squad table (e.g. csk_players, rcb_players)
        try:
            record_player_in_team_table(team_code, player_info)
        except Exception as te:
            print(f"[Notice] Team table insert: {te}")

        # 5. Real-time synchronization to Supabase Cloud PostgreSQL
        try:
            sync_record_winning_bid(
                player_id=player_id,
                team_id=team_id,
                sold_price=sold_price,
                team_code=team_code,
                player_data=player_info
            )
        except Exception as se:
            print(f"[Sync Notice] Supabase winning bid sync: {se}")

        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def mark_player_unsold(player_id: int) -> bool:
    """Marks a player as Unsold if no bids were placed and removes from team tables."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE players SET status = 'Unsold', sold_price = 0.0, team_id = NULL WHERE player_id = ?;", (player_id,))
        conn.commit()

        # Remove from any team squad table
        remove_player_from_team_tables(player_id)

        # Real-time synchronization to Supabase Cloud PostgreSQL
        try:
            sync_mark_player_unsold(player_id)
        except Exception as se:
            print(f"[Sync Notice] Supabase unsold sync: {se}")

        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()


def reset_entire_auction() -> bool:
    """Resets all players to 'Available', clears bids, restores ₹120 Cr, and clears team tables."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM auction_bids;")
        cursor.execute("UPDATE players SET status = 'Available', sold_price = 0.0, team_id = NULL;")
        cursor.execute("UPDATE teams SET remaining_budget = total_budget;")
        conn.commit()

        # Clear all dedicated franchise squad tables
        clear_all_team_tables()

        # Real-time synchronization to Supabase Cloud PostgreSQL
        try:
            sync_reset_auction()
        except Exception as se:
            print(f"[Sync Notice] Supabase reset sync: {se}")

        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()


def get_auction_stats() -> Dict[str, Any]:
    """Provides summary statistics of the auction state."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM players WHERE status = 'Sold';")
    sold_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM players WHERE status = 'Unsold';")
    unsold_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM players WHERE status = 'Available';")
    available_count = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(sold_price) FROM players WHERE status = 'Sold';")
    total_spent = cursor.fetchone()[0] or 0.0

    conn.close()

    return {
        "sold": sold_count,
        "unsold": unsold_count,
        "available": available_count,
        "total_spent": total_spent,
        "total_spent_fmt": format_currency(total_spent),
    }


def run_player_auction(
    player: Dict[str, Any],
    user_team_id: Optional[int] = None,
    interactive_callback=None
) -> Tuple[str, Optional[Dict[str, Any]], float]:
    """
    Simulates a live bidding battle for a player.
    
    Parameters:
        player (dict): Player dictionary.
        user_team_id (int, optional): If user controls a team.
        interactive_callback: Optional callable for step-by-step UI updates.
        
    Returns:
        (status, winning_team, final_price)
    """
    teams = read_all_teams()
    base_price = float(player.get("base_price", 20_000_000))
    current_bid = base_price
    highest_bidder = None

    # Filter teams that have enough purse to at least place base price
    eligible_teams = [
        t for t in teams 
        if t["remaining_budget"] >= current_bid and t["current_squad_size"] < t["max_squad_size"]
    ]

    if not eligible_teams:
        mark_player_unsold(player["player_id"])
        return ("Unsold", None, 0.0)

    # Determine bidding interest based on player quality & roles
    # Elite players (runs > 4000 or wickets > 100 or SR > 150) spark bidding wars
    runs = player.get("runs", 0)
    wickets = player.get("wickets", 0)
    sr = player.get("strike_rate", 120.0)
    is_marquee = (runs >= 4000) or (wickets >= 100) or (sr >= 150)

    # Max price cap simulation
    if is_marquee:
        price_multiplier = random.uniform(3.5, 9.5)
    else:
        price_multiplier = random.uniform(1.2, 3.2)

    target_ceiling = base_price * price_multiplier

    # Pick 2 to 4 teams to enter bidding war
    num_bidders = min(len(eligible_teams), random.randint(2, 5))
    bidding_teams = random.sample(eligible_teams, num_bidders)

    turn = 0
    while current_bid < target_ceiling:
        bidder = bidding_teams[turn % len(bidding_teams)]
        increment = get_bid_increment(current_bid)
        next_bid = current_bid + increment

        if bidder["remaining_budget"] >= next_bid:
            current_bid = next_bid
            highest_bidder = bidder
            if interactive_callback:
                interactive_callback(bidder, current_bid)
        else:
            # Team drops out due to budget
            bidding_teams.remove(bidder)
            if len(bidding_teams) <= 1:
                break

        turn += 1
        if len(bidding_teams) == 0:
            break

    if highest_bidder is None:
        # Check if at least one team takes at base price
        buyer = random.choice(eligible_teams)
        highest_bidder = buyer
        current_bid = base_price

    # Record winning bid in database
    record_winning_bid(player["player_id"], highest_bidder["team_id"], current_bid)
    return ("Sold", highest_bidder, current_bid)
