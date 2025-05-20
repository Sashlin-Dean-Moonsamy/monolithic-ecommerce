from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage
from .forms import ProductAdminForm, ProductImageAdminForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'primary_image_preview')

    def primary_image_preview(self, obj):
        if obj.primary_image_url:
            return format_html('<img src="{}" style="height: 60px;" />', obj.primary_image_url)
        return "-"
    primary_image_preview.short_description = 'Primary Image'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    form = ProductImageAdminForm
    list_display = ('product', 'order', 'image_preview')

    def image_preview(self, obj):
        return format_html('<img src="{}" style="height: 50px;" />', obj.image_url)
    image_preview.short_description = 'Image'
