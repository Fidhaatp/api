from django.db import models
from datetime import timedelta
# Create your models here.

class Recipes(models.Model):
    name = models.CharField(max_length=100)
    prep_time = models.DurationField(default=timedelta(minutes=120))
    DIFFICULTY_CHOICES = [
    (1, 'Easy'),
    (2, 'Medium'),
    (3, 'Hard'),
    ]
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    vegitarian = models.BooleanField()
    recipe_img = models.ImageField(upload_to='recipe/')
    description = models.CharField(max_length=5000)

    def __str__(self):
        return self.name