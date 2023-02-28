from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Wall,
    Route,
    WallHold
)


class WallForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        wall_owner = cleaned_data.get('owner')
        wall_name = cleaned_data.get('name')
        if Wall.objects.filter(owner=wall_owner, name=wall_name).exists():
            self.add_error('name', 'A wall with that name already exists.')
        return cleaned_data

    class Meta:
        model = Wall
        fields = ['name', 'image']


class RouteForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        if Route.objects.filter(
            wall=self.data['wall_id'], name=cleaned_data['name']
        ).exists():
            raise ValidationError('A route with that name for this wall already exists.')
        return cleaned_data

    class Meta:
        model = Route
        fields = ['name', 'grade', 'tags', 'notes']


class WallHoldForm(forms.ModelForm):
    class Meta:
        model = WallHold
        fields = '__all__'
