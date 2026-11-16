-- ============================================================================
-- TATA IPL 2026 - NON-DESTRUCTIVE SUPABASE SCHEMA UPDATE
-- Run this in Supabase SQL Editor to add new columns and populate RTM data!
-- ============================================================================

-- 1. Add missing columns to teams and players
ALTER TABLE teams ADD COLUMN IF NOT EXISTS retention_spend NUMERIC(15, 2) NOT NULL DEFAULT 0.00;
ALTER TABLE teams ADD COLUMN IF NOT EXISTS retentions_count INT NOT NULL DEFAULT 0;
ALTER TABLE teams ADD COLUMN IF NOT EXISTS rtm_cards INT NOT NULL DEFAULT 0;
ALTER TABLE teams ADD COLUMN IF NOT EXISTS retained_names TEXT DEFAULT '';
ALTER TABLE teams ADD COLUMN IF NOT EXISTS min_squad_size INT NOT NULL DEFAULT 18;
ALTER TABLE teams ADD COLUMN IF NOT EXISTS max_overseas INT NOT NULL DEFAULT 8;

ALTER TABLE players ADD COLUMN IF NOT EXISTS set_name VARCHAR(100) DEFAULT 'Set 1: Capped Batters (BA1)';
ALTER TABLE players ADD COLUMN IF NOT EXISTS set_code VARCHAR(10) DEFAULT 'BA1';
ALTER TABLE players ADD COLUMN IF NOT EXISTS is_capped INT DEFAULT 1;
ALTER TABLE players ADD COLUMN IF NOT EXISTS is_overseas INT DEFAULT 0;
ALTER TABLE players ADD COLUMN IF NOT EXISTS former_team VARCHAR(10) DEFAULT NULL;
ALTER TABLE players ADD COLUMN IF NOT EXISTS is_shortlisted INT DEFAULT 1;
ALTER TABLE players ADD COLUMN IF NOT EXISTS accelerated INT DEFAULT 0;

-- 2. Update teams with official retentions and RTM cards
UPDATE teams SET 
    retention_spend = 650000000.0,
    retentions_count = 5,
    rtm_cards = 1,
    retained_names = 'Ruturaj Gaikwad, Ravindra Jadeja, MS Dhoni, Shivam Dube, Matheesha Pathirana',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'CSK';
UPDATE teams SET 
    retention_spend = 750000000.0,
    retentions_count = 5,
    rtm_cards = 1,
    retained_names = 'Jasprit Bumrah, Suryakumar Yadav, Hardik Pandya, Rohit Sharma, Tilak Varma',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'MI';
UPDATE teams SET 
    retention_spend = 370000000.0,
    retentions_count = 3,
    rtm_cards = 3,
    retained_names = 'Virat Kohli, Rajat Patidar, Yash Dayal',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'RCB';
UPDATE teams SET 
    retention_spend = 690000000.0,
    retentions_count = 6,
    rtm_cards = 0,
    retained_names = 'Rinku Singh, Andre Russell, Sunil Narine, Varun Chakaravarthy, Harshit Rana, Ramandeep Singh',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'KKR';
UPDATE teams SET 
    retention_spend = 790000000.0,
    retentions_count = 6,
    rtm_cards = 0,
    retained_names = 'Sanju Samson, Yashasvi Jaiswal, Riyan Parag, Dhruv Jurel, Shimron Hetmyer, Sandeep Sharma',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'RR';
UPDATE teams SET 
    retention_spend = 750000000.0,
    retentions_count = 5,
    rtm_cards = 1,
    retained_names = 'Heinrich Klaasen, Pat Cummins, Abhishek Sharma, Travis Head, Nitish Kumar Reddy',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'SRH';
UPDATE teams SET 
    retention_spend = 510000000.0,
    retentions_count = 5,
    rtm_cards = 1,
    retained_names = 'Rashid Khan, Shubman Gill, Sai Sudharsan, Rahul Tewatia, Shahrukh Khan',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'GT';
UPDATE teams SET 
    retention_spend = 510000000.0,
    retentions_count = 5,
    rtm_cards = 1,
    retained_names = 'Nicholas Pooran, Ravi Bishnoi, Mayank Yadav, Mohsin Khan, Ayush Badoni',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'LSG';
UPDATE teams SET 
    retention_spend = 470000000.0,
    retentions_count = 4,
    rtm_cards = 2,
    retained_names = 'Axar Patel, Kuldeep Yadav, Tristan Stubbs, Abishek Porel',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'DC';
UPDATE teams SET 
    retention_spend = 95000000.0,
    retentions_count = 2,
    rtm_cards = 4,
    retained_names = 'Shashank Singh, Prabhsimran Singh',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'PBKS';

-- 3. Update players with sets, capped, overseas and former teams
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Virat Kohli';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Rohit Sharma';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'GT'
WHERE name = 'Shubman Gill';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Suryakumar Yadav';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Yashasvi Jaiswal';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Ruturaj Gaikwad';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Travis Head';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Shreyas Iyer';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'David Warner';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Faf du Plessis';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Shikhar Dhawan';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Hardik Pandya';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Ravindra Jadeja';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Andre Russell';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Sunil Narine';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Glenn Maxwell';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Axar Patel';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Marcus Stoinis';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Shivam Dube';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Sam Curran';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Rishabh Pant';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'MS Dhoni';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Heinrich Klaasen';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'KL Rahul';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Sanju Samson';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Nicholas Pooran';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Jos Buttler';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Phil Salt';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Ishan Kishan';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Jasprit Bumrah';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Mitchell Starc';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Pat Cummins';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'GT'
WHERE name = 'Mohammed Shami';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Trent Boult';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Kagiso Rabada';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Arshdeep Singh';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Bhuvneshwar Kumar';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Mohammed Siraj';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'GT'
WHERE name = 'Rashid Khan';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Yuzvendra Chahal';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Kuldeep Yadav';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Varun Chakaravarthy';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'GT'
WHERE name = 'Sai Sudharsan';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Abhishek Sharma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Rinku Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Tilak Varma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Matheesha Pathirana';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Mayank Yadav';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Harshal Patel';

-- 4. Create 10 dedicated franchise squad tables if not exist
CREATE TABLE IF NOT EXISTS csk_players (
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
);
CREATE TABLE IF NOT EXISTS mi_players (
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
);
CREATE TABLE IF NOT EXISTS rcb_players (
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
);
CREATE TABLE IF NOT EXISTS kkr_players (
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
);
CREATE TABLE IF NOT EXISTS rr_players (
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
);
CREATE TABLE IF NOT EXISTS srh_players (
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
);
CREATE TABLE IF NOT EXISTS gt_players (
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
);
CREATE TABLE IF NOT EXISTS lsg_players (
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
);
CREATE TABLE IF NOT EXISTS dc_players (
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
);
CREATE TABLE IF NOT EXISTS pbks_players (
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
);