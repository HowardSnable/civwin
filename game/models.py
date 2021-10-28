from django.db import models

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class MetaData(SingletonModel):
	version = models.IntegerField()
	last_pull = models.DateTimeField(auto_now_add=True)
	support_mail = models.EmailField(blank= True, null=True)

class Civ(models.Model):
	class Meta:
		ordering = ['name']
	name = models.TextField(blank = False, null = False)
	icon = models.TextField()
	civ_id = models.IntegerField()


class Map(models.Model):
	name = models.TextField(blank=False, null = False)
	map_id = models.IntegerField()
	gamecount = models.IntegerField(blank=False, null = True)


class GameMode(models.Model):
	name = models.TextField(blank=False, null = False)
	ranked = models.BooleanField()
	gamemode_id = models.IntegerField()

class Player(models.Model):
	name = models.TextField(blank = False, null = False )
	rating = models.IntegerField(blank = True, null = True)
	player_id = models.IntegerField()

# Create your models here.
class Game(models.Model):
	date = models.DateTimeField(null=True)
	player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name = 'player1')
	player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name = 'player2')
	winner = models.BooleanField(null = True) # did player1 win?
	civ1 =  models.ForeignKey(Civ, on_delete=models.CASCADE, related_name = 'civ1')
	civ2 =  models.ForeignKey(Civ, on_delete=models.CASCADE, related_name = 'civ2')
	maptype =  models.ForeignKey(Map, on_delete=models.CASCADE, related_name = 'map')
	match_id = models.IntegerField()
	duration = models.DurationField()
	avgelo  = models.IntegerField()
	version = models.IntegerField()


	def getRating():
		return (player1.rating + player2.rating)/2


	