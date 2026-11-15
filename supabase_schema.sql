-- ============================================================================
-- TATA IPL 2026 MEGA AUCTION - REAL DATA SUPABASE POSTGRESQL SCHEMA
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
    max_squad_size INT NOT NULL DEFAULT 25
);

CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'India',
    base_price NUMERIC(15, 2) NOT NULL,
    sold_price NUMERIC(15, 2) DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'Available',
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
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'CSK';
CREATE OR REPLACE VIEW mi_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'MI';
CREATE OR REPLACE VIEW rcb_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'RCB';
CREATE OR REPLACE VIEW kkr_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'KKR';
CREATE OR REPLACE VIEW rr_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'RR';
CREATE OR REPLACE VIEW srh_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'SRH';
CREATE OR REPLACE VIEW gt_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'GT';
CREATE OR REPLACE VIEW lsg_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'LSG';
CREATE OR REPLACE VIEW dc_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'DC';
CREATE OR REPLACE VIEW pbks_squad AS
SELECT 
    p.player_id, p.name, p.role, p.country, p.sold_price,
    s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate,
    s.fours, s.sixes, s.wickets, s.bowling_economy
FROM players p
JOIN teams t ON p.team_id = t.team_id
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE UPPER(t.short_code) = 'PBKS';

-- 6. Seed 10 Real IPL Franchises (₹120.00 Crore purse each)
INSERT INTO teams (team_id, team_name, short_code, primary_color, secondary_color, total_budget, remaining_budget, max_squad_size) VALUES
(1, 'Chennai Super Kings', 'CSK', '#FDB913', '#0081E8', 1200000000.00, 1200000000.00, 25),
(2, 'Mumbai Indians', 'MI', '#004BA0', '#D1AB3E', 1200000000.00, 1200000000.00, 25),
(3, 'Royal Challengers Bengaluru', 'RCB', '#EC1C24', '#2B2A29', 1200000000.00, 1200000000.00, 25),
(4, 'Kolkata Knight Riders', 'KKR', '#3A225D', '#F7D54E', 1200000000.00, 1200000000.00, 25),
(5, 'Rajasthan Royals', 'RR', '#EA1A85', '#254AA5', 1200000000.00, 1200000000.00, 25),
(6, 'Sunrisers Hyderabad', 'SRH', '#F26522', '#000000', 1200000000.00, 1200000000.00, 25),
(7, 'Gujarat Titans', 'GT', '#1C1C1C', '#0B4973', 1200000000.00, 1200000000.00, 25),
(8, 'Lucknow Super Giants', 'LSG', '#A72056', '#0055A5', 1200000000.00, 1200000000.00, 25),
(9, 'Delhi Capitals', 'DC', '#004C93', '#E41B17', 1200000000.00, 1200000000.00, 25),
(10, 'Punjab Kings', 'PBKS', '#DD1F2D', '#C3A25D', 1200000000.00, 1200000000.00, 25);

-- 7. Seed Real IPL Players & Authentic Career Statistics
INSERT INTO players (player_id, name, role, country, base_price, sold_price, status, team_id) VALUES
(1, 'Virat Kohli', 'Batsman', 'India', 20000000.00, 0.00, 'Available', NULL),
(2, 'Rohit Sharma', 'Batsman', 'India', 20000000.00, 0.00, 'Available', NULL),
(3, 'Shubman Gill', 'Batsman', 'India', 20000000.00, 0.00, 'Available', NULL),
(4, 'Suryakumar Yadav', 'Batsman', 'India', 20000000.00, 0.00, 'Available', NULL),
(5, 'Yashasvi Jaiswal', 'Batsman', 'India', 20000000.00, 0.00, 'Available', NULL),
(6, 'Ruturaj Gaikwad', 'Batsman', 'India', 20000000.00, 0.00, 'Available', NULL),
(7, 'Sai Sudharsan', 'Batsman', 'India', 10000000.00, 0.00, 'Available', NULL),
(8, 'Travis Head', 'Batsman', 'Australia', 20000000.00, 0.00, 'Available', NULL),
(9, 'Abhishek Sharma', 'Batsman', 'India', 15000000.00, 0.00, 'Available', NULL),
(10, 'Shreyas Iyer', 'Batsman', 'India', 20000000.00, 0.00, 'Available', NULL),
(11, 'David Warner', 'Batsman', 'Australia', 20000000.00, 0.00, 'Available', NULL),
(12, 'Faf du Plessis', 'Batsman', 'South Africa', 20000000.00, 0.00, 'Available', NULL),
(13, 'Shikhar Dhawan', 'Batsman', 'India', 20000000.00, 0.00, 'Available', NULL),
(14, 'Rinku Singh', 'Batsman', 'India', 10000000.00, 0.00, 'Available', NULL),
(15, 'Tilak Varma', 'Batsman', 'India', 15000000.00, 0.00, 'Available', NULL),
(16, 'Rishabh Pant', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', NULL),
(17, 'MS Dhoni', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', NULL),
(18, 'Heinrich Klaasen', 'Wicketkeeper', 'South Africa', 20000000.00, 0.00, 'Available', NULL),
(19, 'KL Rahul', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', NULL),
(20, 'Sanju Samson', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', NULL),
(21, 'Nicholas Pooran', 'Wicketkeeper', 'West Indies', 20000000.00, 0.00, 'Available', NULL),
(22, 'Jos Buttler', 'Wicketkeeper', 'England', 20000000.00, 0.00, 'Available', NULL),
(23, 'Phil Salt', 'Wicketkeeper', 'England', 15000000.00, 0.00, 'Available', NULL),
(24, 'Ishan Kishan', 'Wicketkeeper', 'India', 20000000.00, 0.00, 'Available', NULL),
(25, 'Hardik Pandya', 'Allrounder', 'India', 20000000.00, 0.00, 'Available', NULL),
(26, 'Ravindra Jadeja', 'Allrounder', 'India', 20000000.00, 0.00, 'Available', NULL),
(27, 'Andre Russell', 'Allrounder', 'West Indies', 20000000.00, 0.00, 'Available', NULL),
(28, 'Sunil Narine', 'Allrounder', 'West Indies', 20000000.00, 0.00, 'Available', NULL),
(29, 'Rashid Khan', 'Allrounder', 'Afghanistan', 20000000.00, 0.00, 'Available', NULL),
(30, 'Glenn Maxwell', 'Allrounder', 'Australia', 20000000.00, 0.00, 'Available', NULL),
(31, 'Axar Patel', 'Allrounder', 'India', 20000000.00, 0.00, 'Available', NULL),
(32, 'Marcus Stoinis', 'Allrounder', 'Australia', 20000000.00, 0.00, 'Available', NULL),
(33, 'Shivam Dube', 'Allrounder', 'India', 15000000.00, 0.00, 'Available', NULL),
(34, 'Sam Curran', 'Allrounder', 'England', 20000000.00, 0.00, 'Available', NULL),
(35, 'Jasprit Bumrah', 'Bowler', 'India', 20000000.00, 0.00, 'Available', NULL),
(36, 'Mitchell Starc', 'Bowler', 'Australia', 20000000.00, 0.00, 'Available', NULL),
(37, 'Pat Cummins', 'Bowler', 'Australia', 20000000.00, 0.00, 'Available', NULL),
(38, 'Yuzvendra Chahal', 'Bowler', 'India', 20000000.00, 0.00, 'Available', NULL),
(39, 'Mohammed Shami', 'Bowler', 'India', 20000000.00, 0.00, 'Available', NULL),
(40, 'Trent Boult', 'Bowler', 'New Zealand', 20000000.00, 0.00, 'Available', NULL),
(41, 'Kagiso Rabada', 'Bowler', 'South Africa', 20000000.00, 0.00, 'Available', NULL),
(42, 'Arshdeep Singh', 'Bowler', 'India', 20000000.00, 0.00, 'Available', NULL),
(43, 'Bhuvneshwar Kumar', 'Bowler', 'India', 20000000.00, 0.00, 'Available', NULL),
(44, 'Kuldeep Yadav', 'Bowler', 'India', 20000000.00, 0.00, 'Available', NULL),
(45, 'Mohammed Siraj', 'Bowler', 'India', 20000000.00, 0.00, 'Available', NULL),
(46, 'Matheesha Pathirana', 'Bowler', 'Sri Lanka', 15000000.00, 0.00, 'Available', NULL),
(47, 'Varun Chakaravarthy', 'Bowler', 'India', 15000000.00, 0.00, 'Available', NULL),
(48, 'Mayank Yadav', 'Bowler', 'India', 10000000.00, 0.00, 'Available', NULL),
(49, 'Harshal Patel', 'Bowler', 'India', 20000000.00, 0.00, 'Available', NULL);

-- 8. Seed Player Career Statistics
INSERT INTO player_stats (stat_id, player_id, matches, runs, highest_score, batting_avg, strike_rate, fours, sixes, centuries, fifties, wickets, bowling_economy, bowling_avg) VALUES
(1, 1, 252, 8004, 113, 38.67, 131.97, 705, 272, 8, 55, 4, 8.80, 92.00),
(2, 2, 257, 6628, 109, 29.72, 131.14, 599, 280, 2, 43, 15, 8.02, 30.20),
(3, 3, 103, 3216, 129, 37.84, 135.70, 310, 98, 4, 20, 0, 0.00, 0.00),
(4, 4, 150, 3594, 103, 32.09, 145.33, 382, 130, 2, 24, 0, 0.00, 0.00),
(5, 5, 52, 1607, 124, 32.14, 150.61, 198, 64, 2, 9, 0, 0.00, 0.00),
(6, 6, 66, 2380, 108, 41.75, 136.86, 224, 91, 2, 18, 0, 0.00, 0.00),
(7, 7, 25, 1039, 103, 47.23, 139.09, 110, 27, 1, 6, 0, 0.00, 0.00),
(8, 8, 25, 772, 102, 36.76, 185.13, 88, 43, 1, 5, 2, 9.10, 45.00),
(9, 9, 63, 1377, 75, 25.50, 155.24, 136, 68, 0, 7, 9, 8.85, 34.20),
(10, 10, 115, 3127, 96, 32.24, 127.48, 277, 113, 0, 21, 0, 0.00, 0.00),
(11, 11, 184, 6565, 126, 40.52, 139.77, 663, 236, 4, 62, 0, 0.00, 0.00),
(12, 12, 145, 4571, 96, 35.99, 136.37, 421, 165, 0, 37, 0, 0.00, 0.00),
(13, 13, 222, 6769, 106, 35.26, 127.14, 768, 152, 2, 51, 4, 8.25, 16.50),
(14, 14, 45, 893, 67, 30.79, 143.34, 68, 48, 0, 4, 0, 0.00, 0.00),
(15, 15, 38, 1156, 84, 39.86, 146.33, 95, 55, 0, 6, 0, 0.00, 0.00),
(16, 16, 111, 3284, 128, 35.31, 148.93, 296, 154, 1, 18, 0, 0.00, 0.00),
(17, 17, 264, 5243, 84, 39.13, 137.53, 363, 252, 0, 24, 0, 0.00, 0.00),
(18, 18, 35, 993, 104, 38.19, 168.31, 66, 64, 1, 6, 0, 0.00, 0.00),
(19, 19, 132, 4683, 132, 45.47, 134.61, 415, 187, 4, 37, 0, 0.00, 0.00),
(20, 20, 168, 4419, 119, 30.69, 138.96, 352, 206, 3, 25, 0, 0.00, 0.00),
(21, 21, 76, 1769, 77, 32.16, 162.29, 118, 127, 0, 9, 0, 0.00, 0.00),
(22, 22, 107, 3582, 124, 38.11, 147.53, 359, 161, 7, 19, 0, 0.00, 0.00),
(23, 23, 21, 653, 89, 34.37, 175.54, 75, 34, 0, 6, 0, 0.00, 0.00),
(24, 24, 105, 2644, 99, 28.43, 135.87, 265, 110, 0, 16, 0, 0.00, 0.00),
(25, 25, 137, 2525, 91, 28.69, 145.87, 190, 132, 0, 10, 64, 8.94, 33.26),
(26, 26, 240, 2959, 62, 27.40, 129.55, 210, 102, 0, 3, 160, 7.60, 30.12),
(27, 27, 127, 2484, 88, 29.22, 174.93, 178, 209, 0, 11, 115, 9.20, 23.00),
(28, 28, 177, 1534, 109, 17.04, 165.84, 165, 93, 1, 7, 180, 6.73, 25.39),
(29, 29, 121, 545, 79, 13.62, 144.18, 38, 39, 0, 1, 149, 6.82, 21.82),
(30, 30, 134, 2771, 95, 24.74, 156.73, 236, 158, 0, 18, 37, 8.35, 35.50),
(31, 31, 150, 1653, 66, 21.47, 130.88, 125, 72, 0, 4, 123, 7.24, 30.50),
(32, 32, 96, 1866, 124, 28.27, 142.01, 152, 91, 1, 9, 43, 9.48, 31.60),
(33, 33, 65, 1502, 95, 29.45, 159.28, 98, 97, 0, 9, 5, 9.50, 42.00),
(34, 34, 59, 883, 63, 24.53, 135.64, 76, 41, 0, 4, 58, 9.48, 31.50),
(35, 35, 133, 69, 16, 9.85, 95.83, 6, 1, 0, 0, 165, 7.30, 22.51),
(36, 36, 41, 115, 29, 11.50, 108.49, 10, 3, 0, 0, 51, 8.21, 24.12),
(37, 37, 58, 515, 66, 18.39, 151.47, 38, 31, 0, 3, 63, 8.95, 30.12),
(38, 38, 160, 37, 8, 4.11, 43.52, 1, 0, 0, 0, 205, 7.80, 22.45),
(39, 39, 110, 79, 21, 7.90, 90.80, 7, 2, 0, 0, 127, 8.44, 26.87),
(40, 40, 104, 51, 17, 6.37, 86.44, 4, 1, 0, 0, 121, 8.29, 26.51),
(41, 41, 80, 186, 44, 11.62, 103.91, 16, 6, 0, 0, 117, 8.42, 22.15),
(42, 42, 65, 28, 10, 5.60, 70.00, 2, 1, 0, 0, 76, 9.03, 27.00),
(43, 43, 176, 312, 27, 8.66, 96.29, 28, 6, 0, 0, 181, 7.56, 27.23),
(44, 44, 84, 114, 16, 9.50, 78.62, 8, 2, 0, 0, 87, 8.13, 26.97),
(45, 45, 93, 109, 14, 7.78, 81.34, 9, 3, 0, 0, 93, 8.65, 30.34),
(46, 46, 20, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 34, 7.88, 17.50),
(47, 47, 71, 24, 7, 4.80, 60.00, 2, 0, 0, 0, 83, 7.56, 25.10),
(48, 48, 4, 0, 0, 0.00, 0.00, 0, 0, 0, 0, 7, 6.98, 12.14),
(49, 49, 105, 236, 36, 11.23, 131.11, 20, 11, 0, 0, 135, 8.62, 23.33);

-- 9. Record Virat Kohli's Purchase for Royal Challengers Bengaluru (RCB)
UPDATE players SET status = 'Sold', sold_price = 25000000.00, team_id = 3 WHERE player_id = 1;
UPDATE teams SET remaining_budget = 1175000000.00 WHERE team_id = 3;
INSERT INTO auction_bids (player_id, team_id, bid_amount) VALUES (1, 3, 25000000.00);

INSERT INTO rcb_players (player_id, name, role, country, sold_price, matches, runs, highest_score, batting_avg, strike_rate, fours, sixes, wickets, bowling_economy, bowling_avg)
SELECT p.player_id, p.name, p.role, p.country, 25000000.00, s.matches, s.runs, s.highest_score, s.batting_avg, s.strike_rate, s.fours, s.sixes, s.wickets, s.bowling_economy, s.bowling_avg
FROM players p
LEFT JOIN player_stats s ON p.player_id = s.player_id
WHERE p.player_id = 1;

-- 10. Reset PostgreSQL ID Sequences so future user inserts continue smoothly
SELECT setval('teams_team_id_seq', (SELECT MAX(team_id) FROM teams));
SELECT setval('players_player_id_seq', (SELECT MAX(player_id) FROM players));
SELECT setval('player_stats_stat_id_seq', (SELECT MAX(stat_id) FROM player_stats));
SELECT setval('auction_bids_bid_id_seq', (SELECT MAX(bid_id) FROM auction_bids));
