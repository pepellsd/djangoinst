import uuid
import unittest

from unittest import TestCase
from django.test import Client
from django.shortcuts import reverse

from instagram.models import Post, Comment, Like
from user.models import User


class TestSite(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(email="example@example.com", password="1234")

    def test_index(self):
        response = self.client.get(reverse("index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("подробнее", encoding="utf8"), response.content)

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
        post = Post.objects.filter(description="some desc",).first()
        self.assertTrue(post is not None)
        self.assertEqual(str(post.user), "example@example.com")

    def test_leave_comment(self):
        post = Post(description="for comment test", user=User.objects.filter(email="example@example.com").first())
        post.save()
        comment_text = str(uuid.uuid4())
        response = self.client.post(
            reverse("leave_comment", kwargs={"post_id": post.pk})
            , data={"comment_text": comment_text}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(text=comment_text).first() is not None)

    @unittest.skipIf(Like.objects.filter(post__comments__text="for like test").first() is not None, "call as unlike")
    def test_like(self):
        post = Post(description="for like test", user=User.objects.filter(email="example@example.com").first())
        post.save()
        response = self.client.post(reverse("like_unlike", kwargs={"post_id": post.pk})
                                    , follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(post_id=post.pk).first() is not None)

    def test_delete_post(self):
        post = Post(description="khjsdkjfhjks", user=User.objects.filter(email="example@example.com").first())
        post.save()
        del_post = Post.objects.filter(description="khjsdkjfhjks").first()
        response = self.client.post(reverse("delete_post", kwargs={"post_id": del_post.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(description="khjsdkjfhjks").first() is None)
