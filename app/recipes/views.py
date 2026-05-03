import socket

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RecipeForm
from .models import Recipe


def hostname_context(request):
    return {"container_hostname": socket.gethostname()}


class RecipeListView(ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "recipes/recipe_list.html"


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/recipe_detail.html"


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"


class RecipeDeleteView(DeleteView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/recipe_confirm_delete.html"
    success_url = reverse_lazy("recipes:list")


@require_POST
def create_sample_recipe(request):
    sample_number = Recipe.objects.count() + 1
    recipe = Recipe.objects.create(
        title=f"Sample Recipe {sample_number}",
        description=(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "This sample recipe exists for quick workshop demos."
        ),
        ingredients=(
            "Lorem ipsum flour\n"
            "Dolor sit amet tomatoes\n"
            "Consectetur herbs\n"
            "Adipiscing olive oil"
        ),
        notes=(
            "Lorem ipsum notes: use this generated recipe when you need "
            "fresh demo content quickly."
        ),
        photo="recipes/lemon-rice.svg",
    )
    return redirect(recipe)
