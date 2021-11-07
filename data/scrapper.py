from datetime import datetime, time, timedelta
import urllib.request
import ssl
import getopt, sys
import os, re, os.path
from pathlib import Path
import json
from types import SimpleNamespace

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(__file__).resolve().parent.parent
basepath = os.path.join(BASE_DIR,"data/")
matchpath = os.path.join(basepath,"matches/")
perHour = 2
nTopPlayers = 300
nGamesperPlayer = 50

try:
	options = "h:p:g:d"
	long_options = ["perHour=", "players=", "games=", "delete"]
	arguments, values = getopt.getopt(sys.argv[1:], options, long_options)
	# checking each argument
	for currentArgument, currentValue in arguments:
	    if currentArgument in ("-h", "--perHour"):
	    	perHour = int(currentValue)             
	    elif currentArgument in ("-p", "--players"):
	        nTopPlayers = int(currentValue)             
	    elif currentArgument in ("-g", "--games"):
	        nGamesperPlayer = int(currentValue)             
	    elif currentArgument in ("-d", "--delte"):	          
	        # delte old files
	        for root, dirs, files in os.walk(matchpath):
	            for file in files:
	                os.remove(os.path.join(root, file))
           
except getopt.GetoptError:
	pass



#####################
# get "all" games
timenow = datetime.now()

for i in range(24*perHour):
	print("loading for time " + str(i+1) + " of " + str(24*perHour) + "...")
	time_i = timenow-timedelta(hours = i/perHour+1)
	url = "https://aoe2.net/api/matches?game=aoe2de&count=1000&since="+ str(round(time_i.timestamp()) )
	r = urllib.request.urlopen(url)
	with open(matchpath+"matches"+"%s" %i+".json", 'wb') as f:
		f.write(r.read()) 


###################
# get last games from top players

# save leaderboard
url = "https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=3&start=1&count="+ str(nTopPlayers) 
r = urllib.request.urlopen(url)
with open(basepath+"leaderboard.json", 'wb') as f:
	f.write(r.read()) 

#iterate through players and save files
leaderboardData = json.load(open(basepath+"leaderboard.json", 'r', encoding = 'utf8'), object_hook=lambda d: SimpleNamespace(**d))
for i in range(len(leaderboardData.leaderboard)):
	print("loading for player " + str(i+1) + " of " + str(len(leaderboardData.leaderboard)) + "...")
	player = leaderboardData.leaderboard[i]
	url = "https://aoe2.net/api/player/matches?game=aoe2de&steam_id="+player.steam_id+ "&count="+ str(nGamesperPlayer)
	r = urllib.request.urlopen(url)
	with open(matchpath+"top_matches"+"%s" %i+".json", 'wb') as f:
		f.write(r.read()) 
