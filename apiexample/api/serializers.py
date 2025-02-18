from .models import *
from rest_framework import serializers

class RecipesSerializer(serializers.ModelSerializer):
    Recipes_img = serializers.ImageField(required=False)    
    class Meta:
        model = Recipes
        fields = '__all__'