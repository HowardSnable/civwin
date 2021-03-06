import json
import os
from datetime import datetime, timezone, timedelta
from types import SimpleNamespace

from django.conf import settings
from django.core.management.base import BaseCommand

from game.models import (Game, Map, Civ, Player, MetaData)


class Command(BaseCommand):
    help = 'Imports json match data from aoe2.net'

    def handle(self, *args, **options):
        # import matches and players from other files
        for f in os.listdir(os.path.join(settings.BASE_DIR, "data/matches")):
            print("importing " + f + "...")
            fpath = os.path.join(settings.BASE_DIR, "data", "matches", f)
            try:
                match_data = json.load(open(fpath, 'r', encoding="utf-8"),
                                       object_hook=lambda d: SimpleNamespace(**d))
                importMatches(match_data)
                os.remove(fpath)
            except Exception as e:
                print("Could not read" + f + "with error" + str(e))

        # add timestamp to metadata
        metadata = MetaData.load()
        metadata.last_pull = datetime.now()
        metadata.save()


###################
# If version of game and DB coincide: continue
# If version of DB > version of game: dont import this file
# Else: update version
#       OR:  clean DB, set Version, readBaseData, readMatches again
#
def checkVersion(match):
    try:
        if match.version is None:
            return False
        matchver = int(match.version)
        metadata = MetaData.load()
        if metadata.version is None or metadata.version < matchver:
            # (#optimization clean DB)
            metadata.version = matchver
            metadata.save()
            return True
        if metadata.version == matchver:
            return True
        if metadata.version > matchver:
            # dont import old games
            return False

    except Exception as e:
        # No metadata etc. -> still import
        print(e)
        return False


def importPlayer(player):
    myPlayer = Player()
    myPlayer.name = player.name if player.name else ""
    myPlayer.rating = player.rating
    myPlayer.player_id = player.profile_id
    myPlayer.save()


def importMatches(matches):
    newMatchList = []

    for newMatch in matches:
        if not Game.objects.filter(match_id=newMatch.match_id):
            # only ranked 1v1 RM 
            # only finished matches
            # only current version
            if newMatch.rating_type == 2 and newMatch.finished and checkVersion(newMatch):
                newP1 = newMatch.players[0]
                newP2 = newMatch.players[-1]
                # import players if not yet in database
                if not Player.objects.filter(player_id=newP1.profile_id):
                    importPlayer(newP1)
                if not Player.objects.filter(player_id=newP2.profile_id):
                    importPlayer(newP2)

                myMatch = Game()
                myMatch.match_id = newMatch.match_id
                myMatch.date = datetime.fromtimestamp(newMatch.started, tz=timezone.utc)
                myMatch.player1 = Player.objects.get(player_id=newP1.profile_id)
                myMatch.player2 = Player.objects.get(player_id=newP2.profile_id)
                myMatch.winner = newP1.won
                myMatch.civ1 = Civ.objects.get(civ_id=newP1.civ)
                myMatch.civ2 = Civ.objects.get(civ_id=newP2.civ)
                myMatch.duration = timedelta(seconds=newMatch.finished - newMatch.started)
                myMatch.version = int(newMatch.version)

                # Elo
                elo1 = 1000 if not myMatch.player1.rating else myMatch.player1.rating
                elo2 = 1000 if not myMatch.player2.rating else myMatch.player2.rating
                myMatch.avgelo = (elo1 + elo2) / 2

                myMap = Map.objects.get(map_id=newMatch.map_type)
                if myMap.gamecount:
                    myMap.gamecount += 1
                else:  # issue with 0 -> None
                    myMap.gamecount = 1
                myMap.save()
                myMatch.maptype = myMap

                newMatchList.append(myMatch)

    Game.objects.bulk_create(newMatchList)
