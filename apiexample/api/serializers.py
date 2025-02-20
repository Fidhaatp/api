from .models import *
from rest_framework import serializers

class RecipesSerializer(serializers.ModelSerializer):
    recipe_img = serializers.ImageField(required=False)  # Use correct field name

    class Meta:
        model = Recipes
        fields = '__all__'
