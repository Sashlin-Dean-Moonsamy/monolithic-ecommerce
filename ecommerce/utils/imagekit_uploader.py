"""
ImageKit integration utilities for the e-commerce store.

This module provides functionality for uploading and managing images using
the ImageKit service, including client initialization and file upload handling.
"""

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from django.conf import settings
import os
import base64
import logging

logger = logging.getLogger(__name__)

def get_imagekit_client():
    """
    Initialize and return an ImageKit client instance.
    
    This function creates a new ImageKit client using the configured settings
    from Django's settings module.
    
    Returns:
        ImageKit: An initialized ImageKit client instance
        
    Raises:
        RuntimeError: If required settings are missing or client initialization fails
    """
    if not all([settings.IMAGEKIT_PRIVATE_KEY, settings.IMAGEKIT_PUBLIC_KEY, settings.IMAGEKIT_URL_ENDPOINT]):
        raise RuntimeError("ImageKit settings (IMAGEKIT_PRIVATE_KEY, IMAGEKIT_PUBLIC_KEY, IMAGEKIT_URL_ENDPOINT) are not configured in Django settings.")
    
    try:
        return ImageKit(
            private_key=settings.IMAGEKIT_PRIVATE_KEY,
            public_key=settings.IMAGEKIT_PUBLIC_KEY,
            url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
        )
    except Exception as e:
        logger.error(f"Failed to initialize ImageKit client: {str(e)}")
        raise RuntimeError(f"Failed to initialize ImageKit client: {str(e)}")

def upload_image_to_imagekit(file, file_name, folder="/products/primary/"):
    """
    Upload an image file to ImageKit.
    
    This function handles the process of uploading an image to ImageKit,
    including file validation, base64 encoding, and response handling.
    
    Args:
        file: A file-like object containing the image data
        file_name (str): The name to give the uploaded file
        folder (str): The folder path in ImageKit where the file should be stored
        
    Returns:
        str: The URL of the uploaded image
        
    Raises:
        ValueError: If the file is invalid or empty
        RuntimeError: If the upload fails or returns an invalid response
    """
    try:
        # Initialize ImageKit client
        imagekit = get_imagekit_client()
        
        # Ensure file is valid
        if not file or not hasattr(file, 'read'):
            raise ValueError("Invalid file object provided")
            
        # Read file content in binary mode
        file_content = file.read()
        if not file_content:
            raise ValueError("Empty file content")
            
        # Reset file pointer
        file.seek(0)
        
        # Convert file content to base64
        base64_file = base64.b64encode(file_content).decode('utf-8')
        
        # Create upload options
        options = UploadFileRequestOptions(
            folder=folder,
            use_unique_file_name=True
        )
        
        # Upload to ImageKit using base64
        response = imagekit.upload(
            file=base64_file,
            file_name=file_name,
            options=options
        )
        
        # Log the response for debugging
        logger.debug(f"ImageKit upload response: {response}")
        
        if not response:
            logger.error("No response received from ImageKit")
            raise RuntimeError("No response received from ImageKit")
            
        if isinstance(response, dict) and response.get("error"):
            logger.error(f"ImageKit error: {response['error']}")
            raise RuntimeError(f"ImageKit error: {response['error']}")
            
        # Extract URL from response
        url = None
        if isinstance(response, dict):
            url = response.get("url")
        elif hasattr(response, "url"):
            url = response.url
            
        if not url:
            logger.error(f"Invalid response format from ImageKit: {response}")
            raise RuntimeError("No URL received in ImageKit response")
            
        return url

    except Exception as e:
        logger.error(f"ImageKit upload failed: {str(e)}")
        raise RuntimeError(f"ImageKit upload failed: {str(e)}") 