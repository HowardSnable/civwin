from django import forms
from django.forms import ModelChoiceField, ChoiceField
from .models import Map, Game, Civ
from .fields import RangeSliderField

class CivChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


def get_relevant_maps(allmaps):
    map_names = [("All","All Maps")]
    try:    
        for mymap in allmaps:
            if mymap.gamecount and mymap.gamecount >= 100:
                map_names.append((mymap.id,mymap.name))
    except:
        print("Error")
    finally:
        return map_names


class MatchSearchForm(forms.Form):      
    elorange = RangeSliderField(minimum=0,
        maximum=3000,
        step = 50,
        label="Elo", 
        name= "Elo: ", 
        attrs={'onchange':'this.form.submit()'},
        initialMin = 0 ,
        initialMax = 3000 )
    winneronly1 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onchange':'this.form.submit()'}),
        label= "Only Civ 1 wins", 
        required=False, 
        initial=True)
    civs1 = CivChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()'}), 
        queryset=Civ.objects.all(), 
        label= "",  
        empty_label=None )
    civs2 = CivChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()'}),
        queryset=Civ.objects.all(),
        label= "",  
        empty_label=None)
    winneronly2 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onchange':'this.form.submit()'}),
        label= "Only Civ 2 wins", 
        required=False, 
        initial=True)
    maps = ChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()'}),
        choices=get_relevant_maps(Map.objects.all()), 
        label= "Map:")
    durationrange = ChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()'}),
        choices = [("All","All Durations"),
                ("Short","Short (< 25 min)"),
                ("Medium","Medium (25-45 min)"),
                ("Long","Long (>45 min)")], label = "Duration:")


    def __init__(self, *args,**kwargs):
        super(MatchSearchForm, self).__init__(*args, **kwargs)
        if (args is None or args[0] is None) or (not 'elorange' in args[0]) or args[0]['elorange'] == None:
            self.initialMin = 0
            self.initialMax = 3000
        else:
            searchedElo = args[0]['elorange'].replace(" ", "").split(":")[1].split("-")
            self.fields['elorange'].widget.initialMin = str(searchedElo[0])
            self.fields['elorange'].widget.initialMax = str(searchedElo[1])
       