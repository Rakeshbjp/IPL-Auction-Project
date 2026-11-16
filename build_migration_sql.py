"""
Build non-destructive migration SQL script for Supabase
"""
from seed_data import INITIAL_TEAMS, INITIAL_PLAYERS

lines = []
lines.append("-- ============================================================================")
lines.append("-- TATA IPL 2026 - NON-DESTRUCTIVE SUPABASE SCHEMA UPDATE")
lines.append("-- Run this in Supabase SQL Editor to add new columns and populate RTM data!")
lines.append("-- ============================================================================\n")

# 1. Alter tables
lines.append("-- 1. Add missing columns to teams and players")
lines.append("ALTER TABLE teams ADD COLUMN IF NOT EXISTS retention_spend NUMERIC(15, 2) NOT NULL DEFAULT 0.00;")
lines.append("ALTER TABLE teams ADD COLUMN IF NOT EXISTS retentions_count INT NOT NULL DEFAULT 0;")
lines.append("ALTER TABLE teams ADD COLUMN IF NOT EXISTS rtm_cards INT NOT NULL DEFAULT 0;")
lines.append("ALTER TABLE teams ADD COLUMN IF NOT EXISTS retained_names TEXT DEFAULT '';")
lines.append("ALTER TABLE teams ADD COLUMN IF NOT EXISTS min_squad_size INT NOT NULL DEFAULT 18;")
lines.append("ALTER TABLE teams ADD COLUMN IF NOT EXISTS max_overseas INT NOT NULL DEFAULT 8;\n")

lines.append("ALTER TABLE players ADD COLUMN IF NOT EXISTS set_name VARCHAR(100) DEFAULT 'Set 1: Capped Batters (BA1)';")
lines.append("ALTER TABLE players ADD COLUMN IF NOT EXISTS set_code VARCHAR(10) DEFAULT 'BA1';")
lines.append("ALTER TABLE players ADD COLUMN IF NOT EXISTS is_capped INT DEFAULT 1;")
lines.append("ALTER TABLE players ADD COLUMN IF NOT EXISTS is_overseas INT DEFAULT 0;")
lines.append("ALTER TABLE players ADD COLUMN IF NOT EXISTS former_team VARCHAR(10) DEFAULT NULL;")
lines.append("ALTER TABLE players ADD COLUMN IF NOT EXISTS is_shortlisted INT DEFAULT 1;")
lines.append("ALTER TABLE players ADD COLUMN IF NOT EXISTS accelerated INT DEFAULT 0;\n")

# 2. Update teams
lines.append("-- 2. Update teams with official retentions and RTM cards")
for t in INITIAL_TEAMS:
    ret_names = t.get('retained_names', '').replace("'", "''")
    lines.append(f"""UPDATE teams SET 
    retention_spend = {t.get('retention_spend', 0.0)},
    retentions_count = {t.get('retentions_count', 0)},
    rtm_cards = {t.get('rtm_cards', 0)},
    retained_names = '{ret_names}',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = '{t['short_code']}';""")

# 3. Update players
lines.append("\n-- 3. Update players with sets, capped, overseas and former teams")
for p in INITIAL_PLAYERS:
    p_name = p['name'].replace("'", "''")
    set_name = p.get('set_name', 'Set 1: Capped Batters (BA1)').replace("'", "''")
    set_code = p.get('set_code', 'BA1')
    is_capped = 1 if p.get('is_capped', True) else 0
    is_overseas = 1 if p.get('is_overseas', False) else 0
    former = f"'{p.get('former_team')}'" if p.get('former_team') else 'NULL'
    lines.append(f"""UPDATE players SET
    set_name = '{set_name}',
    set_code = '{set_code}',
    is_capped = {is_capped},
    is_overseas = {is_overseas},
    former_team = {former}
WHERE name = '{p_name}';""")

# 4. Create team squad tables if not exist
lines.append("\n-- 4. Create 10 dedicated franchise squad tables if not exist")
TEAM_CODES = ['csk', 'mi', 'rcb', 'kkr', 'rr', 'srh', 'gt', 'lsg', 'dc', 'pbks']
for code in TEAM_CODES:
    lines.append(f"""CREATE TABLE IF NOT EXISTS {code}_players (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
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

with open('update_supabase_columns.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Created update_supabase_columns.sql successfully!')
