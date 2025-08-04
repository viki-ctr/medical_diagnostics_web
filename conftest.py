import pytest
from faker import Faker
from model_bakery import baker


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


@pytest.fixture
def service_factory():
    def factory(**kwargs):
        return baker.make("services.Service", **kwargs)
    return factory

@pytest.fixture
def service_category_factory():
    def factory(**kwargs):
        return baker.make("services.ServiceCategory", **kwargs)
    return factory


@pytest.fixture
def category():
    return baker.make('services.ServiceCategory')

@pytest.fixture
def service(category):
    return baker.make('services.Service', category=category)
