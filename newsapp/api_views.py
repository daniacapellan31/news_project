from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Article
from .serializers import ArticleSerializer


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def article_list_create_api(request):
    if request.method == "GET":
        articles = Article.objects.filter(is_published=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        if request.user.role != "journalist":
            return Response(
                {"error": "Only journalists can create articles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, is_published=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscribed_articles_api(request):
    subscribed_journalists = request.user.subscribed_journalists.all()
    articles = Article.objects.filter(
        is_published=True, author__in=subscribed_journalists
    )
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def article_detail_api(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "GET":
        if not article.is_published and request.user.role == "reader":
            return Response(
                {"error": "Readers can only view published articles."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method == "PUT":
        if request.user.role not in ["journalist", "editor"]:
            return Response(
                {"error": "Only journalists or editors can update articles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.user.role == "journalist" and article.author != request.user:
            return Response(
                {"error": "Journalists can only update their own articles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        if request.user.role not in ["journalist", "editor"]:
            return Response(
                {"error": "Only journalists or editors can delete articles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.user.role == "journalist" and article.author != request.user:
            return Response(
                {"error": "Journalists can only delete their own articles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        article.delete()
        return Response(
            {"message": "Article deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
