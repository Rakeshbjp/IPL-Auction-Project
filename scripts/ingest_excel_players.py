"""
Ingest all players from cricket_data_2026.csv into seed_data.py and ipl_auction.db
Aggregates career totals across all historical seasons and classifies:
- Roles: Batsman, Bowler, Allrounder, Wicketkeeper
- Capped vs Uncapped status
- Overseas vs Indian
- Base Price categories
- Auction Sets: BA1, AL1, WK1, FA1, SP1, UN1
- Former IPL Franchise
"""

import csv
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = Path(r"C:\Users\srake\.gemini\antigravity\brain\7f3628bc-367c-4cb8-924b-cde0ad934438\.user_uploaded\media_1795014208313_3952e021.csv")
DB_PATH = BASE_DIR / "ipl_auction.db"

# Canonical name aliases
NAME_ALIASES = {
    "Surya Kumar Yadav": "Suryakumar Yadav",
    "N. Tilak Varma": "Tilak Varma",
    "Mohammad Shami": "Mohammed Shami",
    "Rasikh Dar": "Rasikh Salam",
    "Matthew William Short": "Matt Short",
}

# Country mapping for Overseas players (default is India)
OVERSEAS_COUNTRY_MAP = {
    # Australia
    "Pat Cummins": "Australia",
    "Travis Head": "Australia",
    "Mitchell Marsh": "Australia",
    "Josh Hazlewood": "Australia",
    "Josh Inglis": "Australia",
    "Cameron Green": "Australia",
    "Marcus Stoinis": "Australia",
    "Tim David": "Australia",
    "Ben Dwarshuis": "Australia",
    "Cooper Connolly": "Australia",
    "Jack Edwards": "Australia",
    "Xavier Bartlett": "Australia",
    "Matthew William Short": "Australia",
    "Matt Short": "Australia",
    "Mitch Owen": "Australia",
    "Mitchell Starc": "Australia",
    "Nathan Ellis": "Australia",
    "David Warner": "Australia",
    "Glenn Maxwell": "Australia",
    "Spencer Johnson": "Australia",
    # England
    "Jos Buttler": "England",
    "Phil Salt": "England",
    "Sam Curran": "England",
    "Liam Livingstone": "England",
    "Will Jacks": "England",
    "Jofra Archer": "England",
    "Ben Duckett": "England",
    "Brydon Carse": "England",
    "Jacob Bethell": "England",
    "Luke Wood": "England",
    "Jordan Cox": "England",
    "Tom Banton": "England",
    "Jamie Overton": "England",
    "Moeen Ali": "England",
    # South Africa
    "Heinrich Klaasen": "South Africa",
    "Quinton de Kock": "South Africa",
    "Kagiso Rabada": "South Africa",
    "David Miller": "South Africa",
    "Anrich Nortje": "South Africa",
    "Tristan Stubbs": "South Africa",
    "Marco Jansen": "South Africa",
    "Donovan Ferreira": "South Africa",
    "Corbin Bosch": "South Africa",
    "Dewald Brevis": "South Africa",
    "Kwena Maphaka": "South Africa",
    "Lhuan-dre Pretorius": "South Africa",
    "Lungisani Ngidi": "South Africa",
    "Matthew Breetzke": "South Africa",
    "Nandre Burger": "South Africa",
    "Ryan Rickelton": "South Africa",
    "Aiden Markram": "South Africa",
    "Faf du Plessis": "South Africa",
    # West Indies
    "Nicholas Pooran": "West Indies",
    "Sunil Narine": "West Indies",
    "Shimron Hetmyer": "West Indies",
    "Romario Shepherd": "West Indies",
    "Rovman Powell": "West Indies",
    "Sherfane Rutherford": "West Indies",
    "Jason Holder": "West Indies",
    "Akeal Hosein": "West Indies",
    "Andre Russell": "West Indies",
    # New Zealand
    "Trent Boult": "New Zealand",
    "Rachin Ravindra": "New Zealand",
    "Mitchell Santner": "New Zealand",
    "Lockie Ferguson": "New Zealand",
    "Finn Allen": "New Zealand",
    "Glenn Phillips": "New Zealand",
    "Jacob Duffy": "New Zealand",
    "Kyle Jamieson": "New Zealand",
    "Matt Henry": "New Zealand",
    "Tim Seifert": "New Zealand",
    "Adam Milne": "New Zealand",
    "Zak Foulkes": "New Zealand",
    # Sri Lanka
    "Matheesha Pathirana": "Sri Lanka",
    "Wanindu Hasaranga": "Sri Lanka",
    "Nuwan Thushara": "Sri Lanka",
    "Dushmantha Chameera": "Sri Lanka",
    "Kamindu Mendis": "Sri Lanka",
    "Pathum Nissanka": "Sri Lanka",
    "Eshan Malinga": "Sri Lanka",
    # Afghanistan
    "Rashid Khan": "Afghanistan",
    "Noor Ahmad": "Afghanistan",
    "Allah Ghazanfar": "Afghanistan",
    "Azmatullah Omarzai": "Afghanistan",
    "Naveen-ul-Haq": "Afghanistan",
    "Rahmanullah Gurbaz": "Afghanistan",
    # Zimbabwe
    "Blessing Muzarabani": "Zimbabwe",
}

# Role Mapping
WICKETKEEPERS = {
    "MS Dhoni", "Rishabh Pant", "Sanju Samson", "KL Rahul", "Heinrich Klaasen",
    "Nicholas Pooran", "Jos Buttler", "Ishan Kishan", "Phil Salt", "Jitesh Sharma",
    "Quinton de Kock", "Prabhsimran Singh", "Dhruv Jurel", "Abishek Porel",
    "Ryan Rickelton", "Josh Inglis", "Kumar Kushagra", "Robin Minz", "Vishnu Vinod",
    "Donovan Ferreira", "Anuj Rawat", "Tom Banton", "Tim Seifert", "Jordan Cox",
    "Urvil Patel", "Salil Arora", "Mukul Choudhary", "Finn Allen", "Rahmanullah Gurbaz"
}

ALLROUNDERS = {
    "Hardik Pandya", "Ravindra Jadeja", "Glenn Maxwell", "Andre Russell", "Sunil Narine",
    "Axar Patel", "Marcus Stoinis", "Liam Livingstone", "Washington Sundar", "Sam Curran",
    "Mitchell Marsh", "Nitish Kumar Reddy", "Shahrukh Khan", "Rahul Tewatia", "Krunal Pandya",
    "Venkatesh Iyer", "Shivam Dube", "Riyan Parag", "Vijay Shankar", "Swapnil Singh",
    "Ramandeep Singh", "Harpreet Brar", "Deepak Chahar", "Shardul Thakur", "Romario Shepherd",
    "Marco Jansen", "Moeen Ali", "Rachin Ravindra", "Cameron Green", "Will Jacks",
    "Shahbaz Ahamad", "Abdul Samad", "Abhishek Sharma", "Ayush Badoni", "Anukul Roy",
    "Arjun Tendulkar", "Arshin Kulkarni", "Atharva Ankolekar", "Azmatullah Omarzai",
    "Cooper Connolly", "Corbin Bosch", "Glenn Phillips", "Jack Edwards", "Jacob Bethell",
    "Jason Holder", "Jayant Yadav", "Kamindu Mendis", "Manav Suthar", "Matthew William Short",
    "Matt Short", "Mitch Owen", "Mitchell Santner", "Naman Dhir", "Nishant Sindhu",
    "Nitish Rana", "Pravin Dubey", "Raj Angad Bawa", "Rovman Powell", "Suryansh Shedge",
    "Tripurana Vijay", "Wanindu Hasaranga", "Yudhvir Singh Charak", "Zak Foulkes", "Ajay Mandal",
    "Jamie Overton", "Harsh Dubey", "Prince Yadav", "Prashant Veer", "Anshul Kamboj"
}

BATSMEN = {
    "Virat Kohli", "Rohit Sharma", "Shubman Gill", "Yashasvi Jaiswal", "Ruturaj Gaikwad",
    "Suryakumar Yadav", "Travis Head", "Rinku Singh", "Sai Sudharsan", "Tilak Varma",
    "Rajat Patidar", "Shashank Singh", "David Miller", "Faf du Plessis", "Devdutt Padikkal",
    "Prithvi Shaw", "Rahul Tripathi", "Mayank Agarwal", "David Warner", "Shikhar Dhawan",
    "Shimron Hetmyer", "Tristan Stubbs", "Nehal Wadhera", "Sameer Rizvi", "Ashutosh Sharma",
    "Angkrish Raghuvanshi", "Aiden Markram", "Ajinkya Rahane", "Akshat Raghuwanshi",
    "Aman Khan", "Aman Rao Perala", "Amit Kumar", "Aniket Verma", "Ayush Mhatre",
    "Ben Duckett", "Brijesh Sharma", "Daksh Kamra", "Danish Malewar", "Dewald Brevis",
    "Harnoor Pannu", "Himmat Singh", "Kanishk Chouhan", "Karun Nair", "Krains Fuletra",
    "Lhuan-dre Pretorius", "Madhav Tiwari", "Manish Pandey", "Matthew Breetzke",
    "Mayank Rawat", "Musheer Khan", "Pathum Nissanka", "Priyansh Arya", "Pyla Avinash",
    "Ravi Singh", "Sahil Parakh", "Sarfaraz Khan", "Sarthak Ranjan", "Satvik Deswal",
    "Sherfane Rutherford", "Shivang Kumar", "Shreyas Iyer", "Shubham Dubey",
    "Smaran Ravichandran", "Tejasvi Singh", "Tim David", "Vaibhav Suryavanshi",
    "Vihaan Malhotra", "Vishal Nishad"
}

# Spinners for set SP1 classification
SPINNERS = {
    "Kuldeep Yadav", "Yuzvendra Chahal", "Rashid Khan", "Varun Chakaravarthy",
    "Ravi Bishnoi", "Rahul Chahar", "Noor Ahmad", "Suyash Sharma", "Mayank Markande",
    "Shreyas Gopal", "M. Siddharth", "Manav Suthar", "Vicky Ostwal", "Prashant Solanki",
    "Akeal Hosein", "Allah Ghazanfar", "Zeeshan Ansari", "Raghu Sharma", "Digvesh Singh"
}

# Former team mapping for RTM
FORMER_TEAM_MAP = {
    "Virat Kohli": "RCB", "Rajat Patidar": "RCB", "Yash Dayal": "RCB", "Glenn Maxwell": "RCB",
    "Mohammed Siraj": "RCB", "Faf du Plessis": "RCB", "Will Jacks": "RCB", "Cameron Green": "RCB",
    "Swapnil Singh": "RCB", "Anuj Rawat": "RCB",
    "Jasprit Bumrah": "MI", "Suryakumar Yadav": "MI", "Hardik Pandya": "MI", "Rohit Sharma": "MI",
    "Tilak Varma": "MI", "Ishan Kishan": "MI", "Tim David": "MI", "Nehal Wadhera": "MI",
    "Naman Dhir": "MI", "Piyush Chawla": "MI", "Akash Madhwal": "MI", "Arjun Tendulkar": "MI",
    "Ruturaj Gaikwad": "CSK", "Ravindra Jadeja": "CSK", "MS Dhoni": "CSK", "Shivam Dube": "CSK",
    "Matheesha Pathirana": "CSK", "Deepak Chahar": "CSK", "Tushar Deshpande": "CSK",
    "Ajinkya Rahane": "CSK", "Shardul Thakur": "CSK", "Sameer Rizvi": "CSK", "Mukesh Choudhary": "CSK",
    "Rinku Singh": "KKR", "Andre Russell": "KKR", "Sunil Narine": "KKR", "Varun Chakaravarthy": "KKR",
    "Harshit Rana": "KKR", "Ramandeep Singh": "KKR", "Shreyas Iyer": "KKR", "Mitchell Starc": "KKR",
    "Phil Salt": "KKR", "Venkatesh Iyer": "KKR", "Nitish Rana": "KKR", "Vaibhav Arora": "KKR",
    "Sanju Samson": "RR", "Yashasvi Jaiswal": "RR", "Riyan Parag": "RR", "Dhruv Jurel": "RR",
    "Shimron Hetmyer": "RR", "Sandeep Sharma": "RR", "Jos Buttler": "RR", "Yuzvendra Chahal": "RR",
    "Ravichandran Ashwin": "RR", "Trent Boult": "RR", "Avesh Khan": "RR", "Prasidh Krishna": "RR",
    "Heinrich Klaasen": "SRH", "Pat Cummins": "SRH", "Abhishek Sharma": "SRH", "Travis Head": "SRH",
    "Nitish Kumar Reddy": "SRH", "Bhuvneshwar Kumar": "SRH", "T. Natarajan": "SRH", "Abdul Samad": "SRH",
    "Rahul Tripathi": "SRH", "Mayank Agarwal": "SRH", "Umran Malik": "SRH", "Washington Sundar": "SRH",
    "Rashid Khan": "GT", "Shubman Gill": "GT", "Sai Sudharsan": "GT", "Rahul Tewatia": "GT",
    "Shahrukh Khan": "GT", "Mohammed Shami": "GT", "David Miller": "GT", "Mohit Sharma": "GT",
    "Noor Ahmad": "GT", "Sai Kishore": "GT", "Umesh Yadav": "GT",
    "Nicholas Pooran": "LSG", "Ravi Bishnoi": "LSG", "Mayank Yadav": "LSG", "Mohsin Khan": "LSG",
    "Ayush Badoni": "LSG", "KL Rahul": "LSG", "Marcus Stoinis": "LSG", "Quinton de Kock": "LSG",
    "Krunal Pandya": "LSG", "Naveen-ul-Haq": "LSG", "Yash Thakur": "LSG",
    "Axar Patel": "DC", "Kuldeep Yadav": "DC", "Tristan Stubbs": "DC", "Abishek Porel": "DC",
    "Rishabh Pant": "DC", "David Warner": "DC", "Mitchell Marsh": "DC", "Khaleel Ahmed": "DC",
    "Mukesh Kumar": "DC", "Ishant Sharma": "DC", "Prithvi Shaw": "DC", "Anrich Nortje": "DC",
    "Shashank Singh": "PBKS", "Prabhsimran Singh": "PBKS", "Arshdeep Singh": "PBKS", "Sam Curran": "PBKS",
    "Liam Livingstone": "PBKS", "Kagiso Rabada": "PBKS", "Harshal Patel": "PBKS", "Jitesh Sharma": "PBKS",
    "Ashutosh Sharma": "PBKS", "Harpreet Brar": "PBKS", "Rahul Chahar": "PBKS",
}

# Uncapped players classification
UNCAPPED_PLAYERS = {
    "Shashank Singh", "Prabhsimran Singh", "Harpreet Brar", "Ashutosh Sharma",
    "Angkrish Raghuvanshi", "Sameer Rizvi", "Nehal Wadhera", "Naman Dhir",
    "Kumar Kushagra", "Robin Minz", "Swapnil Singh", "Vaibhav Suryavanshi",
    "Rasikh Salam", "Vaibhav Arora", "Vipraj Nigam", "Abhinandan Singh",
    "Ajay Mandal", "Akshat Raghuwanshi", "Aman Khan", "Aman Rao Perala",
    "Amit Kumar", "Aniket Verma", "Anshul Kamboj", "Arjun Tendulkar",
    "Arshin Kulkarni", "Ashok Sharma", "Ashwani Kumar", "Atharva Ankolekar",
    "Auqib Dar", "Ayush Mhatre", "Brijesh Sharma", "Daksh Kamra",
    "Danish Malewar", "Digvesh Singh", "Gurjapneet Singh", "Gurnoor Singh Brar",
    "Harnoor Pannu", "Harsh Dubey", "Himmat Singh", "Kanishk Chouhan",
    "Kartik Sharma", "Kartik Tyagi", "Krains Fuletra", "Madhav Tiwari",
    "Manav Suthar", "Mangesh Yadav", "Mayank Rawat", "Mohammad Izhar",
    "Mohd. Arshad Khan", "Mukul Choudhary", "Musheer Khan", "Naman Tiwari",
    "Nishant Sindhu", "Onkar Tarmale", "Praful Hinge", "Prashant Solanki",
    "Prashant Veer", "Pravin Dubey", "Prince Yadav", "Prithvi Raj Yarra",
    "Priyansh Arya", "Pyla Avinash", "Raghu Sharma", "Raj Angad Bawa",
    "Ramakrishna Ghosh", "Ravi Singh", "Sahil Parakh", "Sakib Hussain",
    "Salil Arora", "Sarthak Ranjan", "Satvik Deswal", "Shivang Kumar",
    "Shubham Dubey", "Smaran Ravichandran", "Suryansh Shedge", "Sushant Mishra",
    "Tejasvi Singh", "Tripurana Vijay", "Urvil Patel", "Vicky Ostwal",
    "Vignesh Puthur", "Vihaan Malhotra", "Vishal Nishad", "Yash Raj Punja",
    "Yash Thakur", "Yudhvir Singh Charak", "Zeeshan Ansari", "Abishek Porel",
    "Anuj Rawat", "Suyash Sharma", "Mayank Yadav", "Mohsin Khan", "Harshit Rana",
    "Ramandeep Singh", "Rasikh Dar", "Ayush Badoni", "Shahrukh Khan", "Abdul Samad"
}

# Marquee ₹2.00 Cr (20,000,000) players
TIER_2CR = {
    "Virat Kohli", "Rohit Sharma", "Jasprit Bumrah", "Rishabh Pant", "Heinrich Klaasen",
    "Pat Cummins", "Mitchell Starc", "Travis Head", "KL Rahul", "Jos Buttler",
    "Shreyas Iyer", "Arshdeep Singh", "Yuzvendra Chahal", "Mohammed Shami", "Mohammed Siraj",
    "Ravindra Jadeja", "Hardik Pandya", "Suryakumar Yadav", "Rashid Khan", "Nicholas Pooran",
    "Sanju Samson", "Shubman Gill", "Yashasvi Jaiswal", "Ruturaj Gaikwad", "Axar Patel",
    "Kuldeep Yadav", "Trent Boult", "Kagiso Rabada", "Glenn Maxwell", "Andre Russell",
    "Sunil Narine", "Faf du Plessis", "David Warner", "Liam Livingstone", "Sam Curran"
}

# ₹1.50 Cr (15,000,000) players
TIER_1_5CR = {
    "Rinku Singh", "Tilak Varma", "Rajat Patidar", "Sai Sudharsan", "Shivam Dube",
    "Matheesha Pathirana", "Harshal Patel", "Avesh Khan", "Khaleel Ahmed", "Mukesh Kumar",
    "Tushar Deshpande", "Bhuvneshwar Kumar", "Deepak Chahar", "Shardul Thakur", "Ishan Kishan",
    "Phil Salt", "Jitesh Sharma", "Quinton de Kock", "David Miller", "Anrich Nortje",
    "Tristan Stubbs", "Marco Jansen", "Marcus Stoinis", "Lockie Ferguson", "Devdutt Padikkal",
    "Prithvi Shaw", "Rahul Tripathi", "Ajinkya Rahane", "Ravichandran Ashwin", "Dinesh Karthik"
}

# ₹1.00 Cr (10,000,000) players
TIER_1CR = {
    "Nitish Kumar Reddy", "Dhruv Jurel", "Varun Chakaravarthy", "Sandeep Sharma",
    "Ravi Bishnoi", "Rahul Chahar", "Washington Sundar", "Krunal Pandya", "Venkatesh Iyer",
    "Riyan Parag", "Noor Ahmad", "Wanindu Hasaranga", "Will Jacks", "Cameron Green",
    "Glenn Phillips", "Jason Holder", "Jofra Archer", "Josh Hazlewood", "Nathan Ellis"
}


def to_int(v):
    try:
        return int(float(str(v).replace("*", "").strip()))
    except:
        return 0


def to_float(v):
    try:
        return float(str(v).replace("*", "").strip())
    except:
        return 0.0


def main():
    print(f"Reading CSV from {CSV_PATH}...")
    with open(CSV_PATH, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        rows_by_player = defaultdict(list)
        for r in reader:
            raw_name = r.get("Player_Name", "").strip()
            if raw_name:
                name = NAME_ALIASES.get(raw_name, raw_name)
                rows_by_player[name].append(r)

    print(f"Found {len(rows_by_player)} unique players in CSV.")

    # Aggregate career stats per player
    all_players_data = []

    for name, rows in rows_by_player.items():
        # Aggregated stats
        tot_matches = sum(max(to_int(r.get("Matches_Batted", 0)), to_int(r.get("Matches_Bowled", 0))) for r in rows)
        tot_runs = sum(to_int(r.get("Runs_Scored", 0)) for r in rows)
        tot_balls_faced = sum(to_int(r.get("Balls_Faced", 0)) for r in rows)
        tot_outs = sum(to_int(r.get("Matches_Batted", 0)) - to_int(r.get("Not_Outs", 0)) for r in rows)
        hs = max([to_int(r.get("Highest_Score", 0)) for r in rows] + [0])
        fours = sum(to_int(r.get("Fours", 0)) for r in rows)
        sixes = sum(to_int(r.get("Sixes", 0)) for r in rows)
        centuries = sum(to_int(r.get("Centuries", 0)) for r in rows)
        fifties = sum(to_int(r.get("Half_Centuries", 0)) for r in rows)

        tot_wickets = sum(to_int(r.get("Wickets_Taken", 0)) for r in rows)
        balls_bowled = sum(to_int(r.get("Balls_Bowled", 0)) for r in rows)
        runs_conceded = sum(to_int(r.get("Runs_Conceded", 0)) for r in rows)

        bat_avg = round(tot_runs / tot_outs, 2) if tot_outs > 0 else float(tot_runs)
        strike_rate = round((tot_runs / tot_balls_faced) * 100, 2) if tot_balls_faced > 0 else 0.0
        econ = round(runs_conceded / (balls_bowled / 6.0), 2) if balls_bowled > 0 else 0.0
        bowl_avg = round(runs_conceded / tot_wickets, 2) if tot_wickets > 0 else 0.0

        # Classify Role
        if name in WICKETKEEPERS:
            role = "Wicketkeeper"
        elif name in ALLROUNDERS:
            role = "Allrounder"
        elif name in BATSMEN:
            role = "Batsman"
        elif tot_wickets >= 10 or balls_bowled >= 60:
            role = "Bowler"
        elif tot_runs >= 200:
            role = "Batsman"
        else:
            role = "Bowler"

        # Classify Country & Overseas
        country = OVERSEAS_COUNTRY_MAP.get(name, "India")
        is_overseas = 1 if country != "India" else 0

        # Classify Capped vs Uncapped
        if name in UNCAPPED_PLAYERS:
            is_capped = False
        elif is_overseas:
            # Overseas players in IPL are generally capped international stars
            is_capped = True
        elif tot_matches > 40 or name in TIER_2CR or name in TIER_1_5CR or name in TIER_1CR:
            is_capped = True
        elif name in {"MS Dhoni", "Virat Kohli", "Rohit Sharma", "Jasprit Bumrah", "Hardik Pandya", "Ravindra Jadeja"}:
            is_capped = True
        else:
            # Emerging Indian player with low matches
            is_capped = False if tot_matches <= 15 else True

        # Base Price
        if not is_capped:
            if tot_runs > 400 or tot_wickets > 15:
                base_price = 5000000.0  # ₹50 L
            elif tot_runs > 150 or tot_wickets > 5:
                base_price = 4000000.0  # ₹40 L
            elif tot_matches > 0:
                base_price = 3000000.0  # ₹30 L
            else:
                base_price = 3000000.0  # ₹30 L
        else:
            if name in TIER_2CR or tot_runs >= 3000 or tot_wickets >= 100:
                base_price = 20000000.0  # ₹2.00 Cr
            elif name in TIER_1_5CR or tot_runs >= 1500 or tot_wickets >= 50:
                base_price = 15000000.0  # ₹1.50 Cr
            elif name in TIER_1CR or tot_runs >= 800 or tot_wickets >= 25:
                base_price = 10000000.0  # ₹1.00 Cr
            else:
                base_price = 7500000.0   # ₹75 Lakh

        # Set Name & Set Code
        if not is_capped:
            set_code = "UN1"
            set_name = "Set 6: Uncapped Players (UN1)"
        elif role == "Batsman":
            set_code = "BA1"
            set_name = "Set 1: Capped Batters (BA1)"
        elif role == "Allrounder":
            set_code = "AL1"
            set_name = "Set 2: Capped All-rounders (AL1)"
        elif role == "Wicketkeeper":
            set_code = "WK1"
            set_name = "Set 3: Capped Wicketkeepers (WK1)"
        elif role == "Bowler" and name in SPINNERS:
            set_code = "SP1"
            set_name = "Set 5: Capped Spinners (SP1)"
        else:
            set_code = "FA1"
            set_name = "Set 4: Capped Fast Bowlers (FA1)"

        former_team = FORMER_TEAM_MAP.get(name)

        player_dict = {
            "name": name,
            "role": role,
            "country": country,
            "base_price": base_price,
            "set_name": set_name,
            "set_code": set_code,
            "is_capped": is_capped,
            "is_overseas": is_overseas,
            "former_team": former_team,
            "stats": {
                "matches": tot_matches,
                "runs": tot_runs,
                "highest_score": hs,
                "batting_avg": bat_avg,
                "strike_rate": strike_rate,
                "fours": fours,
                "sixes": sixes,
                "centuries": centuries,
                "fifties": fifties,
                "wickets": tot_wickets,
                "bowling_economy": econ,
                "bowling_avg": bowl_avg,
            }
        }
        all_players_data.append(player_dict)

    # Also make sure legends like Glenn Maxwell, Andre Russell, Faf du Plessis, David Warner, Shikhar Dhawan are included if missing
    existing_names = {p["name"] for p in all_players_data}
    extra_legends = [
        {
            "name": "Andre Russell", "role": "Allrounder", "country": "West Indies",
            "base_price": 20000000.0, "set_name": "Set 2: Capped All-rounders (AL1)", "set_code": "AL1",
            "is_capped": True, "is_overseas": 1, "former_team": "KKR",
            "stats": {"matches": 127, "runs": 2484, "highest_score": 88, "batting_avg": 29.22, "strike_rate": 174.93, "fours": 174, "sixes": 209, "centuries": 0, "fifties": 11, "wickets": 115, "bowling_economy": 9.24, "bowling_avg": 23.82}
        },
        {
            "name": "Glenn Maxwell", "role": "Allrounder", "country": "Australia",
            "base_price": 20000000.0, "set_name": "Set 2: Capped All-rounders (AL1)", "set_code": "AL1",
            "is_capped": True, "is_overseas": 1, "former_team": "RCB",
            "stats": {"matches": 134, "runs": 2771, "highest_score": 95, "batting_avg": 24.74, "strike_rate": 156.73, "fours": 232, "sixes": 158, "centuries": 0, "fifties": 18, "wickets": 37, "bowling_economy": 8.32, "bowling_avg": 35.49}
        },
        {
            "name": "Faf du Plessis", "role": "Batsman", "country": "South Africa",
            "base_price": 20000000.0, "set_name": "Set 1: Capped Batters (BA1)", "set_code": "BA1",
            "is_capped": True, "is_overseas": 1, "former_team": "RCB",
            "stats": {"matches": 145, "runs": 4571, "highest_score": 96, "batting_avg": 36.57, "strike_rate": 136.37, "fours": 425, "sixes": 165, "centuries": 0, "fifties": 37, "wickets": 0, "bowling_economy": 0.0, "bowling_avg": 0.0}
        },
        {
            "name": "David Warner", "role": "Batsman", "country": "Australia",
            "base_price": 20000000.0, "set_name": "Set 1: Capped Batters (BA1)", "set_code": "BA1",
            "is_capped": True, "is_overseas": 1, "former_team": "DC",
            "stats": {"matches": 184, "runs": 6565, "highest_score": 126, "batting_avg": 40.52, "strike_rate": 139.77, "fours": 663, "sixes": 236, "centuries": 4, "fifties": 62, "wickets": 0, "bowling_economy": 0.0, "bowling_avg": 0.0}
        },
        {
            "name": "Shikhar Dhawan", "role": "Batsman", "country": "India",
            "base_price": 20000000.0, "set_name": "Set 1: Capped Batters (BA1)", "set_code": "BA1",
            "is_capped": True, "is_overseas": 0, "former_team": "PBKS",
            "stats": {"matches": 222, "runs": 6769, "highest_score": 106, "batting_avg": 35.26, "strike_rate": 127.14, "fours": 768, "sixes": 152, "centuries": 2, "fifties": 51, "wickets": 4, "bowling_economy": 8.25, "bowling_avg": 16.5}
        }
    ]

    for leg in extra_legends:
        if leg["name"] not in existing_names:
            all_players_data.append(leg)

    # Sort players: Capped first by Base Price descending, then Uncapped by Base Price descending
    all_players_data.sort(key=lambda x: (0 if x["is_capped"] else 1, -x["base_price"], -x["stats"]["runs"], -x["stats"]["wickets"]))

    print(f"Total processed players: {len(all_players_data)}")
    batters = [p for p in all_players_data if p["role"] == "Batsman"]
    bowlers = [p for p in all_players_data if p["role"] == "Bowler"]
    allrounders = [p for p in all_players_data if p["role"] == "Allrounder"]
    wicketkeepers = [p for p in all_players_data if p["role"] == "Wicketkeeper"]
    capped = [p for p in all_players_data if p["is_capped"]]
    uncapped = [p for p in all_players_data if not p["is_capped"]]

    print(f"  - Batters: {len(batters)}")
    print(f"  - Bowlers: {len(bowlers)}")
    print(f"  - Allrounders: {len(allrounders)}")
    print(f"  - Wicketkeepers: {len(wicketkeepers)}")
    print(f"  - Capped: {len(capped)}")
    print(f"  - Uncapped: {len(uncapped)}")

    # Update seed_data.py
    update_seed_data_file(all_players_data)

    # Populate SQLite database
    populate_sqlite_database(all_players_data)

    print("Ingestion completed successfully!")


def update_seed_data_file(players_data):
    seed_file = BASE_DIR / "seed_data.py"
    with open(seed_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split at INITIAL_PLAYERS =
    split_marker = "INITIAL_PLAYERS: List[Dict[str, Any]] = ["
    if split_marker not in content:
        split_marker = "INITIAL_PLAYERS = ["
        if split_marker not in content:
            raise ValueError("Could not find INITIAL_PLAYERS in seed_data.py")

    header_part = content.split(split_marker)[0]
    new_players_repr = json.dumps(players_data, indent=4)
    # Convert json bools/nulls to python
    new_players_repr = (
        new_players_repr.replace("true", "True")
        .replace("false", "False")
        .replace("null", "None")
    )

    new_content = f"{header_part}INITIAL_PLAYERS: List[Dict[str, Any]] = {new_players_repr}\n"
    with open(seed_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {seed_file} with {len(players_data)} players.")


def populate_sqlite_database(players_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing players and player_stats to freshly seed
    cursor.execute("DELETE FROM auction_bids;")
    cursor.execute("DELETE FROM player_stats;")
    cursor.execute("DELETE FROM players;")

    # Reset SQLite autoincrement for clean IDs
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('players', 'player_stats', 'auction_bids');")

    for p in players_data:
        is_os = 1 if p.get("country", "India") != "India" else 0
        is_cap = 1 if p.get("is_capped", True) else 0

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

        stats = p.get("stats", {})
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
            stats.get("bowling_avg", 0.0),
        ))

    conn.commit()
    conn.close()
    print(f"Populated {DB_PATH} with {len(players_data)} players and their career statistics.")


if __name__ == "__main__":
    main()
