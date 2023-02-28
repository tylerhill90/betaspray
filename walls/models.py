from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

class Wall(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=20, help_text='Enter wall name')
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='./images')
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('owner', 'name',)


class Route(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    wall = models.ForeignKey(Wall, related_name='routes', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, help_text='Enter route name')
    GRADE_CHOICES = (
        ('V0', 'V0'),
        ('V1', 'V1'),
        ('V2', 'V2'),
        ('V3','V3'),
        ('V4', 'V4'),
        ('V5', 'V5'),
        ('V6', 'V6'),
        ('V7', 'V7'),
        ('V8', 'V8'),
        ('V9', 'V9'),
        ('V10', 'V10'),
        ('V11', 'V11'),
        ('V12', 'V12'),
    )
    grade = models.CharField(max_length=6, choices=GRADE_CHOICES, default='V0')
    tags = TaggableManager(blank=True)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wall', 'name',)

    def __str__(self):
        return self.name


class WallHold(models.Model):
    wall = models.ForeignKey(Wall, related_name='walls', on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    radius = models.IntegerField()


class RouteHold(models.Model):
    route = models.ForeignKey(Route, related_name='routes', on_delete=models.CASCADE)
    wall_hold = models.ForeignKey(WallHold, related_name='wall_holds', on_delete=models.CASCADE)
    HOLD_TYPES = (
        ('Foot', 'Foot'),
        ('Start', 'Start'),
        ('Hold', 'Hold'),
        ('Finish', 'Finish'),
    )
    hold_type = models.CharField(max_length=6, choices=HOLD_TYPES, default='Hold')
