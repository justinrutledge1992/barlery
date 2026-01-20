"""
Image Compression Utility for Barlery Django Project

This module provides automatic image compression for uploaded images.
It compresses images while maintaining reasonable quality to reduce
file sizes and improve page load times.
"""

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(uploaded_image, max_width=1200, max_height=1200, quality=85):
    """
    Compress an uploaded image to reduce file size while maintaining quality.
    
    Args:
        uploaded_image: Django UploadedFile object (from form)
        max_width: Maximum width in pixels (default: 1200)
        max_height: Maximum height in pixels (default: 1200)
        quality: JPEG quality 1-100 (default: 85, good balance of quality/size)
    
    Returns:
        InMemoryUploadedFile: Compressed image ready to save to model
    
    Example usage in forms.py:
        from .utils import compress_image
        
        def save(self, commit=True):
            instance = super().save(commit=False)
            if instance.image:
                instance.image = compress_image(instance.image)
            if commit:
                instance.save()
            return instance
    """
    # Open the uploaded image
    img = Image.open(uploaded_image)
    
    # Convert RGBA to RGB (for PNG with transparency)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        # Paste image on white background
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Get original dimensions
    width, height = img.size
    
    # Calculate new dimensions while maintaining aspect ratio
    if width > max_width or height > max_height:
        # Calculate scaling factor
        width_ratio = max_width / width
        height_ratio = max_height / height
        scale_factor = min(width_ratio, height_ratio)
        
        # Calculate new dimensions
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        # Resize image using high-quality resampling
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save to BytesIO object
    output = BytesIO()
    
    # Save as JPEG with specified quality
    # JPEG is more efficient than PNG for photos
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    # Get the original filename and change extension to .jpg
    original_name = uploaded_image.name
    name_without_ext = original_name.rsplit('.', 1)[0]
    new_name = f"{name_without_ext}.jpg"
    
    # Create new InMemoryUploadedFile
    compressed_image = InMemoryUploadedFile(
        output,
        'ImageField',
        new_name,
        'image/jpeg',
        sys.getsizeof(output),
        None
    )
    
    return compressed_image


def compress_image_aggressive(uploaded_image, max_width=800, max_height=800, quality=75):
    """
    More aggressive compression for thumbnails or less critical images.
    
    Args:
        uploaded_image: Django UploadedFile object
        max_width: Maximum width (default: 800px)
        max_height: Maximum height (default: 800px)
        quality: JPEG quality (default: 75)
    
    Returns:
        InMemoryUploadedFile: Compressed image
    """
    return compress_image(uploaded_image, max_width, max_height, quality)


def get_image_size_kb(image_field):
    """
    Get the size of an image in kilobytes.
    
    Args:
        image_field: Django ImageField
    
    Returns:
        float: Size in KB, or 0 if image doesn't exist
    """
    try:
        return image_field.size / 1024
    except (AttributeError, FileNotFoundError):
        return 0