from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
import requests

from .models import Article, Newsletter, User, Editorial
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

    journalists = User.objects.filter(role="journalist")
    editorials = Editorial.objects.all()

    return render(
        request,
        "newsapp/home.html",
        {
            "articles": articles,
            "newsletters": newsletters,
            "journalists": journalists,
            "editorials": editorials,
        },
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


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    return render(
        request,
        "newsapp/article_detail.html",
        {"article": article}
    )


@login_required
def article_create(request):
    if request.user.role != "journalist":
        messages.error(request, "Only journalists can create articles.")
        return redirect("home")

    if request.method == "POST":
        form = ArticleForm(request.POST)

        # Set the author before form validation
        form.instance.author = request.user
        form.instance.editor = None
        form.instance.approved_by = None
        form.instance.is_published = False

        if form.is_valid():
            article = form.save(commit=False)

            article.author = request.user
            article.editor = None
            article.approved_by = None
            article.is_published = False

            article.save()
            messages.success(request, "Article created successfully.")
            return redirect("home")
    else:
        form = ArticleForm()

    return render(request, "newsapp/article_form.html", {"form": form})


@login_required
def editor_article_create(request):
    if request.user.role != "editor":
        messages.error(request, "Only editors can create editor articles.")
        return redirect("home")

    if request.method == "POST":
        form = ArticleForm(request.POST)

        # Set the editor before form validation
        form.instance.editor = request.user
        form.instance.author = None
        form.instance.approved_by = request.user
        form.instance.approved_at = timezone.now()
        form.instance.is_published = True

        if form.is_valid():
            article = form.save(commit=False)

            article.editor = request.user
            article.author = None
            article.approved_by = request.user
            article.approved_at = timezone.now()
            article.is_published = True

            article.save()
            messages.success(request, "Editor article created successfully.")
            return redirect("home")
    else:
        form = ArticleForm()

    return render(request, "newsapp/article_form.html", {"form": form})


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user.role == "journalist" and article.author != request.user:
        messages.error(request, "You do not have permission to edit this article.")
        return redirect("home")

    if request.user.role not in ["journalist", "editor"]:
        messages.error(request, "You do not have permission to edit this article.")
        return redirect("home")

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            updated_article = form.save(commit=False)

            if request.user.role == "editor":
                updated_article.editor = request.user
                updated_article.approved_by = request.user
                updated_article.approved_at = timezone.now()
                updated_article.is_published = True
            else:
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

    if request.user.role == "journalist" and article.author != request.user:
        messages.error(request, "You do not have permission to delete this article.")
        return redirect("home")

    if request.user.role not in ["journalist", "editor"]:
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
            form.save_m2m()

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
        article.approved_by = request.user
        article.approved_at = timezone.now()
        article.save()

        # Send email to subscribers of the author
        subscribers = User.objects.filter(
            role="reader", subscribed_journalists=article.author
        ).distinct()

        send_mail(
            subject=f"New article published: {article.title}",
            message=f"{article.author.username} published a new article:\n\n{article.title}\n\n{article.content}",
            from_email="your_email@gmail.com",
            recipient_list=["test@test.com"],  
            fail_silently=False,
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


@login_required
def subscribe_to_journalist(request, journalist_id):
    journalist = get_object_or_404(User, id=journalist_id, role="journalist")

    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe to journalists.")
        return redirect("home")

    request.user.subscribed_journalists.add(journalist)
    messages.success(request, f"You are now subscribed to {journalist.username}.")

    return redirect("home")


@login_required
def unsubscribe_from_journalist(request, journalist_id):
    journalist = get_object_or_404(User, id=journalist_id, role="journalist")

    if request.user.role != "reader":
        messages.error(request, "Only readers can unsubscribe from journalists.")
        return redirect("home")

    request.user.subscribed_journalists.remove(journalist)
    messages.success(request, f"You have unsubscribed from {journalist.username}.")

    return redirect("home")

@login_required
def subscribe_to_newsletter(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe to newsletters.")
        return redirect("home")

    newsletter.subscribers.add(request.user)
    messages.success(request, f"You are now subscribed to {newsletter.title}.")

    return redirect("home")


@login_required
def unsubscribe_from_newsletter(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.user.role != "reader":
        messages.error(request, "Only readers can unsubscribe from newsletters.")
        return redirect("home")

    newsletter.subscribers.remove(request.user)
    messages.success(request, f"You have unsubscribed from {newsletter.title}.")

    return redirect("home")


@login_required
def subscribe_to_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, id=editorial_id)

    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe to editorials.")
        return redirect("home")

    request.user.subscribed_editorials.add(editorial)
    messages.success(request, f"You are now subscribed to {editorial.name}.")

    return redirect("home")


@login_required
def unsubscribe_from_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, id=editorial_id)

    if request.user.role != "reader":
        messages.error(request, "Only readers can unsubscribe from editorials.")
        return redirect("home")

    request.user.subscribed_editorials.remove(editorial)
    messages.success(request, f"You have unsubscribed from {editorial.name}.")

    return redirect("home")


@login_required
def join_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, id=editorial_id)

    if request.user.role == "journalist":
        editorial.journalists.add(request.user)
        messages.success(request, f"You joined {editorial.name} as a journalist.")

    elif request.user.role == "editor":
        editorial.editors.add(request.user)
        messages.success(request, f"You joined {editorial.name} as an editor.")

    else:
        messages.error(request, "Only journalists and editors can join editorials.")

    return redirect("home")