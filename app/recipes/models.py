from django.db import models
from django.urls import reverse


class Recipe(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    notes = models.TextField(blank=True)
    photo = models.FileField(upload_to="recipes/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:detail", args=[self.pk])
