
import pytest
from django.contrib.auth import get_user_model
from kitchen.models import DishType, Ingredient, Dish

@pytest.mark.django_db
def test_models_str():
    Cook = get_user_model()
    c = Cook.objects.create_user(username="chef", password="x", years_of_experience=2)
    t = DishType.objects.create(name="Soup")
    i = Ingredient.objects.create(name="Tomato")
    d = Dish.objects.create(name="Borscht", price=10.50, dish_type=t)
    d.cooks.add(c); d.ingredients.add(i)
    assert str(c).startswith("chef (2 yrs)")
    assert str(t) == "Soup"
    assert str(i) == "Tomato"
    assert str(d) == "Borscht"
