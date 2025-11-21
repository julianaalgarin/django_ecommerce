from django.db import models
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet

# Create your models here.


class Category(models.Model):
    """representa una categoria del catalogo, ej: portatiles, monitores, teclados"""
    name = models.CharField("nombre", max_length=100, unique= True)
    slug = models.SlugField("slug", max_length=120, unique= True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)

    @property
    def product_count(self) -> int:
        """cuenta cuantos productos tiene una categoria en especifico"""
        # Note: 'products' is a reverse relationship created by Django
        # when Product.category has related_name="products"
        return self.products.count()  # type: ignore
    
class Product(models.Model):
    name = models.CharField("nombre", max_length= 200 )    
    slug = models.SlugField("slug", max_length=220, unique=True)
    category = models.ForeignKey(
        Category,
        related_name= "products",
        on_delete=models.PROTECT,
        verbose_name="categoría",
         
    )

    descripcion = models.TextField("descripción", blank= True)
    price = models.DecimalField("precio", max_digits=10, decimal_places=2)
    is_activate = models.BooleanField("activo", default=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["name"]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_activate"]),
        ]

    def __str__(self) -> str:
        return str(self.name)

    def price_with_tax(self, tax_rate: Decimal = Decimal ("0.19")) -> Decimal:
        return self.price * (Decimal("1") + tax_rate)
    
    @classmethod
    def active (cls):
        return cls.objects.filter(is_activate=True)
    

