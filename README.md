# 🏏 Real IPL Auction & Player Analytics System

A comprehensive, production-grade Python system designed for a real **Indian Premier League (IPL) Auction**, featuring 10 official franchises (CSK, MI, RCB, KKR, RR, SRH, GT, LSG, DC, PBKS) with real budgets (₹120 Crore each) and authentic player career statistics.

---

## 🎯 Direct Answers to Boss's 10 Questions

This project answers every single question from your boss directly, both in the **Interactive Terminal Dashboard (`python main.py`)** and in the **Modern Web Interface (`python web/app.py`)**:

| # | Boss's Question | How to Showcase to Your Boss | Technical Topic Used |
|---|-----------------|------------------------------|----------------------|
| **1** | **Show all players** | Select **Option [1]** in terminal or visit `/players` in web | SQL `SELECT` with `JOIN`, Lists, Dictionaries |
| **2** | **Show only bowlers** | Select **Option [2]** in terminal or click *Bowlers Only* button | Python Loop Filtering, SQL `WHERE role = 'Bowler'` |
| **3** | **Find Virat Kohli** | Select **Option [3]** and press Enter (or search "Virat") | Substring Search, Hash Dictionary Lookup |
| **4** | **Show top 10 run scorers** | Select **Option [4]** | **Merge Sort** Algorithm (Divide & Conquer, $O(n \log n)$) |
| **5** | **Show highest batting averages** | Select **Option [5]** | **Quick Sort** Algorithm (Pivot Partitioning, $O(n \log n)$) |
| **6** | **Add a new player** | Select **Option [6]** or click *+ Add Player* in web | **CRUD: Create**, Primary Keys, Foreign Keys |
| **7** | **Update player statistics** | Select **Option [7]** or click ✏️ *Edit* on any player | **CRUD: Update**, SQL Transactions |
| **8** | **Delete a player** | Select **Option [8]** or click 🗑️ *Delete* on any player | **CRUD: Delete**, Foreign Key Cascade Constraints |
| **9** | **Show a team's purchased players** | Select **Option [9]** and choose a team (e.g. `CSK`, `RCB`, `MI`) | Relational Foreign Key JOIN (`players.team_id == teams.team_id`) |
| **10** | **Show remaining team budget** | Select **Option [10]** or visit `/teams` in web | SQL Aggregation, Real-time Purse Deductions |
| **11** | **Live IPL Auction Simulation** | Select **Option [11]** or visit `/auction` in web | Interactive Bidding, Paddle Raises, Hammer Knockdowns |

---

## 📚 Technical Concepts Guide (How to Explain to Your Boss)

### 1. Lists (`list`)
- **Where it is used**:
  - `read_all_players()` returns a Python `list` of player objects.
  - Slicing during **Merge Sort** (`players[:mid]` and `players[mid:]`).
  - Storing team squads and auction pools.

### 2. Dictionaries (`dict`)
- **Where it is used**:
  - Every player is modeled as a rich key-value dictionary:
    ```python
    {
        "player_id": 1,
        "name": "Virat Kohli",
        "role": "Batsman",
        "country": "India",
        "base_price": 20000000.0,
        "runs": 8004,
        "batting_avg": 38.67,
        "strike_rate": 131.97,
        "wickets": 4,
        "team_id": 3
    }
    ```
  - Enables instant $O(1)$ property lookups and field updates.

### 3. Loops (`for` & `while`)
- **Where it is used**:
  - `while True`: Powers the main menu navigation and real-time auction bidding increments.
  - `for player in players`: Traverses lists to filter bowlers, format currency, and calculate team purse totals.

### 4. Merge Sort Algorithm ($O(n \log n)$ Stable Sort)
- **File**: `dsa/merge_sort.py`
- **Explanation**: Divides the unsorted player list into two halves recursively until individual elements remain, then merges them back in descending order of runs. Guaranteed $O(n \log n)$ time complexity and stable.
- **Used For**: **Boss Question 4 (Top 10 Run Scorers)**.

### 5. Quick Sort Algorithm ($O(n \log n)$ Average Pivot Sort)
- **File**: `dsa/quick_sort.py`
- **Explanation**: Selects a pivot element and partitions players such that elements with higher batting averages are on the left and lower averages on the right, recursively sorting both partitions.
- **Used For**: **Boss Question 5 (Highest Batting Averages)**.

### 6. SQL Database & Relational Schema
- **Files**: `database.py`, `supabase_schema.sql`
- **Tables**:
  1. `teams`: Franchise details, total budget, remaining purse, squad capacity.
  2. `players`: Marquee details, role, country, base price, auction status, and team foreign key.
  3. `player_stats`: Deep career statistics linked to player via foreign key.
  4. `auction_bids`: Full transaction log of every bid placed during the auction.

### 7. Primary Keys & Foreign Keys
- **Primary Keys (PK)**:
  - `teams.team_id` uniquely identifies each IPL franchise.
  - `players.player_id` uniquely identifies each player.
  - `player_stats.stat_id` uniquely identifies each stats record.
- **Foreign Keys (FK)**:
  - `players.team_id` references `teams.team_id` (enforces relational ownership).
  - `player_stats.player_id` references `players.player_id` with `ON DELETE CASCADE`.

### 8. CRUD Operations
- **Create**: Add a new player and their stats into linked tables (Boss Q6).
- **Read**: Fetch all players, filter bowlers, search Virat Kohli, top run scorers (Boss Q1, Q2, Q3, Q4, Q5).
- **Update**: Update player statistics and deduct franchise purse (Boss Q7, Q10).
- **Delete**: Safely delete a player while maintaining relational integrity (Boss Q8).

---

## 🚀 How to Run the Project

### Option A: Interactive Terminal Dashboard (Recommended for CLI Demo)
```bash
python main.py
```
This opens a modern, color-coded terminal dashboard where you can press `1` to `10` to directly show your boss each question!

### Option B: Modern Web Dashboard (Browser Demo)
```bash
python web/app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in Google Chrome or any browser to show your boss the visual web dashboard!

### Option C: Run Automated Test Suite
```bash
python test_system.py
```
Runs a 100% automated test verification proving all 10 questions and algorithms function flawlessly.

---

## ☁️ Supabase Cloud Database Setup (Optional)

The system automatically runs locally using **SQLite3** with zero configuration required.

If you want to connect your cloud **Supabase** account:
1. Log in to your [Supabase Dashboard](https://supabase.com/dashboard).
2. Go to **Project Settings** -> **API**.
3. Copy your **Project URL** and **anon / service_role key**.
4. Open the `.env` file in the project folder and set:
   ```env
   DB_MODE=supabase
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-supabase-api-key
   ```
5. Open Supabase's **SQL Editor** and paste the contents of `supabase_schema.sql` to initialize your cloud tables!
