from django.test import SimpleTestCase
from django.urls import resolve, reverse

from applications import views


class ApplicationUrlsResolvesToViewTest(SimpleTestCase):
    def test_create_url_resolves_to_create_view(self):
        """assert that create url resolves to the create view class"""

        found = resolve(reverse("create"))
        self.assertEqual(found.func.view_class, views.CreateView)

    def test_list_url_resolves_to_list_view(self):
        """assert that the list url resolves to the list view class"""

        found = resolve(reverse("list"))
        self.assertEqual(found.func.view_class, views.ListView)

    def test_delete_url_resolves_to_register_view(self):
        """assert that the delete url resolves to the delete view"""

        found = resolve(reverse("delete", args=[1]))
        self.assertEqual(found.func.view_class, views.DeleteView)
