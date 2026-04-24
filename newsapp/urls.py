from django.urls import path
from .views import (
    home,
    register_view,
    article_create,
    article_update,
    article_delete,
    newsletter_create,
    newsletter_update,
    newsletter_delete,
    approve_article,
    editorial_create,
)
from .api_views import (
    article_list_create_api,
    subscribed_articles_api,
    article_detail_api,
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_view, name="register"),
    # articles
    path("articles/create/", article_create, name="article_create"),
    path("articles/<int:pk>/edit/", article_update, name="article_update"),
    path("articles/<int:pk>/delete/", article_delete, name="article_delete"),
    path("articles/<int:pk>/approve/", approve_article, name="approve_article"),
    # newsletters
    path("newsletters/create/", newsletter_create, name="newsletter_create"),
    path("newsletters/<int:pk>/edit/", newsletter_update, name="newsletter_update"),
    path("newsletters/<int:pk>/delete/", newsletter_delete, name="newsletter_delete"),
    path("editorial/create/", editorial_create, name="editorial_create"),
    # API endpoints
    path("api/articles/", article_list_create_api, name="api_articles"),
    path(
        "api/articles/subscribed/",
        subscribed_articles_api,
        name="api_subscribed_articles",
    ),
    path("api/articles/<int:pk>/", article_detail_api, name="api_article_detail"),
]
