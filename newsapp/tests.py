from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Article, Newsletter, Editorial
from rest_framework.authtoken.models import Token


class NewsAppTests(TestCase):

    def setUp(self):
        """
        Create test users, editorial, article, and newsletter.
        This setup runs before every test.
        """
        User = get_user_model()

        # Create users with different roles
        self.reader = User.objects.create_user(
            username="reader1", password="testpass123", role="reader"
        )

        self.journalist = User.objects.create_user(
            username="journalist1", password="testpass123", role="journalist"
        )

        self.editor = User.objects.create_user(
            username="editor1", password="testpass123", role="editor"
        )

        # Create editorial
        self.editorial = Editorial.objects.create(name="Tech News")

        # Create article (initially not published)
        self.article = Article.objects.create(
            title="Test Article",
            content="Test content",
            author=self.journalist,
            editorial=self.editorial,
            is_published=False,
        )

        # Create newsletter
        self.newsletter = Newsletter.objects.create(
            title="Test Newsletter",
            content="Newsletter content",
            author=self.journalist,
        )

    # -----------------------------
    # 1. ROLE ACCESS TESTS
    # -----------------------------

    def test_reader_cannot_create_article(self):
        """Ensure reader cannot access article creation page."""
        self.client.login(username="reader1", password="testpass123")
        response = self.client.get(reverse("article_create"))
        self.assertEqual(response.status_code, 302)

    def test_journalist_can_create_article(self):
        """Ensure journalist can access article creation page."""
        self.client.login(username="journalist1", password="testpass123")
        response = self.client.get(reverse("article_create"))
        self.assertEqual(response.status_code, 200)

    def test_editor_can_approve_article(self):
        """Ensure editor can approve an article."""
        self.client.login(username="editor1", password="testpass123")
        response = self.client.post(reverse("approve_article", args=[self.article.id]))
        self.article.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.article.is_published)

    # -----------------------------
    # 2. READER SUBSCRIPTIONS
    # -----------------------------

    def test_reader_sees_only_subscriptions(self):
        """Ensure reader sees articles from subscribed journalists."""

        # Make article visible
        self.article.is_published = True
        self.article.save()

        # Subscribe reader
        self.reader.subscribed_journalists.add(self.journalist)

        self.client.login(username="reader1", password="testpass123")
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    # -----------------------------
    # 3. JOURNALIST CREATES ARTICLE
    # -----------------------------

    def test_journalist_creates_article(self):
        """Ensure journalist can create an article."""
        self.client.login(username="journalist1", password="testpass123")

        response = self.client.post(
            reverse("article_create"),
            {
                "title": "New Article",
                "content": "New content",
                "editorial": self.editorial.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(title="New Article").exists())

    # -----------------------------
    # 4. EDITOR ACTIONS
    # -----------------------------

    def test_editor_approves_article(self):
        """Ensure editor can approve an article."""
        self.client.login(username="editor1", password="testpass123")

        response = self.client.post(reverse("approve_article", args=[self.article.id]))

        self.article.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.article.is_published)

    def test_editor_deletes_article_api(self):
        """Ensure editor can delete an article via API using token authentication."""

        # Create token for editor
        token, _ = Token.objects.get_or_create(user=self.editor)

        # Send DELETE request with token
        response = self.client.delete(
            reverse("api_article_detail", args=[self.article.id]),
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

        self.assertIn(response.status_code, [200, 204])

    # -----------------------------
    # 5. NEWSLETTERS
    # -----------------------------

    def test_journalist_creates_newsletter(self):
        """Ensure journalist can create a newsletter."""
        self.client.login(username="journalist1", password="testpass123")

        response = self.client.post(
            reverse("newsletter_create"),
            {"title": "New Newsletter", "content": "Newsletter body"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newsletter.objects.filter(title="New Newsletter").exists())

    # -----------------------------
    # 6. APPROVAL LOGIC / SIGNALS
    # -----------------------------

    def test_article_approval_logic_works(self):
        """
        Ensure approval logic updates:
        - is_published
        - editor
        - approved_at
        """
        self.client.login(username="editor1", password="testpass123")

        response = self.client.post(reverse("approve_article", args=[self.article.id]))

        self.article.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.article.editor, self.editor)
        self.assertTrue(self.article.is_published)
        self.assertIsNotNone(self.article.approved_at)
