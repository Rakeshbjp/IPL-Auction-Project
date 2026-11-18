"""
Database manager for IPL Auction System.
Supports both SQLite3 (local relational SQL) and Supabase (Cloud PostgreSQL).
Enforces Primary Keys, Foreign Keys, and Referential Integrity.
Includes realistic team colors and full batting/bowling statistics (4s, 6s).
"""

import sqlite3
import importlib
from typing import Optional, Dict, Any, List
from config import SQLITE_DB_PATH, DB_MODE, SUPABASE_URL, SUPABASE_KEY, is_supabase_configured
from seed_data import INITIAL_TEAMS, INITIAL_PLAYERS

# Supabase Client reference
_supabase_client = None


def get_supabase_client():
    """Initializes and returns the Supabase client if credentials are configured."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if is_supabase_configured():
        try:
            supabase_module = importlib.import_module("supabase")
            create_client = getattr(supabase_module, "create_client")
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            return _supabase_client
        except Exception as e:
            print(f"[Warning] Could not initialize Supabase client: {e}. Falling back to SQLite.")
            return None
    return None


def get_connection() -> sqlite3.Connection:
    """
    Returns an SQLite database connection.
    Enforces Foreign Key constraints and provides dictionary-like row access.
    """
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(force_reset: bool = False) -> None:
    """
    Initializes the relational database schema with Primary Keys and Foreign Keys,
    and seeds initial authentic IPL teams and players if empty.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if force_reset:
        cursor.execute("DROP TABLE IF EXISTS auction_bids;")
        cursor.execute("DROP TABLE IF EXISTS player_stats;")
        cursor.execute("DROP TABLE IF EXISTS players;")
        cursor.execute("DROP TABLE IF EXISTS teams;")
        conn.commit()

    # 1. TEAMS TABLE (Primary Key: team_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name TEXT NOT NULL UNIQUE,
        short_code TEXT NOT NULL UNIQUE,
        primary_color TEXT DEFAULT '#FDB913',
        secondary_color TEXT DEFAULT '#000000',
        total_budget REAL NOT NULL DEFAULT 1200000000.0,
        remaining_budget REAL NOT NULL DEFAULT 1200000000.0,
        retention_spend REAL NOT NULL DEFAULT 0.0,
        retentions_count INTEGER NOT NULL DEFAULT 0,
        rtm_cards INTEGER NOT NULL DEFAULT 0,
        retained_names TEXT DEFAULT '',
        min_squad_size INTEGER NOT NULL DEFAULT 18,
        max_squad_size INTEGER NOT NULL DEFAULT 25,
        max_overseas INTEGER NOT NULL DEFAULT 8
    );
    """)

    # 2. PLAYERS TABLE (Primary Key: player_id, Foreign Key: team_id -> teams.team_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        country TEXT NOT NULL DEFAULT 'India',
        base_price REAL NOT NULL,
        sold_price REAL DEFAULT 0.0,
        status TEXT NOT NULL DEFAULT 'Available',
        set_name TEXT DEFAULT 'Set 1: Capped Batters (BA1)',
        set_code TEXT DEFAULT 'BA1',
        is_capped INTEGER DEFAULT 1,
        is_overseas INTEGER DEFAULT 0,
        former_team TEXT DEFAULT NULL,
        is_shortlisted INTEGER DEFAULT 1,
        accelerated INTEGER DEFAULT 0,
        team_id INTEGER,
        FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
    );
    """)

    # 3. PLAYER STATS TABLE (Primary Key: stat_id, Foreign Key: player_id -> players.player_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_stats (
        stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL UNIQUE,
        matches INTEGER NOT NULL DEFAULT 0,
        runs INTEGER NOT NULL DEFAULT 0,
        highest_score INTEGER NOT NULL DEFAULT 0,
        batting_avg REAL NOT NULL DEFAULT 0.0,
        strike_rate REAL NOT NULL DEFAULT 0.0,
        fours INTEGER NOT NULL DEFAULT 0,
        sixes INTEGER NOT NULL DEFAULT 0,
        centuries INTEGER NOT NULL DEFAULT 0,
        fifties INTEGER NOT NULL DEFAULT 0,
        wickets INTEGER NOT NULL DEFAULT 0,
        bowling_economy REAL NOT NULL DEFAULT 0.0,
        bowling_avg REAL NOT NULL DEFAULT 0.0,
        FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
    );
    """)

    # 4. AUCTION BIDS TABLE (Primary Key: bid_id, Foreign Keys to players and teams)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auction_bids (
        bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        bid_amount REAL NOT NULL,
        bid_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
        FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
    );
    """)

    # 5. INDIVIDUAL TEAM TABLES (Dedicated squad databases for each franchise)
    team_codes = ["csk", "mi", "rcb", "kkr", "rr", "srh", "gt", "lsg", "dc", "pbks"]
    for code in team_codes:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {code}_players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL UNIQUE,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            country TEXT NOT NULL DEFAULT 'India',
            sold_price REAL NOT NULL,
            matches INTEGER DEFAULT 0,
            runs INTEGER DEFAULT 0,
            highest_score INTEGER DEFAULT 0,
            batting_avg REAL DEFAULT 0.0,
            strike_rate REAL DEFAULT 0.0,
            fours INTEGER DEFAULT 0,
            sixes INTEGER DEFAULT 0,
            wickets INTEGER DEFAULT 0,
            bowling_economy REAL DEFAULT 0.0,
            bowling_avg REAL DEFAULT 0.0,
            bought_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

    # Ensure columns exist for teams
    cursor.execute("PRAGMA table_info(teams);")
    existing_team_cols = [r[1] for r in cursor.fetchall()]
    if "retentions_count" not in existing_team_cols:
        cursor.execute("ALTER TABLE teams ADD COLUMN retentions_count INTEGER DEFAULT 0;")
    if "rtm_cards" not in existing_team_cols:
        cursor.execute("ALTER TABLE teams ADD COLUMN rtm_cards INTEGER DEFAULT 0;")
    if "retained_names" not in existing_team_cols:
        cursor.execute("ALTER TABLE teams ADD COLUMN retained_names TEXT DEFAULT '';")
    if "retention_spend" not in existing_team_cols:
        cursor.execute("ALTER TABLE teams ADD COLUMN retention_spend REAL DEFAULT 0.0;")
    if "min_squad_size" not in existing_team_cols:
        cursor.execute("ALTER TABLE teams ADD COLUMN min_squad_size INTEGER DEFAULT 18;")
    if "max_overseas" not in existing_team_cols:
        cursor.execute("ALTER TABLE teams ADD COLUMN max_overseas INTEGER DEFAULT 8;")

    # Ensure columns exist for players
    cursor.execute("PRAGMA table_info(players);")
    existing_player_cols = [r[1] for r in cursor.fetchall()]
    if "set_name" not in existing_player_cols:
        cursor.execute("ALTER TABLE players ADD COLUMN set_name TEXT DEFAULT 'Set 1: Capped Batters (BA1)';")
    if "set_code" not in existing_player_cols:
        cursor.execute("ALTER TABLE players ADD COLUMN set_code TEXT DEFAULT 'BA1';")
    if "is_capped" not in existing_player_cols:
        cursor.execute("ALTER TABLE players ADD COLUMN is_capped INTEGER DEFAULT 1;")
    if "is_overseas" not in existing_player_cols:
        cursor.execute("ALTER TABLE players ADD COLUMN is_overseas INTEGER DEFAULT 0;")
    if "former_team" not in existing_player_cols:
        cursor.execute("ALTER TABLE players ADD COLUMN former_team TEXT DEFAULT NULL;")
    if "is_shortlisted" not in existing_player_cols:
        cursor.execute("ALTER TABLE players ADD COLUMN is_shortlisted INTEGER DEFAULT 1;")
    if "accelerated" not in existing_player_cols:
        cursor.execute("ALTER TABLE players ADD COLUMN accelerated INTEGER DEFAULT 0;")

    conn.commit()

    # Seed initial data if tables are empty or need update
    _seed_initial_data(conn)
    conn.close()


def _seed_initial_data(conn: sqlite3.Connection) -> None:
    """Populates initial teams and authentic IPL players if not already present."""
    cursor = conn.cursor()

    # Check if teams exist
    cursor.execute("SELECT COUNT(*) FROM teams;")
    team_count = cursor.fetchone()[0]

    if team_count == 0:
        for team in INITIAL_TEAMS:
            cursor.execute("""
            INSERT INTO teams (
                team_name, short_code, primary_color, secondary_color,
                total_budget, remaining_budget, retention_spend, retentions_count,
                rtm_cards, retained_names, min_squad_size, max_squad_size, max_overseas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                team["team_name"],
                team["short_code"],
                team.get("primary_color", "#FDB913"),
                team.get("secondary_color", "#000000"),
                team["total_budget"],
                team["remaining_budget"],
                team.get("retention_spend", 0.0),
                team.get("retentions_count", 0),
                team.get("rtm_cards", 0),
                team.get("retained_names", ""),
                team.get("min_squad_size", 18),
                team.get("max_squad_size", 25),
                team.get("max_overseas", 8)
            ))
        conn.commit()
    else:
        # Update teams with authentic retentions & RTM values
        for team in INITIAL_TEAMS:
            cursor.execute("""
            UPDATE teams SET
                retention_spend = ?,
                retentions_count = ?,
                rtm_cards = ?,
                retained_names = ?,
                min_squad_size = ?,
                max_squad_size = ?,
                max_overseas = ?
            WHERE short_code = ?;
            """, (
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

    # Seed / synchronize players and stats
    cursor.execute("SELECT name FROM players;")
    existing_player_names = {r[0] for r in cursor.fetchall()}

    for p in INITIAL_PLAYERS:
        name = p["name"]
        is_os = 1 if p.get("country", "India") != "India" else 0
        is_cap = 1 if p.get("is_capped", True) else 0
        stats = p.get("stats", {})

        if name not in existing_player_names:
            cursor.execute("""
            INSERT INTO players (
                name, role, country, base_price, sold_price, status, team_id,
                set_name, set_code, is_capped, is_overseas, former_team, is_shortlisted, accelerated
            ) VALUES (?, ?, ?, ?, 0.0, 'Available', NULL, ?, ?, ?, ?, ?, 1, 0);
            """, (
                p["name"],
                p["role"],
                p["country"],
                p["base_price"],
                p.get("set_name", "Set 1: Capped Batters (BA1)"),
                p.get("set_code", "BA1"),
                is_cap,
                is_os,
                p.get("former_team"),
            ))
            player_id = cursor.lastrowid

            cursor.execute("""
            INSERT INTO player_stats (
                player_id, matches, runs, highest_score, batting_avg, strike_rate,
                fours, sixes, centuries, fifties, wickets, bowling_economy, bowling_avg
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                player_id,
                stats.get("matches", 0),
                stats.get("runs", 0),
                stats.get("highest_score", 0),
                stats.get("batting_avg", 0.0),
                stats.get("strike_rate", 0.0),
                stats.get("fours", 0),
                stats.get("sixes", 0),
                stats.get("centuries", 0),
                stats.get("fifties", 0),
                stats.get("wickets", 0),
                stats.get("bowling_economy", 0.0),
                stats.get("bowling_avg", 0.0)
            ))
        else:
            cursor.execute("""
            UPDATE players SET
                role = ?,
                country = ?,
                base_price = ?,
                set_name = ?,
                set_code = ?,
                is_capped = ?,
                is_overseas = ?,
                former_team = ?
            WHERE name = ?;
            """, (
                p["role"],
                p["country"],
                p["base_price"],
                p.get("set_name", "Set 1: Capped Batters (BA1)"),
                p.get("set_code", "BA1"),
                is_cap,
                is_os,
                p.get("former_team"),
                p["name"]
            ))
            cursor.execute("""
            UPDATE player_stats SET
                matches = ?, runs = ?, highest_score = ?, batting_avg = ?,
                strike_rate = ?, fours = ?, sixes = ?, centuries = ?,
                fifties = ?, wickets = ?, bowling_economy = ?, bowling_avg = ?
            WHERE player_id = (SELECT player_id FROM players WHERE name = ?);
            """, (
                stats.get("matches", 0),
                stats.get("runs", 0),
                stats.get("highest_score", 0),
                stats.get("batting_avg", 0.0),
                stats.get("strike_rate", 0.0),
                stats.get("fours", 0),
                stats.get("sixes", 0),
                stats.get("centuries", 0),
                stats.get("fifties", 0),
                stats.get("wickets", 0),
                stats.get("bowling_economy", 0.0),
                stats.get("bowling_avg", 0.0),
                p["name"]
            ))
    conn.commit()


def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Converts an SQLite row into a clean Python dictionary."""
    return dict(row) if row is not None else {}


def record_player_in_team_table(team_code: str, player_info: Dict[str, Any]) -> bool:
    """Inserts a sold player into the team's dedicated table in SQLite."""
    table_name = f"{team_code.strip().lower()}_players"
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
        INSERT OR REPLACE INTO {table_name} (
            player_id, name, role, country, sold_price, matches, runs,
            highest_score, batting_avg, strike_rate, fours, sixes,
            wickets, bowling_economy, bowling_avg
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            player_info["player_id"],
            player_info["name"],
            player_info.get("role", "Batsman"),
            player_info.get("country", "India"),
            player_info.get("sold_price", 0.0),
            player_info.get("matches", 0),
            player_info.get("runs", 0),
            player_info.get("highest_score", 0),
            player_info.get("batting_avg", 0.0),
            player_info.get("strike_rate", 0.0),
            player_info.get("fours", 0),
            player_info.get("sixes", 0),
            player_info.get("wickets", 0),
            player_info.get("bowling_economy", 0.0),
            player_info.get("bowling_avg", 0.0),
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Database Error] Could not insert into {table_name}: {e}")
        return False
    finally:
        conn.close()


def clear_all_team_tables() -> None:
    """Clears all records from every team's dedicated squad table."""
    conn = get_connection()
    cursor = conn.cursor()
    team_codes = ["csk", "mi", "rcb", "kkr", "rr", "srh", "gt", "lsg", "dc", "pbks"]
    for code in team_codes:
        cursor.execute(f"DELETE FROM {code}_players;")
    conn.commit()
    conn.close()


def remove_player_from_team_tables(player_id: int) -> None:
    """Removes a player from all team tables (e.g. upon delete or unsold)."""
    conn = get_connection()
    cursor = conn.cursor()
    team_codes = ["csk", "mi", "rcb", "kkr", "rr", "srh", "gt", "lsg", "dc", "pbks"]
    for code in team_codes:
        cursor.execute(f"DELETE FROM {code}_players WHERE player_id = ?;", (player_id,))
    conn.commit()
    conn.close()

