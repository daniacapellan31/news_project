from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Article, Newsletter, Editorial


class RegisterForm(UserCreationForm):
    """
    Form for registering a new user.

    Extends Django's UserCreationForm to include role selection
    and optional subscriptions to editorials and journalists.
    """
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
            "subscribed_editorials",
            "subscribed_journalists",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with available editorials and journalists.

        Subscription fields are optional and pre-populated with
        all available editorials and journalists.
        """
        super().__init__(*args, **kwargs)

        # Show available editorials and journalists for reader subscriptions
        self.fields["subscribed_editorials"].queryset = Editorial.objects.all()

        self.fields["subscribed_journalists"].queryset = User.objects.filter(
            role="journalist"
        )

        # Optional: Make them non-mandatory.
        self.fields["subscribed_editorials"].required = False
        self.fields["subscribed_journalists"].required = False


class ArticleForm(forms.ModelForm):
    """
    Form for creating and updating an article.

    Includes fields for title, content, and editorial.
    """
    class Meta:
        model = Article
        fields = ["title", "content", "editorial"]


class NewsletterForm(forms.ModelForm):
    """
    Form for creating and updating a newsletter.

    Allows the journalist to select multiple articles to include
    in the newsletter using checkboxes.
    """
    articles = forms.ModelMultipleChoiceField(
        queryset=Article.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Newsletter
        fields = ["title", "content", "articles"]


class EditorialForm(forms.ModelForm):
    """
    Form for creating and updating an editorial.

    Includes fields for name, associated journalists, and editors.
    """
    class Meta:
        model = Editorial
        fields = ["name", "journalists", "editors"]