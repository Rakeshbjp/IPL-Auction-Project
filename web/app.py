"""
Flask Web Application for Official TATA IPL Mega Auction & Pre-Auction Center
Supports:
- Pre-Auction Preparations: Player Registration, Shortlisting, Purse & Squad Limits (18-25, max 8 overseas)
- Mega Auction vs Mini Auction Modes (Mega: RTM = 6 - Retentions; Mini: 0 RTM)
- Sequential Categorized Sets (Capped Batters, All-rounders, Wicketkeepers, Fast Bowlers, Spinners, Uncapped)
- Live Auction Arena with Official Increment Slabs and RTM Card Invocations
- Accelerated Auction Round for Shortlisted Unsold Players
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
    get_team_by_code,
    retain_player_for_team,
    release_player_from_team,
    get_team_full_dossier,
)
from auction.auction_engine import (
    get_available_players_pool,
    get_unsold_players_pool,
    add_to_accelerated_shortlist,
    get_auction_sets,
    get_auction_mode,
    set_auction_mode,
    run_player_auction,
    record_winning_bid,
    mark_player_unsold,
    reset_entire_auction,
    get_auction_stats,
    get_bid_increment,
    check_rtm_eligibility,
    execute_rtm_claim,
    validate_team_bid,
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
    """
    Official IPL Auction Command & Pre-Auction Center:
    - Mode Switcher (Mega vs Mini Auction)
    - Pre-Auction Hub (Retentions, RTM allocations, Squad limits 18-25, max 8 overseas)
    - Sequential Sets Hub (BA1, AL1, WK1, FA1, SP1, UN1)
    - Player Registration & Shortlisting Pool
    - Accelerated Auction Round Preparation
    """
    teams = read_all_teams()
    players = read_all_players()
    auction_sets = get_auction_sets()
    auction_stats = get_auction_stats()
    unsold_players = get_unsold_players_pool()
    current_mode = get_auction_mode()

    # Pre-auction calculations
    total_purse_league = sum(t.get("total_budget", 0) for t in teams)
    total_retained_players = sum(t.get("retentions_count", 0) for t in teams)
    total_retention_spend = sum(t.get("retention_spend", 0.0) for t in teams)
    total_rtm_cards_available = sum(t.get("rtm_cards", 0) for t in teams)

    # Separate Capped and Uncapped player pools
    capped_players = [p for p in players if p.get("is_capped", 1) == 1]
    uncapped_players = [p for p in players if p.get("is_capped", 1) == 0]

    # Base price tiers count
    tiers = {
        "2_cr": len([p for p in players if p.get("base_price") == 20000000.0]),
        "1_5_cr": len([p for p in players if p.get("base_price") == 15000000.0]),
        "1_cr": len([p for p in players if p.get("base_price") == 10000000.0]),
        "uncapped_50_l": len([p for p in players if p.get("base_price") == 5000000.0]),
        "uncapped_40_l": len([p for p in players if p.get("base_price") == 4000000.0]),
        "uncapped_30_l": len([p for p in players if p.get("base_price") == 3000000.0]),
        "uncapped_20_l": len([p for p in players if p.get("base_price") == 2000000.0]),
    }

    db_engine = "Supabase PostgreSQL" if (DB_MODE == "supabase" and is_supabase_configured()) else "SQLite3 (Relational)"

    return render_template(
        "index.html",
        teams=teams,
        players=players,
        capped_players=capped_players,
        uncapped_players=uncapped_players,
        auction_sets=auction_sets,
        auction_stats=auction_stats,
        unsold_players=unsold_players,
        current_mode=current_mode,
        total_purse_league=total_purse_league,
        total_retained_players=total_retained_players,
        total_retention_spend=total_retention_spend,
        total_rtm_cards_available=total_rtm_cards_available,
        tiers=tiers,
        db_engine=db_engine,
        teams_json=json.dumps(teams),
        players_json=json.dumps(players),
        capped_players_json=json.dumps(capped_players),
        uncapped_players_json=json.dumps(uncapped_players),
    )


@app.route("/players")
def players_page():
    """Rosters with search, capped/uncapped filtering, and DSA sorting (Merge Sort & Quick Sort by Base Price)."""
    role_filter = request.args.get("role", "").strip()
    set_filter = request.args.get("set", "").strip()
    sort_filter = request.args.get("sort", "").strip()
    cap_filter = request.args.get("cap", "all").strip().lower()
    search_query = request.args.get("q", "").strip()

    if search_query:
        players = find_player_by_name(search_query)
    elif role_filter:
        players = read_players_by_role(role_filter)
    else:
        players = read_all_players()

    if cap_filter == "capped":
        players = [p for p in players if p.get("is_capped", 1) == 1]
    elif cap_filter == "uncapped":
        players = [p for p in players if p.get("is_capped", 1) == 0]

    if set_filter and set_filter != "ALL":
        players = [p for p in players if p.get("set_code") == set_filter]

    # DSA Sorting options using Merge Sort & Quick Sort by Base Price, Runs, or Avg
    if sort_filter == "mergesort_price":
        from dsa.merge_sort import merge_sort
        players = merge_sort(players, key="base_price", descending=True)
    elif sort_filter == "mergesort_price_asc":
        from dsa.merge_sort import merge_sort
        players = merge_sort(players, key="base_price", descending=False)
    elif sort_filter == "quicksort_price":
        from dsa.quick_sort import quick_sort
        players = quick_sort(players, key="base_price", descending=True)
    elif sort_filter == "quicksort_price_asc":
        from dsa.quick_sort import quick_sort
        players = quick_sort(players, key="base_price", descending=False)
    elif sort_filter == "runs":
        from dsa.merge_sort import merge_sort
        players = merge_sort(players, key="runs", descending=True)
    elif sort_filter == "avg":
        from dsa.quick_sort import quick_sort
        players = quick_sort(players, key="batting_avg", descending=True)

    auction_sets = get_auction_sets()

    return render_template(
        "players.html",
        players=players,
        active_role=role_filter,
        active_set=set_filter,
        active_sort=sort_filter,
        active_cap=cap_filter,
        search_query=search_query,
        auction_sets=auction_sets
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
    """CRUD: Create - Register a new player with base price category and set."""
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
            flash(f"Player '{name}' registered successfully with ID #{pid}!", "success")
            return redirect(url_for("player_detail", player_id=pid))
        except Exception as e:
            flash(f"Error registering player: {e}", "error")

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
    """Franchise Squads, Purse Tracking, Retentions & RTM Cards."""
    teams = read_all_teams()
    selected_code = request.args.get("team", "CSK").strip().upper()
    dossier = get_team_full_dossier(selected_code)
    current_mode = get_auction_mode()
    return render_template(
        "teams.html",
        teams=teams,
        selected_code=selected_code,
        dossier=dossier,
        squad_data=dossier,
        current_mode=current_mode
    )


@app.route("/auction")
def auction_page():
    """
    Live Interactive TATA IPL Mega Auction Arena:
    - 3D Floating Drone Pod
    - Sequential Sets filtering (BA1, AL1, WK1, FA1, SP1, UN1)
    - Increments: <1Cr: +10L, 1-2Cr: +20L, 2-5Cr: +25L, 5-10Cr: +50L, >10Cr: +1Cr
    - Right-To-Match (RTM) Card Challenge Prompts for Former Teams
    - Accelerated Round Mode
    - Strict Squad Limits (18-25) & Overseas Cap (max 8)
    """
    set_code = request.args.get("set", "ALL").strip()
    is_accelerated = request.args.get("accelerated", "0") == "1"

    pool = get_available_players_pool(set_code=set_code if set_code != "ALL" else None, accelerated_only=is_accelerated)
    stats = get_auction_stats()
    teams = read_all_teams()
    auction_sets = get_auction_sets()
    current_mode = get_auction_mode()

    return render_template(
        "auction.html",
        pool=pool,
        stats=stats,
        teams=teams,
        auction_sets=auction_sets,
        active_set=set_code,
        is_accelerated=is_accelerated,
        current_mode=current_mode,
        pool_json=json.dumps(pool),
        teams_json=json.dumps(teams),
    )


# ============================================================================
# REAL-TIME AUCTION & RTM APIS
# ============================================================================

@app.route("/api/auction/mode", methods=["POST"])
def api_set_auction_mode():
    """Toggles between Mega Auction and Mini Auction."""
    data = request.get_json() or {}
    mode = data.get("mode", "mega")
    new_mode = set_auction_mode(mode)
    teams = read_all_teams()
    return jsonify({
        "success": True,
        "mode": new_mode,
        "message": f"Switched to {'TATA IPL Mega Auction (RTM Active)' if new_mode == 'mega' else 'IPL Mini Auction (0 RTM Cards)'}",
        "teams": teams
    })


@app.route("/api/auction/simulate_next", methods=["POST"])
def api_auction_simulate_next():
    """Simulates next player bidding battle with RTM handling."""
    data = request.get_json() or {}
    set_code = data.get("set_code")
    is_accelerated = data.get("accelerated", False)

    pool = get_available_players_pool(set_code=set_code if set_code != "ALL" else None, accelerated_only=is_accelerated)
    if not pool:
        return jsonify({"success": False, "message": "No available players in selected pool/set."})

    player = pool[0]
    status, winner, price, rtm_team = run_player_auction(player)

    return jsonify({
        "success": True,
        "player_id": player["player_id"],
        "player_name": player["name"],
        "role": player["role"],
        "country": player["country"],
        "set_code": player.get("set_code", "BA1"),
        "status": status,
        "winning_team": winner["team_name"] if winner else "None",
        "winning_code": winner["short_code"] if winner else "UNSOLD",
        "sold_price": price,
        "sold_price_fmt": format_currency(price),
        "rtm_invoked": rtm_team is not None,
        "rtm_team": rtm_team["short_code"] if rtm_team else None
    })


@app.route("/api/auction/check_rtm", methods=["POST"])
def api_check_rtm():
    """Checks if former franchise is eligible to invoke RTM Card."""
    data = request.get_json() or {}
    player_id = int(data.get("player_id", 0))
    winning_team_id = int(data.get("winning_team_id", 0))

    eligible, former_team, message = check_rtm_eligibility(player_id, winning_team_id)
    return jsonify({
        "eligible": eligible,
        "former_team": former_team,
        "message": message
    })


@app.route("/api/auction/execute_rtm", methods=["POST"])
def api_execute_rtm():
    """Executes RTM Card match by former team."""
    data = request.get_json() or {}
    player_id = int(data.get("player_id", 0))
    former_team_id = int(data.get("former_team_id", 0))
    final_price = float(data.get("final_price", 0.0))

    if player_id and former_team_id and final_price > 0:
        success = execute_rtm_claim(player_id, former_team_id, final_price)
        if success:
            return jsonify({"success": True, "message": "RTM Card successfully exercised! Player retained!"})
        else:
            return jsonify({"success": False, "message": "Could not complete RTM transaction."})

    return jsonify({"success": False, "message": "Invalid RTM parameters."})


@app.route("/api/auction/record_manual_bid", methods=["POST"])
def api_auction_record_manual():
    """Records a manual gavel knockdown or bid from interactive arena."""
    data = request.get_json() or {}
    player_id = int(data.get("player_id", 0))
    team_id = int(data.get("team_id", 0))
    sold_price = float(data.get("sold_price", 0.0))

    if player_id and team_id and sold_price > 0:
        # Validate squad constraints
        team = get_team_by_id(team_id)
        player = find_player_by_id(player_id)
        if team and player:
            can_bid, reason = validate_team_bid(team, player, sold_price)
            if not can_bid:
                return jsonify({"success": False, "message": reason})

        success = record_winning_bid(player_id, team_id, sold_price)
        if success:
            return jsonify({"success": True, "message": "Winning bid recorded!"})
        else:
            return jsonify({"success": False, "message": "Insufficient team purse!"})
    elif player_id and data.get("unsold"):
        mark_player_unsold(player_id)
        return jsonify({"success": True, "message": "Player marked as UNSOLD."})

    return jsonify({"success": False, "message": "Invalid bid parameters."})


@app.route("/api/auction/shortlist_accelerated", methods=["POST"])
def api_shortlist_accelerated():
    """Adds an unsold player to the Accelerated Auction shortlist."""
    data = request.get_json() or {}
    player_id = int(data.get("player_id", 0))
    if player_id:
        success = add_to_accelerated_shortlist(player_id)
        return jsonify({"success": success, "message": "Added to Accelerated Auction Round!"})
    return jsonify({"success": False, "message": "Player ID required."})


@app.route("/api/auction/reset", methods=["POST"])
def api_auction_reset():
    """Reset entire auction state."""
    reset_entire_auction()
    flash("Auction state reset! All purses and RTM cards restored.", "success")
    return redirect(url_for("auction_page"))


@app.route("/api/team/<team_code>/details", methods=["GET"])
def api_team_details(team_code):
    """Returns complete franchise details: info, retentions, auction buys, and available players to retain."""
    dossier = get_team_full_dossier(team_code)
    if not dossier:
        return jsonify({"success": False, "message": "Team not found"}), 404
    return jsonify({"success": True, "data": dossier})


@app.route("/api/team/retain", methods=["POST"])
def api_team_retain():
    """Retains a player for a franchise."""
    data = request.get_json() or {}
    team_id = int(data.get("team_id", 0))
    player_id = int(data.get("player_id", 0))
    retention_price = float(data.get("retention_price", 0.0)) if data.get("retention_price") else None

    if not team_id or not player_id:
        return jsonify({"success": False, "message": "Team ID and Player ID are required."}), 400

    success, msg = retain_player_for_team(team_id, player_id, retention_price)
    return jsonify({"success": success, "message": msg})


@app.route("/api/team/release", methods=["POST"])
def api_team_release():
    """Releases a player from a franchise back to the available pool."""
    data = request.get_json() or {}
    team_id = int(data.get("team_id", 0))
    player_id = int(data.get("player_id", 0))

    if not team_id or not player_id:
        return jsonify({"success": False, "message": "Team ID and Player ID are required."}), 400

    success, msg = release_player_from_team(team_id, player_id)
    return jsonify({"success": success, "message": msg})


if __name__ == "__main__":
    print("\n=======================================================")
    print("🚀 TATA IPL Mega Auction Command Center is starting!")
    print("🌐 Open http://127.0.0.1:5000 in your browser.")
    print("=======================================================\n")
    app.run(debug=True, port=5000)
