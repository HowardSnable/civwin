import re

from django import forms
from django.utils.safestring import mark_safe


class RangeSlider(forms.TextInput):
    def __init__(self, minimum:int, 
                        maximum:int, 
                        step:int, 
                        elem_name, 
                        initialMin:int, 
                        initialMax:int, 
                        *args, **kwargs):
        self.minimum = minimum
        self.maximum = maximum
        self.step = step
        self.elem_name = elem_name
        self.attrs = kwargs['attrs']
        self.initialMin = initialMin
        self.initialMax = initialMax
        self.widget = super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        s = super().render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        html = f"""<div id="slider-range-{self.elem_id}"></div>
        <script src = "{{% static 'scripts/eloslider.js' %}}">        </script>
        """
        return mark_safe(s + html)
