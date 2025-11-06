
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cook, DishType, Ingredient, Dish
from .forms import CookCreationForm, CookChangeForm

@admin.register(Cook)
class CookAdmin(UserAdmin):
    add_form = CookCreationForm
    form = CookChangeForm
    model = Cook

    fieldsets = UserAdmin.fieldsets + (
        ('Kitchen info', {'fields': ('years_of_experience', 'rating')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Kitchen info', {'fields': ('years_of_experience', 'rating', 'is_active')}),
    )
    list_display = ('username', 'email', 'years_of_experience', 'rating', 'is_active')

@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish_type', 'price', 'date_created')
    list_filter = ('dish_type',)
    search_fields = ('name', 'description')
    filter_horizontal = ('cooks', 'ingredients')
