from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Game, Civ, Player, Map, GameMode, MetaData

admin.site.register(Game)
admin.site.register(Civ)
admin.site.register(Player)
admin.site.register(Map)
admin.site.register(GameMode)
admin.site.register(MetaData)
