"""
Models for the e-commerce store application.

This module defines the core data models for the e-commerce platform,
including products and their associated images.
"""

from django.db import models
from ecommerce.utils.imagekit_uploader import upload_image_to_imagekit


class Product(models.Model):
    """
    Represents a product in the e-commerce store.
    
    Attributes:
        name (str): The name of the product
        description (str): Detailed description of the product
        price (Decimal): The price of the product
        primary_image_url (str): URL to the main product image
        created_at (datetime): Timestamp of when the product was created
        updated_at (datetime): Timestamp of the last update
    """
    
    name = models.CharField(
        max_length=255,
        help_text="The name of the product"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the product"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The price of the product"
    )
    primary_image_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL to the main product image (from ImageKit)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of when the product was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the last update"
    )

    class Meta:
        """Meta options for the Product model."""
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        """String representation of the product."""
        return self.name

    def set_primary_image(self, image_file):
        """
        Set the primary image for the product.
        
        Args:
            image_file: The image file to be uploaded
            
        Returns:
            None
        """
        url = upload_image_to_imagekit(image_file, image_file.name, folder='/products/primary/')
        self.primary_image_url = url
        self.save(update_fields=['primary_image_url'])


class ProductImage(models.Model):
    """
    Represents additional images for a product.
    
    Attributes:
        product (Product): The associated product
        image_url (str): URL to the image (from ImageKit)
        order (int): Display order of the image
    """
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="The associated product"
    )
    image_url = models.URLField(
        help_text="URL to the image (from ImageKit)"
    )
    order = models.PositiveIntegerField(
        help_text="Display order of the image"
    )

    class Meta:
        """Meta options for the ProductImage model."""
        ordering = ['order']
        unique_together = ('product', 'order')
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        """String representation of the product image."""
        return f"{self.product.name} Image #{self.order}"


class Cart(models.Model):
    """
    Represents a shopping cart.
    
    Attributes:
        created_at (datetime): Timestamp of when the cart was created
        updated_at (datetime): Timestamp of the last update
    """
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

    @property
    def total_price(self):
        """Calculate the total price of all items in the cart."""
        return sum(item.total_price for item in self.items.all())

    @property
    def item_count(self):
        """Get the total number of items in the cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Represents an item in a shopping cart.
    
    Attributes:
        cart (Cart): The associated cart
        product (Product): The product in the cart
        quantity (int): The quantity of the product
    """
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The associated cart"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="The product in the cart"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="The quantity of the product"
    )

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        """Calculate the total price for this item."""
        return self.product.price * self.quantity
