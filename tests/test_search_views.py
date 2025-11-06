
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from kitchen.models import Dish, Ingredient

@pytest.mark.django_db
def test_search_dishes_by_name():
    client = Client()
    User = get_user_model()
    User.objects.create_user(username="u", password="x")
    Dish.objects.create(name="Borscht", price=10.0)
    Dish.objects.create(name="Pizza", price=12.0)
    client.login(username="u", password="x")
    resp = client.get("/dishes/?q=bor")
    assert resp.status_code == 200
    content = resp.content.decode()
    assert "Borscht" in content and "Pizza" not in content

@pytest.mark.django_db
def test_search_cooks_by_username():
    client = Client()
    User = get_user_model()
    User.objects.create_user(username="john", password="x")
    User.objects.create_user(username="mary", password="x")
    client.login(username="john", password="x")
    resp = client.get("/cooks/?q=jo")
    assert "john" in resp.content.decode()
    assert "mary" not in resp.content.decode()

@pytest.mark.django_db
def test_search_ingredients_by_name():
    client = Client()
    User = get_user_model()
    User.objects.create_user(username="u", password="x")
    Ingredient.objects.create(name="Cheese")
    Ingredient.objects.create(name="Tomato")
    client.login(username="u", password="x")
    resp = client.get("/ingredients/?q=che")
    assert "Cheese" in resp.content.decode()
    assert "Tomato" not in resp.content.decode()
