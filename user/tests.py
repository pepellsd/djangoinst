from unittest.case import TestCase
from django.shortcuts import reverse
from django.test import Client

from user.models import User


class TestUserApp(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_register(self):
        response = self.client.post(reverse("register"), data={"email": "email@domain.com",
                                                               "password1": "password123456789",
                                                               "password2": "password123456789",
                                                               "first_name": "oleg",
                                                               "last_name": "olegov"}, follow=True)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertTrue("confirm email" in str(response.content))
        new_user = User.objects.filter(email="email@domain.com").first()
        self.assertTrue(new_user is not None)
        self.assertEqual(new_user.is_active, False)

    def test_login(self):
        response = self.client.post(reverse("login"), data={"email": "example@example.com",
                                                            "password": "1234"}, follow=True)
        self.assertEqual(response.status_code, 200)
        # incorrect password
        response1 = self.client.post(reverse("login"), data={"email": "example@example.com",
                                                             "password": "12345"}, follow=True)
        self.assertTrue("password not correct" in str(response1.content))

    def test_upload_image(self):
        self.client.login(email="example@example.com", password="1234")
        with open("instagram/management/commands/fake_images/avatar.jpg", "rb") as img:
            response = self.client.post(reverse("upload_images"),
                                        data={"images": img}, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(email="example@example.com").first()
        self.assertTrue("avatar.jpg" in str(user.avatar))

    def test_edit_profile(self):
        self.client.login(email="example@example.com", password="1234")
        response = self.client.post(reverse("edit_profile"), data={"bio": "some bio"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("some bio" in User.objects.filter(email="example@example.com").first().bio)
