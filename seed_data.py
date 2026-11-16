"""
Pre-populated authentic dataset of 10 Real IPL Franchises and 49 Marquee Star Players.
Features:
- Official IPL 2026 Mega Auction Rules:
  - Fixed Purse: ₹120.00 Crore per franchise
  - Squad Limits: Minimum 18, Maximum 25 players, Maximum 8 Overseas players
  - Pre-Auction Retentions & RTM Formula: Total (Retentions + RTM Cards) = 6
  - Mini Auction Rule: 0 RTM cards (RTM cannot be used in Mini Auction)
- Sequential Categorized Sets:
  - Set 1: Capped Batters (BA1)
  - Set 2: Capped All-rounders (AL1)
  - Set 3: Capped Wicketkeepers (WK1)
  - Set 4: Capped Fast Bowlers (FA1)
  - Set 5: Capped Spinners (SP1)
  - Set 6: Uncapped Players (UN1)
- Former IPL Team mapping for Right-To-Match (RTM) card execution.
"""

from typing import List, Dict, Any

# 10 Official IPL Franchises with exact team colors, ₹120 Cr Purse, Retentions, and RTM allocations
INITIAL_TEAMS: List[Dict[str, Any]] = [
    {
        "team_name": "Chennai Super Kings",
        "short_code": "CSK",
        "primary_color": "#FDB913",
        "secondary_color": "#0081E8",
        "total_budget": 1200000000.0,
        "remaining_budget": 550000000.0,  # ₹55 Cr after ₹65 Cr retentions
        "retention_spend": 650000000.0,
        "retentions_count": 5,
        "rtm_cards": 1,  # 6 - 5 = 1 in Mega Auction
        "retained_names": "Ruturaj Gaikwad, Ravindra Jadeja, MS Dhoni, Shivam Dube, Matheesha Pathirana",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Mumbai Indians",
        "short_code": "MI",
        "primary_color": "#004BA0",
        "secondary_color": "#D1AB3E",
        "total_budget": 1200000000.0,
        "remaining_budget": 450000000.0,  # ₹45 Cr after ₹75 Cr retentions
        "retention_spend": 750000000.0,
        "retentions_count": 5,
        "rtm_cards": 1,  # 6 - 5 = 1
        "retained_names": "Jasprit Bumrah, Suryakumar Yadav, Hardik Pandya, Rohit Sharma, Tilak Varma",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Royal Challengers Bengaluru",
        "short_code": "RCB",
        "primary_color": "#EC1C24",
        "secondary_color": "#2B2A29",
        "total_budget": 1200000000.0,
        "remaining_budget": 830000000.0,  # ₹83 Cr after ₹37 Cr retentions
        "retention_spend": 370000000.0,
        "retentions_count": 3,
        "rtm_cards": 3,  # 6 - 3 = 3
        "retained_names": "Virat Kohli, Rajat Patidar, Yash Dayal",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Kolkata Knight Riders",
        "short_code": "KKR",
        "primary_color": "#3A225D",
        "secondary_color": "#F7D54E",
        "total_budget": 1200000000.0,
        "remaining_budget": 510000000.0,  # ₹51 Cr after ₹69 Cr retentions
        "retention_spend": 690000000.0,
        "retentions_count": 6,
        "rtm_cards": 0,  # 6 - 6 = 0 (max 6 retained -> 0 RTM)
        "retained_names": "Rinku Singh, Andre Russell, Sunil Narine, Varun Chakaravarthy, Harshit Rana, Ramandeep Singh",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Rajasthan Royals",
        "short_code": "RR",
        "primary_color": "#EA1A85",
        "secondary_color": "#254AA5",
        "total_budget": 1200000000.0,
        "remaining_budget": 410000000.0,  # ₹41 Cr after ₹79 Cr retentions
        "retention_spend": 790000000.0,
        "retentions_count": 6,
        "rtm_cards": 0,  # 6 - 6 = 0
        "retained_names": "Sanju Samson, Yashasvi Jaiswal, Riyan Parag, Dhruv Jurel, Shimron Hetmyer, Sandeep Sharma",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Sunrisers Hyderabad",
        "short_code": "SRH",
        "primary_color": "#F26522",
        "secondary_color": "#000000",
        "total_budget": 1200000000.0,
        "remaining_budget": 450000000.0,  # ₹45 Cr after ₹75 Cr retentions
        "retention_spend": 750000000.0,
        "retentions_count": 5,
        "rtm_cards": 1,  # 6 - 5 = 1
        "retained_names": "Heinrich Klaasen, Pat Cummins, Abhishek Sharma, Travis Head, Nitish Kumar Reddy",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Gujarat Titans",
        "short_code": "GT",
        "primary_color": "#1C1C1C",
        "secondary_color": "#0B4973",
        "total_budget": 1200000000.0,
        "remaining_budget": 690000000.0,  # ₹69 Cr after ₹51 Cr retentions
        "retention_spend": 510000000.0,
        "retentions_count": 5,
        "rtm_cards": 1,  # 6 - 5 = 1
        "retained_names": "Rashid Khan, Shubman Gill, Sai Sudharsan, Rahul Tewatia, Shahrukh Khan",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Lucknow Super Giants",
        "short_code": "LSG",
        "primary_color": "#A72056",
        "secondary_color": "#0055A5",
        "total_budget": 1200000000.0,
        "remaining_budget": 690000000.0,  # ₹69 Cr after ₹51 Cr retentions
        "retention_spend": 510000000.0,
        "retentions_count": 5,
        "rtm_cards": 1,  # 6 - 5 = 1
        "retained_names": "Nicholas Pooran, Ravi Bishnoi, Mayank Yadav, Mohsin Khan, Ayush Badoni",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Delhi Capitals",
        "short_code": "DC",
        "primary_color": "#004C93",
        "secondary_color": "#E41B17",
        "total_budget": 1200000000.0,
        "remaining_budget": 730000000.0,  # ₹73 Cr after ₹47 Cr retentions
        "retention_spend": 470000000.0,
        "retentions_count": 4,
        "rtm_cards": 2,  # 6 - 4 = 2
        "retained_names": "Axar Patel, Kuldeep Yadav, Tristan Stubbs, Abishek Porel",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
    {
        "team_name": "Punjab Kings",
        "short_code": "PBKS",
        "primary_color": "#DD1F2D",
        "secondary_color": "#C3A25D",
        "total_budget": 1200000000.0,
        "remaining_budget": 1105000000.0,  # ₹110.5 Cr after ₹9.5 Cr retentions
        "retention_spend": 95000000.0,
        "retentions_count": 2,
        "rtm_cards": 4,  # 6 - 2 = 4
        "retained_names": "Shashank Singh, Prabhsimran Singh",
        "min_squad_size": 18,
        "max_squad_size": 25,
        "max_overseas": 8,
    },
]

# 49 Authentic IPL Star Players organized into official sets with former teams for RTM
INITIAL_PLAYERS: List[Dict[str, Any]] = [
    # ==================== SET 1: CAPPED BATTERS (BA1) ====================
    {
        "name": "Virat Kohli",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "RCB",
        "stats": {"matches": 252, "runs": 8004, "highest_score": 113, "batting_avg": 38.67, "strike_rate": 131.97, "fours": 705, "sixes": 272, "centuries": 8, "fifties": 55, "wickets": 4, "bowling_economy": 8.80, "bowling_avg": 92.00}
    },
    {
        "name": "Rohit Sharma",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "MI",
        "stats": {"matches": 257, "runs": 6628, "highest_score": 109, "batting_avg": 29.72, "strike_rate": 131.14, "fours": 599, "sixes": 280, "centuries": 2, "fifties": 43, "wickets": 15, "bowling_economy": 8.02, "bowling_avg": 30.20}
    },
    {
        "name": "Shubman Gill",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "GT",
        "stats": {"matches": 103, "runs": 3216, "highest_score": 129, "batting_avg": 37.84, "strike_rate": 135.70, "fours": 310, "sixes": 98, "centuries": 4, "fifties": 20, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Suryakumar Yadav",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "MI",
        "stats": {"matches": 150, "runs": 3594, "highest_score": 103, "batting_avg": 32.09, "strike_rate": 145.33, "fours": 382, "sixes": 130, "centuries": 2, "fifties": 24, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Yashasvi Jaiswal",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "RR",
        "stats": {"matches": 52, "runs": 1607, "highest_score": 124, "batting_avg": 32.14, "strike_rate": 150.61, "fours": 198, "sixes": 64, "centuries": 2, "fifties": 9, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Ruturaj Gaikwad",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "CSK",
        "stats": {"matches": 66, "runs": 2380, "highest_score": 108, "batting_avg": 41.75, "strike_rate": 136.86, "fours": 224, "sixes": 91, "centuries": 2, "fifties": 18, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Travis Head",
        "role": "Batsman",
        "country": "Australia",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "SRH",
        "stats": {"matches": 25, "runs": 772, "highest_score": 102, "batting_avg": 36.76, "strike_rate": 185.13, "fours": 88, "sixes": 43, "centuries": 1, "fifties": 5, "wickets": 2, "bowling_economy": 9.10, "bowling_avg": 45.00}
    },
    {
        "name": "Shreyas Iyer",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "KKR",
        "stats": {"matches": 115, "runs": 3127, "highest_score": 96, "batting_avg": 32.24, "strike_rate": 127.48, "fours": 277, "sixes": 113, "centuries": 0, "fifties": 21, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "David Warner",
        "role": "Batsman",
        "country": "Australia",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "DC",
        "stats": {"matches": 184, "runs": 6565, "highest_score": 126, "batting_avg": 40.52, "strike_rate": 139.77, "fours": 663, "sixes": 236, "centuries": 4, "fifties": 62, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Faf du Plessis",
        "role": "Batsman",
        "country": "South Africa",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "RCB",
        "stats": {"matches": 145, "runs": 4571, "highest_score": 96, "batting_avg": 35.99, "strike_rate": 136.37, "fours": 421, "sixes": 165, "centuries": 0, "fifties": 37, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Shikhar Dhawan",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 1: Capped Batters (BA1)",
        "set_code": "BA1",
        "is_capped": True,
        "former_team": "PBKS",
        "stats": {"matches": 222, "runs": 6769, "highest_score": 106, "batting_avg": 35.26, "strike_rate": 127.14, "fours": 768, "sixes": 152, "centuries": 2, "fifties": 51, "wickets": 4, "bowling_economy": 8.25, "bowling_avg": 16.50}
    },

    # ==================== SET 2: CAPPED ALL-ROUNDERS (AL1) ====================
    {
        "name": "Hardik Pandya",
        "role": "Allrounder",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "MI",
        "stats": {"matches": 137, "runs": 2525, "highest_score": 91, "batting_avg": 28.69, "strike_rate": 145.87, "fours": 196, "sixes": 134, "centuries": 0, "fifties": 10, "wickets": 64, "bowling_economy": 8.98, "bowling_avg": 33.20}
    },
    {
        "name": "Ravindra Jadeja",
        "role": "Allrounder",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "CSK",
        "stats": {"matches": 240, "runs": 2959, "highest_score": 62, "batting_avg": 27.40, "strike_rate": 129.78, "fours": 218, "sixes": 107, "centuries": 0, "fifties": 3, "wickets": 160, "bowling_economy": 7.60, "bowling_avg": 29.57}
    },
    {
        "name": "Andre Russell",
        "role": "Allrounder",
        "country": "West Indies",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "KKR",
        "stats": {"matches": 127, "runs": 2484, "highest_score": 88, "batting_avg": 29.22, "strike_rate": 174.93, "fours": 176, "sixes": 209, "centuries": 0, "fifties": 11, "wickets": 115, "bowling_economy": 9.25, "bowling_avg": 23.01}
    },
    {
        "name": "Sunil Narine",
        "role": "Allrounder",
        "country": "West Indies",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "KKR",
        "stats": {"matches": 177, "runs": 1534, "highest_score": 109, "batting_avg": 17.04, "strike_rate": 165.84, "fours": 167, "sixes": 98, "centuries": 1, "fifties": 7, "wickets": 180, "bowling_economy": 6.73, "bowling_avg": 25.39}
    },
    {
        "name": "Glenn Maxwell",
        "role": "Allrounder",
        "country": "Australia",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "RCB",
        "stats": {"matches": 134, "runs": 2771, "highest_score": 95, "batting_avg": 24.74, "strike_rate": 156.73, "fours": 236, "sixes": 158, "centuries": 0, "fifties": 18, "wickets": 37, "bowling_economy": 8.35, "bowling_avg": 35.50}
    },
    {
        "name": "Axar Patel",
        "role": "Allrounder",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "DC",
        "stats": {"matches": 150, "runs": 1653, "highest_score": 66, "batting_avg": 21.47, "strike_rate": 130.88, "fours": 125, "sixes": 72, "centuries": 0, "fifties": 4, "wickets": 123, "bowling_economy": 7.24, "bowling_avg": 30.50}
    },
    {
        "name": "Marcus Stoinis",
        "role": "Allrounder",
        "country": "Australia",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "LSG",
        "stats": {"matches": 96, "runs": 1866, "highest_score": 124, "batting_avg": 28.27, "strike_rate": 142.01, "fours": 152, "sixes": 91, "centuries": 1, "fifties": 9, "wickets": 43, "bowling_economy": 9.48, "bowling_avg": 31.60}
    },
    {
        "name": "Shivam Dube",
        "role": "Allrounder",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "CSK",
        "stats": {"matches": 65, "runs": 1502, "highest_score": 95, "batting_avg": 29.45, "strike_rate": 159.28, "fours": 98, "sixes": 97, "centuries": 0, "fifties": 9, "wickets": 5, "bowling_economy": 9.50, "bowling_avg": 42.00}
    },
    {
        "name": "Sam Curran",
        "role": "Allrounder",
        "country": "England",
        "base_price": 20000000.0,
        "set_name": "Set 2: Capped All-rounders (AL1)",
        "set_code": "AL1",
        "is_capped": True,
        "former_team": "PBKS",
        "stats": {"matches": 59, "runs": 883, "highest_score": 63, "batting_avg": 24.53, "strike_rate": 135.64, "fours": 76, "sixes": 41, "centuries": 0, "fifties": 4, "wickets": 58, "bowling_economy": 9.48, "bowling_avg": 31.50}
    },

    # ==================== SET 3: CAPPED WICKETKEEPERS (WK1) ====================
    {
        "name": "Rishabh Pant",
        "role": "Wicketkeeper",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "DC",
        "stats": {"matches": 111, "runs": 3284, "highest_score": 128, "batting_avg": 35.31, "strike_rate": 148.93, "fours": 296, "sixes": 154, "centuries": 1, "fifties": 18, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "MS Dhoni",
        "role": "Wicketkeeper",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "CSK",
        "stats": {"matches": 264, "runs": 5243, "highest_score": 84, "batting_avg": 39.13, "strike_rate": 137.53, "fours": 363, "sixes": 252, "centuries": 0, "fifties": 24, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Heinrich Klaasen",
        "role": "Wicketkeeper",
        "country": "South Africa",
        "base_price": 20000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "SRH",
        "stats": {"matches": 35, "runs": 993, "highest_score": 104, "batting_avg": 38.19, "strike_rate": 168.31, "fours": 66, "sixes": 64, "centuries": 1, "fifties": 6, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "KL Rahul",
        "role": "Wicketkeeper",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "LSG",
        "stats": {"matches": 132, "runs": 4683, "highest_score": 132, "batting_avg": 45.47, "strike_rate": 134.61, "fours": 415, "sixes": 187, "centuries": 4, "fifties": 37, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Sanju Samson",
        "role": "Wicketkeeper",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "RR",
        "stats": {"matches": 168, "runs": 4419, "highest_score": 119, "batting_avg": 30.69, "strike_rate": 138.96, "fours": 352, "sixes": 206, "centuries": 3, "fifties": 25, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Nicholas Pooran",
        "role": "Wicketkeeper",
        "country": "West Indies",
        "base_price": 20000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "LSG",
        "stats": {"matches": 76, "runs": 1769, "highest_score": 77, "batting_avg": 30.50, "strike_rate": 158.23, "fours": 113, "sixes": 128, "centuries": 0, "fifties": 9, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Jos Buttler",
        "role": "Wicketkeeper",
        "country": "England",
        "base_price": 20000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "RR",
        "stats": {"matches": 107, "runs": 3582, "highest_score": 124, "batting_avg": 37.71, "strike_rate": 147.53, "fours": 359, "sixes": 161, "centuries": 7, "fifties": 19, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Phil Salt",
        "role": "Wicketkeeper",
        "country": "England",
        "base_price": 15000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "KKR",
        "stats": {"matches": 21, "runs": 653, "highest_score": 89, "batting_avg": 36.28, "strike_rate": 175.54, "fours": 79, "sixes": 34, "centuries": 0, "fifties": 6, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Ishan Kishan",
        "role": "Wicketkeeper",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 3: Capped Wicketkeepers (WK1)",
        "set_code": "WK1",
        "is_capped": True,
        "former_team": "MI",
        "stats": {"matches": 105, "runs": 2644, "highest_score": 99, "batting_avg": 28.43, "strike_rate": 135.87, "fours": 267, "sixes": 118, "centuries": 0, "fifties": 16, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },

    # ==================== SET 4: CAPPED FAST BOWLERS (FA1) ====================
    {
        "name": "Jasprit Bumrah",
        "role": "Bowler",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "MI",
        "stats": {"matches": 133, "runs": 69, "highest_score": 16, "batting_avg": 9.85, "strike_rate": 95.83, "fours": 6, "sixes": 1, "centuries": 0, "fifties": 0, "wickets": 165, "bowling_economy": 7.30, "bowling_avg": 22.51}
    },
    {
        "name": "Mitchell Starc",
        "role": "Bowler",
        "country": "Australia",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "KKR",
        "stats": {"matches": 41, "runs": 115, "highest_score": 29, "batting_avg": 11.50, "strike_rate": 108.49, "fours": 10, "sixes": 3, "centuries": 0, "fifties": 0, "wickets": 51, "bowling_economy": 8.21, "bowling_avg": 24.12}
    },
    {
        "name": "Pat Cummins",
        "role": "Bowler",
        "country": "Australia",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "SRH",
        "stats": {"matches": 58, "runs": 515, "highest_score": 66, "batting_avg": 18.39, "strike_rate": 151.47, "fours": 38, "sixes": 31, "centuries": 0, "fifties": 3, "wickets": 63, "bowling_economy": 8.95, "bowling_avg": 30.12}
    },
    {
        "name": "Mohammed Shami",
        "role": "Bowler",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "GT",
        "stats": {"matches": 110, "runs": 79, "highest_score": 21, "batting_avg": 7.90, "strike_rate": 90.80, "fours": 7, "sixes": 2, "centuries": 0, "fifties": 0, "wickets": 127, "bowling_economy": 8.44, "bowling_avg": 26.87}
    },
    {
        "name": "Trent Boult",
        "role": "Bowler",
        "country": "New Zealand",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "RR",
        "stats": {"matches": 104, "runs": 51, "highest_score": 17, "batting_avg": 6.37, "strike_rate": 86.44, "fours": 4, "sixes": 1, "centuries": 0, "fifties": 0, "wickets": 121, "bowling_economy": 8.29, "bowling_avg": 26.51}
    },
    {
        "name": "Kagiso Rabada",
        "role": "Bowler",
        "country": "South Africa",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "PBKS",
        "stats": {"matches": 80, "runs": 186, "highest_score": 44, "batting_avg": 11.62, "strike_rate": 103.91, "fours": 16, "sixes": 6, "centuries": 0, "fifties": 0, "wickets": 117, "bowling_economy": 8.42, "bowling_avg": 22.15}
    },
    {
        "name": "Arshdeep Singh",
        "role": "Bowler",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "PBKS",
        "stats": {"matches": 65, "runs": 28, "highest_score": 10, "batting_avg": 5.60, "strike_rate": 70.00, "fours": 2, "sixes": 1, "centuries": 0, "fifties": 0, "wickets": 76, "bowling_economy": 9.03, "bowling_avg": 27.00}
    },
    {
        "name": "Bhuvneshwar Kumar",
        "role": "Bowler",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "SRH",
        "stats": {"matches": 176, "runs": 312, "highest_score": 27, "batting_avg": 8.66, "strike_rate": 96.29, "fours": 28, "sixes": 6, "centuries": 0, "fifties": 0, "wickets": 181, "bowling_economy": 7.56, "bowling_avg": 27.23}
    },
    {
        "name": "Mohammed Siraj",
        "role": "Bowler",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "RCB",
        "stats": {"matches": 93, "runs": 109, "highest_score": 14, "batting_avg": 7.78, "strike_rate": 81.34, "fours": 9, "sixes": 3, "centuries": 0, "fifties": 0, "wickets": 93, "bowling_economy": 8.65, "bowling_avg": 30.34}
    },

    # ==================== SET 5: CAPPED SPINNERS (SP1) ====================
    {
        "name": "Rashid Khan",
        "role": "Bowler",
        "country": "Afghanistan",
        "base_price": 20000000.0,
        "set_name": "Set 5: Capped Spinners (SP1)",
        "set_code": "SP1",
        "is_capped": True,
        "former_team": "GT",
        "stats": {"matches": 121, "runs": 543, "highest_score": 79, "batting_avg": 13.92, "strike_rate": 154.26, "fours": 42, "sixes": 36, "centuries": 0, "fifties": 1, "wickets": 149, "bowling_economy": 6.82, "bowling_avg": 21.82}
    },
    {
        "name": "Yuzvendra Chahal",
        "role": "Bowler",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 5: Capped Spinners (SP1)",
        "set_code": "SP1",
        "is_capped": True,
        "former_team": "RR",
        "stats": {"matches": 160, "runs": 37, "highest_score": 8, "batting_avg": 4.11, "strike_rate": 43.52, "fours": 1, "sixes": 0, "centuries": 0, "fifties": 0, "wickets": 205, "bowling_economy": 7.80, "bowling_avg": 22.45}
    },
    {
        "name": "Kuldeep Yadav",
        "role": "Bowler",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 5: Capped Spinners (SP1)",
        "set_code": "SP1",
        "is_capped": True,
        "former_team": "DC",
        "stats": {"matches": 84, "runs": 114, "highest_score": 16, "batting_avg": 9.50, "strike_rate": 78.62, "fours": 8, "sixes": 2, "centuries": 0, "fifties": 0, "wickets": 87, "bowling_economy": 8.13, "bowling_avg": 26.97}
    },
    {
        "name": "Varun Chakaravarthy",
        "role": "Bowler",
        "country": "India",
        "base_price": 15000000.0,
        "set_name": "Set 5: Capped Spinners (SP1)",
        "set_code": "SP1",
        "is_capped": True,
        "former_team": "KKR",
        "stats": {"matches": 71, "runs": 24, "highest_score": 7, "batting_avg": 4.80, "strike_rate": 60.00, "fours": 2, "sixes": 0, "centuries": 0, "fifties": 0, "wickets": 83, "bowling_economy": 7.56, "bowling_avg": 25.10}
    },

    # ==================== SET 6: UNCAPPED PLAYERS (UN1) ====================
    {
        "name": "Sai Sudharsan",
        "role": "Batsman",
        "country": "India",
        "base_price": 4000000.0,  # ₹40 Lakhs Uncapped tier
        "set_name": "Set 6: Uncapped Players (UN1)",
        "set_code": "UN1",
        "is_capped": False,
        "former_team": "GT",
        "stats": {"matches": 25, "runs": 1039, "highest_score": 103, "batting_avg": 47.23, "strike_rate": 139.09, "fours": 110, "sixes": 27, "centuries": 1, "fifties": 6, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Abhishek Sharma",
        "role": "Allrounder",
        "country": "India",
        "base_price": 4000000.0,
        "set_name": "Set 6: Uncapped Players (UN1)",
        "set_code": "UN1",
        "is_capped": False,
        "former_team": "SRH",
        "stats": {"matches": 63, "runs": 1377, "highest_score": 75, "batting_avg": 25.50, "strike_rate": 155.24, "fours": 136, "sixes": 68, "centuries": 0, "fifties": 7, "wickets": 9, "bowling_economy": 8.85, "bowling_avg": 34.20}
    },
    {
        "name": "Rinku Singh",
        "role": "Batsman",
        "country": "India",
        "base_price": 4000000.0,
        "set_name": "Set 6: Uncapped Players (UN1)",
        "set_code": "UN1",
        "is_capped": False,
        "former_team": "KKR",
        "stats": {"matches": 45, "runs": 893, "highest_score": 67, "batting_avg": 30.79, "strike_rate": 143.34, "fours": 68, "sixes": 48, "centuries": 0, "fifties": 4, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Tilak Varma",
        "role": "Batsman",
        "country": "India",
        "base_price": 4000000.0,
        "set_name": "Set 6: Uncapped Players (UN1)",
        "set_code": "UN1",
        "is_capped": False,
        "former_team": "MI",
        "stats": {"matches": 38, "runs": 1156, "highest_score": 84, "batting_avg": 39.86, "strike_rate": 146.33, "fours": 95, "sixes": 55, "centuries": 0, "fifties": 6, "wickets": 0, "bowling_economy": 0.00, "bowling_avg": 0.00}
    },
    {
        "name": "Matheesha Pathirana",
        "role": "Bowler",
        "country": "Sri Lanka",
        "base_price": 4000000.0,
        "set_name": "Set 6: Uncapped Players (UN1)",
        "set_code": "UN1",
        "is_capped": False,
        "former_team": "CSK",
        "stats": {"matches": 20, "runs": 0, "highest_score": 0, "batting_avg": 0.00, "strike_rate": 0.00, "fours": 0, "sixes": 0, "centuries": 0, "fifties": 0, "wickets": 34, "bowling_economy": 7.88, "bowling_avg": 17.50}
    },
    {
        "name": "Mayank Yadav",
        "role": "Bowler",
        "country": "India",
        "base_price": 4000000.0,
        "set_name": "Set 6: Uncapped Players (UN1)",
        "set_code": "UN1",
        "is_capped": False,
        "former_team": "LSG",
        "stats": {"matches": 4, "runs": 0, "highest_score": 0, "batting_avg": 0.00, "strike_rate": 0.00, "fours": 0, "sixes": 0, "centuries": 0, "fifties": 0, "wickets": 7, "bowling_economy": 6.98, "bowling_avg": 12.14}
    },
    {
        "name": "Harshal Patel",
        "role": "Bowler",
        "country": "India",
        "base_price": 20000000.0,
        "set_name": "Set 4: Capped Fast Bowlers (FA1)",
        "set_code": "FA1",
        "is_capped": True,
        "former_team": "PBKS",
        "stats": {"matches": 105, "runs": 236, "highest_score": 36, "batting_avg": 11.23, "strike_rate": 131.11, "fours": 20, "sixes": 11, "centuries": 0, "fifties": 0, "wickets": 135, "bowling_economy": 8.62, "bowling_avg": 23.33}
    },
]
