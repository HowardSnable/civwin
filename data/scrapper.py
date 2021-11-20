import getopt
import json
import os.path
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace


def fetch_hours(n_per_hour: int, matchpath: str):
    time_now = datetime.now()

    for i in range(24 * n_per_hour):
        print(f"loading for time {i + 1} of {24 * n_per_hour} ...")
        time_i = time_now - timedelta(hours=i / n_per_hour + 1)
        url = "https://aoe2.net/api/matches?game=aoe2de&count=1000&since=" + str(round(time_i.timestamp()))
        r = urllib.request.urlopen(url)
        with open(f"{matchpath}matches{i}.json", 'wb') as f:
            f.write(r.read())


def fetch_leaderboard(n_players: str, datapath: str):
    # save leaderboard
    url = "https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=3&start=1&count=" + n_players
    r = urllib.request.urlopen(url)
    with open(datapath + "leaderboard.json", 'wb') as f:
        f.write(r.read())


def fetch_tops(n_games: str, datapath: str, matchpath: str):
    # iterate through players and save files
    leaderboard_data = json.load(open(datapath + "leaderboard.json", 'r', encoding='utf8'),
                                 object_hook=lambda d: SimpleNamespace(**d))
    for i in range(len(leaderboard_data.leaderboard)):
        print("loading for player " + str(i + 1) + " of " + str(len(leaderboard_data.leaderboard)) + "...")
        player = leaderboard_data.leaderboard[i]
        url = "https://aoe2.net/api/player/matches?game=aoe2de&steam_id=" + player.steam_id + "&count=" + n_games
        r = urllib.request.urlopen(url)
        with open(matchpath + "top_matches" + "%s" % i + ".json", 'wb') as f:
            f.write(r.read())


BASE_DIR = Path(__file__).resolve().parents[1]
data_path = os.path.join(BASE_DIR, "data/")
match_path = os.path.join(data_path, "matches/")
per_hour = 2
top_players = "300"
games_per_player = "50"

options = "h:p:g:d"
long_options = ["perHour=", "players=", "games=", "delete"]
try:
    arguments, values = getopt.getopt(sys.argv[1:], options, long_options)
    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--perHour"):
            per_hour = int(currentValue)
        elif currentArgument in ("-p", "--players"):
            top_players = currentValue
        elif currentArgument in ("-g", "--games"):
            games_per_player = currentValue
        elif currentArgument in ("-d", "--delte"):
            # delete old files
            for root, dirs, files in os.walk(matchpath):
                for file in files:
                    os.remove(os.path.join(root, file))

except getopt.GetoptError:
    pass

fetch_hours(per_hour, match_path)
fetch_leaderboard(top_players, data_path)
fetch_tops(games_per_player, data_path, match_path)
