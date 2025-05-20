"""
URL configuration for the store application.

This module defines the URL routing for the main store functionality,
including the home page, product listing, and product detail views.

URL Patterns:
    - /: Home page
    - /shop/: Product listing page
    - /product/<id>/: Product detail page
    - /cart/: Shopping cart page
    - /cart/add/<id>/: Add product to cart
    - /cart/remove/<id>/: Remove item from cart
    - /cart/update/<id>/: Update cart item quantity
    - /cart/clear/: Clear cart
"""

from django.urls import path
from . import views

# URL patterns for the store application
urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Product listing page
    path('shop/', views.ProductListView.as_view(), name='shop'),
    
    # Individual product detail page
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Shopping cart page
    path('cart/', views.cart_view, name='cart'),
    
    # Add product to cart
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # Remove item from cart
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Update cart item quantity
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    
    # Clear cart
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # Search products
    path('search/', views.search_products, name='search_products'),
]