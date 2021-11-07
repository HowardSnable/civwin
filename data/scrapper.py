import getopt
import json
import os.path      # pathlib gives you an easier time and better to use one tools for path operations than two
import ssl
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

ssl._create_default_https_context = ssl._create_unverified_context      # todo: this looks suspicious (is this needed?)

BASE_DIR = Path(__file__).resolve().parents[1]
datapath = os.path.join(BASE_DIR, "data/")
matchpath = os.path.join(datapath, "matches/")
perHour = 2
nTopPlayers = 300
nGamesperPlayer = 50
# todo: consider using snake case names instead of camel case names for variables, functions, methods etc.

options = "h:p:g:d"
long_options = ["perHour=", "players=", "games=", "delete"]
try:
    # todo: consider using argparse instead
    arguments, values = getopt.getopt(sys.argv[1:], options, long_options)
    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--perHour"):
            perHour = int(currentValue)
        elif currentArgument in ("-p", "--players"):
            nTopPlayers = int(currentValue)
            # todo: not really required to cast to int right, because you convert it back to str later on
        elif currentArgument in ("-g", "--games"):
            nGamesperPlayer = int(currentValue)
            # same as above
        elif currentArgument in ("-d", "--delte"):
            # delte old files todo: guess this should mean 'delete'?
            for root, dirs, files in os.walk(matchpath):
                for file in files:
                    os.remove(os.path.join(root, file))

except getopt.GetoptError:
    pass

#####################
# get "all" games
time_now = datetime.now()

for i in range(24 * perHour):
    print(f"loading for time {i + 1} of {24 * perHour} ...")
    time_i = time_now - timedelta(hours=i / perHour + 1)
    url = "https://aoe2.net/api/matches?game=aoe2de&count=1000&since=" + str(round(time_i.timestamp()))
    r = urllib.request.urlopen(url)
    with open(f"{matchpath}matches{i}.json", 'wb') as f:
        f.write(r.read())

    ###################
# get last games from top players

# save leaderboard
url = "https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=3&start=1&count=" + str(nTopPlayers)
r = urllib.request.urlopen(url)
with open(datapath + "leaderboard.json", 'wb') as f:
    f.write(r.read())

# iterate through players and save files
leaderboardData = json.load(open(datapath + "leaderboard.json", 'r', encoding='utf8'),
                            object_hook=lambda d: SimpleNamespace(**d))
for i in range(len(leaderboardData.leaderboard)):
    print("loading for player " + str(i + 1) + " of " + str(len(leaderboardData.leaderboard)) + "...")
    player = leaderboardData.leaderboard[i]
    url = "https://aoe2.net/api/player/matches?game=aoe2de&steam_id=" + player.steam_id + "&count=" + str(
        nGamesperPlayer)
    r = urllib.request.urlopen(url)
    with open(matchpath + "top_matches" + "%s" % i + ".json", 'wb') as f:
        f.write(r.read())
