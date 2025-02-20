from .models import *
from rest_framework import serializers

# class RecipesSerializer(serializers.ModelSerializer):
#     Recipes_img = serializers.ImageField(required=False)    
#     class Meta:
#         model = Recipes
#         fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    recipe_img = serializers.SerializerMethodField()

    def get_recipe_img(self, obj):
        request = self.context.get('request')
        if obj.recipe_img:
            return request.build_absolute_uri(obj.recipe_img.url)
        return None

    class Meta:
        model = Recipes
        fields = ['id', 'name', 'recipe_img']