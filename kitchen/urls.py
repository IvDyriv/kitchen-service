from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    HomeView,
    SignUpView,

    # Cooks
    CookListView, CookDetailView, CookCreateView, CookUpdateView, CookDeleteView,

    # Dishes
    DishListView, DishDetailView, DishCreateView, DishUpdateView, DishDeleteView,

    # Ingredients
    IngredientListView, IngredientDetailView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # Auth
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Cooks
    path("cooks/", CookListView.as_view(), name="cook_list"),
    path("cooks/create/", CookCreateView.as_view(), name="cook_create"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook_detail"),
    path("cooks/<int:pk>/update/", CookUpdateView.as_view(), name="cook_update"),
    path("cooks/<int:pk>/delete/", CookDeleteView.as_view(), name="cook_delete"),

    # Dishes
    path("dishes/", DishListView.as_view(), name="dish_list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish_create"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish_detail"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish_update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish_delete"),

    # Ingredients
    path("ingredients/", IngredientListView.as_view(), name="ingredient_list"),
    path("ingredients/create/", IngredientCreateView.as_view(), name="ingredient_create"),
    path("ingredients/<int:pk>/", IngredientDetailView.as_view(), name="ingredient_detail"),
    path("ingredients/<int:pk>/update/", IngredientUpdateView.as_view(), name="ingredient_update"),
    path("ingredients/<int:pk>/delete/", IngredientDeleteView.as_view(), name="ingredient_delete"),
]
