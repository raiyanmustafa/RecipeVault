from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from .models import Recipe
from .views import hostname_context


class RecipeViewsTests(TestCase):
    def test_list_page_shows_existing_recipes(self):
        Recipe.objects.create(title="Lemon Rice", ingredients="rice\nlemon")

        response = self.client.get(reverse("recipes:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lemon Rice")

    def test_create_recipe_saves_and_redirects_to_detail(self):
        response = self.client.post(
            reverse("recipes:create"),
            {
                "title": "Tomato Soup",
                "description": "Simple weekday soup",
                "ingredients": "tomatoes\nsalt",
                "notes": "Serve hot",
            },
        )

        recipe = Recipe.objects.get(title="Tomato Soup")
        self.assertRedirects(response, reverse("recipes:detail", args=[recipe.pk]))
        self.assertEqual(recipe.ingredients, "tomatoes\nsalt")

    def test_detail_page_shows_recipe_fields(self):
        recipe = Recipe.objects.create(
            title="Masala Omelette",
            description="Fast breakfast",
            ingredients="eggs\nonion",
            notes="Use medium heat",
        )

        response = self.client.get(reverse("recipes:detail", args=[recipe.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Masala Omelette")
        self.assertContains(response, "Fast breakfast")
        self.assertContains(response, "Use medium heat")

    def test_edit_recipe_updates_existing_record(self):
        recipe = Recipe.objects.create(title="Old Name", ingredients="flour")

        response = self.client.post(
            reverse("recipes:edit", args=[recipe.pk]),
            {
                "title": "Flatbread",
                "description": "Pan cooked",
                "ingredients": "flour\nwater",
                "notes": "Rest dough",
            },
        )

        recipe.refresh_from_db()
        self.assertRedirects(response, reverse("recipes:detail", args=[recipe.pk]))
        self.assertEqual(recipe.title, "Flatbread")
        self.assertEqual(recipe.description, "Pan cooked")

    def test_delete_recipe_removes_record(self):
        recipe = Recipe.objects.create(title="Delete Me", ingredients="salt")

        response = self.client.post(reverse("recipes:delete", args=[recipe.pk]))

        self.assertRedirects(response, reverse("recipes:list"))
        self.assertFalse(Recipe.objects.filter(pk=recipe.pk).exists())

    def test_recipe_photo_is_optional(self):
        recipe = Recipe.objects.create(title="No Photo", ingredients="water")

        self.assertFalse(recipe.photo)

    def test_sample_recipe_button_creates_lorem_recipe_with_demo_image(self):
        response = self.client.post(reverse("recipes:create_sample"))

        recipe = Recipe.objects.get(title__startswith="Sample Recipe")
        self.assertRedirects(response, reverse("recipes:detail", args=[recipe.pk]))
        self.assertIn("Lorem ipsum", recipe.description)
        self.assertIn("Lorem ipsum", recipe.ingredients)
        self.assertEqual(recipe.photo.name, "recipes/lemon-rice.svg")

    def test_sample_recipe_action_requires_post(self):
        response = self.client.get(reverse("recipes:create_sample"))

        self.assertEqual(response.status_code, 405)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_hostname_context_exposes_container_hostname(self):
        context = hostname_context(None)

        self.assertIn("container_hostname", context)
        self.assertTrue(context["container_hostname"])


class DemoSettingsTests(TestCase):
    def test_demo_settings_allow_any_host(self):
        self.assertIn("*", settings.ALLOWED_HOSTS)

    def test_demo_settings_disable_csrf_middleware(self):
        self.assertNotIn("django.middleware.csrf.CsrfViewMiddleware", settings.MIDDLEWARE)

    def test_admin_login_ignores_csrf_origin_checks_for_dev_tunnels(self):
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(
            "/admin/login/",
            {"username": "admin", "password": "admin", "next": "/admin/"},
            HTTP_ORIGIN="https://localhost:8000",
            secure=True,
        )

        self.assertNotEqual(response.status_code, 403)
