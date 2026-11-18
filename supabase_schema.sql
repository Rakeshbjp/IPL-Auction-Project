-- ============================================================================
-- TATA IPL 2026 MEGA AUCTION - OFFICIAL REAL-TIME SUPABASE POSTGRESQL SCHEMA
-- Copy this ENTIRE file, paste into Supabase SQL Editor and click RUN
-- ============================================================================

-- 1. Drop existing Views and Tables cleanly
DROP VIEW IF EXISTS csk_squad CASCADE;
DROP VIEW IF EXISTS mi_squad CASCADE;
DROP VIEW IF EXISTS rcb_squad CASCADE;
DROP VIEW IF EXISTS kkr_squad CASCADE;
DROP VIEW IF EXISTS rr_squad CASCADE;
DROP VIEW IF EXISTS srh_squad CASCADE;
DROP VIEW IF EXISTS gt_squad CASCADE;
DROP VIEW IF EXISTS lsg_squad CASCADE;
DROP VIEW IF EXISTS dc_squad CASCADE;
DROP VIEW IF EXISTS pbks_squad CASCADE;
DROP VIEW IF EXISTS team_squads_overview CASCADE;
DROP TABLE IF EXISTS csk_players CASCADE;
DROP TABLE IF EXISTS mi_players CASCADE;
DROP TABLE IF EXISTS rcb_players CASCADE;
DROP TABLE IF EXISTS kkr_players CASCADE;
DROP TABLE IF EXISTS rr_players CASCADE;
DROP TABLE IF EXISTS srh_players CASCADE;
DROP TABLE IF EXISTS gt_players CASCADE;
DROP TABLE IF EXISTS lsg_players CASCADE;
DROP TABLE IF EXISTS dc_players CASCADE;
DROP TABLE IF EXISTS pbks_players CASCADE;
DROP TABLE IF EXISTS auction_bids CASCADE;
DROP TABLE IF EXISTS player_stats CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS teams CASCADE;

-- 2. Create Core Relational Tables
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

-- 3. Create 10 Dedicated Franchise Squad Tables (Stored by Team Name)
CREATE TABLE csk_players (
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
);
CREATE TABLE mi_players (
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
);
CREATE TABLE rcb_players (
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
);
CREATE TABLE kkr_players (
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
);
CREATE TABLE rr_players (
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
);
CREATE TABLE srh_players (
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
);
CREATE TABLE gt_players (
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
);
CREATE TABLE lsg_players (
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
);
CREATE TABLE dc_players (
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
);
CREATE TABLE pbks_players (
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
);

-- 4. Enable RLS and Create Open Permissive Policies so PostgREST allows full read/write access
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

-- 5. Dynamic Views for Franchise Squads
CREATE OR REPLACE VIEW csk_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'CSK';
CREATE OR REPLACE VIEW mi_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'MI';
CREATE OR REPLACE VIEW rcb_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'RCB';
CREATE OR REPLACE VIEW kkr_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'KKR';
CREATE OR REPLACE VIEW rr_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'RR';
CREATE OR REPLACE VIEW srh_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'SRH';
CREATE OR REPLACE VIEW gt_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'GT';
CREATE OR REPLACE VIEW lsg_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'LSG';
CREATE OR REPLACE VIEW dc_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'DC';
CREATE OR REPLACE VIEW pbks_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price, p.set_name, p.former_team,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'PBKS';

-- 6. Seed 10 Real IPL Franchises with Official Purses, Retentions & RTM allocations
INSERT INTO teams (team_id, team_name, short_code, primary_color, secondary_color, total_budget, remaining_budget, retention_spend, retentions_count, rtm_cards, retained_names, min_squad_size, max_squad_size, max_overseas) VALUES
(1, 'Chennai Super Kings', 'CSK', '#FDB913', '#0081E8', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(2, 'Mumbai Indians', 'MI', '#004BA0', '#D1AB3E', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(3, 'Royal Challengers Bengaluru', 'RCB', '#EC1C24', '#2B2A29', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(4, 'Kolkata Knight Riders', 'KKR', '#3A225D', '#F7D54E', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(5, 'Rajasthan Royals', 'RR', '#EA1A85', '#254AA5', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(6, 'Sunrisers Hyderabad', 'SRH', '#F26522', '#000000', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(7, 'Gujarat Titans', 'GT', '#1C1C1C', '#0B4973', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(8, 'Lucknow Super Giants', 'LSG', '#A72056', '#0055A5', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(9, 'Delhi Capitals', 'DC', '#004C93', '#E41B17', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8),
(10, 'Punjab Kings', 'PBKS', '#DD1F2D', '#C3A25D', 1200000000.00, 1200000000.00, 0.00, 0, 6, '', 18, 25, 8);

-- 7. Seed Real IPL Players organized into Sequential Sets with Former Team RTM mapping
INSERT INTO players (player_id, name, role, country, base_price, sold_price, status, set_name, set_code, is_capped, is_overseas, former_team, is_shortlisted, accelerated, team_id) VALUES
(1, 'Virat Kohli', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'RCB', 1, 0, NULL),
(2, 'Rohit Sharma', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'MI', 1, 0, NULL),
(3, 'Shikhar Dhawan', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'PBKS', 1, 0, NULL),
(4, 'David Warner', 'Batsman', 'Australia', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, 'DC', 1, 0, NULL),
(5, 'MS Dhoni', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 0, 'CSK', 1, 0, NULL),
(6, 'KL Rahul', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 0, 'LSG', 1, 0, NULL),
(7, 'Ajinkya Rahane', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'CSK', 1, 0, NULL),
(8, 'Suryakumar Yadav', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'MI', 1, 0, NULL),
(9, 'Sanju Samson', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 0, 'RR', 1, 0, NULL),
(10, 'Faf du Plessis', 'Batsman', 'South Africa', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, 'RCB', 1, 0, NULL),
(11, 'Jos Buttler', 'Wicketkeeper', 'England', 20000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, 'RR', 1, 0, NULL),
(12, 'Manish Pandey', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, NULL, 1, 0, NULL),
(13, 'Shubman Gill', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'GT', 1, 0, NULL),
(14, 'Shreyas Iyer', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'KKR', 1, 0, NULL),
(15, 'Rishabh Pant', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 0, 'DC', 1, 0, NULL),
(16, 'Quinton de Kock', 'Wicketkeeper', 'South Africa', 20000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, 'LSG', 1, 0, NULL),
(17, 'Ravindra Jadeja', 'Allrounder', 'India', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'CSK', 1, 0, NULL),
(18, 'David Miller', 'Batsman', 'South Africa', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, 'GT', 1, 0, NULL),
(19, 'Glenn Maxwell', 'Allrounder', 'Australia', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'RCB', 1, 0, NULL),
(20, 'Hardik Pandya', 'Allrounder', 'India', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'MI', 1, 0, NULL),
(21, 'Ruturaj Gaikwad', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'CSK', 1, 0, NULL),
(22, 'Andre Russell', 'Allrounder', 'West Indies', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'KKR', 1, 0, NULL),
(23, 'Nicholas Pooran', 'Wicketkeeper', 'West Indies', 20000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, 'LSG', 1, 0, NULL),
(24, 'Yashasvi Jaiswal', 'Batsman', 'India', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'RR', 1, 0, NULL),
(25, 'Axar Patel', 'Allrounder', 'India', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'DC', 1, 0, NULL),
(26, 'Sunil Narine', 'Allrounder', 'West Indies', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'KKR', 1, 0, NULL),
(27, 'Heinrich Klaasen', 'Wicketkeeper', 'South Africa', 20000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, 'SRH', 1, 0, NULL),
(28, 'Travis Head', 'Batsman', 'Australia', 20000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, 'SRH', 1, 0, NULL),
(29, 'Liam Livingstone', 'Allrounder', 'England', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'PBKS', 1, 0, NULL),
(30, 'Sam Curran', 'Allrounder', 'England', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'PBKS', 1, 0, NULL),
(31, 'Pat Cummins', 'Bowler', 'Australia', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, 'SRH', 1, 0, NULL),
(32, 'Rashid Khan', 'Bowler', 'Afghanistan', 20000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 1, 'GT', 1, 0, NULL),
(33, 'Shardul Thakur', 'Allrounder', 'India', 20000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'CSK', 1, 0, NULL),
(34, 'Bhuvneshwar Kumar', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'SRH', 1, 0, NULL),
(35, 'Harshal Patel', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'PBKS', 1, 0, NULL),
(36, 'Kagiso Rabada', 'Bowler', 'South Africa', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, 'PBKS', 1, 0, NULL),
(37, 'Kuldeep Yadav', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 0, 'DC', 1, 0, NULL),
(38, 'Jaydev Unadkat', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, NULL, 1, 0, NULL),
(39, 'Mohammed Siraj', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'RCB', 1, 0, NULL),
(40, 'Mitchell Starc', 'Bowler', 'Australia', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, 'KKR', 1, 0, NULL),
(41, 'Trent Boult', 'Bowler', 'New Zealand', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, 'RR', 1, 0, NULL),
(42, 'Mohammed Shami', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'GT', 1, 0, NULL),
(43, 'Jasprit Bumrah', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'MI', 1, 0, NULL),
(44, 'Sandeep Sharma', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'RR', 1, 0, NULL),
(45, 'Yuzvendra Chahal', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 0, 'RR', 1, 0, NULL),
(46, 'Arshdeep Singh', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'PBKS', 1, 0, NULL),
(47, 'Varun Chakaravarthy', 'Bowler', 'India', 20000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 0, 'KKR', 1, 0, NULL),
(48, 'Ishan Kishan', 'Wicketkeeper', 'India', 15000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 0, 'MI', 1, 0, NULL),
(49, 'Nitish Rana', 'Allrounder', 'India', 15000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'KKR', 1, 0, NULL),
(50, 'Rahul Tripathi', 'Batsman', 'India', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'SRH', 1, 0, NULL),
(51, 'Marcus Stoinis', 'Allrounder', 'Australia', 15000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'LSG', 1, 0, NULL),
(52, 'Prithvi Shaw', 'Batsman', 'India', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'DC', 1, 0, NULL),
(53, 'Shivam Dube', 'Allrounder', 'India', 15000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'CSK', 1, 0, NULL),
(54, 'Abhishek Sharma', 'Allrounder', 'India', 15000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'SRH', 1, 0, NULL),
(55, 'Devdutt Padikkal', 'Batsman', 'India', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, NULL, 1, 0, NULL),
(56, 'Sai Sudharsan', 'Batsman', 'India', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'GT', 1, 0, NULL),
(57, 'Krunal Pandya', 'Allrounder', 'India', 15000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'LSG', 1, 0, NULL),
(58, 'Karun Nair', 'Batsman', 'India', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, NULL, 1, 0, NULL),
(59, 'Riyan Parag', 'Allrounder', 'India', 15000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'RR', 1, 0, NULL),
(60, 'Tilak Varma', 'Batsman', 'India', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'MI', 1, 0, NULL),
(61, 'Rajat Patidar', 'Batsman', 'India', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'RCB', 1, 0, NULL),
(62, 'Rinku Singh', 'Batsman', 'India', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, 'KKR', 1, 0, NULL),
(63, 'Phil Salt', 'Wicketkeeper', 'England', 15000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, 'KKR', 1, 0, NULL),
(64, 'Jitesh Sharma', 'Wicketkeeper', 'India', 15000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 0, 'PBKS', 1, 0, NULL),
(65, 'Tristan Stubbs', 'Batsman', 'South Africa', 15000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, 'DC', 1, 0, NULL),
(66, 'Jofra Archer', 'Bowler', 'England', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(67, 'Shreyas Gopal', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 0, NULL, 1, 0, NULL),
(68, 'Marco Jansen', 'Allrounder', 'South Africa', 15000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(69, 'Rahul Chahar', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 0, 'PBKS', 1, 0, NULL),
(70, 'Deepak Chahar', 'Allrounder', 'India', 15000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'CSK', 1, 0, NULL),
(71, 'Lockie Ferguson', 'Bowler', 'New Zealand', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(72, 'Avesh Khan', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'RR', 1, 0, NULL),
(73, 'Ishant Sharma', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'DC', 1, 0, NULL),
(74, 'Anrich Nortje', 'Bowler', 'South Africa', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, 'DC', 1, 0, NULL),
(75, 'Ravi Bishnoi', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 0, 'LSG', 1, 0, NULL),
(76, 'Tushar Deshpande', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'CSK', 1, 0, NULL),
(77, 'Josh Hazlewood', 'Bowler', 'Australia', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(78, 'Mukesh Kumar', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'DC', 1, 0, NULL),
(79, 'Prasidh Krishna', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'RR', 1, 0, NULL),
(80, 'T. Natarajan', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'SRH', 1, 0, NULL),
(81, 'Khaleel Ahmed', 'Bowler', 'India', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'DC', 1, 0, NULL),
(82, 'Matheesha Pathirana', 'Bowler', 'Sri Lanka', 15000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, 'CSK', 1, 0, NULL),
(83, 'Shimron Hetmyer', 'Batsman', 'West Indies', 10000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, 'RR', 1, 0, NULL),
(84, 'Venkatesh Iyer', 'Allrounder', 'India', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'KKR', 1, 0, NULL),
(85, 'Aiden Markram', 'Batsman', 'South Africa', 10000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, NULL, 1, 0, NULL),
(86, 'Mitchell Marsh', 'Allrounder', 'Australia', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'DC', 1, 0, NULL),
(87, 'Rahul Tewatia', 'Allrounder', 'India', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'GT', 1, 0, NULL),
(88, 'Tim David', 'Batsman', 'Australia', 10000000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, 'MI', 1, 0, NULL),
(89, 'Cameron Green', 'Allrounder', 'Australia', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'RCB', 1, 0, NULL),
(90, 'Dhruv Jurel', 'Wicketkeeper', 'India', 10000000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 0, 'RR', 1, 0, NULL),
(91, 'Washington Sundar', 'Allrounder', 'India', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'SRH', 1, 0, NULL),
(92, 'Nitish Kumar Reddy', 'Allrounder', 'India', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, 'SRH', 1, 0, NULL),
(93, 'Will Jacks', 'Allrounder', 'England', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, 'RCB', 1, 0, NULL),
(94, 'Jason Holder', 'Allrounder', 'West Indies', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(95, 'Mitchell Santner', 'Allrounder', 'New Zealand', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(96, 'Wanindu Hasaranga', 'Allrounder', 'Sri Lanka', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(97, 'Glenn Phillips', 'Allrounder', 'New Zealand', 10000000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(98, 'Shivam Mavi', 'Bowler', 'India', 10000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, NULL, 1, 0, NULL),
(99, 'Mayank Markande', 'Bowler', 'India', 10000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 0, NULL, 1, 0, NULL),
(100, 'Noor Ahmad', 'Bowler', 'Afghanistan', 10000000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 1, 'GT', 1, 0, NULL),
(101, 'Nathan Ellis', 'Bowler', 'Australia', 10000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(102, 'Sai Kishore', 'Bowler', 'India', 10000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'GT', 1, 0, NULL),
(103, 'Yash Dayal', 'Bowler', 'India', 10000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'RCB', 1, 0, NULL),
(104, 'Lungisani Ngidi', 'Bowler', 'South Africa', 10000000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(105, 'Shahbaz Ahamad', 'Allrounder', 'India', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, NULL, 1, 0, NULL),
(106, 'Dewald Brevis', 'Batsman', 'South Africa', 7500000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, NULL, 1, 0, NULL),
(107, 'Sarfaraz Khan', 'Batsman', 'India', 7500000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 0, NULL, 1, 0, NULL),
(108, 'Rachin Ravindra', 'Allrounder', 'New Zealand', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(109, 'Sherfane Rutherford', 'Batsman', 'West Indies', 7500000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, NULL, 1, 0, NULL),
(110, 'Ryan Rickelton', 'Wicketkeeper', 'South Africa', 7500000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, NULL, 1, 0, NULL),
(111, 'Rovman Powell', 'Allrounder', 'West Indies', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(112, 'Josh Inglis', 'Wicketkeeper', 'Australia', 7500000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, NULL, 1, 0, NULL),
(113, 'Romario Shepherd', 'Allrounder', 'West Indies', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(114, 'Azmatullah Omarzai', 'Allrounder', 'Afghanistan', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(115, 'Kamindu Mendis', 'Allrounder', 'Sri Lanka', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(116, 'Jacob Bethell', 'Allrounder', 'England', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(117, 'Kyle Jamieson', 'Bowler', 'New Zealand', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(118, 'Dushmantha Chameera', 'Bowler', 'Sri Lanka', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(119, 'Corbin Bosch', 'Allrounder', 'South Africa', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(120, 'Jayant Yadav', 'Allrounder', 'India', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 0, NULL, 1, 0, NULL),
(121, 'Tim Seifert', 'Wicketkeeper', 'New Zealand', 7500000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, NULL, 1, 0, NULL),
(122, 'Adam Milne', 'Bowler', 'New Zealand', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(123, 'Umran Malik', 'Bowler', 'India', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'SRH', 1, 0, NULL),
(124, 'Tom Banton', 'Wicketkeeper', 'England', 7500000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, NULL, 1, 0, NULL),
(125, 'Jamie Overton', 'Allrounder', 'England', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(126, 'Vyshak Vijaykumar', 'Bowler', 'India', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, NULL, 1, 0, NULL),
(127, 'Matthew Breetzke', 'Batsman', 'South Africa', 7500000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, NULL, 1, 0, NULL),
(128, 'Xavier Bartlett', 'Bowler', 'Australia', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(129, 'Donovan Ferreira', 'Wicketkeeper', 'South Africa', 7500000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, NULL, 1, 0, NULL),
(130, 'Luke Wood', 'Bowler', 'England', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(131, 'Kwena Maphaka', 'Bowler', 'South Africa', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(132, 'Mukesh Choudhary', 'Bowler', 'India', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 0, 'CSK', 1, 0, NULL),
(133, 'Eshan Malinga', 'Bowler', 'Sri Lanka', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(134, 'Nuwan Thushara', 'Bowler', 'Sri Lanka', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(135, 'Nandre Burger', 'Bowler', 'South Africa', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(136, 'Matt Henry', 'Bowler', 'New Zealand', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(137, 'Akeal Hosein', 'Bowler', 'West Indies', 7500000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 1, NULL, 1, 0, NULL),
(138, 'Allah Ghazanfar', 'Bowler', 'Afghanistan', 7500000.00, 0.00, 'Available', 'Set 5: Capped Spinners (SP1)', 'SP1', 1, 1, NULL, 1, 0, NULL),
(139, 'Ben Duckett', 'Batsman', 'England', 7500000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, NULL, 1, 0, NULL),
(140, 'Ben Dwarshuis', 'Bowler', 'Australia', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(141, 'Blessing Muzarabani', 'Bowler', 'Zimbabwe', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(142, 'Brydon Carse', 'Bowler', 'England', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(143, 'Cooper Connolly', 'Allrounder', 'Australia', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(144, 'Finn Allen', 'Wicketkeeper', 'New Zealand', 7500000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, NULL, 1, 0, NULL),
(145, 'Jack Edwards', 'Allrounder', 'Australia', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(146, 'Jacob Duffy', 'Bowler', 'New Zealand', 7500000.00, 0.00, 'Available', 'Set 4: Capped Fast Bowlers (FA1)', 'FA1', 1, 1, NULL, 1, 0, NULL),
(147, 'Jordan Cox', 'Wicketkeeper', 'England', 7500000.00, 0.00, 'Available', 'Set 3: Capped Wicketkeepers (WK1)', 'WK1', 1, 1, NULL, 1, 0, NULL),
(148, 'Lhuan-dre Pretorius', 'Batsman', 'South Africa', 7500000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, NULL, 1, 0, NULL),
(149, 'Matt Short', 'Allrounder', 'Australia', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(150, 'Mitch Owen', 'Allrounder', 'Australia', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(151, 'Pathum Nissanka', 'Batsman', 'Sri Lanka', 7500000.00, 0.00, 'Available', 'Set 1: Capped Batters (BA1)', 'BA1', 1, 1, NULL, 1, 0, NULL),
(152, 'Zak Foulkes', 'Allrounder', 'New Zealand', 7500000.00, 0.00, 'Available', 'Set 2: Capped All-rounders (AL1)', 'AL1', 1, 1, NULL, 1, 0, NULL),
(153, 'Prabhsimran Singh', 'Wicketkeeper', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'PBKS', 1, 0, NULL),
(154, 'Ayush Badoni', 'Allrounder', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'LSG', 1, 0, NULL),
(155, 'Shashank Singh', 'Batsman', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'PBKS', 1, 0, NULL),
(156, 'Abdul Samad', 'Allrounder', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'SRH', 1, 0, NULL),
(157, 'Shahrukh Khan', 'Allrounder', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'GT', 1, 0, NULL),
(158, 'Nehal Wadhera', 'Batsman', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'MI', 1, 0, NULL),
(159, 'Abishek Porel', 'Wicketkeeper', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'DC', 1, 0, NULL),
(160, 'Priyansh Arya', 'Batsman', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(161, 'Angkrish Raghuvanshi', 'Batsman', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(162, 'Harpreet Brar', 'Allrounder', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'PBKS', 1, 0, NULL),
(163, 'Harshit Rana', 'Bowler', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'KKR', 1, 0, NULL),
(164, 'Mohsin Khan', 'Bowler', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'LSG', 1, 0, NULL),
(165, 'Vaibhav Arora', 'Bowler', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'KKR', 1, 0, NULL),
(166, 'Yash Thakur', 'Bowler', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'LSG', 1, 0, NULL),
(167, 'Suyash Sharma', 'Bowler', 'India', 5000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(168, 'Ashutosh Sharma', 'Batsman', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'PBKS', 1, 0, NULL),
(169, 'Naman Dhir', 'Allrounder', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'MI', 1, 0, NULL),
(170, 'Anuj Rawat', 'Wicketkeeper', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'RCB', 1, 0, NULL),
(171, 'Vaibhav Suryavanshi', 'Batsman', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(172, 'Ayush Mhatre', 'Batsman', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(173, 'Aniket Verma', 'Batsman', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(174, 'Ramandeep Singh', 'Allrounder', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'KKR', 1, 0, NULL),
(175, 'Sameer Rizvi', 'Batsman', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'CSK', 1, 0, NULL),
(176, 'Vipraj Nigam', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(177, 'Mohd. Arshad Khan', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(178, 'Swapnil Singh', 'Allrounder', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'RCB', 1, 0, NULL),
(179, 'Rasikh Salam', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(180, 'Anukul Roy', 'Allrounder', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(181, 'Akash Deep', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(182, 'Yudhvir Singh Charak', 'Allrounder', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(183, 'Anshul Kamboj', 'Allrounder', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(184, 'Kartik Tyagi', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(185, 'Digvesh Singh', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(186, 'Kuldeep Sen', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(187, 'Ashwani Kumar', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(188, 'Akash Singh', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(189, 'Mayank Yadav', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'LSG', 1, 0, NULL),
(190, 'Vignesh Puthur', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(191, 'Zeeshan Ansari', 'Bowler', 'India', 4000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(192, 'Shubham Dubey', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(193, 'Urvil Patel', 'Wicketkeeper', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(194, 'Vishnu Vinod', 'Wicketkeeper', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(195, 'Pravin Dubey', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(196, 'Raj Angad Bawa', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(197, 'Arjun Tendulkar', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, 'MI', 1, 0, NULL),
(198, 'Arshin Kulkarni', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(199, 'Suryansh Shedge', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(200, 'Robin Minz', 'Wicketkeeper', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(201, 'Prince Yadav', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(202, 'Kumar Kushagra', 'Wicketkeeper', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(203, 'Madhav Tiwari', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(204, 'Manav Suthar', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(205, 'Harsh Dubey', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(206, 'M. Siddharth', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(207, 'Musheer Khan', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(208, 'Prithvi Raj Yarra', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(209, 'Abhinandan Singh', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(210, 'Ajay Mandal', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(211, 'Akshat Raghuwanshi', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(212, 'Aman Khan', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(213, 'Aman Rao Perala', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(214, 'Amit Kumar', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(215, 'Ashok Sharma', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(216, 'Atharva Ankolekar', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(217, 'Auqib Dar', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(218, 'Brijesh Sharma', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(219, 'Daksh Kamra', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(220, 'Danish Malewar', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(221, 'Gurjapneet Singh', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(222, 'Gurnoor Singh Brar', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(223, 'Harnoor Pannu', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(224, 'Himmat Singh', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(225, 'Kanishk Chouhan', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(226, 'Kartik Sharma', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(227, 'Krains Fuletra', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(228, 'Mangesh Yadav', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(229, 'Mayank Rawat', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(230, 'Mohammad Izhar', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(231, 'Mukul Choudhary', 'Wicketkeeper', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(232, 'Naman Tiwari', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(233, 'Nishant Sindhu', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(234, 'Onkar Tarmale', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(235, 'Praful Hinge', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(236, 'Prashant Solanki', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(237, 'Prashant Veer', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(238, 'Pyla Avinash', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(239, 'Raghu Sharma', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(240, 'Ramakrishna Ghosh', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(241, 'Ravi Singh', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(242, 'Sahil Parakh', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(243, 'Sakib Hussain', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(244, 'Salil Arora', 'Wicketkeeper', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(245, 'Sarthak Ranjan', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(246, 'Satvik Deswal', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(247, 'Shivang Kumar', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(248, 'Smaran Ravichandran', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(249, 'Sushant Mishra', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(250, 'Tejasvi Singh', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(251, 'Tripurana Vijay', 'Allrounder', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(252, 'Vicky Ostwal', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(253, 'Vihaan Malhotra', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(254, 'Vishal Nishad', 'Batsman', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL),
(255, 'Yash Raj Punja', 'Bowler', 'India', 3000000.00, 0.00, 'Available', 'Set 6: Uncapped Players (UN1)', 'UN1', 0, 0, NULL, 1, 0, NULL);

-- 8. Seed Player Career Statistics
INSERT INTO player_stats (stat_id, player_id, matches, runs, highest_score, batting_avg, strike_rate, fours, sixes, centuries, fifties, wickets, bowling_economy, bowling_avg) VALUES
(1, 1, 267, 8661, 113, 38.15, 132.86, 771, 291, 8, 63, 4, 8.80, 92.00),
(2, 2, 272, 7046, 109, 29.12, 132.10, 640, 302, 2, 47, 15, 7.49, 30.20),
(3, 3, 222, 6769, 106, 35.26, 127.14, 768, 152, 2, 51, 4, 8.25, 16.50),
(4, 4, 184, 6565, 126, 40.52, 139.77, 663, 236, 4, 62, 0, 0.00, 0.00),
(5, 5, 278, 5439, 84, 30.56, 137.45, 375, 264, 0, 24, 0, 0.00, 0.00),
(6, 6, 145, 5222, 132, 42.80, 136.03, 452, 208, 5, 40, 0, 0.00, 0.00),
(7, 7, 198, 5032, 105, 27.96, 125.02, 514, 123, 2, 33, 1, 5.00, 5.00),
(8, 8, 182, 5028, 103, 33.74, 151.13, 523, 206, 2, 34, 0, 8.00, 0.00),
(9, 9, 177, 4704, 119, 29.96, 139.05, 379, 219, 3, 26, 0, 0.00, 0.00),
(10, 10, 145, 4571, 96, 36.57, 136.37, 425, 165, 0, 37, 0, 0.00, 0.00),
(11, 11, 121, 4120, 124, 39.24, 149.38, 407, 185, 7, 24, 0, 0.00, 0.00),
(12, 12, 174, 3942, 114, 27.00, 121.52, 340, 115, 1, 22, 0, 0.00, 0.00),
(13, 13, 118, 3866, 129, 38.28, 138.72, 372, 119, 4, 26, 0, 0.00, 0.00),
(14, 14, 133, 3731, 97, 33.92, 133.35, 314, 152, 0, 27, 0, 7.00, 0.00),
(15, 15, 125, 3553, 128, 33.52, 147.61, 319, 170, 2, 19, 0, 0.00, 0.00),
(16, 16, 115, 3309, 140, 30.64, 134.02, 325, 134, 2, 24, 0, 0.00, 0.00),
(17, 17, 254, 3260, 77, 18.84, 130.24, 240, 117, 0, 5, 170, 7.67, 30.52),
(18, 18, 141, 3077, 101, 33.45, 138.60, 220, 138, 1, 13, 0, 0.00, 0.00),
(19, 19, 134, 2771, 95, 24.74, 156.73, 232, 158, 0, 18, 37, 8.32, 35.49),
(20, 20, 152, 2749, 91, 25.22, 146.93, 207, 148, 0, 10, 78, 9.18, 31.95),
(21, 21, 71, 2502, 108, 39.71, 137.47, 231, 95, 2, 20, 0, 0.00, 0.00),
(22, 22, 127, 2484, 88, 29.22, 174.93, 174, 209, 0, 11, 115, 9.24, 23.82),
(23, 23, 90, 2293, 87, 32.76, 168.98, 158, 167, 0, 14, 0, 0.00, 0.00),
(24, 24, 67, 2166, 124, 33.84, 152.86, 258, 92, 2, 15, 0, 36.00, 0.00),
(25, 25, 162, 1916, 66, 15.33, 133.99, 130, 94, 0, 3, 128, 7.35, 31.61),
(26, 26, 189, 1780, 109, 10.60, 166.51, 189, 116, 1, 7, 192, 6.80, 25.64),
(27, 27, 48, 1480, 105, 37.00, 169.72, 98, 89, 2, 7, 0, 0.00, 0.00),
(28, 28, 38, 1146, 102, 33.71, 170.03, 126, 55, 1, 8, 2, 11.69, 56.50),
(29, 29, 49, 1051, 94, 25.02, 158.76, 70, 75, 0, 7, 13, 9.02, 36.08),
(30, 30, 64, 997, 88, 19.55, 136.39, 85, 41, 0, 6, 59, 9.74, 34.46),
(31, 31, 72, 612, 66, 11.77, 152.24, 39, 41, 0, 3, 79, 8.81, 30.04),
(32, 32, 136, 585, 79, 5.32, 160.27, 41, 41, 0, 1, 158, 7.09, 23.84),
(33, 33, 105, 325, 68, 3.57, 139.48, 30, 13, 0, 1, 107, 9.40, 30.32),
(34, 34, 190, 320, 27, 2.06, 91.17, 31, 3, 0, 0, 198, 7.69, 27.33),
(35, 35, 119, 270, 36, 2.65, 117.90, 16, 15, 0, 0, 151, 8.86, 23.70),
(36, 36, 84, 215, 44, 3.07, 106.97, 16, 9, 0, 0, 119, 8.62, 22.96),
(37, 37, 98, 201, 35, 2.68, 86.64, 18, 3, 0, 0, 102, 8.04, 26.97),
(38, 38, 112, 197, 26, 2.05, 118.67, 16, 7, 0, 0, 110, 8.88, 30.58),
(39, 39, 108, 112, 14, 1.22, 91.06, 10, 4, 0, 0, 109, 8.74, 30.73),
(40, 40, 52, 111, 29, 2.77, 93.28, 11, 0, 0, 0, 65, 8.61, 23.12),
(41, 41, 120, 85, 17, 0.85, 104.94, 5, 3, 0, 0, 143, 8.38, 26.20),
(42, 42, 119, 84, 21, 0.81, 94.38, 7, 2, 0, 0, 133, 8.63, 28.19),
(43, 43, 145, 69, 16, 0.57, 87.34, 5, 1, 0, 0, 183, 7.25, 22.02),
(44, 44, 137, 60, 9, 0.52, 81.08, 4, 0, 0, 0, 146, 8.03, 27.88),
(45, 45, 174, 37, 8, 0.23, 43.02, 0, 0, 0, 0, 221, 7.96, 22.77),
(46, 46, 82, 31, 10, 0.42, 67.39, 4, 0, 0, 0, 97, 9.00, 26.49),
(47, 47, 84, 26, 10, 0.35, 55.32, 2, 0, 0, 0, 100, 7.58, 23.85),
(48, 48, 121, 2998, 106, 27.25, 137.65, 288, 134, 1, 17, 0, 24.00, 0.00),
(49, 49, 118, 2853, 87, 26.42, 136.77, 261, 141, 0, 20, 10, 8.44, 27.00),
(50, 50, 100, 2291, 93, 25.74, 137.85, 229, 85, 0, 12, 0, 12.00, 0.00),
(51, 51, 109, 2026, 124, 24.71, 144.71, 158, 106, 1, 9, 44, 9.79, 32.93),
(52, 52, 79, 1892, 99, 23.95, 147.47, 238, 61, 0, 14, 0, 0.00, 0.00),
(53, 53, 79, 1859, 95, 28.60, 143.66, 108, 122, 0, 10, 5, 10.31, 42.60),
(54, 54, 77, 1816, 141, 25.94, 163.02, 174, 101, 1, 9, 11, 8.95, 45.55),
(55, 55, 74, 1806, 101, 25.44, 126.29, 190, 56, 1, 11, 0, 0.00, 0.00),
(56, 56, 40, 1793, 108, 49.81, 145.89, 183, 52, 2, 12, 0, 0.00, 0.00),
(57, 57, 142, 1756, 86, 17.05, 132.43, 153, 65, 0, 2, 93, 7.47, 32.10),
(58, 58, 84, 1694, 89, 21.44, 131.73, 185, 49, 0, 11, 0, 0.00, 0.00),
(59, 59, 84, 1566, 95, 21.75, 141.85, 111, 87, 0, 7, 7, 9.70, 68.14),
(60, 60, 54, 1499, 84, 34.86, 144.41, 113, 74, 0, 8, 0, 7.64, 0.00),
(61, 61, 42, 1111, 112, 27.77, 154.31, 76, 68, 1, 9, 0, 0.00, 0.00),
(62, 62, 59, 1099, 67, 24.98, 145.18, 87, 56, 0, 4, 0, 0.00, 0.00),
(63, 63, 34, 1056, 89, 34.06, 175.71, 122, 56, 0, 10, 0, 0.00, 0.00),
(64, 64, 55, 991, 85, 21.09, 157.05, 77, 62, 0, 1, 0, 0.00, 0.00),
(65, 65, 32, 705, 71, 37.11, 163.19, 51, 37, 0, 3, 4, 11.50, 17.25),
(66, 66, 52, 262, 30, 6.72, 147.19, 14, 18, 0, 0, 59, 7.89, 27.15),
(67, 67, 52, 180, 24, 4.09, 106.51, 19, 2, 0, 0, 52, 8.17, 25.94),
(68, 68, 35, 141, 34, 5.64, 109.30, 8, 6, 0, 0, 36, 9.41, 31.92),
(69, 69, 79, 129, 25, 1.82, 104.03, 13, 5, 0, 0, 75, 7.72, 28.67),
(70, 70, 95, 117, 39, 1.36, 139.29, 5, 8, 0, 0, 88, 8.14, 29.51),
(71, 71, 49, 72, 24, 1.76, 153.19, 7, 2, 0, 0, 51, 8.97, 30.00),
(72, 72, 76, 62, 19, 0.97, 167.57, 6, 4, 0, 0, 87, 9.12, 28.29),
(73, 73, 117, 57, 10, 0.60, 82.61, 4, 2, 0, 0, 97, 8.36, 34.84),
(74, 74, 48, 49, 23, 1.32, 100.00, 6, 0, 0, 0, 61, 9.07, 27.16),
(75, 75, 77, 45, 13, 0.65, 68.18, 2, 2, 0, 0, 72, 8.22, 30.96),
(76, 76, 46, 28, 20, 0.70, 127.27, 2, 1, 0, 0, 51, 9.84, 31.04),
(77, 77, 39, 19, 7, 0.59, 65.52, 1, 0, 0, 0, 57, 8.28, 20.98),
(78, 78, 32, 10, 6, 0.36, 55.56, 0, 0, 0, 0, 36, 10.40, 30.61),
(79, 79, 66, 9, 4, 0.15, 37.50, 0, 0, 0, 0, 74, 8.77, 29.61),
(80, 80, 63, 3, 3, 0.05, 60.00, 0, 0, 0, 0, 67, 8.94, 30.12),
(81, 81, 71, 2, 1, 0.03, 22.22, 0, 0, 0, 0, 89, 8.98, 26.16),
(82, 82, 32, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 47, 8.68, 21.62),
(83, 83, 86, 1483, 75, 25.57, 151.95, 93, 93, 0, 5, 0, 0.00, 0.00),
(84, 84, 62, 1468, 104, 26.69, 137.32, 136, 65, 1, 12, 3, 10.59, 47.67),
(85, 85, 57, 1440, 68, 30.00, 135.08, 111, 57, 0, 10, 6, 8.79, 45.67),
(86, 86, 55, 1293, 117, 24.40, 143.03, 104, 75, 1, 9, 37, 8.52, 21.49),
(87, 87, 108, 1112, 53, 14.08, 137.11, 90, 54, 0, 1, 32, 7.91, 34.72),
(88, 88, 50, 846, 50, 26.44, 173.36, 54, 60, 0, 1, 0, 0.00, 0.00),
(89, 89, 29, 707, 100, 39.28, 153.70, 62, 32, 1, 2, 0, 0.00, 0.00),
(90, 90, 42, 680, 70, 21.94, 153.85, 51, 38, 0, 4, 0, 0.00, 0.00),
(91, 91, 66, 511, 49, 9.64, 126.17, 42, 16, 0, 0, 39, 7.70, 36.82),
(92, 92, 28, 485, 76, 21.09, 132.88, 31, 25, 0, 2, 5, 10.96, 50.80),
(93, 93, 21, 463, 100, 24.37, 152.81, 38, 29, 1, 2, 8, 9.57, 27.50),
(94, 94, 26, 189, 47, 8.22, 121.15, 11, 11, 0, 0, 35, 8.20, 22.46),
(95, 95, 31, 110, 22, 5.50, 105.77, 6, 6, 0, 0, 25, 7.31, 29.40),
(96, 96, 37, 81, 18, 2.45, 92.05, 7, 1, 0, 0, 46, 8.41, 24.33),
(97, 97, 8, 65, 25, 9.29, 118.18, 3, 6, 0, 0, 2, 8.00, 20.00),
(98, 98, 32, 51, 20, 1.76, 91.07, 4, 2, 0, 0, 25, 8.30, 28.60),
(99, 99, 37, 48, 18, 1.66, 114.29, 5, 1, 0, 0, 37, 8.91, 28.89),
(100, 100, 37, 20, 7, 0.62, 57.14, 2, 0, 0, 0, 48, 8.08, 22.23),
(101, 101, 17, 19, 12, 1.19, 76.00, 0, 1, 0, 0, 19, 8.66, 29.16),
(102, 102, 25, 18, 13, 0.75, 112.50, 0, 2, 0, 0, 32, 8.86, 20.34),
(103, 103, 43, 4, 3, 0.10, 44.44, 0, 0, 0, 0, 41, 9.58, 33.90),
(104, 104, 16, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 29, 8.53, 18.24),
(105, 105, 58, 545, 59, 11.12, 121.65, 29, 25, 0, 1, 22, 9.58, 42.68),
(106, 106, 16, 455, 57, 28.44, 153.20, 30, 33, 0, 2, 1, 16.00, 8.00),
(107, 107, 40, 441, 67, 14.23, 138.24, 50, 11, 0, 1, 0, 18.00, 0.00),
(108, 108, 18, 413, 65, 24.29, 143.90, 40, 16, 0, 2, 0, 3.50, 0.00),
(109, 109, 23, 397, 46, 20.89, 137.37, 25, 26, 0, 0, 1, 8.63, 59.00),
(110, 110, 14, 388, 62, 29.85, 150.97, 47, 17, 0, 3, 0, 0.00, 0.00),
(111, 111, 29, 365, 67, 14.04, 146.59, 22, 28, 0, 1, 1, 11.67, 35.00),
(112, 112, 11, 278, 73, 30.89, 162.57, 26, 16, 0, 1, 0, 0.00, 0.00),
(113, 113, 18, 185, 53, 14.23, 212.64, 12, 17, 0, 1, 10, 11.66, 40.80),
(114, 114, 16, 99, 21, 6.60, 133.78, 8, 5, 0, 0, 12, 9.69, 38.75),
(115, 115, 5, 92, 32, 30.67, 133.33, 7, 2, 0, 0, 2, 8.57, 30.00),
(116, 116, 2, 67, 55, 33.50, 171.79, 9, 3, 0, 1, 0, 0.00, 0.00),
(117, 117, 13, 65, 16, 8.12, 108.33, 5, 3, 0, 0, 14, 9.67, 29.71),
(118, 118, 19, 53, 17, 4.42, 126.19, 3, 3, 0, 0, 13, 9.73, 46.38),
(119, 119, 3, 47, 27, 15.67, 146.88, 3, 3, 0, 0, 1, 7.86, 55.00),
(120, 120, 20, 40, 23, 2.11, 111.11, 2, 1, 0, 0, 8, 6.85, 55.62),
(121, 121, 3, 26, 21, 8.67, 113.04, 4, 0, 0, 0, 0, 0.00, 0.00),
(122, 122, 10, 23, 15, 2.88, 79.31, 0, 1, 0, 0, 7, 9.48, 46.71),
(123, 123, 26, 23, 19, 1.05, 143.75, 1, 2, 0, 0, 2, 8.00, 48.00),
(124, 124, 2, 18, 10, 9.00, 90.00, 1, 1, 0, 0, 0, 0.00, 0.00),
(125, 125, 3, 15, 11, 15.00, 214.29, 1, 1, 0, 0, 0, 13.83, 0.00),
(126, 126, 16, 14, 13, 1.00, 116.67, 0, 1, 0, 0, 17, 10.38, 33.88),
(127, 127, 1, 14, 14, 14.00, 116.67, 1, 1, 0, 0, 0, 0.00, 0.00),
(128, 128, 4, 11, 11, 2.75, 73.33, 1, 0, 0, 0, 2, 9.60, 48.00),
(129, 129, 3, 9, 7, 3.00, 64.29, 0, 0, 0, 0, 0, 0.00, 0.00),
(130, 130, 2, 9, 9, 9.00, 300.00, 0, 1, 0, 0, 0, 0.00, 0.00),
(131, 131, 4, 8, 8, 2.67, 400.00, 2, 0, 0, 0, 2, 13.00, 71.50),
(132, 132, 16, 6, 4, 0.40, 100.00, 1, 0, 0, 0, 17, 9.94, 30.71),
(133, 133, 7, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 13, 8.92, 18.31),
(134, 134, 8, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 9, 9.43, 31.44),
(135, 135, 6, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 7, 8.53, 20.71),
(136, 136, 6, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 1, 14.20, 71.00),
(137, 137, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(138, 138, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(139, 139, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(140, 140, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(141, 141, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(142, 142, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(143, 143, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(144, 144, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(145, 145, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(146, 146, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(147, 147, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(148, 148, 1, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(149, 149, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(150, 150, 1, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(151, 151, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(152, 152, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(153, 153, 51, 1305, 103, 25.59, 151.92, 134, 71, 1, 7, 0, 0.00, 0.00),
(154, 154, 56, 963, 74, 20.93, 138.56, 73, 38, 0, 6, 4, 8.40, 12.25),
(155, 155, 41, 773, 68, 28.63, 157.76, 56, 43, 0, 5, 1, 10.40, 52.00),
(156, 156, 63, 741, 45, 15.12, 151.84, 45, 50, 0, 0, 2, 12.75, 59.50),
(157, 157, 55, 732, 58, 18.30, 149.08, 46, 50, 0, 2, 1, 9.33, 28.00),
(158, 158, 36, 719, 70, 22.47, 142.94, 60, 39, 0, 4, 0, 7.76, 0.00),
(159, 159, 31, 661, 65, 23.61, 149.89, 65, 27, 0, 3, 0, 0.00, 0.00),
(160, 160, 17, 475, 103, 27.94, 179.25, 55, 25, 1, 2, 0, 0.00, 0.00),
(161, 161, 22, 463, 54, 23.15, 144.69, 46, 16, 0, 2, 0, 0.00, 0.00),
(162, 162, 49, 244, 29, 6.97, 120.20, 19, 10, 0, 0, 35, 8.03, 31.00),
(163, 163, 34, 59, 34, 1.97, 105.36, 5, 3, 0, 0, 40, 9.51, 25.73),
(164, 164, 24, 25, 13, 1.14, 104.17, 2, 1, 0, 0, 27, 8.51, 25.52),
(165, 165, 32, 9, 2, 0.35, 37.50, 0, 0, 0, 0, 36, 9.55, 28.22),
(166, 166, 21, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 25, 10.43, 30.80),
(167, 167, 27, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 18, 8.75, 45.22),
(168, 168, 24, 393, 66, 19.65, 163.75, 24, 28, 0, 2, 0, 0.00, 0.00),
(169, 169, 23, 392, 62, 21.78, 180.65, 36, 23, 0, 1, 0, 8.77, 0.00),
(170, 170, 24, 318, 66, 16.74, 119.10, 26, 14, 0, 1, 0, 0.00, 0.00),
(171, 171, 7, 252, 101, 36.00, 206.56, 18, 24, 1, 1, 0, 0.00, 0.00),
(172, 172, 7, 240, 94, 34.29, 188.98, 31, 11, 0, 1, 0, 0.00, 0.00),
(173, 173, 14, 236, 74, 21.45, 166.20, 12, 20, 0, 1, 0, 0.00, 0.00),
(174, 174, 31, 217, 35, 9.86, 158.39, 9, 17, 0, 0, 6, 9.45, 10.50),
(175, 175, 13, 172, 58, 15.64, 140.98, 15, 9, 0, 1, 0, 0.00, 0.00),
(176, 176, 14, 142, 39, 10.92, 179.75, 15, 8, 0, 0, 11, 9.13, 32.36),
(177, 177, 19, 124, 58, 9.54, 140.91, 6, 9, 0, 1, 12, 11.49, 43.42),
(178, 178, 14, 51, 15, 5.10, 113.33, 3, 3, 0, 0, 7, 8.83, 30.29),
(179, 179, 13, 40, 10, 3.33, 100.00, 5, 0, 0, 0, 10, 10.62, 40.90),
(180, 180, 12, 26, 13, 2.89, 104.00, 3, 0, 0, 0, 6, 8.17, 36.33),
(181, 181, 14, 25, 17, 2.08, 178.57, 2, 2, 0, 0, 10, 11.83, 54.80),
(182, 182, 9, 22, 14, 2.44, 137.50, 1, 2, 0, 0, 8, 11.00, 31.62),
(183, 183, 11, 16, 5, 2.29, 114.29, 2, 0, 0, 0, 10, 9.08, 28.60),
(184, 184, 20, 13, 7, 0.76, 81.25, 1, 0, 0, 0, 13, 9.41, 37.77),
(185, 185, 13, 1, 1, 0.08, 33.33, 0, 0, 0, 0, 14, 8.25, 30.64),
(186, 186, 12, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 14, 9.63, 27.64),
(187, 187, 7, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 11, 11.32, 21.09),
(188, 188, 10, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 9, 9.54, 36.22),
(189, 189, 6, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 9, 9.17, 20.56),
(190, 190, 5, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 6, 9.08, 18.17),
(191, 191, 10, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 6, 9.84, 55.50),
(192, 192, 13, 139, 34, 17.38, 163.53, 9, 10, 0, 0, 0, 0.00, 0.00),
(193, 193, 3, 68, 37, 22.67, 212.50, 5, 6, 0, 0, 0, 0.00, 0.00),
(194, 194, 6, 56, 30, 9.33, 98.25, 3, 3, 0, 0, 0, 0.00, 0.00),
(195, 195, 5, 23, 16, 5.75, 69.70, 2, 0, 0, 0, 2, 8.54, 55.50),
(196, 196, 5, 19, 11, 4.75, 105.56, 1, 0, 0, 0, 0, 0.00, 0.00),
(197, 197, 5, 13, 13, 2.60, 144.44, 0, 1, 0, 0, 3, 9.37, 38.00),
(198, 198, 2, 9, 9, 4.50, 112.50, 2, 0, 0, 0, 0, 0.00, 0.00),
(199, 199, 5, 7, 4, 1.40, 63.64, 0, 0, 0, 0, 0, 13.33, 0.00),
(200, 200, 2, 6, 3, 3.00, 40.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(201, 201, 6, 5, 4, 1.25, 50.00, 0, 0, 0, 0, 3, 9.85, 75.00),
(202, 202, 4, 3, 2, 0.75, 42.86, 0, 0, 0, 0, 0, 0.00, 0.00),
(203, 203, 1, 3, 3, 3.00, 75.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(204, 204, 1, 1, 1, 1.00, 50.00, 0, 0, 0, 0, 0, 13.00, 0.00),
(205, 205, 3, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 5, 9.80, 19.60),
(206, 206, 5, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 3, 8.62, 46.00),
(207, 207, 1, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 1, 13.50, 27.00),
(208, 208, 2, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 1, 11.40, 57.00),
(209, 209, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(210, 210, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(211, 211, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(212, 212, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(213, 213, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(214, 214, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(215, 215, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(216, 216, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(217, 217, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(218, 218, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(219, 219, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(220, 220, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(221, 221, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(222, 222, 1, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 14.00, 0.00),
(223, 223, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(224, 224, 3, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(225, 225, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(226, 226, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(227, 227, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(228, 228, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(229, 229, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(230, 230, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(231, 231, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(232, 232, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(233, 233, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(234, 234, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(235, 235, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(236, 236, 2, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(237, 237, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(238, 238, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(239, 239, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(240, 240, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(241, 241, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(242, 242, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(243, 243, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(244, 244, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(245, 245, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(246, 246, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(247, 247, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(248, 248, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(249, 249, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(250, 250, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(251, 251, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(252, 252, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(253, 253, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(254, 254, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00),
(255, 255, 0, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 0, 0.00, 0.00);

-- 9. Reset PostgreSQL ID Sequences so future user inserts continue smoothly
SELECT setval('teams_team_id_seq', (SELECT MAX(team_id) FROM teams));
SELECT setval('players_player_id_seq', (SELECT MAX(player_id) FROM players));
SELECT setval('player_stats_stat_id_seq', (SELECT MAX(stat_id) FROM player_stats));
SELECT setval('auction_bids_bid_id_seq', COALESCE((SELECT MAX(bid_id) FROM auction_bids), 1));
