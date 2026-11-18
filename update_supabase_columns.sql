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

-- 2. Reset teams to 100% fresh auction starting state (₹120 Cr, 0 retentions, 6 RTMs)
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'CSK';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'MI';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'RCB';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'KKR';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'RR';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'SRH';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'GT';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'LSG';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'DC';
UPDATE teams SET 
    total_budget = 1200000000.00,
    remaining_budget = 1200000000.00,
    retention_spend = 0.00,
    retentions_count = 0,
    rtm_cards = 6,
    retained_names = '',
    min_squad_size = 18,
    max_squad_size = 25,
    max_overseas = 8
WHERE UPPER(short_code) = 'PBKS';

-- 2b. Reset all players to Available (0 bought, 0 sold)
UPDATE players SET
    status = 'Available',
    sold_price = 0.00,
    team_id = NULL,
    accelerated = 0;

-- 2c. Clear all auction bids and bought squad records
DELETE FROM auction_bids;
DELETE FROM csk_players;
DELETE FROM mi_players;
DELETE FROM rcb_players;
DELETE FROM kkr_players;
DELETE FROM rr_players;
DELETE FROM srh_players;
DELETE FROM gt_players;
DELETE FROM lsg_players;
DELETE FROM dc_players;
DELETE FROM pbks_players;

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
    former_team = 'PBKS'
WHERE name = 'Shikhar Dhawan';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'DC'
WHERE name = 'David Warner';
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
    former_team = 'LSG'
WHERE name = 'KL Rahul';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Ajinkya Rahane';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Suryakumar Yadav';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Sanju Samson';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'RCB'
WHERE name = 'Faf du Plessis';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'RR'
WHERE name = 'Jos Buttler';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Manish Pandey';
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
    former_team = 'KKR'
WHERE name = 'Shreyas Iyer';
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
    is_overseas = 1,
    former_team = 'LSG'
WHERE name = 'Quinton de Kock';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Ravindra Jadeja';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'GT'
WHERE name = 'David Miller';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'RCB'
WHERE name = 'Glenn Maxwell';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Hardik Pandya';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Ruturaj Gaikwad';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'KKR'
WHERE name = 'Andre Russell';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'LSG'
WHERE name = 'Nicholas Pooran';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Yashasvi Jaiswal';
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
    is_overseas = 1,
    former_team = 'KKR'
WHERE name = 'Sunil Narine';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'SRH'
WHERE name = 'Heinrich Klaasen';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'SRH'
WHERE name = 'Travis Head';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'PBKS'
WHERE name = 'Liam Livingstone';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'PBKS'
WHERE name = 'Sam Curran';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'SRH'
WHERE name = 'Pat Cummins';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'GT'
WHERE name = 'Rashid Khan';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Shardul Thakur';
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
    former_team = 'PBKS'
WHERE name = 'Harshal Patel';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'PBKS'
WHERE name = 'Kagiso Rabada';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Kuldeep Yadav';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Jaydev Unadkat';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Mohammed Siraj';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'KKR'
WHERE name = 'Mitchell Starc';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'RR'
WHERE name = 'Trent Boult';
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
    former_team = 'MI'
WHERE name = 'Jasprit Bumrah';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Sandeep Sharma';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Yuzvendra Chahal';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Arshdeep Singh';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Varun Chakaravarthy';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Ishan Kishan';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Nitish Rana';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Rahul Tripathi';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'LSG'
WHERE name = 'Marcus Stoinis';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Prithvi Shaw';
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
    former_team = 'SRH'
WHERE name = 'Abhishek Sharma';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Devdutt Padikkal';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'GT'
WHERE name = 'Sai Sudharsan';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Krunal Pandya';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Karun Nair';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Riyan Parag';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Tilak Varma';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Rajat Patidar';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Rinku Singh';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'KKR'
WHERE name = 'Phil Salt';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Jitesh Sharma';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'DC'
WHERE name = 'Tristan Stubbs';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Jofra Archer';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Shreyas Gopal';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Marco Jansen';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Rahul Chahar';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Deepak Chahar';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Lockie Ferguson';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Avesh Khan';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Ishant Sharma';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'DC'
WHERE name = 'Anrich Nortje';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Ravi Bishnoi';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Tushar Deshpande';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Josh Hazlewood';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Mukesh Kumar';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Prasidh Krishna';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'T. Natarajan';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Khaleel Ahmed';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'CSK'
WHERE name = 'Matheesha Pathirana';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'RR'
WHERE name = 'Shimron Hetmyer';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Venkatesh Iyer';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Aiden Markram';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'DC'
WHERE name = 'Mitchell Marsh';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'GT'
WHERE name = 'Rahul Tewatia';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'MI'
WHERE name = 'Tim David';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'RCB'
WHERE name = 'Cameron Green';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RR'
WHERE name = 'Dhruv Jurel';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Washington Sundar';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Nitish Kumar Reddy';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'RCB'
WHERE name = 'Will Jacks';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Jason Holder';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Mitchell Santner';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Wanindu Hasaranga';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Glenn Phillips';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Shivam Mavi';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Mayank Markande';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 1,
    former_team = 'GT'
WHERE name = 'Noor Ahmad';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Nathan Ellis';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'GT'
WHERE name = 'Sai Kishore';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Yash Dayal';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Lungisani Ngidi';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Shahbaz Ahamad';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Dewald Brevis';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Sarfaraz Khan';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Rachin Ravindra';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Sherfane Rutherford';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Ryan Rickelton';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Rovman Powell';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Josh Inglis';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Romario Shepherd';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Azmatullah Omarzai';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Kamindu Mendis';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Jacob Bethell';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Kyle Jamieson';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Dushmantha Chameera';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Corbin Bosch';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Jayant Yadav';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Tim Seifert';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Adam Milne';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Umran Malik';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Tom Banton';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Jamie Overton';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Vyshak Vijaykumar';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Matthew Breetzke';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Xavier Bartlett';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Donovan Ferreira';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Luke Wood';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Kwena Maphaka';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Mukesh Choudhary';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Eshan Malinga';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Nuwan Thushara';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Nandre Burger';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Matt Henry';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Akeal Hosein';
UPDATE players SET
    set_name = 'Set 5: Capped Spinners (SP1)',
    set_code = 'SP1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Allah Ghazanfar';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Ben Duckett';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Ben Dwarshuis';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Blessing Muzarabani';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Brydon Carse';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Cooper Connolly';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Finn Allen';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Jack Edwards';
UPDATE players SET
    set_name = 'Set 4: Capped Fast Bowlers (FA1)',
    set_code = 'FA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Jacob Duffy';
UPDATE players SET
    set_name = 'Set 3: Capped Wicketkeepers (WK1)',
    set_code = 'WK1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Jordan Cox';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Lhuan-dre Pretorius';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Matt Short';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Mitch Owen';
UPDATE players SET
    set_name = 'Set 1: Capped Batters (BA1)',
    set_code = 'BA1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Pathum Nissanka';
UPDATE players SET
    set_name = 'Set 2: Capped All-rounders (AL1)',
    set_code = 'AL1',
    is_capped = 1,
    is_overseas = 1,
    former_team = NULL
WHERE name = 'Zak Foulkes';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Prabhsimran Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Ayush Badoni';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Shashank Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'SRH'
WHERE name = 'Abdul Samad';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'GT'
WHERE name = 'Shahrukh Khan';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Nehal Wadhera';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'DC'
WHERE name = 'Abishek Porel';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Priyansh Arya';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Angkrish Raghuvanshi';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Harpreet Brar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Harshit Rana';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Mohsin Khan';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Vaibhav Arora';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Yash Thakur';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Suyash Sharma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'PBKS'
WHERE name = 'Ashutosh Sharma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Naman Dhir';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Anuj Rawat';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Vaibhav Suryavanshi';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Ayush Mhatre';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Aniket Verma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'KKR'
WHERE name = 'Ramandeep Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'CSK'
WHERE name = 'Sameer Rizvi';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Vipraj Nigam';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Mohd. Arshad Khan';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'RCB'
WHERE name = 'Swapnil Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Rasikh Salam';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Anukul Roy';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Akash Deep';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Yudhvir Singh Charak';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Anshul Kamboj';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Kartik Tyagi';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Digvesh Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Kuldeep Sen';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Ashwani Kumar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Akash Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'LSG'
WHERE name = 'Mayank Yadav';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Vignesh Puthur';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Zeeshan Ansari';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Shubham Dubey';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Urvil Patel';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Vishnu Vinod';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Pravin Dubey';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Raj Angad Bawa';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = 'MI'
WHERE name = 'Arjun Tendulkar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Arshin Kulkarni';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Suryansh Shedge';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Robin Minz';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Prince Yadav';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Kumar Kushagra';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Madhav Tiwari';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Manav Suthar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Harsh Dubey';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'M. Siddharth';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Musheer Khan';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Prithvi Raj Yarra';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Abhinandan Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Ajay Mandal';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Akshat Raghuwanshi';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Aman Khan';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Aman Rao Perala';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Amit Kumar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Ashok Sharma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Atharva Ankolekar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Auqib Dar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Brijesh Sharma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Daksh Kamra';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Danish Malewar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Gurjapneet Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Gurnoor Singh Brar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Harnoor Pannu';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Himmat Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Kanishk Chouhan';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Kartik Sharma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Krains Fuletra';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Mangesh Yadav';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Mayank Rawat';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Mohammad Izhar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Mukul Choudhary';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Naman Tiwari';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Nishant Sindhu';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Onkar Tarmale';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Praful Hinge';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Prashant Solanki';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Prashant Veer';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Pyla Avinash';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Raghu Sharma';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Ramakrishna Ghosh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Ravi Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Sahil Parakh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Sakib Hussain';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Salil Arora';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Sarthak Ranjan';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Satvik Deswal';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Shivang Kumar';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Smaran Ravichandran';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Sushant Mishra';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Tejasvi Singh';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Tripurana Vijay';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Vicky Ostwal';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Vihaan Malhotra';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Vishal Nishad';
UPDATE players SET
    set_name = 'Set 6: Uncapped Players (UN1)',
    set_code = 'UN1',
    is_capped = 0,
    is_overseas = 0,
    former_team = NULL
WHERE name = 'Yash Raj Punja';

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