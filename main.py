"""
IPL Auction Management System - Main Interactive Console
Addresses all 10 Boss's questions directly with clean menus, formatted rich tables,
custom sorting algorithms (Merge Sort & Quick Sort), and live auction simulation.
"""

import sys
import time
from typing import List, Dict, Any, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm, FloatPrompt, IntPrompt

from config import format_currency, DB_MODE, is_supabase_configured
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
    get_team_by_code,
)
from auction.auction_engine import (
    get_available_players_pool,
    run_player_auction,
    reset_entire_auction,
    get_auction_stats,
    get_bid_increment,
    record_winning_bid,
    mark_player_unsold,
)

console = Console()


# ============================================================================
# HELPER RENDERING FUNCTIONS
# ============================================================================

def display_players_table(players: List[Dict[str, Any]], title: str = "IPL Players List") -> None:
    """Renders a formatted table of players using rich."""
    if not players:
        console.print(Panel("[yellow]No players found matching the criteria.[/yellow]", title="Notice"))
        return

    table = Table(title=f"🏏 {title} (Total: {len(players)})", show_lines=True, header_style="bold cyan")
    table.add_column("ID", style="dim", justify="right", width=5)
    table.add_column("Player Name", style="bold white", width=22)
    table.add_column("Role", style="magenta", width=14)
    table.add_column("Country", style="green", width=12)
    table.add_column("Base Price", justify="right", style="yellow", width=10)
    table.add_column("Status", justify="center", width=11)
    table.add_column("Team", style="bold blue", width=8)
    table.add_column("Matches", justify="right", width=7)
    table.add_column("Runs", justify="right", style="bold yellow", width=7)
    table.add_column("Bat Avg", justify="right", width=7)
    table.add_column("SR", justify="right", width=7)
    table.add_column("Wickets", justify="right", style="bold red", width=7)
    table.add_column("Econ", justify="right", width=6)

    for p in players:
        status_style = "green" if p.get("status") == "Sold" else ("red" if p.get("status") == "Unsold" else "cyan")
        status_text = f"[{status_style}]{p.get('status', 'Available')}[/{status_style}]"
        team_display = p.get("team_code") or "-"
        base_price_fmt = format_currency(p.get("base_price", 0))

        table.add_row(
            str(p.get("player_id", "")),
            str(p.get("name", "")),
            str(p.get("role", "")),
            str(p.get("country", "")),
            base_price_fmt,
            status_text,
            team_display,
            str(p.get("matches", 0)),
            str(p.get("runs", 0)),
            f"{p.get('batting_avg', 0.0):.2f}",
            f"{p.get('strike_rate', 0.0):.2f}",
            str(p.get("wickets", 0)),
            f"{p.get('bowling_economy', 0.0):.2f}",
        )

    console.print(table)


def display_player_profile_card(player: Dict[str, Any]) -> None:
    """Renders a detailed profile card for a single player."""
    status = player.get("status", "Available")
    team = player.get("team_name") or "None (In Pool)"
    base_price = format_currency(player.get("base_price", 0))
    sold_price = format_currency(player.get("sold_price", 0))

    card_content = f"""
[bold cyan]Full Name:[/bold cyan] {player.get('name')}  |  [bold cyan]Role:[/bold cyan] {player.get('role')}  |  [bold cyan]Country:[/bold cyan] {player.get('country')}
[bold yellow]Auction Status:[/bold yellow] {status}  |  [bold yellow]Assigned Team:[/bold yellow] {team}
[bold green]Base Price:[/bold green] {base_price}  |  [bold green]Sold Price:[/bold green] {sold_price}

[bold underline]Career Statistics[/bold underline]
• Matches: {player.get('matches', 0)}
• Total Runs: [bold yellow]{player.get('runs', 0)}[/bold yellow]  |  Highest Score: {player.get('highest_score', 0)}
• Batting Average: [bold yellow]{player.get('batting_avg', 0.0):.2f}[/bold yellow]  |  Strike Rate: [bold yellow]{player.get('strike_rate', 0.0):.2f}[/bold yellow]
• Centuries (100s): {player.get('centuries', 0)}  |  Fifties (50s): {player.get('fifties', 0)}
• Total Wickets: [bold red]{player.get('wickets', 0)}[/bold red]  |  Economy: {player.get('bowling_economy', 0.0):.2f}  |  Bowling Avg: {player.get('bowling_avg', 0.0):.2f}
"""
    console.print(Panel(card_content, title=f"🌟 Player Profile: {player.get('name')} (ID: {player.get('player_id')})", border_style="bright_blue"))


# ============================================================================
# BOSS'S 10 QUESTIONS HANDLERS
# ============================================================================

def handle_q1_show_all_players() -> None:
    """[Boss Question 1: Show all players]"""
    console.print("\n[bold green]Executing: Show All Players (SQL SELECT JOIN on players & player_stats)[/bold green]")
    players = read_all_players()
    display_players_table(players, title="All Registered IPL Players")


def handle_q2_show_only_bowlers() -> None:
    """[Boss Question 2: Show only bowlers]"""
    console.print("\n[bold green]Executing: Show Only Bowlers (Filtering with Python Loops & SQL Role Filter)[/bold green]")
    console.print("[1] Show Bowlers Only (Direct Boss Question)")
    console.print("[2] Show Batsmen Only")
    console.print("[3] Show Allrounders Only")
    console.print("[4] Show Wicketkeepers Only")
    sub_choice = Prompt.ask("Choose category", choices=["1", "2", "3", "4"], default="1")

    role_map = {"1": "Bowler", "2": "Batsman", "3": "Allrounder", "4": "Wicketkeeper"}
    selected_role = role_map[sub_choice]

    bowlers = read_players_by_role(selected_role)
    display_players_table(bowlers, title=f"Filtered: {selected_role}s Category")


def handle_q3_find_virat_kohli() -> None:
    """[Boss Question 3: Find Virat Kohli]"""
    console.print("\n[bold green]Executing: Find Virat Kohli (Search using Dictionaries & Substring Matching)[/bold green]")
    name_query = Prompt.ask("Enter player name to search", default="Virat Kohli")
    matches = find_player_by_name(name_query)

    if not matches:
        console.print(f"[red]No player found matching '{name_query}'.[/red]")
        return

    console.print(f"[bold green]Found {len(matches)} matching player(s):[/bold green]")
    for p in matches:
        display_player_profile_card(p)


def handle_q4_top_10_run_scorers() -> None:
    """[Boss Question 4: Show top 10 run scorers using Merge Sort]"""
    console.print("\n[bold green]Executing: Top 10 Run Scorers using Custom MERGE SORT Algorithm[/bold green]")
    console.print("[dim]Algorithm: Merge Sort | Divide and Conquer | Time Complexity: O(n log n) | Stable[/dim]")
    top_runs = get_top_run_scorers_mergesort(limit=10)

    table = Table(title="🏆 Top 10 Run Scorers in IPL (Sorted via Merge Sort)", header_style="bold gold1")
    table.add_column("Rank", justify="center", width=6)
    table.add_column("Player Name", style="bold white", width=22)
    table.add_column("Role", style="magenta", width=14)
    table.add_column("Matches", justify="right", width=8)
    table.add_column("Total Runs", justify="right", style="bold yellow", width=12)
    table.add_column("Bat Avg", justify="right", width=8)
    table.add_column("Strike Rate", justify="right", width=10)
    table.add_column("100s / 50s", justify="center", width=12)

    for rank, p in enumerate(top_runs, 1):
        hundreds_fifties = f"{p.get('centuries', 0)} / {p.get('fifties', 0)}"
        table.add_row(
            f"#{rank}",
            str(p.get("name", "")),
            str(p.get("role", "")),
            str(p.get("matches", 0)),
            f"{p.get('runs', 0):,}",
            f"{p.get('batting_avg', 0.0):.2f}",
            f"{p.get('strike_rate', 0.0):.2f}",
            hundreds_fifties
        )

    console.print(table)


def handle_q5_highest_batting_averages() -> None:
    """[Boss Question 5: Show highest batting averages using Quick Sort]"""
    console.print("\n[bold green]Executing: Highest Batting Averages using Custom QUICK SORT Algorithm[/bold green]")
    console.print("[dim]Algorithm: Quick Sort | Pivot Partitioning | Time Complexity: O(n log n) | In-Place Partition[/dim]")
    top_avg = get_top_batting_averages_quicksort(limit=10, min_matches=10)

    table = Table(title="📈 Highest Batting Averages in IPL (Sorted via Quick Sort)", header_style="bold cyan")
    table.add_column("Rank", justify="center", width=6)
    table.add_column("Player Name", style="bold white", width=22)
    table.add_column("Role", style="magenta", width=14)
    table.add_column("Matches", justify="right", width=8)
    table.add_column("Batting Avg", justify="right", style="bold cyan", width=12)
    table.add_column("Total Runs", justify="right", width=10)
    table.add_column("Strike Rate", justify="right", width=10)

    for rank, p in enumerate(top_avg, 1):
        table.add_row(
            f"#{rank}",
            str(p.get("name", "")),
            str(p.get("role", "")),
            str(p.get("matches", 0)),
            f"{p.get('batting_avg', 0.0):.2f}",
            f"{p.get('runs', 0):,}",
            f"{p.get('strike_rate', 0.0):.2f}"
        )

    console.print(table)


def handle_q6_add_new_player() -> None:
    """[Boss Question 6: Add a new player (CRUD - Create)]"""
    console.print("\n[bold green]Executing: Add a New Player (CRUD Create with Foreign Key Relationship)[/bold green]")
    name = Prompt.ask("Enter player's full name")
    role = Prompt.ask("Enter role", choices=["Batsman", "Bowler", "Allrounder", "Wicketkeeper"], default="Batsman")
    country = Prompt.ask("Enter country", default="India")
    base_price_cr = FloatPrompt.ask("Enter Base Price in Crores (e.g., 2.0 or 0.50)", default=2.0)
    base_price = base_price_cr * 10_000_000

    matches = IntPrompt.ask("Career Matches", default=50)
    runs = IntPrompt.ask("Total Career Runs", default=1200)
    highest_score = IntPrompt.ask("Highest Score", default=85)
    batting_avg = FloatPrompt.ask("Batting Average", default=32.5)
    strike_rate = FloatPrompt.ask("Strike Rate", default=135.0)
    centuries = IntPrompt.ask("Centuries (100s)", default=1)
    fifties = IntPrompt.ask("Fifties (50s)", default=6)
    wickets = IntPrompt.ask("Total Wickets", default=10)
    bowling_economy = FloatPrompt.ask("Bowling Economy", default=8.2)
    bowling_avg = FloatPrompt.ask("Bowling Average", default=28.5)

    try:
        new_id = create_player(
            name=name,
            role=role,
            country=country,
            base_price=base_price,
            matches=matches,
            runs=runs,
            highest_score=highest_score,
            batting_avg=batting_avg,
            strike_rate=strike_rate,
            centuries=centuries,
            fifties=fifties,
            wickets=wickets,
            bowling_economy=bowling_economy,
            bowling_avg=bowling_avg,
        )
        console.print(f"\n[bold green]✅ Player '{name}' successfully created with Player ID (Primary Key): {new_id}![/bold green]")
        created = find_player_by_id(new_id)
        if created:
            display_player_profile_card(created)
    except Exception as e:
        console.print(f"[bold red]Error creating player: {e}[/bold red]")


def handle_q7_update_player_statistics() -> None:
    """[Boss Question 7: Update player statistics (CRUD - Update)]"""
    console.print("\n[bold green]Executing: Update Player Statistics (CRUD Update)[/bold green]")
    player_id = IntPrompt.ask("Enter Player ID to update (e.g., 1 for Virat Kohli)")
    player = find_player_by_id(player_id)

    if not player:
        console.print(f"[red]Player ID {player_id} not found.[/red]")
        return

    console.print(f"[yellow]Current Record for {player['name']}:[/yellow] Matches={player['matches']}, Runs={player['runs']}, Wickets={player['wickets']}, Avg={player['batting_avg']}")
    
    new_runs = IntPrompt.ask("New Total Runs", default=player["runs"])
    new_matches = IntPrompt.ask("New Matches", default=player["matches"])
    new_avg = FloatPrompt.ask("New Batting Average", default=player["batting_avg"])
    new_sr = FloatPrompt.ask("New Strike Rate", default=player["strike_rate"])
    new_wickets = IntPrompt.ask("New Wickets", default=player["wickets"])

    updates = {
        "runs": new_runs,
        "matches": new_matches,
        "batting_avg": new_avg,
        "strike_rate": new_sr,
        "wickets": new_wickets,
    }

    success = update_player_stats(player_id, updates)
    if success:
        console.print(f"[bold green]✅ Successfully updated statistics for {player['name']}![/bold green]")
        updated = find_player_by_id(player_id)
        if updated:
            display_player_profile_card(updated)
    else:
        console.print("[red]Failed to update player stats.[/red]")


def handle_q8_delete_a_player() -> None:
    """[Boss Question 8: Delete a player (CRUD - Delete)]"""
    console.print("\n[bold green]Executing: Delete a Player (CRUD Delete with Foreign Key cascade verification)[/bold green]")
    player_id = IntPrompt.ask("Enter Player ID to delete")
    player = find_player_by_id(player_id)

    if not player:
        console.print(f"[red]Player with ID {player_id} does not exist.[/red]")
        return

    display_player_profile_card(player)
    confirm = Confirm.ask(f"[bold red]Are you sure you want to permanently delete {player['name']}?[/bold red]", default=False)

    if confirm:
        success = delete_player(player_id)
        if success:
            console.print(f"[bold green]✅ Player '{player['name']}' (ID: {player_id}) has been deleted from database.[/bold green]")
        else:
            console.print("[red]Failed to delete player.[/red]")
    else:
        console.print("[yellow]Deletion cancelled.[/yellow]")


def handle_q9_show_team_purchased_players() -> None:
    """[Boss Question 9: Show a team's purchased players]"""
    console.print("\n[bold green]Executing: Show Team's Purchased Players (Relational SQL Foreign Key JOIN)[/bold green]")
    teams = read_all_teams()
    
    table = Table(title="Available Franchises", header_style="bold blue")
    table.add_column("Team ID", justify="right", width=8)
    table.add_column("Short Code", style="bold yellow", width=12)
    table.add_column("Franchise Name", width=32)
    table.add_column("Players Bought", justify="right", width=14)

    for t in teams:
        table.add_row(str(t["team_id"]), t["short_code"], t["team_name"], str(t["current_squad_size"]))
    console.print(table)

    target_code = Prompt.ask("Enter Team Code or ID (e.g. CSK, MI, RCB, or 1-10)", default="RCB")
    squad_data = get_team_purchased_players(target_code)

    if not squad_data.get("team"):
        console.print(f"[red]Team '{target_code}' not found.[/red]")
        return

    team_info = squad_data["team"]
    players = squad_data["players"]

    console.print(Panel(
        f"[bold cyan]Franchise:[/bold cyan] {team_info['team_name']} ({team_info['short_code']})\n"
        f"[bold green]Remaining Purse:[/bold green] {squad_data['remaining_budget_fmt']}  |  "
        f"[bold yellow]Total Spent:[/bold yellow] {squad_data['total_spent_fmt']}  |  "
        f"[bold magenta]Squad Count:[/bold magenta] {len(players)} / {team_info['max_squad_size']}",
        title="🏆 Franchise Squad Details",
        border_style="green"
    ))

    if not players:
        console.print("[yellow]This team has not purchased any players yet in this auction.[/yellow]")
        console.print("[dim]Tip: Run Option [11] Live Auction to buy players for this team![/dim]")
    else:
        display_players_table(players, title=f"{team_info['short_code']} Purchased Squad")


def handle_q10_show_remaining_team_budget() -> None:
    """[Boss Question 10: Show remaining team budget]"""
    console.print("\n[bold green]Executing: Show Remaining Team Budget across All Franchises[/bold green]")
    teams = get_team_budget_overview()

    table = Table(title="💰 IPL 2026 Franchise Budget & Purse Tracker", header_style="bold green", show_lines=True)
    table.add_column("ID", justify="right", width=4)
    table.add_column("Code", style="bold yellow", width=8)
    table.add_column("Franchise Name", style="bold white", width=28)
    table.add_column("Total Purse", justify="right", width=12)
    table.add_column("Spent Amount", justify="right", style="bold red", width=12)
    table.add_column("Remaining Purse", justify="right", style="bold green", width=14)
    table.add_column("Squad Size", justify="center", width=10)

    total_all_remaining = 0.0
    total_all_spent = 0.0

    for t in teams:
        total_all_remaining += t["remaining_budget"]
        total_all_spent += t["spent_budget"]
        squad_display = f"{t['current_squad_size']} / {t['max_squad_size']}"
        table.add_row(
            str(t["team_id"]),
            t["short_code"],
            t["team_name"],
            t["total_budget_fmt"],
            t["spent_budget_fmt"],
            t["remaining_budget_fmt"],
            squad_display
        )

    console.print(table)
    console.print(f"[bold cyan]Total League Spent:[/bold cyan] {format_currency(total_all_spent)} | [bold green]Total League Remaining Purse:[/bold green] {format_currency(total_all_remaining)}")


# ============================================================================
# REAL IPL AUCTION SIMULATOR MODE
# ============================================================================

def handle_live_auction_room() -> None:
    """Live interactive IPL Auction bidding room."""
    console.print("\n" + "="*70)
    console.print("🔨 [bold gold1]WELCOME TO THE LIVE IPL AUCTION ROOM[/bold gold1] 🔨")
    console.print("="*70)

    stats = get_auction_stats()
    console.print(f"[bold cyan]Pool Status:[/bold cyan] Available: [bold green]{stats['available']}[/bold green] | Sold: [bold blue]{stats['sold']}[/bold blue] | Unsold: [bold red]{stats['unsold']}[/bold red] | Total Spent: [bold yellow]{stats['total_spent_fmt']}[/bold yellow]\n")

    console.print("[1] Bring Next Player Under The Hammer (Live Interactive Bidding)")
    console.print("[2] Auto-Simulate Full Auction (Fast-Forward All Available Players)")
    console.print("[3] Reset Entire Auction (Restore ₹120 Cr to all teams & free players)")
    console.print("[0] Return to Main Menu")

    choice = Prompt.ask("Select option", choices=["1", "2", "3", "0"], default="1")

    if choice == "1":
        _auction_single_player_interactive()
    elif choice == "2":
        _auction_auto_simulate()
    elif choice == "3":
        if Confirm.ask("Reset all budgets back to 120 Cr and free all players?", default=False):
            reset_entire_auction()
            console.print("[bold green]✅ Auction successfully reset![/bold green]")


def _auction_single_player_interactive() -> None:
    """Brings the next available player to the auction stage with interactive bidding."""
    pool = get_available_players_pool()
    if not pool:
        console.print("[yellow]All players have completed their auction turns![/yellow]")
        return

    # Let user pick or bring top player
    console.print(f"\n[cyan]There are {len(pool)} available players in the auction pool.[/cyan]")
    console.print("Next up on the stage:")
    player = pool[0]
    display_player_profile_card(player)

    base_price = float(player["base_price"])
    current_bid = base_price
    highest_team = None

    teams = read_all_teams()
    console.print(f"[bold gold1]📢 Auctioneer:[/bold gold1] 'We have [bold white]{player['name']}[/bold white], base price [bold green]{format_currency(base_price)}[/bold green]!'")

    # Let user participate
    user_team_code = Prompt.ask("Would you like to manage a franchise for this bid? (e.g. CSK, MI, RCB, or press Enter for AI)", default="").strip().upper()
    user_team = get_team_by_code(user_team_code) if user_team_code else None

    if user_team:
        console.print(f"[green]You are managing {user_team['team_name']} (Remaining Purse: {format_currency(user_team['remaining_budget'])})[/green]")

    bidding_active = True
    while bidding_active:
        increment = get_bid_increment(current_bid)
        next_bid = current_bid + increment

        console.print(f"\n[bold yellow]Current Bid: {format_currency(current_bid)}[/bold yellow] (Held by: {highest_team['team_name'] if highest_team else 'None'})")
        console.print(f"Next minimum bid slab: [bold green]{format_currency(next_bid)}[/bold green]")

        options = ["p", "a", "s"]  # Pass, AI bid, Sell/Hammer
        if user_team:
            options.append("b")  # User Bid
            console.print("[b] Place Bid for your team | [a] Let AI teams bid | [p] Pass / Hammer Knockdown")
        else:
            console.print("[a] Next AI Bid | [p] Knock Down Hammer / Finalize")

        action = Prompt.ask("Auctioneer Action", choices=options, default="a")

        if action == "b" and user_team:
            if user_team["remaining_budget"] < next_bid:
                console.print(f"[red]Cannot bid {format_currency(next_bid)}! Your team only has {format_currency(user_team['remaining_budget'])} remaining.[/red]")
            else:
                current_bid = next_bid
                highest_team = user_team
                console.print(f"[bold green]✋ {user_team['team_name']} bids {format_currency(current_bid)}![/bold green]")

        elif action == "a":
            # Pick eligible AI team
            eligible = [
                t for t in teams 
                if t["remaining_budget"] >= next_bid and (highest_team is None or t["team_id"] != highest_team["team_id"])
            ]
            if eligible:
                import random
                bidder = random.choice(eligible)
                current_bid = next_bid
                highest_team = bidder
                console.print(f"[bold cyan]✋ {bidder['team_name']} ({bidder['short_code']}) raises paddle to {format_currency(current_bid)}![/bold cyan]")
            else:
                console.print("[yellow]No other franchise has sufficient purse to outbid![/yellow]")

        elif action in ("p", "s"):
            bidding_active = False

    # Auctioneer gavel knockdown
    if highest_team:
        console.print("\n[bold gold1]🔨 Going once at " + format_currency(current_bid) + "...[/bold gold1]")
        time.sleep(0.4)
        console.print("[bold gold1]🔨 Going twice...[/bold gold1]")
        time.sleep(0.4)
        console.print(f"🔨 [bold green]SOLD! {player['name']} is SOLD to {highest_team['team_name']} for {format_currency(current_bid)}![/bold green] 🎉\n")
        record_winning_bid(player["player_id"], highest_team["team_id"], current_bid)
    else:
        console.print(f"\n[bold red]🔨 UNSOLD! No bids received for {player['name']}.[/bold red]\n")
        mark_player_unsold(player["player_id"])


def _auction_auto_simulate() -> None:
    """Automatically simulates bidding for all remaining available players."""
    pool = get_available_players_pool()
    if not pool:
        console.print("[yellow]No available players left in the pool.[/yellow]")
        return

    console.print(f"\n[bold cyan]Fast-forwarding auction simulation for {len(pool)} players...[/bold cyan]")
    sold_count = 0
    unsold_count = 0

    for idx, player in enumerate(pool, 1):
        status, winning_team, final_price = run_player_auction(player)
        if status == "Sold" and winning_team:
            sold_count += 1
            console.print(f"[{idx}/{len(pool)}] [bold green]SOLD:[/bold green] {player['name']:<20} -> {winning_team['short_code']:<5} for {format_currency(final_price)}")
        else:
            unsold_count += 1
            console.print(f"[{idx}/{len(pool)}] [bold red]UNSOLD:[/bold red] {player['name']:<20}")

    console.print(f"\n[bold green]Simulation Completed![/bold green] Total Sold: {sold_count}, Unsold: {unsold_count}")


# ============================================================================
# COMPUTER SCIENCE TOPICS GUIDE (FOR BOSS DEMONSTRATION)
# ============================================================================

def handle_topics_explanation() -> None:
    """Explains how each topic requested by the boss is implemented in the codebase."""
    explanation = """
[bold underline cyan]HOW THE PROJECT IMPLEMENTS ALL REQUIRED TOPICS[/bold underline cyan]

1. [bold yellow]Lists (`list`)[/bold yellow]:
   - Used in `read_all_players()`, `read_all_teams()`, and sorting functions.
   - Example: Slicing sublists during Merge Sort (`players[:mid]`, `players[mid:]`).

2. [bold yellow]Dictionaries (`dict`)[/bold yellow]:
   - Every player record is modeled as a dictionary containing career statistics and foreign key references.
   - Example: `{'player_id': 1, 'name': 'Virat Kohli', 'runs': 8004, 'batting_avg': 38.67, ...}`.

3. [bold yellow]Loops (`for` and `while`)[/bold yellow]:
   - `while` loops drive the main menu and real-time auction bidding increments.
   - `for` loops iterate through player lists to filter roles and calculate budgets.

4. [bold yellow]Merge Sort[/bold yellow]:
   - Custom implementation in `dsa/merge_sort.py`.
   - Divides player lists recursively and merges them in descending order of runs ($O(n \\log n)$).
   - Used for: [bold]Boss Question 4 (Top 10 Run Scorers)[/bold].

5. [bold yellow]Quick Sort[/bold yellow]:
   - Custom implementation in `dsa/quick_sort.py`.
   - Uses pivot partitioning to sort players by batting average ($O(n \\log n)$).
   - Used for: [bold]Boss Question 5 (Highest Batting Averages)[/bold].

6. [bold yellow]SQL Database with Tables[/bold yellow]:
   - Tables: `teams`, `players`, `player_stats`, `auction_bids`.
   - Supports both Cloud **Supabase (PostgreSQL)** and Local **SQLite3**.

7. [bold yellow]Primary Keys & Foreign Keys[/bold yellow]:
   - `teams.team_id` (PK) -> `players.team_id` (FK).
   - `players.player_id` (PK) -> `player_stats.player_id` (FK with ON DELETE CASCADE).
   - `auction_bids` (FK to both `players` and `teams`).

8. [bold yellow]CRUD Operations[/bold yellow]:
   - [bold green]Create[/bold green]: Add new player into `players` & `player_stats` (Boss Q6).
   - [bold blue]Read[/bold blue]: Fetch all players, filter by role, find Virat Kohli (Boss Q1, Q2, Q3).
   - [bold yellow]Update[/bold yellow]: Update player statistics & update team budget (Boss Q7, Q10).
   - [bold red]Delete[/bold red]: Delete player with relational integrity cascade (Boss Q8).
"""
    console.print(Panel(explanation, title="📚 Technical Concepts Reference", border_style="cyan"))


# ============================================================================
# MAIN MENU LOOP
# ============================================================================

def main_menu() -> None:
    """Main interactive loop."""
    # Ensure database is initialized
    init_db()

    while True:
        db_label = "Cloud Supabase (PostgreSQL)" if (DB_MODE == "supabase" and is_supabase_configured()) else "Local SQLite3 Relational Database"

        console.print("\n" + "="*75)
        console.print("🏏 [bold yellow]IPL AUCTION & PLAYER ANALYTICS SYSTEM[/bold yellow] 🏏")
        console.print(f"[dim]Active Database Engine: {db_label}[/dim]")
        console.print("="*75)

        console.print("[bold cyan]Direct Boss's Questions Showcase:[/bold cyan]")
        console.print("  [bold white][1][/bold white]  Show all players")
        console.print("  [bold white][2][/bold white]  Show only bowlers (and filter other roles)")
        console.print("  [bold white][3][/bold white]  Find Virat Kohli (or search any player)")
        console.print("  [bold white][4][/bold white]  Show top 10 run scorers [bold gold1](Merge Sort)[/bold gold1]")
        console.print("  [bold white][5][/bold white]  Show highest batting averages [bold cyan](Quick Sort)[/bold cyan]")
        console.print("  [bold white][6][/bold white]  Add a new player [bold green](CRUD Create)[/bold green]")
        console.print("  [bold white][7][/bold white]  Update player statistics [bold blue](CRUD Update)[/bold blue]")
        console.print("  [bold white][8][/bold white]  Delete a player [bold red](CRUD Delete)[/bold red]")
        console.print("  [bold white][9][/bold white]  Show a team's purchased players [bold magenta](Foreign Keys)[/bold magenta]")
        console.print("  [bold white][10][/bold white] Show remaining team budget [bold green](Purse Management)[/bold green]")
        console.print("-" * 75)
        console.print("  [bold gold1][11][/bold gold1] Enter Live IPL Auction Simulator Room 🔨")
        console.print("  [bold yellow][12][/bold yellow] Explain Technical Topics (Lists, Dicts, DSA, SQL, FK/PK) 📚")
        console.print("  [bold red][0][/bold red]  Exit Application")
        console.print("="*75)

        choice = Prompt.ask("Enter your choice", default="1").strip()

        if choice == "1":
            handle_q1_show_all_players()
        elif choice == "2":
            handle_q2_show_only_bowlers()
        elif choice == "3":
            handle_q3_find_virat_kohli()
        elif choice == "4":
            handle_q4_top_10_run_scorers()
        elif choice == "5":
            handle_q5_highest_batting_averages()
        elif choice == "6":
            handle_q6_add_new_player()
        elif choice == "7":
            handle_q7_update_player_statistics()
        elif choice == "8":
            handle_q8_delete_a_player()
        elif choice == "9":
            handle_q9_show_team_purchased_players()
        elif choice == "10":
            handle_q10_show_remaining_team_budget()
        elif choice == "11":
            handle_live_auction_room()
        elif choice == "12":
            handle_topics_explanation()
        elif choice == "0":
            console.print("\n[bold green]Thank you for using the IPL Auction System! Goodbye.[/bold green]\n")
            sys.exit(0)
        else:
            console.print("[red]Invalid choice. Please select from 0 to 12.[/red]")

        input("\nPress [Enter] to return to the main menu...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]Session ended by user.[/yellow]")
