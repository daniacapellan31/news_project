from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Reader subscriptions
    subscribed_publishers = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="publisher_subscribers",
        limit_choices_to={"role": "journalist"},
    )

    subscribed_journalists = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="journalist_subscribers",
        limit_choices_to={"role": "journalist"},
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If NOT a reader, delete subscriptions.
        if self.role != "reader":
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()

    def __str__(self):
        return f"{self.username} ({self.role})"


class Editorial(models.Model):
    name = models.CharField(max_length=100)

    journalists = models.ManyToManyField(
        User,
        related_name="journalist_editorials",
        limit_choices_to={"role": "journalist"},
    )

    editors = models.ManyToManyField(
        User, related_name="editor_editorials", limit_choices_to={"role": "editor"}
    )

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="newsletters",
        limit_choices_to={"role": "journalist"},
    )
    articles = models.ManyToManyField(
        "Article",
        blank=True,
        related_name="newsletters",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
        limit_choices_to={"role": "journalist"},
    )
    editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_articles",
        limit_choices_to={"role": "editor"},
    )
    editorial = models.ForeignKey(
        Editorial, on_delete=models.CASCADE, related_name="articles"
    )
    is_published = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
