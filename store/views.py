"""
Views for the e-commerce store application.

This module contains the view logic for displaying products and handling
user interactions in the e-commerce platform.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def home(request):
    """
    View for the home page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered home page template
    """
    return render(request, 'home.html')

class ProductListView(ListView):
    """
    View for displaying a list of products.
    
    This view displays products in a paginated list, ordered by creation date.
    Each page shows 12 products.
    """
    
    model = Product
    template_name = 'store/shop.html'
    context_object_name = 'products'
    paginate_by = 12  # Show 12 products per page
    ordering = ['-created_at']  # Order by newest first

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        
        Args:
            **kwargs: Additional context data
            
        Returns:
            dict: Context data for the template
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop'
        return context

class ProductDetailView(DetailView):
    """
    View for displaying detailed information about a single product.
    
    This view shows all product details including its images and
    related information.
    """
    
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        
        Args:
            **kwargs: Additional context data
            
        Returns:
            dict: Context data for the template
        """
        context = super().get_context_data(**kwargs)
        # Get all images for the product, ordered by their display order
        context['product_images'] = self.object.images.all()
        context['title'] = self.object.name
        return context

def get_or_create_cart(request):
    """Get the current cart from session or create a new one."""
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart

def add_to_cart(request, product_id):
    """Add a product to the cart."""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart')
    
    return redirect('product_detail', product_id=product_id)

def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} removed from cart!")
    return redirect('cart')

def update_cart_item(request, item_id):
    """Update the quantity of a cart item."""
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
            
        return JsonResponse({
            'success': True,
            'total_price': cart.total_price,
            'item_count': cart.item_count
        })
    
    return JsonResponse({'success': False}, status=400)

def clear_cart(request):
    """Clear all items from the cart."""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, "Cart cleared!")
    return redirect('cart')

def cart_view(request):
    """Display the cart page."""
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {
        'cart': cart,
        'title': 'Shopping Cart'
    })

def search_products(request):
    """
    View for searching products.
    
    This view handles product search functionality, searching through
    product names and descriptions using case-insensitive matching.
    """
    query = request.GET.get('query', '')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by('-created_at')
    
    return render(request, 'store/search_results.html', {
        'products': products,
        'query': query,
        'title': f'Search Results for "{query}"' if query else 'Search'
    })
