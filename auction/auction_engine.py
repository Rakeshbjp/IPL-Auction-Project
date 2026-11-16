"""
Real IPL Auction Simulation Engine
Features:
- Official Mega Auction vs Mini Auction Modes:
  - Mega Auction: Teams receive RTM cards based on retentions (6 - Retained Count)
  - Mini Auction: 0 RTM cards (RTM cannot be used in a Mini Auction)
- Sequential Categorized Sets:
  - Set 1: Capped Batters (BA1)
  - Set 2: Capped All-rounders (AL1)
  - Set 3: Capped Wicketkeepers (WK1)
  - Set 4: Capped Fast Bowlers (FA1)
  - Set 5: Capped Spinners (SP1)
  - Set 6: Uncapped Players (UN1)
- Official Bidding Increment Slabs (<₹1 Cr: +10L, 1-2Cr: +20L, 2-5Cr: +25L, 5-10Cr: +50L, >10Cr: +1Cr)
- Right-To-Match (RTM) Card Challenge Protocol:
  - Prompts former franchise before hammer knockdown
  - Winning bidder gets one final raise, former team can match to retain
- Accelerated Auction Round for Shortlisted Unsold Players
- Strict Squad & Purse Constraints (₹120 Cr purse, 18-25 squad size, max 8 overseas)
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

# Current Auction Mode ("mega" or "mini")
CURRENT_AUCTION_MODE = "mega"


def get_auction_mode() -> str:
    """Returns 'mega' or 'mini'."""
    return CURRENT_AUCTION_MODE


def set_auction_mode(mode: str) -> str:
    """
    Sets the auction mode ('mega' or 'mini') and updates franchise RTM cards:
    - Mega Auction: RTM Cards = max(0, 6 - retentions_count)
    - Mini Auction: RTM Cards = 0 (RTM cards cannot be used in Mini Auction)
    """
    global CURRENT_AUCTION_MODE
    clean_mode = "mini" if mode.strip().lower() == "mini" else "mega"
    CURRENT_AUCTION_MODE = clean_mode

    conn = get_connection()
    cursor = conn.cursor()

    if clean_mode == "mini":
        cursor.execute("UPDATE teams SET rtm_cards = 0;")
    else:
        cursor.execute("UPDATE teams SET rtm_cards = MAX(0, 6 - retentions_count);")

    conn.commit()
    conn.close()
    return CURRENT_AUCTION_MODE


def get_available_players_pool(
    set_code: Optional[str] = None,
    accelerated_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Fetches players in the auction pool, optionally filtered by Set or Accelerated round.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        p.player_id, p.name, p.role, p.country, p.base_price, p.sold_price, p.status,
        p.set_name, p.set_code, p.is_capped, p.is_overseas, p.former_team,
        p.is_shortlisted, p.accelerated,
        s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
        s.wickets, s.bowling_economy
    FROM players p
    JOIN player_stats s ON p.player_id = s.player_id
    WHERE 1=1
    """
    params = []

    if accelerated_only:
        query += " AND (p.accelerated = 1 OR p.status = 'Unsold')"
    else:
        query += " AND p.status = 'Available' AND p.is_shortlisted = 1"

    if set_code and set_code != "ALL" and not accelerated_only:
        query += " AND p.set_code = ?"
        params.append(set_code)

    query += " ORDER BY p.player_id ASC;"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def get_unsold_players_pool() -> List[Dict[str, Any]]:
    """Fetches all players currently marked 'Unsold' eligible for the Accelerated Round."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        p.player_id, p.name, p.role, p.country, p.base_price, p.status,
        p.set_name, p.set_code, p.is_capped, p.is_overseas, p.former_team,
        p.is_shortlisted, p.accelerated,
        s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
        s.wickets, s.bowling_economy
    FROM players p
    JOIN player_stats s ON p.player_id = s.player_id
    WHERE p.status = 'Unsold'
    ORDER BY p.player_id ASC;
    """)
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def add_to_accelerated_shortlist(player_id: int) -> bool:
    """Marks an unsold player to be brought back in the accelerated round."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE players SET accelerated = 1, status = 'Available' WHERE player_id = ?;", (player_id,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_auction_sets() -> List[Dict[str, Any]]:
    """
    Summarizes the 6 official sequential sets with their player counts and progress.
    """
    conn = get_connection()
    cursor = conn.cursor()

    set_definitions = [
        {"code": "BA1", "name": "Set 1: Capped Batters (BA1)", "role": "Batsman", "icon": "🏏"},
        {"code": "AL1", "name": "Set 2: Capped All-rounders (AL1)", "role": "Allrounder", "icon": "🔥"},
        {"code": "WK1", "name": "Set 3: Capped Wicketkeepers (WK1)", "role": "Wicketkeeper", "icon": "🧤"},
        {"code": "FA1", "name": "Set 4: Capped Fast Bowlers (FA1)", "role": "Bowler", "icon": "⚡"},
        {"code": "SP1", "name": "Set 5: Capped Spinners (SP1)", "role": "Bowler", "icon": "🌀"},
        {"code": "UN1", "name": "Set 6: Uncapped Players (UN1)", "role": "Uncapped", "icon": "🌟"},
    ]

    sets_data = []
    for s in set_definitions:
        cursor.execute("SELECT COUNT(*) FROM players WHERE set_code = ?;", (s["code"],))
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM players WHERE set_code = ? AND status = 'Available';", (s["code"],))
        available = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM players WHERE set_code = ? AND status = 'Sold';", (s["code"],))
        sold = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM players WHERE set_code = ? AND status = 'Unsold';", (s["code"],))
        unsold = cursor.fetchone()[0]

        sets_data.append({
            "code": s["code"],
            "name": s["name"],
            "role": s["role"],
            "icon": s["icon"],
            "total": total,
            "available": available,
            "sold": sold,
            "unsold": unsold,
            "is_completed": available == 0 and total > 0
        })

    conn.close()
    return sets_data


def get_bid_increment(current_bid: float) -> float:
    """
    Calculates official IPL style bidding slab increments:
    - Under ₹1 Cr: + ₹10 Lakhs
    - ₹1 Cr – ₹2 Cr: + ₹20 Lakhs
    - ₹2 Cr – ₹5 Cr: + ₹25 Lakhs
    - ₹5 Cr – ₹10 Cr: + ₹50 Lakhs
    - Above ₹10 Cr: + ₹1 Crore
    """
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


def validate_team_bid(team: Dict[str, Any], player: Dict[str, Any], bid_amount: float) -> Tuple[bool, str]:
    """
    Enforces official IPL Purse & Squad Limits:
    1. Budget must cover bid amount
    2. Squad maximum cap: 25 players
    3. Overseas maximum cap: 8 overseas players
    4. Minimum reserve purse: must retain enough funds to fill up to min 18 players
    """
    # 1. Budget check
    if team["remaining_budget"] < bid_amount:
        return (False, f"Insufficient purse (Needs {format_currency(bid_amount)}, Has {format_currency(team['remaining_budget'])})")

    # 2. Maximum Squad check (25 players)
    total_squad = team.get("total_squad_size", team.get("current_squad_size", 0))
    if total_squad >= team.get("max_squad_size", 25):
        return (False, f"Squad size reached maximum cap of {team.get('max_squad_size', 25)} players")

    # 3. Maximum Overseas check (8 players)
    is_overseas = player.get("is_overseas") or (player.get("country", "India") != "India")
    if is_overseas and team.get("overseas_count", 0) >= team.get("max_overseas", 8):
        return (False, f"Overseas quota full (Already {team.get('max_overseas', 8)}/8 overseas players)")

    # 4. Minimum Reserve Purse for 18 players (reserve ₹30L per unfilled spot)
    needed_slots = max(0, team.get("min_squad_size", 18) - (total_squad + 1))
    required_reserve = needed_slots * 3_000_000  # ₹30 Lakhs base price buffer
    if (team["remaining_budget"] - bid_amount) < required_reserve:
        return (False, f"Must preserve {format_currency(required_reserve)} to reach minimum squad of 18 players")

    return (True, "Valid bid")


def check_rtm_eligibility(
    player_id: int,
    winning_team_id: int
) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Checks if former franchise can invoke a Right-To-Match (RTM) Card:
    - Rule 1: Mega Auction only (Mini Auction forbids RTM)
    - Rule 2: Player must have a registered former IPL team
    - Rule 3: Winning bidder cannot be the player's former team
    - Rule 4: Former team must have RTM cards > 0
    - Rule 5: Former team must satisfy squad and purse limits
    """
    if CURRENT_AUCTION_MODE != "mega":
        return (False, None, "RTM cards cannot be used in a Mini Auction")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players WHERE player_id = ?;", (player_id,))
    p_row = cursor.fetchone()
    if not p_row:
        conn.close()
        return (False, None, "Player not found")

    player = row_to_dict(p_row)
    former_code = player.get("former_team")
    if not former_code:
        conn.close()
        return (False, None, "Player has no registered former IPL franchise")

    cursor.execute("SELECT * FROM teams WHERE UPPER(short_code) = ?;", (former_code.strip().upper(),))
    t_row = cursor.fetchone()
    conn.close()

    if not t_row:
        return (False, None, f"Former franchise {former_code} not found")

    former_team = row_to_dict(t_row)
    if former_team["team_id"] == winning_team_id:
        return (False, former_team, "Winning bidder is already player's former team")

    if former_team.get("rtm_cards", 0) <= 0:
        return (False, former_team, f"{former_team['short_code']} has 0 RTM cards remaining")

    return (True, former_team, f"{former_team['team_name']} ({former_team['short_code']}) can exercise RTM Card!")


def execute_rtm_claim(player_id: int, former_team_id: int, final_price: float) -> bool:
    """
    Deducts 1 RTM card from former team, then records winning bid transaction.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        UPDATE teams 
        SET rtm_cards = MAX(0, rtm_cards - 1) 
        WHERE team_id = ?;
        """, (former_team_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        return False
    finally:
        conn.close()

    # Record winning bid under former team
    return record_winning_bid(player_id, former_team_id, final_price)


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
    """Resets all players to 'Available', clears bids, restores budgets, and resets RTM counts."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM auction_bids;")
        cursor.execute("UPDATE players SET status = 'Available', sold_price = 0.0, team_id = NULL, accelerated = 0;")

        # Restore budgets based on retentions
        cursor.execute("""
        UPDATE teams 
        SET remaining_budget = total_budget - retention_spend,
            rtm_cards = CASE WHEN ? = 'mini' THEN 0 ELSE MAX(0, 6 - retentions_count) END;
        """, (CURRENT_AUCTION_MODE,))
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
        "mode": CURRENT_AUCTION_MODE
    }


def run_player_auction(
    player: Dict[str, Any],
    interactive_callback=None
) -> Tuple[str, Optional[Dict[str, Any]], float, Optional[Dict[str, Any]]]:
    """
    Simulates a live bidding battle with official increments and RTM check:
    Returns (status, winning_team, final_price, rtm_eligible_team)
    """
    teams = read_all_teams()
    base_price = float(player.get("base_price", 20_000_000))
    current_bid = base_price
    highest_bidder = None

    # Filter teams that satisfy budget and squad limits
    eligible_teams = []
    for t in teams:
        can_bid, _ = validate_team_bid(t, player, current_bid)
        if can_bid:
            eligible_teams.append(t)

    if not eligible_teams:
        mark_player_unsold(player["player_id"])
        return ("Unsold", None, 0.0, None)

    # Star factor calculation
    runs = player.get("runs", 0)
    wickets = player.get("wickets", 0)
    sr = player.get("strike_rate", 120.0)
    is_marquee = (runs >= 4000) or (wickets >= 100) or (sr >= 150)

    price_multiplier = random.uniform(3.0, 7.5) if is_marquee else random.uniform(1.1, 2.8)
    target_ceiling = base_price * price_multiplier

    num_bidders = min(len(eligible_teams), random.randint(2, 4))
    bidding_teams = random.sample(eligible_teams, num_bidders)

    turn = 0
    while current_bid < target_ceiling and len(bidding_teams) > 1:
        bidder = bidding_teams[turn % len(bidding_teams)]
        increment = get_bid_increment(current_bid)
        next_bid = current_bid + increment

        can_bid, _ = validate_team_bid(bidder, player, next_bid)
        if can_bid:
            current_bid = next_bid
            highest_bidder = bidder
            if interactive_callback:
                interactive_callback(bidder, current_bid)
        else:
            bidding_teams.remove(bidder)

        turn += 1

    if highest_bidder is None:
        highest_bidder = random.choice(eligible_teams)
        current_bid = base_price

    # Check RTM challenge
    rtm_eligible, former_team, _ = check_rtm_eligibility(player["player_id"], highest_bidder["team_id"])
    rtm_info = former_team if rtm_eligible else None

    # If RTM is eligible and former team has RTM cards and random choice decides to match:
    # 40% chance former team exercises RTM
    if rtm_eligible and former_team and random.random() < 0.40:
        can_match, _ = validate_team_bid(former_team, player, current_bid)
        if can_match:
            execute_rtm_claim(player["player_id"], former_team["team_id"], current_bid)
            return ("Sold", former_team, current_bid, former_team)

    # Standard sale to highest bidder
    record_winning_bid(player["player_id"], highest_bidder["team_id"], current_bid)
    return ("Sold", highest_bidder, current_bid, None)
