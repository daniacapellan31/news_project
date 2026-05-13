from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Adds a role field to distinguish between readers, journalists, and editors.
    Readers can subscribe to journalists and editorials.
    Non-reader users have their subscriptions cleared automatically on save.
    """
    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Readers can subscribe to journalists.
    subscribed_journalists = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="journalist_subscribers",
        limit_choices_to={"role": "journalist"},
    )

    # Readers can subscribe to editorials/publishers.
    subscribed_editorials = models.ManyToManyField(
        "Editorial",
        blank=True,
        related_name="editorial_subscribers",
    )

    def save(self, *args, **kwargs):
        """
        Saves the user and clears subscriptions if the user is not a reader.
        """
        super().save(*args, **kwargs)

        # If the user is not a reader, remove reader subscriptions.
        if self.role != "reader":
            self.subscribed_journalists.clear()
            self.subscribed_editorials.clear()

    def __str__(self):
        """Returns the username and role of the user."""
        return f"{self.username} ({self.role})"


class Editorial(models.Model):
    """
    Represents a news editorial or publisher.

    An editorial can have multiple journalists and editors associated with it.
    Readers can subscribe to editorials to follow their content.
    """
    name = models.CharField(max_length=100)

    journalists = models.ManyToManyField(
        User,
        related_name="journalist_editorials",
        limit_choices_to={"role": "journalist"},
        blank=True,
    )

    editors = models.ManyToManyField(
        User,
        related_name="editor_editorials",
        limit_choices_to={"role": "editor"},
        blank=True,
    )

    def __str__(self):
        """Returns the name of the editorial."""
        return self.name


class Newsletter(models.Model):
    """
    Represents a newsletter created by a journalist.

    A newsletter can include multiple articles and have multiple reader subscribers.
    """
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

    subscribers = models.ManyToManyField(
        User,
        blank=True,
        related_name="subscribed_newsletters",
        limit_choices_to={"role": "reader"},
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the title of the newsletter."""

        return self.title


class Article(models.Model):
    """
    Represents a news article.

    An article can be written by a journalist or directly by an editor, but not both.
    It must be approved by an editor before it is published.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="articles",
        limit_choices_to={"role": "journalist"},
    )

    editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="editor_articles",
        limit_choices_to={"role": "editor"},
    )

    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    is_published = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_articles",
        limit_choices_to={"role": "editor"},
    )

    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Validates that the article has either a journalist author or an editor, but not both.

        Raises:
            ValidationError: If both or neither author and editor are set.
        """
        if self.author and self.editor:
            raise ValidationError(
                "An article cannot have both a journalist author and an editor author."
            )

        if not self.author and not self.editor:
            raise ValidationError(
                "An article must have either a journalist author or an editor author."
            )

    def save(self, *args, **kwargs):
        """
        Runs full validation before saving the article.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns the title of the article."""
        return self.title