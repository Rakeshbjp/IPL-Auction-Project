import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database import get_supabase_client, SQLITE_DB_PATH

conn = sqlite3.connect(SQLITE_DB_PATH)
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM players WHERE status = 'Available'")
avail_sql = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM players WHERE status != 'Available'")
sold_sql = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM auction_bids")
bids_sql = c.fetchone()[0]
print(f"SQLite: {avail_sql} Available, {sold_sql} Sold, {bids_sql} Bids")

sb = get_supabase_client()
if sb:
    res_players = sb.table("players").select("player_id, status").execute()
    avail_sb = len([p for p in res_players.data if p["status"] == "Available"])
    sold_sb = len([p for p in res_players.data if p["status"] != "Available"])
    res_bids = sb.table("auction_bids").select("bid_id").execute()
    print(f"Supabase: {avail_sb} Available, {sold_sb} Sold, {len(res_bids.data)} Bids")
