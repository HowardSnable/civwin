import os
# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aoematchups.settings")

from aoematchups.models import (Game, Map, Civ, Player)

import json
from types import SimpleNamespace

data = json.load(open(os.path.join(BASE_DIR, "data/strings.json", 'r'),object_hook=lambda d: SimpleNamespace(**d)))


for newCiv in data.civ:
	myCiv = Civ()
	myCiv.name = newCiv.name
	myCiv.icon = Null
	myCiv.save
