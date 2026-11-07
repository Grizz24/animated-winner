from django.db import models


class Show(models.Model):
    """One movie or series in the user's list (replaces the separate Series/Movies APIs in notes.txt)."""

    class MediaType(models.TextChoices):
        MOVIE = "Movie", "Movie"
        SERIES = "Series", "Series"

    class Status(models.TextChoices):
        WATCHED = "Watched", "Watched"
        WATCHING = "Watching", "Watching"
        PLANNING = "Planning To", "Planning To"

    GENRE_CHOICES = [
        (g, g)
        for g in (
            "Action",
            "Comedy",
            "Drama",
            "Fantasy",
            "Horror",
            "Romance",
            "Sci-Fi",
            "Thriller",
        )
    ]

    name = models.CharField(max_length=200)
    media_type = models.CharField(
        max_length=10, choices=MediaType.choices, default=MediaType.SERIES
    )
    # Only meaningful for series, so they are optional.
    seasons = models.PositiveIntegerField(null=True, blank=True)
    episodes = models.PositiveIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES, blank=True)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.PLANNING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
