
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('cooks/', views.cook_list, name='cook_list'),
    path('cooks/<int:pk>/', views.cook_detail, name='cook_detail'),
    path('cooks/create/', views.cook_create, name='cook_create'),
    path('cooks/<int:pk>/update/', views.cook_update, name='cook_update'),
    path('cooks/<int:pk>/delete/', views.cook_delete, name='cook_delete'),

    path('dishes/', views.dish_list, name='dish_list'),
    path('dishes/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('dishes/create/', views.dish_create, name='dish_create'),
    path('dishes/<int:pk>/update/', views.dish_update, name='dish_update'),
    path('dishes/<int:pk>/delete/', views.dish_delete, name='dish_delete'),

    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('ingredients/<int:pk>/', views.ingredient_detail, name='ingredient_detail'),
    path('ingredients/create/', views.ingredient_create, name='ingredient_create'),
    path('ingredients/<int:pk>/update/', views.ingredient_update, name='ingredient_update'),
    path('ingredients/<int:pk>/delete/', views.ingredient_delete, name='ingredient_delete'),

    path('login/', auth_views.LoginView.as_view(template_name='kitchen/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
