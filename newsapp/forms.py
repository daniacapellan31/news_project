from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Article, Newsletter, Editorial


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
            "subscribed_publishers",
            "subscribed_journalists",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show only users who are journalists for subscriptions
        self.fields["subscribed_publishers"].queryset = User.objects.filter(
            role="journalist"
        )
        self.fields["subscribed_journalists"].queryset = User.objects.filter(
            role="journalist"
        )

        # Optional: Make them non-mandatory.
        self.fields["subscribed_publishers"].required = False
        self.fields["subscribed_journalists"].required = False


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "editorial"]


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["title", "content", "articles"]


class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ["name", "journalists", "editors",]
