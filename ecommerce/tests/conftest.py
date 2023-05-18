import datetime
from ecommerce.account.models import User
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .factories import (
    CategoryFactory,
    BrandFactory,
    ProductFactory,
    ProductLineFactory,
    ProductImageFactory,
    ProductTypeFactory,
    AttributeFactory,
    AttributeValueFactory,
    UserFactory
)
import pytest

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(ProductTypeFactory)
register(AttributeValueFactory)
register(AttributeFactory)
register(UserFactory)


@pytest.fixture
def api_client():
   
    user = User.objects.create_user(
        email="js@js.com",
        date_of_birth=datetime.datetime(1981, 4, 8),
        fname="jon",
        remember_me=True,
        lname="Constant",
        phone="4074946120",
        password="js.sj",
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
