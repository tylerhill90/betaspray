from django import forms
from django.core.exceptions import ValidationError

from .models import (Route)

class RouteForm(forms.ModelForm):
    def __int__(self, *args, disabled_project=True, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        self.fields['wall_id'].disabled = disabled_project

    def clean(self):
        cleaned_data = self.cleaned_data
        if Route.objects.filter(
            wall=cleaned_data['wall_id'], name=cleaned_data['name']
        ).exists():
            raise ValidationError('A route with that name for this wall already exists.')
        return cleaned_data

    class Meta:
        model = Route
        fields = ['name', 'wall', 'grade', 'tags', 'notes']
