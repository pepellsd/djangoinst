import pytest

from django.test import Client
from django.conf import settings as _settings


@pytest.fixture(scope="session")
def django_db_setup():
    _settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'external_db',
        'PORT': '5432',
        'USER': 'inst_client',
        'PASSWORD': '123',
    }


@pytest.fixture(scope="function")
def auth_client():
    auth_client = Client()
    auth_client.login(username="example@example.com", password="1234")
    yield auth_client


@pytest.fixture(autouse=True)
def configure_sett(settings):
    settings.SECRET_KEY="iopsuadoifuhjposieuyfishdufhjgsdjkfhjksdhfuiasphiugyweb9g87awy4p89ty98awyt"
