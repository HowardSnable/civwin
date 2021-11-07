from django import forms

from .widgets import RangeSlider


class RangeSliderField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum', 0)
        self.maximum = kwargs.pop('maximum', 100)
        self.step = kwargs.pop('step', 1)
        self.attrs = kwargs.pop('attrs', None)
        self.initialMin = kwargs.pop('initialMin', None)
        self.initialMax = kwargs.pop('initialMax', None)
        kwargs['widget'] = RangeSlider(self.minimum, self.maximum, self.step, self.name, self.initialMin,
                                       self.initialMax, attrs=self.attrs)
        if 'label' not in kwargs:
            kwargs['label'] = False
        super().__init__(*args, **kwargs)
