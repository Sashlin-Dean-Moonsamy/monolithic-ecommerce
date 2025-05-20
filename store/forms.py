"""
Forms for the e-commerce store application.

This module contains form classes for handling product and image uploads,
including validation and processing of uploaded files.
"""

from django import forms
from .models import Product, ProductImage
from ecommerce.utils.imagekit_uploader import upload_image_to_imagekit
import os
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)


class ProductAdminForm(forms.ModelForm):
    """
    Form for managing products in the admin interface.
    
    This form handles product creation and updates, including
    primary image upload and processing.
    """
    
    primary_image_upload = forms.ImageField(
        required=False,
        label="Primary Image Upload",
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'primary_image_upload']

    def clean_primary_image_upload(self):
        """
        Validate and process the uploaded primary image.
        
        Performs the following validations:
        - File size (max 5MB)
        - File type (must be an image)
        - Image format conversion if necessary
        
        Returns:
            The processed image file
            
        Raises:
            forms.ValidationError: If validation fails
        """
        image = self.cleaned_data.get('primary_image_upload')
        if image:
            # Validate file size (e.g., max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            # Validate file type
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("File type not supported")
            
            # Process image to ensure it's in a good format
            try:
                img = Image.open(image)
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                # Save to bytes
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=95)
                output.seek(0)
                # Create a new file-like object
                image.file = output
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                raise forms.ValidationError(f"Error processing image: {str(e)}")
                
        return image

    def save(self, commit=True):
        """
        Save the form data and handle image upload.
        
        Args:
            commit (bool): Whether to save the model instance
            
        Returns:
            The saved model instance
            
        Raises:
            forms.ValidationError: If image upload fails
        """
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('primary_image_upload')
        if image_file:
            try:
                # Ensure proper file extension
                file_name = os.path.splitext(image_file.name)[0] + '.jpg'
                url = upload_image_to_imagekit(image_file, file_name, folder='/products/primary/')
                if not url:
                    raise forms.ValidationError("Failed to get image URL from ImageKit")
                instance.primary_image_url = url
            except Exception as e:
                logger.error(f"Error uploading image: {str(e)}")
                raise forms.ValidationError(f"Error uploading image: {str(e)}")
        if commit:
            instance.save()
        return instance


class ProductImageAdminForm(forms.ModelForm):
    """
    Form for managing additional product images in the admin interface.
    
    This form handles the upload and processing of additional product images,
    including validation and proper ordering.
    """
    
    image_upload = forms.ImageField(
        required=True,
        label="Upload Image",
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    
    class Meta:
        model = ProductImage
        fields = ['product', 'order', 'image_upload']

    def clean_image_upload(self):
        """
        Validate and process the uploaded product image.
        
        Performs the following validations:
        - File size (max 5MB)
        - File type (must be an image)
        - Image format conversion if necessary
        
        Returns:
            The processed image file
            
        Raises:
            forms.ValidationError: If validation fails
        """
        image = self.cleaned_data.get('image_upload')
        if image:
            # Validate file size (e.g., max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            # Validate file type
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("File type not supported")
            
            # Process image to ensure it's in a good format
            try:
                img = Image.open(image)
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                # Save to bytes
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=95)
                output.seek(0)
                # Create a new file-like object
                image.file = output
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                raise forms.ValidationError(f"Error processing image: {str(e)}")
                
        return image

    def save(self, commit=True):
        """
        Save the form data and handle image upload.
        
        Args:
            commit (bool): Whether to save the model instance
            
        Returns:
            The saved model instance
            
        Raises:
            forms.ValidationError: If image upload fails
        """
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image_upload')
        if image_file:
            try:
                # Ensure proper file extension
                file_name = os.path.splitext(image_file.name)[0] + '.jpg'
                url = upload_image_to_imagekit(image_file, file_name, folder='/products/additional/')
                if not url:
                    raise forms.ValidationError("Failed to get image URL from ImageKit")
                instance.image_url = url
            except Exception as e:
                logger.error(f"Error uploading image: {str(e)}")
                raise forms.ValidationError(f"Error uploading image: {str(e)}")
        if commit:
            instance.save()
        return instance
