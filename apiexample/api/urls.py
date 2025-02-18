from django.urls import path
from .views import *

urlpatterns = [
    path('create/', RecipeCreateView.as_view(), name='create-recipe'),
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('update/<int:pk>/', RecipeUpdateView.as_view(), name='update-recipe'),
    path('delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete-recipe'), 
    path('search/<str:name>/', RecipeSearchviewset.as_view(), name='search-recipe'),
]
