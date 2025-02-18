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


class RecipeSearchviewset(generics.ListAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return Recipes.objects.filter(name__icontains=name)
    

# def create_recipe(request):
#     if request.method == 'POST':
#         form = RecipesForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = RecipesForm()
#     return render(request, 'create_recipe.html', {'form': form})    