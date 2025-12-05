from typing import Optional
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import ContextMixin
from .models import Product, Category

# Create your views here.


class BaseStoreView(ContextMixin):
    """
    Mixin = base que va a coordinar las vistas de la tienda
    aportar contexto comun como categorias, nombre de el sitio etc.
    """
    site_name = "mini e-commerce"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("site_name", self.site_name)
        context.setdefault("categories", Category.objects.all())
        return context


class CategoryListMixin:
    """
    Mixin para vistas de listado de productos filtradas por categoría.

    - Lee el slug de categoría desde la URL.
    - Filtra el queryset por esa categoría (si existe).
    - Agrega la categoría actual al contexto.
    """
    category_slug_url_kwarg = "category_slug"

    def get_category(self) -> Optional[Category]:
        slug = self.kwargs.get(self.category_slug_url_kwarg)  # type: ignore
        if not slug:
            return None
        return Category.objects.filter(slug=slug).first()

    def get_queryset(self):
        """
        Extiende el queryset base filtrando por categoría si corresponde.
        """
        qs = super().get_queryset()  # type: ignore
        category = self.get_category()
        if category is not None:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # type: ignore
        context["current_category"] = self.get_category()
        return context


class ProductListView(ListView):
    """
    vista basada en clase para listar productos activos
    """
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        """
        usamos el manager personalizado para devolver solo los productos activos
        """
        return Product.objects.all()


class ProductDetailView(DetailView):
    """
    vista basada en clase para el detalle de un producto
    """
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.active()  # type: ignore


class ProductCreateView(CreateView):
    """
    vista generica para crear un producto.
    mas adelante la vamos a completar por que en mi logica de negocio, solo personal autorizado va a poder crear productos, esto lo hatemos con un mixin llamado loginrquiredmixin o permisos por politicas.
    """
    model = Product
    fields = ["name", "slug", "category", "descripcion", "price", "is_activate"]
    template_name = "store/product_form.html"
    success_url = reverse_lazy("store:product_list")
