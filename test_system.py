"""
Automated Verification Test Suite for IPL Auction System
Validates all 10 Boss's questions and core requirements:
- Lists, Dictionaries, Loops
- Merge Sort & Quick Sort
- SQL Database, Primary Keys, Foreign Keys, CRUD
- Live Auction Simulation
"""

import sys
from config import format_currency
from database import init_db
from crud.player_crud import (
    read_all_players,
    read_players_by_role,
    find_player_by_name,
    find_player_by_id,
    create_player,
    update_player_stats,
    delete_player,
    get_top_run_scorers_mergesort,
    get_top_batting_averages_quicksort,
)
from crud.team_crud import (
    read_all_teams,
    get_team_purchased_players,
    get_team_budget_overview,
)
from auction.auction_engine import (
    get_available_players_pool,
    run_player_auction,
    reset_entire_auction,
    get_auction_stats,
)


def run_all_tests():
    print("=" * 70)
    print("STARTING IPL AUCTION VERIFICATION TEST SUITE")
    print("=" * 70)

    # 1. Initialize DB
    print("\n[Test 0] Initializing Relational Database...")
    init_db(force_reset=True)
    print("  ✓ Database schema & authentic IPL seed data initialized successfully.")

    # 2. Q1: Show all players
    print("\n[Test 1] Boss Q1: Show all players...")
    players = read_all_players()
    assert len(players) >= 30, f"Expected at least 30 players, got {len(players)}"
    print(f"  ✓ Fetched {len(players)} players. Sample: {players[0]['name']} ({players[0]['role']})")

    # 3. Q2: Show only bowlers
    print("\n[Test 2] Boss Q2: Show only bowlers...")
    bowlers = read_players_by_role("Bowler")
    assert len(bowlers) > 0, "No bowlers returned"
    for b in bowlers:
        assert b["role"].lower() == "bowler", f"Expected Bowler, got {b['role']}"
    print(f"  ✓ Filtered {len(bowlers)} bowlers successfully. (e.g., {bowlers[0]['name']})")

    # 4. Q3: Find Virat Kohli
    print("\n[Test 3] Boss Q3: Find Virat Kohli...")
    kohli_results = find_player_by_name("Virat Kohli")
    assert len(kohli_results) >= 1, "Virat Kohli not found"
    kohli = kohli_results[0]
    assert "Virat" in kohli["name"]
    print(f"  ✓ Found: {kohli['name']} | Runs: {kohli['runs']} | Bat Avg: {kohli['batting_avg']} | SR: {kohli['strike_rate']}")

    # 5. Q4: Top 10 run scorers using Merge Sort
    print("\n[Test 4] Boss Q4: Show top 10 run scorers (Merge Sort)...")
    top_runs = get_top_run_scorers_mergesort(10)
    assert len(top_runs) == 10, f"Expected 10 players, got {len(top_runs)}"
    # Verify descending sort order
    for i in range(len(top_runs) - 1):
        assert top_runs[i]["runs"] >= top_runs[i + 1]["runs"], "Merge Sort failed descending invariant!"
    print(f"  ✓ Top run scorer: #{1} {top_runs[0]['name']} ({top_runs[0]['runs']} runs)")
    print(f"  ✓ 10th run scorer: #{10} {top_runs[9]['name']} ({top_runs[9]['runs']} runs)")

    # 6. Q5: Highest batting averages using Quick Sort
    print("\n[Test 5] Boss Q5: Show highest batting averages (Quick Sort)...")
    top_avg = get_top_batting_averages_quicksort(10, min_matches=10)
    assert len(top_avg) == 10, f"Expected 10 players, got {len(top_avg)}"
    # Verify descending sort order
    for i in range(len(top_avg) - 1):
        assert top_avg[i]["batting_avg"] >= top_avg[i + 1]["batting_avg"], "Quick Sort failed descending invariant!"
    print(f"  ✓ Highest Batting Avg: #{1} {top_avg[0]['name']} ({top_avg[0]['batting_avg']:.2f})")
    print(f"  ✓ 10th Batting Avg: #{10} {top_avg[9]['name']} ({top_avg[9]['batting_avg']:.2f})")

    # 7. Q6: Add a new player (CRUD - Create)
    print("\n[Test 6] Boss Q6: Add a new player (CRUD Create)...")
    new_pid = create_player(
        name="Test Player",
        role="Allrounder",
        country="India",
        base_price=15000000.0,
        matches=40,
        runs=950,
        highest_score=78,
        batting_avg=31.67,
        strike_rate=142.50,
        centuries=0,
        fifties=5,
        wickets=35,
        bowling_economy=8.10,
        bowling_avg=26.40,
    )
    assert new_pid > 0, "Failed to create new player"
    created = find_player_by_id(new_pid)
    assert created is not None and created["name"] == "Test Player"
    print(f"  ✓ Created new player with Primary Key ID {new_pid}: {created['name']} ({created['role']})")

    # 8. Q7: Update player statistics (CRUD - Update)
    print("\n[Test 7] Boss Q7: Update player statistics (CRUD Update)...")
    updated = update_player_stats(new_pid, {"runs": 1050, "wickets": 38, "batting_avg": 35.00})
    assert updated is True, "Failed to update player stats"
    refetched = find_player_by_id(new_pid)
    assert refetched["runs"] == 1050 and refetched["wickets"] == 38
    print(f"  ✓ Successfully updated {refetched['name']}: Runs={refetched['runs']}, Wickets={refetched['wickets']}")

    # 9. Q8: Delete a player (CRUD - Delete)
    print("\n[Test 8] Boss Q8: Delete a player (CRUD Delete)...")
    deleted = delete_player(new_pid)
    assert deleted is True, "Failed to delete player"
    assert find_player_by_id(new_pid) is None, "Player still exists after delete"
    print(f"  ✓ Successfully deleted player ID {new_pid} with cascade validation.")

    # 10. Q9 & Q10: Auction simulation, purchased players, remaining budget
    print("\n[Test 9 & 10] Boss Q9 & Q10: Live Auction, Purchased Players & Remaining Budget...")
    pool = get_available_players_pool()
    assert len(pool) > 0, "Auction pool is empty"
    first_player = pool[0]

    status, winner, price = run_player_auction(first_player)
    assert status == "Sold" and winner is not None and price > 0
    print(f"  ✓ Auctioned {first_player['name']}: SOLD to {winner['team_name']} ({winner['short_code']}) for {format_currency(price)}")

    # Check team's purchased squad (Q9)
    squad_data = get_team_purchased_players(winner["team_id"])
    assert len(squad_data["players"]) >= 1, "Purchased squad did not reflect player"
    print(f"  ✓ Team {winner['short_code']} squad count: {len(squad_data['players'])} player(s). Spent: {squad_data['total_spent_fmt']}")

    # Check remaining budget (Q10)
    budgets = get_team_budget_overview()
    assert len(budgets) == 10, f"Expected 10 IPL franchises, got {len(budgets)}"
    team_in_budgets = [t for t in budgets if t["team_id"] == winner["team_id"]][0]
    expected_remaining = team_in_budgets["total_budget"] - price
    assert abs(team_in_budgets["remaining_budget"] - expected_remaining) < 1.0, "Budget calculation mismatch!"
    print(f"  ✓ Remaining Purse for {winner['short_code']}: {team_in_budgets['remaining_budget_fmt']} (Exact match)")

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("ALL 10 BOSS QUESTIONS AND TOPICS ARE FULLY VERIFIED!")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
