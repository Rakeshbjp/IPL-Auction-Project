"""
Script to generate production-ready supabase_schema.sql with:
- Relational core tables (teams, players, player_stats, auction_bids)
- Official IPL Mega Auction Rules: Retentions & RTM Formula (6 - retentions)
- Sequential Categorized Sets: BA1, AL1, WK1, FA1, SP1, UN1
- 10 Dedicated franchise squad tables (csk_players, mi_players, rcb_players, etc.)
- 10 Dynamic squad views (csk_squad, mi_squad, rcb_squad, etc.)
- Permissive Row Level Security Policies ("Public Full Access") for anon and service_role
- 10 Official Teams with ₹120 Cr budget and authentic retentions
- 49 Authentic IPL Star Players and their full statistics
"""

import sys
from seed_data import INITIAL_TEAMS, INITIAL_PLAYERS

TEAM_CODES = ["csk", "mi", "rcb", "kkr", "rr", "srh", "gt", "lsg", "dc", "pbks"]

lines = []
lines.append("-- ============================================================================")
lines.append("-- TATA IPL 2026 MEGA AUCTION - OFFICIAL REAL-TIME SUPABASE POSTGRESQL SCHEMA")
lines.append("-- Copy this ENTIRE file, paste into Supabase SQL Editor and click RUN")
lines.append("-- ============================================================================\n")

# 1. Clean Drop
lines.append("-- 1. Drop existing Views and Tables cleanly")
for code in TEAM_CODES:
    lines.append(f"DROP VIEW IF EXISTS {code}_squad CASCADE;")
lines.append("DROP VIEW IF EXISTS team_squads_overview CASCADE;")

for code in TEAM_CODES:
    lines.append(f"DROP TABLE IF EXISTS {code}_players CASCADE;")

lines.append("DROP TABLE IF EXISTS auction_bids CASCADE;")
lines.append("DROP TABLE IF EXISTS player_stats CASCADE;")
lines.append("DROP TABLE IF EXISTS players CASCADE;")
lines.append("DROP TABLE IF EXISTS teams CASCADE;\n")

# 2. Core Tables
lines.append("""-- 2. Create Core Relational Tables
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    short_code VARCHAR(10) NOT NULL UNIQUE,
    primary_color VARCHAR(20) DEFAULT '#FDB913',
    secondary_color VARCHAR(20) DEFAULT '#000000',
    total_budget NUMERIC(15, 2) NOT NULL DEFAULT 1200000000.00,
    remaining_budget NUMERIC(15, 2) NOT NULL DEFAULT 1200000000.00,
    retention_spend NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    retentions_count INT NOT NULL DEFAULT 0,
    rtm_cards INT NOT NULL DEFAULT 0,
    retained_names TEXT DEFAULT '',
    min_squad_size INT NOT NULL DEFAULT 18,
    max_squad_size INT NOT NULL DEFAULT 25,
    max_overseas INT NOT NULL DEFAULT 8
);

CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'India',
    base_price NUMERIC(15, 2) NOT NULL,
    sold_price NUMERIC(15, 2) DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'Available',
    set_name VARCHAR(100) DEFAULT 'Set 1: Capped Batters (BA1)',
    set_code VARCHAR(10) DEFAULT 'BA1',
    is_capped INT DEFAULT 1,
    is_overseas INT DEFAULT 0,
    former_team VARCHAR(10) DEFAULT NULL,
    is_shortlisted INT DEFAULT 1,
    accelerated INT DEFAULT 0,
    team_id INT REFERENCES teams(team_id) ON DELETE SET NULL
);

CREATE TABLE player_stats (
    stat_id SERIAL PRIMARY KEY,
    player_id INT NOT NULL UNIQUE REFERENCES players(player_id) ON DELETE CASCADE,
    matches INT NOT NULL DEFAULT 0,
    runs INT NOT NULL DEFAULT 0,
    highest_score INT NOT NULL DEFAULT 0,
    batting_avg NUMERIC(6, 2) NOT NULL DEFAULT 0.00,
    strike_rate NUMERIC(6, 2) NOT NULL DEFAULT 0.00,
    fours INT NOT NULL DEFAULT 0,
    sixes INT NOT NULL DEFAULT 0,
    centuries INT NOT NULL DEFAULT 0,
    fifties INT NOT NULL DEFAULT 0,
    wickets INT NOT NULL DEFAULT 0,
    bowling_economy NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    bowling_avg NUMERIC(6, 2) NOT NULL DEFAULT 0.00
);

CREATE TABLE auction_bids (
    bid_id SERIAL PRIMARY KEY,
    player_id INT NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    team_id INT NOT NULL REFERENCES teams(team_id) ON DELETE CASCADE,
    bid_amount NUMERIC(15, 2) NOT NULL,
    bid_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# 3. 10 Dedicated Franchise Squad Tables
lines.append("-- 3. Create 10 Dedicated Franchise Squad Tables (Stored by Team Name)")
for code in TEAM_CODES:
    lines.append(f"""CREATE TABLE {code}_players (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'India',
    sold_price NUMERIC(15, 2) NOT NULL,
    matches INT DEFAULT 0,
    runs INT DEFAULT 0,
    highest_score INT DEFAULT 0,
    batting_avg NUMERIC(6, 2) DEFAULT 0.00,
    strike_rate NUMERIC(6, 2) DEFAULT 0.00,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    wickets INT DEFAULT 0,
    bowling_economy NUMERIC(5, 2) DEFAULT 0.00,
    bowling_avg NUMERIC(6, 2) DEFAULT 0.00,
    bought_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")

lines.append("")

# 4. Explicit Row-Level Security Policies for Full Anon Access
lines.append("""-- 4. Enable RLS and Create Open Permissive Policies so PostgREST allows full read/write access
DO $$
DECLARE
    t text;
BEGIN
    FOR t IN 
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY;', t);
        EXECUTE format('DROP POLICY IF EXISTS "Public Full Access" ON public.%I;', t);
        EXECUTE format('CREATE POLICY "Public Full Access" ON public.%I FOR ALL TO public USING (true) WITH CHECK (true);', t);
        EXECUTE format('GRANT ALL ON public.%I TO anon, authenticated, service_role;', t);
    END LOOP;
END $$;

GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated, service_role;
""")

# 5. Dynamic Views for Franchise Squads
lines.append("-- 5. Dynamic Views for Franchise Squads")
for code in TEAM_CODES:
    lines.append(f"""CREATE OR REPLACE VIEW {code}_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = '{code.upper()}';""")

lines.append("")

# 6. Seed 10 Teams
lines.append("-- 6. Seed 10 Real IPL Franchises with Official Purses, Retentions & RTM allocations")
lines.append("INSERT INTO teams (team_id, team_name, short_code, primary_color, secondary_color, total_budget, remaining_budget, retention_spend, retentions_count, rtm_cards, retained_names, min_squad_size, max_squad_size, max_overseas) VALUES")
team_vals = []
for idx, t in enumerate(INITIAL_TEAMS, start=1):
    safe_retained = t.get("retained_names", "").replace("'", "''")
    val = f"({idx}, '{t['team_name']}', '{t['short_code']}', '{t['primary_color']}', '{t['secondary_color']}', {t['total_budget']:.2f}, {t['remaining_budget']:.2f}, {t.get('retention_spend', 0.0):.2f}, {t.get('retentions_count', 0)}, {t.get('rtm_cards', 0)}, '{safe_retained}', {t.get('min_squad_size', 18)}, {t.get('max_squad_size', 25)}, {t.get('max_overseas', 8)})"
    team_vals.append(val)
lines.append(",\n".join(team_vals) + ";\n")

# 7. Seed Players
lines.append("-- 7. Seed Real IPL Players organized into Sequential Sets with Former Team RTM mapping")
lines.append("INSERT INTO players (player_id, name, role, country, base_price, sold_price, status, set_name, set_code, is_capped, is_overseas, former_team, is_shortlisted, accelerated, team_id) VALUES")
player_vals = []
for idx, p in enumerate(INITIAL_PLAYERS, start=1):
    safe_name = p['name'].replace("'", "''")
    is_os = 1 if p.get('country', 'India') != 'India' else 0
    is_cap = 1 if p.get('is_capped', True) else 0
    former = f"'{p.get('former_team')}'" if p.get('former_team') else "NULL"
    val = f"({idx}, '{safe_name}', '{p['role']}', '{p['country']}', {p['base_price']:.2f}, 0.00, 'Available', '{p.get('set_name', 'Set 1: Capped Batters (BA1)')}', '{p.get('set_code', 'BA1')}', {is_cap}, {is_os}, {former}, 1, 0, NULL)"
    player_vals.append(val)
lines.append(",\n".join(player_vals) + ";\n")

# 8. Seed Player Stats
lines.append("-- 8. Seed Player Career Statistics")
lines.append("INSERT INTO player_stats (stat_id, player_id, matches, runs, highest_score, batting_avg, strike_rate, fours, sixes, centuries, fifties, wickets, bowling_economy, bowling_avg) VALUES")
stats_vals = []
for idx, p in enumerate(INITIAL_PLAYERS, start=1):
    s = p['stats']
    val = f"({idx}, {idx}, {s.get('matches', 0)}, {s.get('runs', 0)}, {s.get('highest_score', 0)}, {s.get('batting_avg', 0.0):.2f}, {s.get('strike_rate', 0.0):.2f}, {s.get('fours', 0)}, {s.get('sixes', 0)}, {s.get('centuries', 0)}, {s.get('fifties', 0)}, {s.get('wickets', 0)}, {s.get('bowling_economy', 0.0):.2f}, {s.get('bowling_avg', 0.0):.2f})"
    stats_vals.append(val)
lines.append(",\n".join(stats_vals) + ";\n")

# 9. Sequence resets
lines.append("""-- 9. Reset PostgreSQL ID Sequences so future user inserts continue smoothly
SELECT setval('teams_team_id_seq', (SELECT MAX(team_id) FROM teams));
SELECT setval('players_player_id_seq', (SELECT MAX(player_id) FROM players));
SELECT setval('player_stats_stat_id_seq', (SELECT MAX(stat_id) FROM player_stats));
SELECT setval('auction_bids_bid_id_seq', COALESCE((SELECT MAX(bid_id) FROM auction_bids), 1));
""")

with open("supabase_schema.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Successfully written updated supabase_schema.sql!")
