from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import RecipesSerializer
from .models import Recipes
from rest_framework.permissions import AllowAny
from .forms import RecipesForm
import requests
from django.contrib import messages

# API Views
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

# Django Form View
def create_recipe(request):
    if request.method == 'POST':
        form = RecipesForm(request.POST, request.FILES)
        if form.is_valid(): 
            try:
                form.save()
                api_url = 'http://127.0.0.1:2000/create/'
                data = form.cleaned_data
                print(data)
                response = requests.post(api_url, data=data, files={'recipe_img': request.FILES['recipe_img']})    
                if response.status_code == 400:
                    messages.success(request, 'Recipe inserted successfully')
                else:
                    messages.error(request, f'Error {response.status_code}')    

            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')

        else:
            messages.error(request, 'Form is not valid')

    else:
        form = RecipesForm()

    return render(request, 'create-recipe.html', {'form': form})        


def update_detail(request, id):
    api_url = 'http://127.0.0.1:2000/detail/{id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        ingredients = data['description'].split(',')
    return render(request, 'recipe_update.html', {'data': data, 'ingredients': ingredients})

def update_recipe(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        prep_time = request.POST['prep_time']
        difficulty = request.POST['difficulty']
        vegitarian = request.POST['vegitarian', 'false']
        if vegitarian == True:
           vegitarian = True 
        else:
            vegitarian = False

        print('image url', request.FILES.get('recipe_img'))
        description = request.POST['description']
        api_url = 'http://127.0.0.1:2000/update/{id}'

        data = {
            'name': name,
            'prep_time': prep_time,
            'difficulty': difficulty,
            'vegitarian': vegitarian,
            'description': description
        }