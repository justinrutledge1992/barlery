"""
Django Management Command: Compress Existing Event Images

This command compresses all existing event images that are already
stored in your media/storage system.

Usage:
    # Preview what will happen
    python manage.py compress_existing_images --dry-run

    # Compress all images (standard)
    python manage.py compress_existing_images

    # Aggressive compression
    python manage.py compress_existing_images --aggressive

    # Single event
    python manage.py compress_existing_images --event-id 5

    # Preview aggressive
    python manage.py compress_existing_images --dry-run --aggressive
"""

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from barlery.models import Event
from PIL import Image
from io import BytesIO
import sys


class Command(BaseCommand):
    help = 'Compress all existing event images to reduce file sizes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be compressed without actually doing it',
        )
        parser.add_argument(
            '--aggressive',
            action='store_true',
            help='Use more aggressive compression (800px, 75% quality)',
        )
        parser.add_argument(
            '--event-id',
            type=int,
            help='Compress only a specific event by ID',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        aggressive = options['aggressive']
        specific_event_id = options.get('event_id')
        
        # Set compression parameters
        if aggressive:
            max_width = 800
            max_height = 800
            quality = 75
            self.stdout.write(self.style.WARNING('Using aggressive compression (800px, 75% quality)'))
        else:
            max_width = 1200
            max_height = 1200
            quality = 85
            self.stdout.write(self.style.SUCCESS('Using standard compression (1200px, 85% quality)'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No files will be modified'))
        
        # Get events with images
        if specific_event_id:
            events = Event.objects.filter(id=specific_event_id, image__isnull=False).exclude(image='')
            if not events.exists():
                self.stdout.write(self.style.ERROR(f'Event with ID {specific_event_id} not found or has no image'))
                return
        else:
            events = Event.objects.filter(image__isnull=False).exclude(image='')
        
        total_events = events.count()
        
        if total_events == 0:
            self.stdout.write(self.style.WARNING('No events with images found'))
            return
        
        self.stdout.write(f'\nFound {total_events} event(s) with images\n')
        
        compressed_count = 0
        skipped_count = 0
        error_count = 0
        total_original_size = 0
        total_compressed_size = 0
        
        for index, event in enumerate(events, 1):
            self.stdout.write(f'[{index}/{total_events}] Processing: {event.title}')
            
            try:
                # Check if image file exists
                if not event.image.storage.exists(event.image.name):
                    self.stdout.write(self.style.ERROR(f'  ✗ Image file not found in storage'))
                    skipped_count += 1
                    continue
                
                # Get original size
                original_size = event.image.size / 1024  # KB
                total_original_size += original_size
                
                # Open the image
                image_file = event.image.open('rb')
                img = Image.open(image_file)
                
                # Get original dimensions
                original_width, original_height = img.size
                
                # Check if compression is needed
                needs_compression = (
                    original_width > max_width or 
                    original_height > max_height or
                    img.format != 'JPEG'
                )
                
                if not needs_compression and original_size < 500:  # Less than 500KB and already optimized
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Already optimized ({original_size:.1f}KB, {original_width}x{original_height})'))
                    total_compressed_size += original_size
                    skipped_count += 1
                    image_file.close()
                    continue
                
                if dry_run:
                    self.stdout.write(self.style.WARNING(f'  → Would compress: {original_size:.1f}KB ({original_width}x{original_height})'))
                    total_compressed_size += original_size * 0.3  # Estimate 70% reduction
                    compressed_count += 1
                    image_file.close()
                    continue
                
                # Convert RGBA to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate new dimensions
                width, height = img.size
                if width > max_width or height > max_height:
                    width_ratio = max_width / width
                    height_ratio = max_height / height
                    scale_factor = min(width_ratio, height_ratio)
                    
                    new_width = int(width * scale_factor)
                    new_height = int(height * scale_factor)
                    
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save compressed image
                output = BytesIO()
                img.save(output, format='JPEG', quality=quality, optimize=True)
                output.seek(0)
                
                # Get compressed size
                compressed_size = len(output.getvalue()) / 1024  # KB
                total_compressed_size += compressed_size
                
                # Calculate reduction
                reduction = ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0
                
                # Get the filename
                original_name = event.image.name
                name_parts = original_name.rsplit('.', 1)
                new_name = f"{name_parts[0]}.jpg"
                
                # Delete old file if it exists
                if event.image.storage.exists(event.image.name):
                    event.image.delete(save=False)
                
                # Save the compressed image
                event.image.save(new_name, ContentFile(output.getvalue()), save=True)
                
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Compressed: {original_size:.1f}KB → {compressed_size:.1f}KB '
                    f'({reduction:.1f}% reduction, {img.size[0]}x{img.size[1]})'
                ))
                
                compressed_count += 1
                image_file.close()
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error: {str(e)}'))
                error_count += 1
                continue
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('COMPRESSION SUMMARY'))
        self.stdout.write('='*60)
        self.stdout.write(f'Total events processed: {total_events}')
        self.stdout.write(f'Successfully compressed: {compressed_count}')
        self.stdout.write(f'Already optimized (skipped): {skipped_count}')
        self.stdout.write(f'Errors: {error_count}')
        
        if not dry_run and (compressed_count > 0 or skipped_count > 0):
            total_reduction = ((total_original_size - total_compressed_size) / total_original_size) * 100 if total_original_size > 0 else 0
            self.stdout.write(f'\nTotal original size: {total_original_size:.1f}KB ({total_original_size/1024:.1f}MB)')
            self.stdout.write(f'Total compressed size: {total_compressed_size:.1f}KB ({total_compressed_size/1024:.1f}MB)')
            self.stdout.write(self.style.SUCCESS(f'Total reduction: {total_reduction:.1f}%'))
            self.stdout.write(self.style.SUCCESS(f'Space saved: {(total_original_size - total_compressed_size)/1024:.1f}MB'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nThis was a dry run. Run without --dry-run to actually compress images.'))