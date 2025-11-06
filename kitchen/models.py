
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, blank=True)

    def __str__(self):
        return f"{self.username} ({self.years_of_experience} yrs)"

class DishType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cooks = models.ManyToManyField(Cook, related_name="dishes", blank=True)
    dish_type = models.ForeignKey(DishType, on_delete=models.SET_NULL, null=True, blank=True, related_name="dishes")
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="dish_images/", blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
