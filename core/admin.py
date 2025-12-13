from django.contrib import admin
from .models import FarmerProfile, Product, Order

# Register your models here.

# Register FarmerProfile model
@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'location', 'created_at']
    search_fields = ['user__username', 'phone', 'location']
    list_filter = ['created_at']

# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'category', 'price', 'stock', 'created_at']
    search_fields = ['name', 'farmer__username', 'description']
    list_filter = ['category', 'created_at']
    list_editable = ['price', 'stock']

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer_name', 'quantity', 'total_price', 'status', 'order_date']
    search_fields = ['customer_name', 'customer_email', 'product__name']
    list_filter = ['status', 'order_date']
    list_editable = ['status']