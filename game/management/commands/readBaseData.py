from django.core.management.base import BaseCommand, CommandError
from game.models import  (Game, Map, Civ, Player, GameMode)
import os
from datetime import datetime, timezone
from django.conf import settings

import json
from types import SimpleNamespace
import urllib
import urllib.request
from django.core.files import File

class Command(BaseCommand):
    help = 'Imports json match data from aoe2.net'

    def handle(self, *args, **options):

        base_data = json.load(open(os.path.join(settings.BASE_DIR, "data","strings.json"), 'r'), object_hook=lambda d: SimpleNamespace(**d))

        # import civs
        importCivs(base_data.civ)

        # import maps
        importMaps(base_data.map_type)

        return
     

        
def importCivs(civs):
     for newCiv in civs:
        # only import if not yet in DB
        if(not Civ.objects.filter(civ_id = newCiv.id)):
            myCiv = Civ()
            myCiv.name = newCiv.string
            myCiv.icon =  "../media/civs/"+  myCiv.name+".png"
            myCiv.civ_id = newCiv.id
            myCiv.save()

def importMaps(maps):     
    for newMap in maps:
         # only import if not yet in DB
        if(not Map.objects.filter(map_id = newMap.id)):
            myMap = Map()
            myMap.name = newMap.string
            myMap.map_id = newMap.id
            myMap.game_count = 0
            myMap.save()
