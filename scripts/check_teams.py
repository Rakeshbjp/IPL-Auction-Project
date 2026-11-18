import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from crud.team_crud import read_all_teams

teams = read_all_teams()
for t in teams:
    code = t["short_code"]
    ret_cnt = t["retentions_count"]
    names = t["retained_names"]
    spend = t["retention_spend_fmt"]
    rem = t["remaining_budget_fmt"]
    rtm = t["rtm_cards"]
    squad = t["total_squad_size"]
    print(f"{code}: Retentions={ret_cnt}, Names='{names}', Spend={spend}, Remaining={rem}, RTM={rtm}, Squad={squad}/25")
