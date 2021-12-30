import pytest

from django.urls import reverse
from django.test import Client
from .models import User, Post, Picture, Like, Comment, Tag


@pytest.fixture(scope="function")
def auth_client(db):
    auth_client = Client()
    auth_client.login(username="example@example.com", password="1234")
    yield auth_client


@pytest.mark.django_db
class TestSite:
    def test_index_noauth(self, client):
        response = client.get(reverse('index'))
        assert response.status_code == 302

    def test_login(self, client):
        response = client.post(reverse("login"), {"email": "example@example.com", "password": "1234"})
        assert response.status_code == 200

    def test_logout(self, auth_client):
        response = auth_client.get(reverse("profile"))
        assert response.status_code == 200