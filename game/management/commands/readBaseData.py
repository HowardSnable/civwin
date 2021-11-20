import json
import os
from types import SimpleNamespace

from django.conf import settings
from django.core.management.base import BaseCommand

from game.models import (Map, Civ)


class Command(BaseCommand):
    help = 'Imports json match data from aoe2.net'

    def handle(self, *args, **options):
        base_data = json.load(open(os.path.join(settings.BASE_DIR, "data", "strings.json"), 'r'),
                              object_hook=lambda d: SimpleNamespace(**d))

        # import civs
        import_civs(base_data.civ)

        # import maps
        import_maps(base_data.map_type)

        return


def import_civs(civs):
    for newCiv in civs:
        # only import if not yet in DB
        if not Civ.objects.filter(civ_id=newCiv.id):
            my_civ = Civ()
            my_civ.name = newCiv.string
            my_civ.icon = f"{{% static 'civs/' %}} {my_civ.name}.png"
            my_civ.civ_id = newCiv.id
            my_civ.save()


def import_maps(maps):
    for newMap in maps:
        # only import if not yet in DB
        if not Map.objects.filter(map_id=newMap.id):
            my_map = Map()
            my_map.name = newMap.string
            my_map.map_id = newMap.id
            my_map.game_count = 0
            my_map.save()
