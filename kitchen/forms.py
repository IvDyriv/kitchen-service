from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Cook, Dish, DishType, Ingredient

class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = (
            "username", "first_name", "last_name", "email",
            "years_of_experience", "rating",
            "password1", "password2"
        )

class CookChangeForm(UserChangeForm):
    class Meta:
        model = Cook
        fields = ("username", "first_name", "last_name", "email",
                  "years_of_experience", "rating", "is_active", "is_staff")

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "description", "price", "cooks", "dish_type", "ingredients", "image"]
        widgets = {
            "cooks": forms.CheckboxSelectMultiple(),
            "ingredients": forms.CheckboxSelectMultiple(),
        }

class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = ["name"]

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]