import re

from django import forms
from django.utils.safestring import mark_safe


class RangeSlider(forms.TextInput):
    def __init__(self, minimum, maximum, step, elem_name, initialMin, initialMax, *args, **kwargs):
        # todo: try to use type hints for function and method signatures
        self.minimum = str(minimum)     # todo: if you'd use f-strings this type cast is no longer required
        self.maximum = str(maximum)
        self.step = str(step)
        self.elem_name = str(elem_name)
        self.attrs = kwargs['attrs']
        self.initialMin = str(initialMin)
        self.initialMax = str(initialMax)
        widget = super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        s = super().render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        # todo: defined outside __init__ (you could just remove the self. right?)
        # todo: use f-strings for this multiline html thing (I think the js stuff should be moved to /static/js/main.js)
        html = """<div id="slider-range-""" + self.elem_id + """"></div>
        <script>
        $('#id_""" + self.elem_id + """')
        $( "#slider-range-""" + self.elem_id + """" ).slider({
        range: true,
        min: """ + self.minimum + """,
        max: """ + self.maximum + """,
        step: """ + self.step + """,
        values: [ """ + self.initialMin + """,""" + self.initialMax + """ ],
        slide: function( event, ui ) {  
          $( "#id_""" + self.elem_id + """" ).val(" """ + self.elem_name + """ "+ ui.values[ 0 ] + " - " + ui.values[ 1 ] );   
          document.getElementById("match_form").submit();
        }
        });
        $( "#id_""" + self.elem_id + """" ).val(" """ + self.elem_name + """ "+ $( "#slider-range-""" + self.elem_id + """" ).slider( "values", 0 ) +
        " - " + $( "#slider-range-""" + self.elem_id + """" ).slider( "values", 1 ) );
        
       

        </script>
        """
        return mark_safe(s + html)
