from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('create/', RecipeCreateView.as_view(), name='create-recipe'),
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('update/<int:pk>/', RecipeUpdateView.as_view(), name='update-recipe'),
    path('delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete-recipe'), 
    path('search/<str:name>/', RecipeSearchviewset.as_view(), name='search-recipe'),

    path('create-recipe/', views.create_recipe, name='create_recipe'),
    path('recipe_fetch/<int:id>/', views.recipe_fetch, name='recipe_fetch'),
    path('update_recipe/<int:id>/', views.update_recipe, name='update_recipe'),
    path('recipe_delete/<int:id>/', views.recipe_delete, name='recipe_delete'),
    path('', views.index, name='index'),
    path('update_detail/<int:id>/', views.update_detail, name='update_detail'),

]
