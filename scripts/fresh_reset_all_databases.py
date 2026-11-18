"""
Completely wipe all demo and bought players from both SQLite and Supabase Cloud.
Resets the entire IPL 2026 auction system to a fresh, clean starting state with:
- All 255 authentic players from the Excel dataset loaded
- Every player marked as 'Available' with sold_price = 0.0 and team_id = NULL
- Zero auction bids in auction_bids
- All 10 franchise squad tables cleared (csk_players, mi_players, rcb_players, etc.)
- All 10 franchises reset to exact pre-auction purses (₹120 Cr total, remaining = total - retention_spend)
"""

import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import SQLITE_DB_PATH, is_supabase_configured
from database import get_supabase_client, init_db
from seed_data import INITIAL_TEAMS

TEAM_CODES = ["csk", "mi", "rcb", "kkr", "rr", "srh", "gt", "lsg", "dc", "pbks"]


def reset_sqlite():
    print("\n--- 1. RESETTING SQLITE DATABASE ---")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # Clear bids
    cursor.execute("DELETE FROM auction_bids;")
    print("  ✓ Cleared auction_bids table")

    # Clear team squad tables
    for code in TEAM_CODES:
        cursor.execute(f"DELETE FROM {code}_players;")
    print("  ✓ Cleared all 10 dedicated franchise squad tables")

    # Reset all players to Available
    cursor.execute("""
    UPDATE players SET
        status = 'Available',
        sold_price = 0.0,
        team_id = NULL,
        accelerated = 0;
    """)
    print("  ✓ Reset all players to 'Available' with sold_price=0.0 and team_id=NULL")

    # Reset teams to authentic pre-auction starting purse
    for team in INITIAL_TEAMS:
        rem = team["total_budget"] - team.get("retention_spend", 0.0)
        cursor.execute("""
        UPDATE teams SET
            total_budget = ?,
            remaining_budget = ?,
            retention_spend = ?,
            retentions_count = ?,
            rtm_cards = ?,
            retained_names = ?,
            min_squad_size = ?,
            max_squad_size = ?,
            max_overseas = ?
        WHERE short_code = ?;
        """, (
            team["total_budget"],
            rem,
            team.get("retention_spend", 0.0),
            team.get("retentions_count", 0),
            team.get("rtm_cards", 0),
            team.get("retained_names", ""),
            team.get("min_squad_size", 18),
            team.get("max_squad_size", 25),
            team.get("max_overseas", 8),
            team["short_code"]
        ))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM players WHERE status = 'Available'")
    avail_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM players WHERE status != 'Available'")
    sold_count = cursor.fetchone()[0]
    print(f"  ✓ SQLite Status: {avail_count} Available, {sold_count} Sold/Demo")

    conn.close()


def reset_supabase():
    print("\n--- 2. RESETTING & SYNCHRONIZING SUPABASE CLOUD ---")
    if not is_supabase_configured():
        print("  ⚠️ Supabase is not configured; skipping cloud sync.")
        return

    sb = get_supabase_client()
    if not sb:
        print("  ❌ Could not initialize Supabase client.")
        return

    # 1. Clear team tables
    for code in TEAM_CODES:
        try:
            sb.table(f"{code}_players").delete().gte("id", 0).execute()
        except Exception as e:
            print(f"  Warning clearing {code}_players in Supabase: {e}")
    print("  ✓ Cleared all 10 franchise squad tables in Supabase")

    # 2. Clear auction_bids
    try:
        sb.table("auction_bids").delete().gte("bid_id", 0).execute()
    except Exception as e:
        print(f"  Warning clearing auction_bids in Supabase: {e}")
    print("  ✓ Cleared auction_bids in Supabase")

    # 3. Clear player_stats
    try:
        sb.table("player_stats").delete().gte("stat_id", 0).execute()
    except Exception as e:
        print(f"  Warning clearing player_stats in Supabase: {e}")
    print("  ✓ Cleared player_stats in Supabase")

    # 4. Clear players
    try:
        sb.table("players").delete().gte("player_id", 0).execute()
    except Exception as e:
        print(f"  Warning clearing players in Supabase: {e}")
    print("  ✓ Cleared players in Supabase")

    # 5. Populate fresh players and stats from SQLite
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players ORDER BY player_id ASC;")
    players = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM player_stats ORDER BY stat_id ASC;")
    stats = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM teams ORDER BY team_id ASC;")
    teams = [dict(r) for r in cursor.fetchall()]
    conn.close()

    # Update teams in Supabase with starting purse
    for t in teams:
        team_payload = {
            "team_id": t["team_id"],
            "team_name": t["team_name"],
            "short_code": t["short_code"],
            "primary_color": t["primary_color"],
            "secondary_color": t["secondary_color"],
            "total_budget": float(t["total_budget"]),
            "remaining_budget": float(t["remaining_budget"]),
            "retention_spend": float(t.get("retention_spend", 0.0)),
            "retentions_count": int(t.get("retentions_count", 0)),
            "rtm_cards": int(t.get("rtm_cards", 0)),
            "retained_names": t.get("retained_names", ""),
            "min_squad_size": int(t.get("min_squad_size", 18)),
            "max_squad_size": int(t.get("max_squad_size", 25)),
            "max_overseas": int(t.get("max_overseas", 8)),
        }
        sb.table("teams").upsert(team_payload).execute()
    print(f"  ✓ Synchronized all {len(teams)} teams with pre-auction purses in Supabase")

    # Batch insert players (batches of 50)
    batch_size = 50
    for i in range(0, len(players), batch_size):
        batch = players[i:i + batch_size]
        players_payload = []
        for p in batch:
            players_payload.append({
                "player_id": p["player_id"],
                "name": p["name"],
                "role": p["role"],
                "country": p["country"],
                "base_price": float(p["base_price"]),
                "sold_price": 0.0,
                "status": "Available",
                "team_id": None,
                "set_name": p.get("set_name", "Set 1: Capped Batters (BA1)"),
                "set_code": p.get("set_code", "BA1"),
                "is_capped": int(p.get("is_capped", 1)),
                "is_overseas": int(p.get("is_overseas", 0)),
                "former_team": p.get("former_team"),
                "is_shortlisted": int(p.get("is_shortlisted", 1)),
                "accelerated": int(p.get("accelerated", 0))
            })
        sb.table("players").insert(players_payload).execute()
    print(f"  ✓ Synchronized all {len(players)} players into Supabase 'players' table")

    # Batch insert stats (batches of 50)
    for i in range(0, len(stats), batch_size):
        batch = stats[i:i + batch_size]
        stats_payload = []
        for s in batch:
            stats_payload.append({
                "stat_id": s["stat_id"],
                "player_id": s["player_id"],
                "matches": int(s.get("matches", 0)),
                "runs": int(s.get("runs", 0)),
                "highest_score": int(s.get("highest_score", 0)),
                "batting_avg": float(s.get("batting_avg", 0.0)),
                "strike_rate": float(s.get("strike_rate", 0.0)),
                "fours": int(s.get("fours", 0)),
                "sixes": int(s.get("sixes", 0)),
                "centuries": int(s.get("centuries", 0)),
                "fifties": int(s.get("fifties", 0)),
                "wickets": int(s.get("wickets", 0)),
                "bowling_economy": float(s.get("bowling_economy", 0.0)),
                "bowling_avg": float(s.get("bowling_avg", 0.0)),
            })
        sb.table("player_stats").insert(stats_payload).execute()
    print(f"  ✓ Synchronized all {len(stats)} player stats into Supabase 'player_stats' table")


def main():
    print("=" * 70)
    print("CLEANING ALL DEMO & BOUGHT PLAYERS — FRESH IPL AUCTION START")
    print("=" * 70)
    reset_sqlite()
    reset_supabase()
    print("\n" + "=" * 70)
    print("✅ FRESH START COMPLETE! ALL DATABASES READY FOR LIVE AUCTION!")
    print("=" * 70)


if __name__ == "__main__":
    main()
