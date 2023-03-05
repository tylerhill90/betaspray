from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Wall,
    Route,
    WallHold
)


class WallForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super(WallForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(WallForm, self).clean()
        wall_name = cleaned_data.get('name')
        if Wall.objects.filter(owner=self.owner, name=wall_name).exists():
            self.add_error(field='name', error=ValidationError('You already have a wall with that name.'))
        return cleaned_data

    class Meta:
        model = Wall
        fields = ['name', 'image']


class WallHoldForm(forms.ModelForm):
    class Meta:
        model = WallHold
        fields = '__all__'


class RouteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.wall_id = kwargs.pop('wall_id', None)
        super(RouteForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RouteForm, self).clean()
        route_name = cleaned_data.get('name')
        if Route.objects.filter(wall=self.wall_id, name=route_name).exists():
            self.add_error(field='name', error=ValidationError('A route with that name for already exists for this wall.'))
        return cleaned_data

    class Meta:
        model = Route
        fields = ['name', 'grade', 'tags', 'notes']
