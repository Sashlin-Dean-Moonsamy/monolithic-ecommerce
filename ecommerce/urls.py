"""
URL configuration for the e-commerce project.

This module defines the main URL routing for the e-commerce platform.
It includes routes for the admin interface and the main store application.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

URL Patterns:
    - /admin/: Django admin interface
    - /: Main store application (included from store.urls)
"""

from django.contrib import admin
from django.urls import path, include

# Main URL patterns for the e-commerce platform
urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Main store application
    path('', include('store.urls')),
]
