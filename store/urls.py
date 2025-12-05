from django.urls import path

from .views import ProductListView, ProductDetailView

app_name = "store"

urlpatterns = [
    # lista de productos de todas las categorias
    path("", ProductListView.as_view(), name="product_list"),

    #Listado de productos filtrados por categoria
    path(
        "categoria/<slug:category_slug>",
         ProductListView.as_view(),
         name="product_list_by_category"
        ),

    #detalle de producto
    path(
        "producto/<slug:slug>",
        ProductDetailView.as_view(),
        name="product_detail"
    )
]