"""
Supabase Real-Time Sync Manager for IPL Auction System
Synchronizes all CRUD operations, auction bids, team budget transactions,
and dedicated franchise squad tables directly to Supabase Cloud PostgreSQL.
"""

from typing import List, Dict, Any, Optional
from config import DB_MODE, is_supabase_configured
from database import get_supabase_client, get_connection, row_to_dict

TEAM_CODES = ["csk", "mi", "rcb", "kkr", "rr", "srh", "gt", "lsg", "dc", "pbks"]


def is_supabase_enabled() -> bool:
    """Returns True if Supabase mode is configured in .env."""
    return DB_MODE == "supabase" and is_supabase_configured()


def sync_create_player(
    name: str,
    role: str,
    country: str,
    base_price: float,
    matches: int,
    runs: int,
    highest_score: int,
    batting_avg: float,
    strike_rate: float,
    fours: int,
    sixes: int,
    centuries: int,
    fifties: int,
    wickets: int,
    bowling_economy: float,
    bowling_avg: float,
    known_id: Optional[int] = None
) -> Optional[int]:
    """Inserts a new player and their career statistics into Supabase tables."""
    if not is_supabase_enabled():
        return None

    sb = get_supabase_client()
    if not sb:
        return None

    try:
        player_payload = {
            "name": name.strip(),
            "role": role.strip(),
            "country": country.strip(),
            "base_price": float(base_price),
            "sold_price": 0.0,
            "status": "Available",
            "team_id": None
        }
        if known_id:
            player_payload["player_id"] = known_id

        res = sb.table("players").insert(player_payload).execute()
        if not res.data:
            return None

        new_player_id = res.data[0]["player_id"]

        stats_payload = {
            "player_id": new_player_id,
            "matches": matches,
            "runs": runs,
            "highest_score": highest_score,
            "batting_avg": batting_avg,
            "strike_rate": strike_rate,
            "fours": fours,
            "sixes": sixes,
            "centuries": centuries,
            "fifties": fifties,
            "wickets": wickets,
            "bowling_economy": bowling_economy,
            "bowling_avg": bowling_avg,
        }
        sb.table("player_stats").insert(stats_payload).execute()
        print(f"[Supabase Sync] Successfully created player '{name}' (ID: {new_player_id}) in Supabase!")
        return new_player_id
    except Exception as e:
        print(f"[Supabase Sync Warning] Could not sync player creation to Supabase: {e}")
        return None


def sync_update_player_stats(player_id: int, updates: Dict[str, Any]) -> bool:
    """Updates statistics for a player in Supabase player_stats table."""
    if not is_supabase_enabled():
        return False

    sb = get_supabase_client()
    if not sb:
        return False

    try:
        allowed = [
            "matches", "runs", "highest_score", "batting_avg", "strike_rate",
            "fours", "sixes", "centuries", "fifties", "wickets", "bowling_economy", "bowling_avg"
        ]
        clean_updates = {k: v for k, v in updates.items() if k in allowed and v is not None}
        if not clean_updates:
            return False

        sb.table("player_stats").update(clean_updates).eq("player_id", player_id).execute()
        print(f"[Supabase Sync] Updated stats for player #{player_id} in Supabase!")
        return True
    except Exception as e:
        print(f"[Supabase Sync Warning] Could not sync player update to Supabase: {e}")
        return False


def sync_delete_player(player_id: int) -> bool:
    """Deletes a player from Supabase players table and all team squad tables."""
    if not is_supabase_enabled():
        return False

    sb = get_supabase_client()
    if not sb:
        return False

    try:
        sb.table("players").delete().eq("player_id", player_id).execute()

        # Clean from all franchise squad tables
        for code in TEAM_CODES:
            try:
                sb.table(f"{code}_players").delete().eq("player_id", player_id).execute()
            except Exception:
                pass

        print(f"[Supabase Sync] Deleted player #{player_id} from Supabase!")
        return True
    except Exception as e:
        print(f"[Supabase Sync Warning] Could not sync player delete to Supabase: {e}")
        return False


def sync_record_winning_bid(
    player_id: int,
    team_id: int,
    sold_price: float,
    team_code: Optional[str] = None,
    player_data: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Updates player as Sold to winning team, deducts budget, records bid,
    and stores player details into that specific team's database table (e.g. csk_players, mi_players) in Supabase.
    """
    if not is_supabase_enabled():
        return False

    sb = get_supabase_client()
    if not sb:
        return False

    try:
        # 1. Update player status, sold_price, and team_id in Supabase
        sb.table("players").update({
            "status": "Sold",
            "sold_price": float(sold_price),
            "team_id": int(team_id)
        }).eq("player_id", player_id).execute()

        # 2. Fetch current team budget and deduct
        team_res = sb.table("teams").select("remaining_budget, short_code").eq("team_id", team_id).execute()
        code = team_code
        if team_res.data:
            current_rem = float(team_res.data[0]["remaining_budget"])
            code = code or team_res.data[0].get("short_code")
            new_rem = max(0.0, current_rem - float(sold_price))
            sb.table("teams").update({"remaining_budget": new_rem}).eq("team_id", team_id).execute()

        # 3. Record entry into auction_bids table
        sb.table("auction_bids").insert({
            "player_id": int(player_id),
            "team_id": int(team_id),
            "bid_amount": float(sold_price)
        }).execute()

        # 4. Insert into that specific team's squad table (e.g. csk_players, rcb_players)
        if code and player_data:
            team_table = f"{code.strip().lower()}_players"
            team_payload = {
                "player_id": int(player_id),
                "name": str(player_data.get("name", "")),
                "role": str(player_data.get("role", "Batsman")),
                "country": str(player_data.get("country", "India")),
                "sold_price": float(sold_price),
                "matches": int(player_data.get("matches", 0)),
                "runs": int(player_data.get("runs", 0)),
                "highest_score": int(player_data.get("highest_score", 0)),
                "batting_avg": float(player_data.get("batting_avg", 0.0)),
                "strike_rate": float(player_data.get("strike_rate", 0.0)),
                "fours": int(player_data.get("fours", 0)),
                "sixes": int(player_data.get("sixes", 0)),
                "wickets": int(player_data.get("wickets", 0)),
                "bowling_economy": float(player_data.get("bowling_economy", 0.0)),
                "bowling_avg": float(player_data.get("bowling_avg", 0.0)),
            }
            try:
                # Remove if previously in another team table
                for other_code in TEAM_CODES:
                    try:
                        sb.table(f"{other_code}_players").delete().eq("player_id", player_id).execute()
                    except Exception:
                        pass
                sb.table(team_table).insert(team_payload).execute()
                print(f"[Supabase Sync] Player '{player_data.get('name')}' saved to '{team_table}' table in Supabase!")
            except Exception as te:
                print(f"[Supabase Sync Warning] Could not insert into {team_table}: {te}")

        print(f"[Supabase Sync] Recorded winning bid: Player #{player_id} -> Team #{team_id} for ₹{sold_price:,.0f} in Supabase!")
        return True
    except Exception as e:
        print(f"[Supabase Sync Warning] Could not sync winning bid to Supabase: {e}")
        return False


def sync_mark_player_unsold(player_id: int) -> bool:
    """Marks player as Unsold in Supabase and removes from all team tables."""
    if not is_supabase_enabled():
        return False

    sb = get_supabase_client()
    if not sb:
        return False

    try:
        sb.table("players").update({
            "status": "Unsold",
            "sold_price": 0.0,
            "team_id": None
        }).eq("player_id", player_id).execute()

        # Remove from any team squad table
        for code in TEAM_CODES:
            try:
                sb.table(f"{code}_players").delete().eq("player_id", player_id).execute()
            except Exception:
                pass

        print(f"[Supabase Sync] Marked player #{player_id} as UNSOLD in Supabase!")
        return True
    except Exception as e:
        print(f"[Supabase Sync Warning] Could not sync unsold status to Supabase: {e}")
        return False


def sync_reset_auction() -> bool:
    """Resets all players to Available, clears auction_bids, and restores ₹120 Cr in Supabase."""
    if not is_supabase_enabled():
        return False

    sb = get_supabase_client()
    if not sb:
        return False

    try:
        # 1. Clear auction bids
        sb.table("auction_bids").delete().gte("bid_id", 0).execute()

        # 2. Reset players
        sb.table("players").update({
            "status": "Available",
            "sold_price": 0.0,
            "team_id": None
        }).gte("player_id", 0).execute()

        # 3. Reset team budgets to total_budget (₹120 Cr)
        sb.table("teams").update({
            "remaining_budget": 1200000000.0
        }).gte("team_id", 0).execute()

        # 4. Clear all 10 team franchise tables
        for code in TEAM_CODES:
            try:
                sb.table(f"{code}_players").delete().gte("id", 0).execute()
            except Exception:
                pass

        print("[Supabase Sync] Entire auction successfully reset in Supabase!")
        return True
    except Exception as e:
        print(f"[Supabase Sync Warning] Could not sync auction reset to Supabase: {e}")
        return False


def sync_push_all_to_supabase() -> Dict[str, Any]:
    """
    Reads all SQLite tables (teams, players, stats, bids, and team squads)
    and pushes/upserts everything cleanly into Supabase.
    """
    if not is_supabase_enabled():
        return {"success": False, "message": "Supabase not enabled in .env"}

    sb = get_supabase_client()
    if not sb:
        return {"success": False, "message": "Supabase client not initialized"}

    conn = get_connection()
    cursor = conn.cursor()

    results = {"teams": 0, "players": 0, "stats": 0, "bids": 0, "team_squads": 0}

    try:
        # 1. Sync Teams
        cursor.execute("SELECT * FROM teams;")
        teams = [row_to_dict(r) for r in cursor.fetchall()]
        for t in teams:
            sb.table("teams").upsert({
                "team_id": t["team_id"],
                "team_name": t["team_name"],
                "short_code": t["short_code"],
                "primary_color": t["primary_color"],
                "secondary_color": t["secondary_color"],
                "total_budget": float(t["total_budget"]),
                "remaining_budget": float(t["remaining_budget"]),
                "max_squad_size": t["max_squad_size"]
            }).execute()
            results["teams"] += 1

        # 2. Sync Players
        cursor.execute("SELECT * FROM players;")
        players = [row_to_dict(r) for r in cursor.fetchall()]
        for p in players:
            sb.table("players").upsert({
                "player_id": p["player_id"],
                "name": p["name"],
                "role": p["role"],
                "country": p["country"],
                "base_price": float(p["base_price"]),
                "sold_price": float(p["sold_price"]),
                "status": p["status"],
                "team_id": p["team_id"]
            }).execute()
            results["players"] += 1

        # 3. Sync Player Stats
        cursor.execute("SELECT * FROM player_stats;")
        stats = [row_to_dict(r) for r in cursor.fetchall()]
        for s in stats:
            sb.table("player_stats").upsert({
                "player_id": s["player_id"],
                "matches": s["matches"],
                "runs": s["runs"],
                "highest_score": s["highest_score"],
                "batting_avg": float(s["batting_avg"]),
                "strike_rate": float(s["strike_rate"]),
                "fours": s.get("fours", 0),
                "sixes": s.get("sixes", 0),
                "centuries": s.get("centuries", 0),
                "fifties": s.get("fifties", 0),
                "wickets": s["wickets"],
                "bowling_economy": float(s["bowling_economy"]),
                "bowling_avg": float(s["bowling_avg"])
            }).execute()
            results["stats"] += 1

        # 4. Sync Auction Bids
        cursor.execute("SELECT * FROM auction_bids;")
        bids = [row_to_dict(r) for r in cursor.fetchall()]
        for b in bids:
            sb.table("auction_bids").upsert({
                "bid_id": b["bid_id"],
                "player_id": b["player_id"],
                "team_id": b["team_id"],
                "bid_amount": float(b["bid_amount"]),
                "bid_time": b["bid_time"]
            }).execute()
            results["bids"] += 1

        # 5. Sync Individual Team Tables
        for code in TEAM_CODES:
            table_name = f"{code}_players"
            cursor.execute(f"SELECT * FROM {table_name};")
            team_players = [row_to_dict(r) for r in cursor.fetchall()]
            for tp in team_players:
                sb.table(table_name).upsert({
                    "player_id": tp["player_id"],
                    "name": tp["name"],
                    "role": tp["role"],
                    "country": tp["country"],
                    "sold_price": float(tp["sold_price"]),
                    "matches": tp.get("matches", 0),
                    "runs": tp.get("runs", 0),
                    "highest_score": tp.get("highest_score", 0),
                    "batting_avg": float(tp.get("batting_avg", 0.0)),
                    "strike_rate": float(tp.get("strike_rate", 0.0)),
                    "fours": tp.get("fours", 0),
                    "sixes": tp.get("sixes", 0),
                    "wickets": tp.get("wickets", 0),
                    "bowling_economy": float(tp.get("bowling_economy", 0.0)),
                    "bowling_avg": float(tp.get("bowling_avg", 0.0)),
                }).execute()
                results["team_squads"] += 1

        conn.close()
        return {"success": True, "results": results}
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e), "results": results}
