from django.urls import path
from .views import RecipeCreateView, RecipeDetailView, RecipeUpdateView, RecipeDeleteView  # Explicit imports

urlpatterns = [
    path('create/', RecipeCreateView.as_view(), name='create-recipe'),
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('update/<int:pk>/', RecipeUpdateView.as_view(), name='update-recipe'),
    path('delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete-recipe'),
]
