
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Cook, Dish, Ingredient
from .forms import CookCreationForm, CookChangeForm, DishForm, IngredientForm
from django.contrib.auth import login
from django.contrib import messages



def home(request):
    total_dishes = Dish.objects.count()
    total_cooks = Cook.objects.count()
    cheapest_dish = Dish.objects.order_by("price").first()
    most_expensive_dish = Dish.objects.order_by("-price").first()
    return render(request, "kitchen/home.html", {
        "total_dishes": total_dishes,
        "total_cooks": total_cooks,
        "cheapest_dish": cheapest_dish,
        "most_expensive_dish": most_expensive_dish,
    })

def cook_list(request):
    q = request.GET.get("q", "").strip()
    cooks = Cook.objects.all()

    if q:
        cooks = cooks.filter(
            Q(username__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
        )

    page_obj = Paginator(cooks.order_by("username"), 10).get_page(request.GET.get("page"))
    return render(
        request,
        "kitchen/cook_list.html",
        {"page_obj": page_obj, "q": q},
    )


def cook_detail(request, pk):
    cook = get_object_or_404(Cook, pk=pk)
    return render(request, "kitchen/cook_detail.html", {"cook": cook})

def cook_create(request):
    if request.method == "POST":
        form = CookCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cook_list")
    else:
        form = CookCreationForm()
    return render(request, "kitchen/cook_form.html", {"form": form})

def cook_update(request, pk):
    cook = get_object_or_404(Cook, pk=pk)
    if request.method == "POST":
        form = CookChangeForm(request.POST, instance=cook)
        if form.is_valid():
            form.save()
            return redirect("cook_detail", pk=cook.pk)
    else:
        form = CookChangeForm(instance=cook)
    return render(request, "kitchen/cook_form.html", {"form": form})

def cook_delete(request, pk):
    cook = get_object_or_404(Cook, pk=pk)
    if request.method == "POST":
        cook.delete()
        return redirect("cook_list")
    return render(request, "kitchen/confirm_delete.html", {"object": cook})

def dish_list(request):
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "")
    dishes = Dish.objects.select_related("dish_type").prefetch_related("cooks", "ingredients")
    if q:
        dishes = dishes.filter(name__icontains=q)
    if sort == "name_asc":
        dishes = dishes.order_by("name")
    elif sort == "name_desc":
        dishes = dishes.order_by("-name")
    elif sort == "price_asc":
        dishes = dishes.order_by("price")
    elif sort == "price_desc":
        dishes = dishes.order_by("-price")
    page_obj = Paginator(dishes, 10).get_page(request.GET.get("page"))
    return render(request, "kitchen/dish_list.html", {"page_obj": page_obj, "q": q, "sort": sort})

def dish_detail(request, pk):
    dish = get_object_or_404(Dish.objects.select_related("dish_type").prefetch_related("cooks", "ingredients"), pk=pk)
    return render(request, "kitchen/dish_detail.html", {"dish": dish})

def dish_create(request):
    if request.method == "POST":
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save()
            return redirect("dish_detail", pk=dish.pk)
    else:
        form = DishForm()
    return render(request, "kitchen/dish_form.html", {"form": form})

def dish_update(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == "POST":
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            return redirect("dish_detail", pk=dish.pk)
    else:
        form = DishForm(instance=dish)
    return render(request, "kitchen/dish_form.html", {"form": form})

def dish_delete(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == "POST":
        dish.delete()
        return redirect("dish_list")
    return render(request, "kitchen/confirm_delete.html", {"object": dish})

def ingredient_list(request):
    q = request.GET.get("q", "").strip()
    ingredients = Ingredient.objects.all()
    if q:
        ingredients = ingredients.filter(name__icontains=q)
    page_obj = Paginator(ingredients.order_by("name"), 10).get_page(request.GET.get("page"))
    return render(request, "kitchen/ingredient_list.html", {"ingredients": page_obj, "q": q})

def ingredient_detail(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    return render(request, "kitchen/ingredient_detail.html", {"ingredient": ingredient})

def ingredient_create(request):
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ingredient_list")
    else:
        form = IngredientForm()
    return render(request, "kitchen/ingredient_form.html", {"form": form})

def ingredient_update(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect("ingredient_detail", pk=ingredient.pk)
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, "kitchen/ingredient_form.html", {"form": form})

def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == "POST":
        ingredient.delete()
        return redirect("ingredient_list")
    return render(request, "kitchen/confirm_delete.html", {"object": ingredient})

def signup(request):
    if request.method == "POST":
        form = CookCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматично логінемо після реєстрації
            messages.success(request, "Account created. Welcome!")
            return redirect("home")
    else:
        form = CookCreationForm()
    return render(request, "kitchen/signup.html", {"form": form})
