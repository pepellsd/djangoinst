import pytest

from django.urls import reverse
from .models import Post, Picture, Like, Comment, Tag


class TestSite:
    def test_index_noauth(self, client, db):
        response = client.get(reverse('index'))
        assert response.status_code == 302

    def test_login(self, client, db):
        response = client.post(reverse("login"), {"email": "example@example.com", "password": "1234"})
        assert response.status_code == 200

    def test_logout(self, auth_client, db):
        response = auth_client.get(reverse("profile"))
        assert response.status_code == 200