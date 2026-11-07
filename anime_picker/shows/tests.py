from django.test import TestCase
from django.urls import reverse

from .models import Show


class ShowTests(TestCase):
    def setUp(self):
        Show.objects.create(name="One Piece", media_type="Series", seasons=1,
                            episodes=1000, genre="Action", status="Watching")
        Show.objects.create(name="Konosuba", media_type="Series", seasons=2,
                            episodes=20, genre="Comedy", status="Planning To")
        Show.objects.create(name="Your Name", media_type="Movie",
                            genre="Romance", status="Watched")

    def test_home_shows_real_stats(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["watching_count"], 1)
        self.assertEqual(response.context["planned_count"], 1)
        self.assertEqual(response.context["done_count"], 1)

    def test_add_series_requires_seasons_and_episodes(self):
        response = self.client.post(reverse("add_show"), {
            "name": "Dandadan", "media_type": "Series",
            "genre": "Action", "status": "Watching",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Show.objects.filter(name="Dandadan").exists())

    def test_add_movie_without_seasons(self):
        response = self.client.post(reverse("add_show"), {
            "name": "Spirited Away", "media_type": "Movie",
            "genre": "Fantasy", "status": "Watched",
        })
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Show.objects.filter(name="Spirited Away").exists())

    def test_quick_add(self):
        self.client.post(reverse("quick_add"),
                         {"name": "Dragon Ball", "status": "Planning To"})
        self.assertTrue(Show.objects.filter(name="Dragon Ball").exists())

    def test_pick_modes(self):
        data = self.client.get(reverse("pick"), {"mode": "continue"}).json()
        self.assertEqual(data["name"], "One Piece")
        data = self.client.get(reverse("pick"), {"mode": "new"}).json()
        self.assertEqual(data["name"], "Konosuba")

    def test_pick_empty(self):
        Show.objects.all().delete()
        data = self.client.get(reverse("pick")).json()
        self.assertFalse(data["found"])
