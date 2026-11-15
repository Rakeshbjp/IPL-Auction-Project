"""
Flask Web Application for IPL Auction & Player Analytics
Provides an interactive, visual browser interface matching real broadcast IPL Auctions.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from pathlib import Path
import json
import sys

# Ensure root project directory is on path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

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
    get_team_by_id,
)
from auction.auction_engine import (
    get_available_players_pool,
    run_player_auction,
    record_winning_bid,
    mark_player_unsold,
    reset_entire_auction,
    get_auction_stats,
    get_bid_increment,
)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "ipl_auction_secret_key_super_secure"

# Initialize DB on start
init_db()


@app.context_processor
def utility_processor():
    return dict(format_currency=format_currency)


@app.route("/")
def dashboard():
    """Main broadcast analytics dashboard matching Image 3 (Batting Analysis Dashboard)."""
    players = read_all_players()
    teams = get_team_budget_overview()
    top_runs = get_top_run_scorers_mergesort(10)
    top_avg = get_top_batting_averages_quicksort(10, min_matches=10)
    auction_stats = get_auction_stats()

    # Calculate aggregate league batting statistics
    total_runs = sum(p.get("runs", 0) for p in players)
    total_fours = sum(p.get("fours", 0) for p in players)
    total_sixes = sum(p.get("sixes", 0) for p in players)
    valid_sr_players = [p.get("strike_rate", 0.0) for p in players if p.get("strike_rate", 0.0) > 0]
    avg_strike_rate = (sum(valid_sr_players) / len(valid_sr_players)) if valid_sr_players else 0.0

    db_engine = "Supabase PostgreSQL" if (DB_MODE == "supabase" and is_supabase_configured()) else "SQLite3 (Relational)"

    return render_template(
        "index.html",
        total_players=len(players),
        total_runs=total_runs,
        total_fours=total_fours,
        total_sixes=total_sixes,
        avg_strike_rate=avg_strike_rate,
        teams=teams,
        top_runs=top_runs,
        top_avg=top_avg,
        auction_stats=auction_stats,
        db_engine=db_engine,
        players_json=json.dumps(players),
        teams_json=json.dumps(teams),
    )


@app.route("/players")
def players_page():
    """Rosters with search and role filtering (Bowler, Batsman, Allrounder, Wicketkeeper)."""
    role_filter = request.args.get("role", "").strip()
    search_query = request.args.get("q", "").strip()

    if search_query:
        players = find_player_by_name(search_query)
    elif role_filter:
        players = read_players_by_role(role_filter)
    else:
        players = read_all_players()

    return render_template(
        "players.html",
        players=players,
        active_role=role_filter,
        search_query=search_query
    )


@app.route("/player/<int:player_id>")
def player_detail(player_id):
    """Single player profile with detailed career statistics card."""
    player = find_player_by_id(player_id)
    if not player:
        flash("Player not found", "error")
        return redirect(url_for("players_page"))
    return render_template("player_detail.html", player=player)


@app.route("/player/add", methods=["GET", "POST"])
def add_player_page():
    """CRUD: Create - Add new player."""
    if request.method == "POST":
        try:
            name = request.form.get("name")
            role = request.form.get("role")
            country = request.form.get("country", "India")
            base_price = float(request.form.get("base_price", 2.0)) * 10_000_000

            matches = int(request.form.get("matches", 0))
            runs = int(request.form.get("runs", 0))
            highest_score = int(request.form.get("highest_score", 0))
            batting_avg = float(request.form.get("batting_avg", 0.0))
            strike_rate = float(request.form.get("strike_rate", 0.0))
            fours = int(request.form.get("fours", 0))
            sixes = int(request.form.get("sixes", 0))
            centuries = int(request.form.get("centuries", 0))
            fifties = int(request.form.get("fifties", 0))
            wickets = int(request.form.get("wickets", 0))
            bowling_economy = float(request.form.get("bowling_economy", 0.0))
            bowling_avg = float(request.form.get("bowling_avg", 0.0))

            pid = create_player(
                name=name, role=role, country=country, base_price=base_price,
                matches=matches, runs=runs, highest_score=highest_score,
                batting_avg=batting_avg, strike_rate=strike_rate,
                centuries=centuries, fifties=fifties, wickets=wickets,
                bowling_economy=bowling_economy, bowling_avg=bowling_avg
            )
            flash(f"Player '{name}' added successfully with ID #{pid}!", "success")
            return redirect(url_for("player_detail", player_id=pid))
        except Exception as e:
            flash(f"Error adding player: {e}", "error")

    return render_template("add_player.html")


@app.route("/player/<int:player_id>/edit", methods=["GET", "POST"])
def edit_player_page(player_id):
    """CRUD: Update - Update player statistics."""
    player = find_player_by_id(player_id)
    if not player:
        flash("Player not found", "error")
        return redirect(url_for("players_page"))

    if request.method == "POST":
        try:
            updates = {
                "matches": int(request.form.get("matches", player["matches"])),
                "runs": int(request.form.get("runs", player["runs"])),
                "highest_score": int(request.form.get("highest_score", player["highest_score"])),
                "batting_avg": float(request.form.get("batting_avg", player["batting_avg"])),
                "strike_rate": float(request.form.get("strike_rate", player["strike_rate"])),
                "centuries": int(request.form.get("centuries", player["centuries"])),
                "fifties": int(request.form.get("fifties", player["fifties"])),
                "wickets": int(request.form.get("wickets", player["wickets"])),
                "bowling_economy": float(request.form.get("bowling_economy", player["bowling_economy"])),
                "bowling_avg": float(request.form.get("bowling_avg", player["bowling_avg"])),
            }
            update_player_stats(player_id, updates)
            flash(f"Updated statistics for {player['name']} successfully!", "success")
            return redirect(url_for("player_detail", player_id=player_id))
        except Exception as e:
            flash(f"Error updating stats: {e}", "error")

    return render_template("edit_player.html", player=player)


@app.route("/player/<int:player_id>/delete", methods=["POST"])
def delete_player_action(player_id):
    """CRUD: Delete - Remove player with cascade check."""
    player = find_player_by_id(player_id)
    name = player["name"] if player else f"ID #{player_id}"
    delete_player(player_id)
    flash(f"Player '{name}' has been deleted.", "info")
    return redirect(url_for("players_page"))


@app.route("/teams")
def teams_page():
    """Teams & Budget Overview + Purchased squads."""
    teams = get_team_budget_overview()
    selected_code = request.args.get("team", "CSK").strip().upper()
    squad_data = get_team_purchased_players(selected_code)
    return render_template(
        "teams.html",
        teams=teams,
        selected_code=selected_code,
        squad_data=squad_data
    )


@app.route("/auction")
def auction_page():
    """Live interactive IPL Mega Auction Arena matching Image 2 & 4."""
    pool = get_available_players_pool()
    stats = get_auction_stats()
    teams = read_all_teams()
    return render_template(
        "auction.html",
        pool=pool,
        stats=stats,
        teams=teams,
        pool_json=json.dumps(pool),
        teams_json=json.dumps(teams),
    )


@app.route("/api/auction/simulate_next", methods=["POST"])
def api_auction_simulate_next():
    """Simulates next player bidding battle."""
    pool = get_available_players_pool()
    if not pool:
        return jsonify({"success": False, "message": "No available players in pool."})

    player = pool[0]
    status, winner, price = run_player_auction(player)

    return jsonify({
        "success": True,
        "player_id": player["player_id"],
        "player_name": player["name"],
        "status": status,
        "winning_team": winner["team_name"] if winner else "None",
        "winning_code": winner["short_code"] if winner else "UNSOLD",
        "sold_price": price,
        "sold_price_fmt": format_currency(price),
    })


@app.route("/api/auction/record_manual_bid", methods=["POST"])
def api_auction_record_manual():
    """Records a manual gavel knockdown or bid from interactive arena."""
    data = request.get_json() or {}
    player_id = int(data.get("player_id", 0))
    team_id = int(data.get("team_id", 0))
    sold_price = float(data.get("sold_price", 0.0))

    if player_id and team_id and sold_price > 0:
        success = record_winning_bid(player_id, team_id, sold_price)
        if success:
            return jsonify({"success": True, "message": "Winning bid recorded!"})
        else:
            return jsonify({"success": False, "message": "Insufficient team purse!"})
    elif player_id and data.get("unsold"):
        mark_player_unsold(player_id)
        return jsonify({"success": True, "message": "Player marked as UNSOLD."})

    return jsonify({"success": False, "message": "Invalid bid parameters."})


@app.route("/api/auction/reset", methods=["POST"])
def api_auction_reset():
    """Reset entire auction state."""
    reset_entire_auction()
    flash("Auction state reset! All ₹120 Cr purses restored.", "success")
    return redirect(url_for("auction_page"))


if __name__ == "__main__":
    print("\n=======================================================")
    print("🚀 IPL Auction Broadcast Arena is starting!")
    print("🌐 Open http://127.0.0.1:5000 in your browser.")
    print("=======================================================\n")
    app.run(debug=True, port=5000)
