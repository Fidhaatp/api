from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny
# Create your views here.

class RecipeCreateView(generics.ListCreateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [AllowAny] 


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer


class RecipeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer


class RecipeDeleteView(generics.DestroyAPIView):    
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer