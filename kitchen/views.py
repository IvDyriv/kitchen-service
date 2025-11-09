from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from .models import Cook, Dish, Ingredient
from .forms import CookCreationForm, CookChangeForm, DishForm, IngredientForm


class HomeView(TemplateView):
    template_name = "kitchen/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_dishes"] = Dish.objects.count()
        context["total_cooks"] = Cook.objects.count()
        context["cheapest_dish"] = Dish.objects.order_by("price").first()
        context["most_expensive_dish"] = Dish.objects.order_by("-price").first()
        return context


class CookListView(ListView):
    model = Cook
    template_name = "kitchen/cook_list.html"
    context_object_name = "page_obj"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        queryset = Cook.objects.all()
        if q:
            queryset = queryset.filter(
                Q(username__icontains=q)
                | Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
            )
        return queryset.order_by("username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "").strip()
        return context


class CookDetailView(DetailView):
    model = Cook
    template_name = "kitchen/cook_detail.html"
    context_object_name = "cook"


class CookCreateView(CreateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("cook_list")


class CookUpdateView(UpdateView):
    model = Cook
    form_class = CookChangeForm
    template_name = "kitchen/cook_form.html"

    def get_success_url(self):
        return reverse_lazy("cook_detail", kwargs={"pk": self.object.pk})


class CookDeleteView(DeleteView):
    model = Cook
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("cook_list")


class DishListView(ListView):
    model = Dish
    template_name = "kitchen/dish_list.html"
    context_object_name = "page_obj"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        sort = self.request.GET.get("sort", "")
        queryset = Dish.objects.select_related("dish_type").prefetch_related("cooks", "ingredients")
        if q:
            queryset = queryset.filter(name__icontains=q)
        if sort == "name_asc":
            queryset = queryset.order_by("name")
        elif sort == "name_desc":
            queryset = queryset.order_by("-name")
        elif sort == "price_asc":
            queryset = queryset.order_by("price")
        elif sort == "price_desc":
            queryset = queryset.order_by("-price")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "").strip()
        context["sort"] = self.request.GET.get("sort", "")
        return context


class DishDetailView(DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    context_object_name = "dish"


class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("dish_list")


class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"

    def get_success_url(self):
        return reverse_lazy("dish_detail", kwargs={"pk": self.object.pk})


class DishDeleteView(DeleteView):
    model = Dish
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("dish_list")


class IngredientListView(ListView):
    model = Ingredient
    template_name = "kitchen/ingredient_list.html"
    context_object_name = "ingredients"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        queryset = Ingredient.objects.all()
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "").strip()
        return context


class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = "kitchen/ingredient_detail.html"
    context_object_name = "ingredient"


class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "kitchen/ingredient_form.html"
    success_url = reverse_lazy("ingredient_list")


class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "kitchen/ingredient_form.html"

    def get_success_url(self):
        return reverse_lazy("ingredient_detail", kwargs={"pk": self.object.pk})


class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("ingredient_list")


class SignUpView(CreateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "kitchen/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created. Welcome!")
        return response
