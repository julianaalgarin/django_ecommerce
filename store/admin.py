from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "product_count")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_activate", "created_at")
    list_filter = ("category", "is_activate", "created_at")
    search_fields = ("name", "slug", "descripcion")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "created_at", "total_orders")
    search_fields = ("first_name", "last_name", "email")
    readonly_fields = ("created_at",)


class OrderItemInline(admin.TabularInline):
    """
    Inline para gestionar los ítems de una orden directamente desde la orden.
    Ejemplo claro de composición Order ↔ OrderItem.
    """
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_at", "total_amount_display")
    list_filter = ("status", "created_at")
    search_fields = ("customer__first_name", "customer__last_name", "customer__email")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "updated_at")

    def total_amount_display(self, obj):
        return obj.total_amount()
    total_amount_display.short_description = "Total"
