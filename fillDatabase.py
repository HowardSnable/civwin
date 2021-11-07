import os
# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aoematchups.settings")

# todo what's the purpose of this file? It looks kinda broken

from aoematchups.models import (Game, Map, Civ, Player)

import json
from types import SimpleNamespace

data = json.load(open(os.path.join(BASE_DIR, "data/strings.json", 'r'),object_hook=lambda d: SimpleNamespace(**d)))


for newCiv in data.civ:
	myCiv = Civ()
	myCiv.name = newCiv.name
	myCiv.icon = Null		# todo: 'null' instead?
	myCiv.save
