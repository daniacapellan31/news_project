from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
import requests

from .models import Article, Newsletter, User
from .forms import RegisterForm, ArticleForm, NewsletterForm, EditorialForm


def home(request):
    if request.user.is_authenticated:
        if request.user.role == "reader":
            articles = Article.objects.filter(is_published=True)
            newsletters = Newsletter.objects.all()
        elif request.user.role == "journalist":
            articles = Article.objects.filter(author=request.user)
            newsletters = Newsletter.objects.filter(author=request.user)
        elif request.user.role == "editor":
            articles = Article.objects.all()
            newsletters = Newsletter.objects.all()
        else:
            articles = Article.objects.none()
            newsletters = Newsletter.objects.none()
    else:
        articles = Article.objects.filter(is_published=True)
        newsletters = Newsletter.objects.none()

    return render(
        request, "newsapp/home.html", {"articles": articles, "newsletters": newsletters}
    )


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "newsapp/register.html", {"form": form})


@login_required
def article_create(request):
    if request.user.role != "journalist":
        messages.error(request, "Only journalists can create articles.")
        return redirect("home")

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.is_published = False
            article.save()
            messages.success(request, "Article created successfully.")
            return redirect("home")
    else:
        form = ArticleForm()

    return render(request, "newsapp/article_form.html", {"form": form})


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user.role != "journalist" or article.author != request.user:
        messages.error(request, "You do not have permission to edit this article.")
        return redirect("home")

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            updated_article = form.save(commit=False)
            updated_article.is_published = False
            updated_article.editor = None
            updated_article.approved_at = None
            updated_article.save()
            messages.success(request, "Article updated successfully.")
            return redirect("home")
    else:
        form = ArticleForm(instance=article)

    return render(request, "newsapp/article_form.html", {"form": form})


@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user.role != "journalist" or article.author != request.user:
        messages.error(request, "You do not have permission to delete this article.")
        return redirect("home")

    if request.method == "POST":
        article.delete()
        messages.success(request, "Article deleted successfully.")
        return redirect("home")

    return render(request, "newsapp/article_confirm_delete.html", {"article": article})


@login_required
def newsletter_create(request):
    if request.user.role != "journalist":
        messages.error(request, "Only journalists can create newsletters.")
        return redirect("home")

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            messages.success(request, "Newsletter created successfully.")
            return redirect("home")
    else:
        form = NewsletterForm()

    return render(request, "newsapp/newsletter_form.html", {"form": form})


@login_required
def newsletter_update(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if request.user.role != "journalist" or newsletter.author != request.user:
        messages.error(request, "You do not have permission to edit this newsletter.")
        return redirect("home")

    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated successfully.")
            return redirect("home")
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, "newsapp/newsletter_form.html", {"form": form})


@login_required
def newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if request.user.role != "journalist" or newsletter.author != request.user:
        messages.error(request, "You do not have permission to delete this newsletter.")
        return redirect("home")

    if request.method == "POST":
        newsletter.delete()
        messages.success(request, "Newsletter deleted successfully.")
        return redirect("home")

    return render(
        request, "newsapp/newsletter_confirm_delete.html", {"newsletter": newsletter}
    )


@login_required
def approve_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user.role != "editor":
        messages.error(request, "Only editors can approve articles.")
        return redirect("home")

    if request.method == "POST":
        article.is_published = True
        article.editor = request.user
        article.approved_at = timezone.now()
        article.save()

        # Send email to subscribers of the author
        subscribers = User.objects.filter(
            role="reader", subscribed_journalists=article.author
        ).distinct()

        recipient_list = [user.email for user in subscribers if user.email]

        if recipient_list:
            send_mail(
                subject=f"New article published: {article.title}",
                message=f"{article.author.username} published a new article:\n\n{article.title}\n\n{article.content}",
                from_email="your_email@gmail.com",
                recipient_list=recipient_list,
                fail_silently=True,
            )

        # Optional POST request
        try:
            requests.post(
                "https://httpbin.org/post",
                json={
                    "title": article.title,
                    "author": article.author.username,
                    "published": article.is_published,
                },
                timeout=5,
            )
        except requests.RequestException:
            pass

        messages.success(request, "Article approved and published successfully.")
        return redirect("home")

    return render(request, "newsapp/approve_article.html", {"article": article})


@login_required
def editorial_create(request):
    if request.user.role != "editor":
        messages.error(request, "Only editors can create editorials.")
        return redirect("home")

    if request.method == "POST":
        form = EditorialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Editorial created successfully.")
            return redirect("home")
    else:
        form = EditorialForm()

    return render(request, "newsapp/editorial_form.html", {"form": form})
