from datetime import timedelta

from django.shortcuts import render

from .forms import MatchSearchForm
from .models import Game, Map, MetaData


def games_query(request, inOrder, nGames):
    # filter civs & winner
    if inOrder:
        searched1 = request.POST['civs1']
        searched2 = request.POST['civs2']
    else:
        # flip civ order
        searched1 = request.POST['civs2']
        searched2 = request.POST['civs1']

    if request.POST.get('winneronly1', False) and not request.POST.get('winneronly2', False):
        # Team 1 wins if in order
        games = Game.objects.filter(civ1=searched1, civ2=searched2, winner=inOrder)
    elif request.POST.get('winneronly2', False) and not request.POST.get('winneronly1', False):
        # Team 2 wins if in order
        games = Game.objects.filter(civ1=searched1, civ2=searched2, winner=not inOrder)
    else:
        # any team wins
        games = Game.objects.filter(civ1=searched1, civ2=searched2)

    # do not show mirrors twice
    if searched1 == searched2:
        if inOrder:
            nGames *= 2
        else:  # twice as many since games2 is empty
            return Game.objects.none()

    # filter by patch version
    version = MetaData.load().version
    games = games.filter(version=version)

    # filter by map
    searchedMap = request.POST['maps']
    if searchedMap != "All":
        s_map = Map.objects.get(id=searchedMap)
        games = games.filter(maptype=s_map)

    # filter by elo
    try:
        searchedElo = request.POST['elorange'].replace(" ", "").split(":")[1].split("-")
        games = games.filter(avgelo__gte=int(searchedElo[0]), avgelo__lte=int(searchedElo[1]))
    except:
        print("No Elo searched")

    # filter by duration
    searchedDuration = request.POST['durationrange']
    if searchedDuration == "Short":
        games = games.filter(duration__lte=timedelta(minutes=25))
    elif searchedDuration == "Medium":
        games = games.filter(duration__lte=timedelta(minutes=45), duration__gte=timedelta(minutes=25))
    elif searchedDuration == "Long":
        games = games.filter(duration__gte=timedelta(minutes=45))

    # only limited number
    games = games[:nGames]

    return games


def home_view(request, *args, **kwargs):
    # still show form
    queryset = Game.objects.all()
    form = MatchSearchForm(request.POST or None)
    # if form.is_valid():
    #	 form.save()

    nGames = 50

    # show results
    if request.method == "POST":
        games = games_query(request, True, nGames)
        games2 = games_query(request, False, nGames)
        context = {"object_list": games,
                   "object_list2": games2,
                   "form": form,
                   "metadata": MetaData.load()}
        return render(request, 'results.html', context)
    else:
        # only show form
        context = {"form": form, "metadata": MetaData.load()}
        return render(request, "search.html", context)
