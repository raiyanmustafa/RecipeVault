from django.urls import path

from . import views


app_name = "recipes"

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="list"),
    path("recipes/add/", views.RecipeCreateView.as_view(), name="create"),
    path("recipes/sample/", views.create_sample_recipe, name="create_sample"),
    path("recipes/<int:pk>/", views.RecipeDetailView.as_view(), name="detail"),
    path("recipes/<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="edit"),
    path("recipes/<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="delete"),
]
