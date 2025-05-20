"""
Context processors for the store application.

This module provides context processors that make certain data available
to all templates in the application.
"""

from .views import get_or_create_cart

def cart(request):
    """
    Make the current cart available to all templates.
    
    Args:
        request: The HTTP request object
        
    Returns:
        dict: Context data containing the cart
    """
    return {
        'cart': get_or_create_cart(request)
    } 