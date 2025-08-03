import pytest
from faker import Faker


@pytest.fixture(scope="session")
def faker_seed():
    return 42


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture(autouse=True)
def cleanup_db(db):
    """Автоматическая очистка тестовой БД после каждого теста"""
    yield
    from django.contrib.auth import get_user_model

    User = get_user_model()
    User.objects.all().delete()
