"""
CRUD operations package for IPL Auction System.
Handles Create, Read, Update, Delete for Players, Stats, Teams, and Budgets.
"""

from .player_crud import (
    create_player,
    read_all_players,
    read_players_by_role,
    find_player_by_name,
    find_player_by_id,
    update_player_stats,
    delete_player,
    get_top_run_scorers_mergesort,
    get_top_batting_averages_quicksort,
)
from .team_crud import (
    read_all_teams,
    get_team_by_id,
    get_team_by_code,
    get_team_purchased_players,
    get_team_budget_overview,
    update_team_budget,
)

__all__ = [
    "create_player",
    "read_all_players",
    "read_players_by_role",
    "find_player_by_name",
    "find_player_by_id",
    "update_player_stats",
    "delete_player",
    "get_top_run_scorers_mergesort",
    "get_top_batting_averages_quicksort",
    "read_all_teams",
    "get_team_by_id",
    "get_team_by_code",
    "get_team_purchased_players",
    "get_team_budget_overview",
    "update_team_budget",
]
