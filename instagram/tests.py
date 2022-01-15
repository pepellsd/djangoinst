from unittest import TestCase
from django.test import Client
from django.shortcuts import reverse

from instagram.models import Post, Comment, Like


class TestSite(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(email="example@example.com", password="1234")

    def test_index(self):
        response = self.client.get(reverse("index"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_post(self):
        response = self.client.get(reverse("view_post", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("darth vader cat" in str(response.content))

    def test_profile(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("example@example.com" and "some cool advertising" in str(response.content))

    def test_create_post(self):
        with open("instagram/management/commands/fake_images/kot.jpg", "rb") as img:
            response = self.client.post(reverse("create_post"),
                                        data={"images": img, "description": "some desc"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(description="some desc").first() is not None)

    def test_leave_comment(self):
        response = self.client.post(
            reverse("leave_comment", kwargs={"post_id": Post.objects.order_by("-id").first().id})
            , data={"comment_text": "test comment"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(text="test comment").first() is not None)

    def test_like_unlike(self):
        response = self.client.post(reverse("like_unlike", kwargs={"post_id": Post.objects.order_by("-id").first().id})
                                    , follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(post_id=Post.objects.order_by("-id").first().id).first() is not None)

    def test_delete_post(self):
        del_post = Post.objects.order_by("-id").first()
        response = self.client.post(reverse("delete_post", kwargs={"post_id": del_post.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(description="some desc").first() is None)
