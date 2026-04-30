from django.urls import path
from .views import (
    home,
    register_view,
    article_detail,
    article_create,
    article_update,
    article_delete,
    newsletter_create,
    newsletter_update,
    newsletter_delete,
    approve_article,
    editorial_create,
    subscribe_to_journalist,
    unsubscribe_from_journalist,
    subscribe_to_newsletter,
    unsubscribe_from_newsletter,
    subscribe_to_editorial,
    unsubscribe_from_editorial,
    join_editorial,
    editor_article_create,
)
from .api_views import (
    article_list_create_api,
    subscribed_articles_api,
    article_detail_api,
    approve_article_api,
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_view, name="register"),
    path("article/editor/create/", editor_article_create, name="editor_article_create"),
   
   # articles
    path("articles/<int:pk>/", article_detail, name="article_detail"),
    path("articles/create/", article_create, name="article_create"),
    path("articles/<int:pk>/edit/", article_update, name="article_update"),
    path("articles/<int:pk>/delete/", article_delete, name="article_delete"),
    path("articles/<int:pk>/approve/", approve_article, name="approve_article"),
        
    # newsletters
    path("newsletters/create/", newsletter_create, name="newsletter_create"),
    path("newsletters/<int:pk>/edit/", newsletter_update, name="newsletter_update"),
    path("newsletters/<int:pk>/delete/", newsletter_delete, name="newsletter_delete"),
    path("editorial/create/", editorial_create, name="editorial_create"),
   
    # subscriptions
    path(
        "journalists/<int:journalist_id>/subscribe/",
        subscribe_to_journalist,
        name="subscribe_to_journalist",
    ),
    path(
        "journalists/<int:journalist_id>/unsubscribe/",
        unsubscribe_from_journalist,
        name="unsubscribe_from_journalist",
    ),
    path(
        "newsletters/<int:newsletter_id>/subscribe/",
        subscribe_to_newsletter,
        name="subscribe_to_newsletter",
    ),
    path(
        "newsletters/<int:newsletter_id>/unsubscribe/",
        unsubscribe_from_newsletter,
        name="unsubscribe_from_newsletter",
    ),
    path(
        "editorials/<int:editorial_id>/subscribe/",
        subscribe_to_editorial,
        name="subscribe_to_editorial",
    ),
    path(
        "editorials/<int:editorial_id>/unsubscribe/",
        unsubscribe_from_editorial,
        name="unsubscribe_from_editorial",
    ),
    path(
        "editorials/<int:editorial_id>/join/",
        join_editorial,
        name="join_editorial",
    ),
   
    # API endpoints
    path("api/articles/", article_list_create_api, name="api_articles"),
    path(
        "api/articles/subscribed/",
        subscribed_articles_api,
        name="api_subscribed_articles",
    ),
    path("api/articles/<int:pk>/", article_detail_api, name="api_article_detail"),
    path(
    "api/articles/<int:pk>/approve/",
    approve_article_api,
    name="api_approve_article",
    ),
]
