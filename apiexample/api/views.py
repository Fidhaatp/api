from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import RecipesSerializer
from .models import Recipes
from rest_framework.permissions import AllowAny
from .forms import RecipesForm
import requests
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

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
                # Save to Django database
                recipe = form.save()

                # API request to external service
                api_url = 'http://127.0.0.1:8000/create/'
                data = {
                    'name': recipe.name,
                    'prep_time': recipe.prep_time,
                    'difficulty': recipe.difficulty,
                    'vegitarian': recipe.vegitarian,
                    'description': recipe.description
                }
                
                files = {}
                if recipe.recipe_img:  # Ensure an image was uploaded
                    image_path = recipe.recipe_img.path  # Get full file path
                    files['recipe_img'] = open(image_path, 'rb')  # Open file in    binary mode

                response = requests.post(api_url, data=data, files=files)

                # Close the file after sending
                if 'recipe_img' in files:
                    files['recipe_img'].close()

                if response.status_code == 201:
                    messages.success(request, 'Recipe created successfully!')
                else:
                    messages.error(request, f'Error {response.status_code}: {response.text}')

                return redirect('index')  # Redirect to home page

            except requests.RequestException as e:
                messages.error(request, f'Error sending data: {str(e)}')

    else:
        form = RecipesForm()

    return render(request, 'create_recipe.html', {'form': form})


def update_detail(request, id):
    api_url = 'http://127.0.0.1:8000/detail/{id}'
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
        api_url = 'http://127.0.0.1:8000/update/{id}'

        data = {
            'name': name,
            'prep_time': prep_time,
            'difficulty': difficulty,
            'vegitarian': vegitarian,
            'description': description
        }

        files = {'recipe_img': request.FILES.get('recipe_img')}
        response = requests.put(api_url, data=data, files=files)
        if response.status_code == 200:
            messages.success(request, 'Recipe updated successfully')
            return redirect('/')
        else:
            messages.error(request, f'Error submiting data to the REST API {response.status_code}')

    return render(request, 'recipe_update.html')


def index(request):
    if request.method == 'POST':
        search = request.POST.get('search', '')

        api_url = f'http://127.0.0.1:8000/search/{search}/'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
            else:
                data = []
        except requests.RequestException:
            data = []

        return render(request, 'index.html', {'recipes': data})

    else:
        api_url = 'http://127.0.0.1:8000/create/'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()

                paginator = Paginator(data, 6)  # Show 6 recipes per page
                page = request.GET.get('page', 1)

                try:
                    recipes = paginator.page(page)
                except (EmptyPage, PageNotAnInteger):
                    recipes = paginator.page(paginator.num_pages)

                return render(request, 'index.html', {'recipes': recipes})

            else:
                return render(request, 'index.html', {'recipes': [], 'error_message': f'Error: {response.status_code}'})

        except requests.RequestException:
            return render(request, 'index.html', {'recipes': [], 'error_message': 'Failed to fetch recipes'})
        


def recipe_fetch(request, id):

    api_url = 'http://127.0.0.1:8000/detail/{id}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        ingredients = data['description'].split(',')
        return render(request, 'recipe_fetch.html', {'data': data, 'ingredients': ingredients})
    
    return render(request, 'recipe_fetch.html')


def recipe_delete(request, id):
    api_url = f'http://127.0.0.1:8000/delete/{id}/'
    response = requests.delete(api_url)

    if response.status_code == 204:
        print(f'item with id {id} deleted successfully')

    else:
        print(f'Failed to delete item. status code {response.status_code}')    

    return redirect('/')   