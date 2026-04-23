from rest_framework import serializers
from .models import Article, User, Newsletter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class NewsletterSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Newsletter
        fields = ['id', 'title', 'content', 'author', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    editor = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'author',
            'editor',
            'editorial',
            'is_published',
            'approved_at',
            'created_at',
        ]

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']