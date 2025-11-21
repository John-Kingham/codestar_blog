from http import HTTPStatus
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import Post, PUBLISHED


class TestBlogViews(TestCase):

    def setUp(self):
        self.username = "myUsername"
        self.password = "myPassword"
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password,
            email="test@example.com",
        )
        self.post = Post(
            title="Blog title",
            author=self.user,
            slug="blog-slug",
            excerpt="Blog except",
            content="Blog content",
            status=PUBLISHED,
        )
        self.post.save()

    def test_render_post_detail_page_with_comment_form(self):
        """Test that the post details page contains the correct info"""

        response = self.client.get(reverse("post_detail", args=["blog-slug"]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(b"Blog title", response.content)
        self.assertIn(b"Blog content", response.content)
        self.assertIsInstance(response.context["comment_form"], CommentForm)

    def test_successful_comment_submission(self):
        """Test posting a comment"""

        self.client.login(username=self.username, password=self.password)
        comment_form_data = {"body": "Comment body"}
        response = self.client.post(
            reverse("post_detail", args=["blog-slug"]), comment_form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            b"Comment submitted and awaiting approval", response.content
        )
