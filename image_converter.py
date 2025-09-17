#!/usr/bin/env python3
"""
Image Converter Class
Handles image conversion, compression, and manipulation using Pillow (PIL)
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Optional, Union, Tuple, List
from PIL import Image, ImageOps, ImageFilter, ExifTags
from PIL.ExifTags import TAGS
import io


class ImageConverter:
    """A class for converting and compressing images using Pillow"""

    def __init__(self):
        # Supported input formats
        self.supported_input_formats = {
            '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif',
            '.webp', '.gif', '.ico', '.ppm', '.pgm', '.pbm'
        }

        # Supported output formats
        self.supported_output_formats = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'webp': 'WebP',
            'tiff': 'TIFF',
            'bmp': 'BMP',
            'gif': 'GIF',
            'ico': 'ICO'
        }

        # Quality presets for lossy formats
        self.quality_presets = {
            'low': 60,
            'medium': 85,
            'high': 95,
            'maximum': 100
        }

    def _check_dependencies(self) -> bool:
        """Check if required dependencies are available"""
        try:
            import PIL
            return True
        except ImportError:
            print("Error: Pillow not found. Please install it:")
            print("  pip install Pillow")
            return False

    def get_image_info(self, input_path: str) -> Optional[Dict]:
        """Get image information"""
        try:
            with Image.open(input_path) as img:
                info = {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                }

                # Get EXIF data if available
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    exif_dict = {}
                    exif = img._getexif()
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_dict[tag] = value
                    info['exif'] = exif_dict

                # File size
                info['file_size'] = Path(input_path).stat().st_size

                return info
        except Exception as e:
            print(f"Error getting image info: {e}")
            return None

    def _parse_resize(self, resize_spec: str, original_size: Tuple[int, int]) -> Tuple[int, int]:
        """Parse resize specification"""
        width, height = original_size

        if resize_spec.endswith('%'):
            # Percentage resize
            percentage = float(resize_spec[:-1]) / 100
            return int(width * percentage), int(height * percentage)
        elif 'x' in resize_spec.lower():
            # Explicit dimensions
            parts = resize_spec.lower().split('x')
            new_width = int(parts[0]) if parts[0] else width
            new_height = int(parts[1]) if parts[1] else height
            return new_width, new_height
        else:
            # Single number - assume width, maintain aspect ratio
            new_width = int(resize_spec)
            aspect_ratio = height / width
            new_height = int(new_width * aspect_ratio)
            return new_width, new_height

    def _optimize_image(self, img: Image.Image, format_name: str, **options) -> Image.Image:
        """Apply optimization settings to image"""
        # Handle transparency for formats that don't support it
        if format_name == 'JPEG' and img.mode in ('RGBA', 'LA'):
            # Convert RGBA to RGB with white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            else:
                background.paste(img)
            img = background
        elif format_name == 'JPEG' and img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        # Handle PNG optimization
        if format_name == 'PNG' and img.mode == 'RGB':
            # Convert RGB to P mode with palette for better compression
            if options.get('optimize', True):
                try:
                    img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
                except:
                    pass  # Keep original if conversion fails

        return img

    def _apply_filters(self, img: Image.Image, **options) -> Image.Image:
        """Apply image filters and effects"""
        # Sharpen
        if options.get('sharpen'):
            img = img.filter(ImageFilter.SHARPEN)

        # Blur
        if options.get('blur'):
            blur_radius = options.get('blur_radius', 1.0)
            img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        # Auto-enhance
        if options.get('auto_enhance'):
            img = ImageOps.autocontrast(img)

        return img

    def _add_watermark(self, img: Image.Image, watermark_path: str, **options) -> Image.Image:
        """Add watermark to image"""
        try:
            with Image.open(watermark_path) as watermark:
                # Resize watermark if needed
                position = options.get('watermark_position', 'bottom-right')
                opacity = options.get('watermark_opacity', 0.5)
                size_ratio = options.get('watermark_size', 0.1)

                # Calculate watermark size
                img_width, img_height = img.size
                wm_size = int(min(img_width, img_height) * size_ratio)
                watermark = watermark.convert('RGBA')
                watermark.thumbnail((wm_size, wm_size), Image.Resampling.LANCZOS)

                # Apply opacity
                if opacity < 1.0:
                    alpha = watermark.split()[-1]
                    alpha = alpha.point(lambda p: int(p * opacity))
                    watermark.putalpha(alpha)

                # Calculate position
                wm_width, wm_height = watermark.size
                if position == 'top-left':
                    pos = (10, 10)
                elif position == 'top-right':
                    pos = (img_width - wm_width - 10, 10)
                elif position == 'bottom-left':
                    pos = (10, img_height - wm_height - 10)
                elif position == 'bottom-right':
                    pos = (img_width - wm_width - 10, img_height - wm_height - 10)
                elif position == 'center':
                    pos = ((img_width - wm_width) // 2, (img_height - wm_height) // 2)
                else:
                    pos = (10, 10)

                # Convert main image to RGBA for transparency support
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Paste watermark
                img.paste(watermark, pos, watermark)

        except Exception as e:
            print(f"Warning: Could not add watermark: {e}")

        return img

    def convert(self, input_path: str, output_path: str, **options) -> bool:
        """
        Convert image with specified options

        Args:
            input_path: Path to input image file
            output_path: Path to output image file
            **options: Conversion options

        Returns:
            bool: True if successful, False otherwise
        """
        if not self._check_dependencies():
            return False

        input_file = Path(input_path)
        if not input_file.exists():
            print(f"Error: Input file '{input_path}' not found")
            return False

        if input_file.suffix.lower() not in self.supported_input_formats:
            print(f"Error: Unsupported input format '{input_file.suffix}'")
            return False

        try:
            # Create output directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            with Image.open(input_path) as img:
                # Store original format for reference
                original_format = img.format

                # Determine output format
                output_format = options.get('format')
                if output_format:
                    format_name = self.supported_output_formats.get(output_format.lower())
                    if not format_name:
                        print(f"Error: Unsupported output format '{output_format}'")
                        return False
                else:
                    # Use output file extension or keep original format
                    output_ext = Path(output_path).suffix.lower().lstrip('.')
                    if output_ext in self.supported_output_formats:
                        format_name = self.supported_output_formats[output_ext]
                    else:
                        format_name = original_format

                # Apply resize if specified
                if options.get('resize'):
                    new_size = self._parse_resize(options['resize'], img.size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

                # Apply filters
                img = self._apply_filters(img, **options)

                # Add watermark if specified
                if options.get('watermark'):
                    img = self._add_watermark(img, options['watermark'], **options)

                # Get quality setting
                quality = options.get('quality', 85)
                if isinstance(quality, str) and quality in self.quality_presets:
                    quality = self.quality_presets[quality]

                # Optimize image for target format
                img = self._optimize_image(img, format_name, **options)

                # Prepare save options
                save_options = {}

                if format_name == 'JPEG':
                    save_options['quality'] = quality
                    save_options['optimize'] = options.get('optimize', True)
                    if options.get('progressive'):
                        save_options['progressive'] = True
                elif format_name == 'PNG':
                    save_options['optimize'] = options.get('optimize', True)
                elif format_name == 'WebP':
                    save_options['quality'] = quality
                    save_options['optimize'] = options.get('optimize', True)

                # Remove EXIF data if requested
                if options.get('strip_metadata', False):
                    # Create a new image without EXIF data
                    data = list(img.getdata())
                    img_no_exif = Image.new(img.mode, img.size)
                    img_no_exif.putdata(data)
                    img = img_no_exif

                # Save the image
                img.save(output_path, format=format_name, **save_options)

                return True

        except Exception as e:
            print(f"Error during conversion: {e}")
            return False

    def compress(self, input_path: str, output_path: str, quality: Union[int, str] = 85, **options) -> bool:
        """
        Compress image file

        Args:
            input_path: Path to input image
            output_path: Path to output image
            quality: Compression quality (1-100 or preset name)
            **options: Additional options

        Returns:
            bool: True if successful, False otherwise
        """
        options['quality'] = quality
        options['compress'] = True
        options['optimize'] = True
        return self.convert(input_path, output_path, **options)

    def resize(self, input_path: str, output_path: str, size: str, **options) -> bool:
        """
        Resize image

        Args:
            input_path: Path to input image
            output_path: Path to output image
            size: Target size (e.g., '1920x1080', '50%', '800')
            **options: Additional options

        Returns:
            bool: True if successful, False otherwise
        """
        options['resize'] = size
        return self.convert(input_path, output_path, **options)

    def create_thumbnail(self, input_path: str, output_path: str, size: Tuple[int, int] = (200, 200), **options) -> bool:
        """
        Create thumbnail from image

        Args:
            input_path: Path to input image
            output_path: Path to output thumbnail
            size: Thumbnail size as (width, height)
            **options: Additional options

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with Image.open(input_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)

                # Prepare save options
                save_options = {'quality': options.get('quality', 85), 'optimize': True}

                # Save thumbnail
                img.save(output_path, **save_options)
                return True

        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return False

    def batch_convert(self, input_files: List[str], output_dir: str, **options) -> Dict[str, bool]:
        """
        Batch convert multiple image files

        Args:
            input_files: List of input file paths
            output_dir: Output directory
            **options: Conversion options

        Returns:
            Dict mapping input files to success status
        """
        results = {}
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for input_file in input_files:
            input_path = Path(input_file)
            if not input_path.exists():
                results[input_file] = False
                continue

            # Generate output filename
            output_format = options.get('format')
            if output_format:
                output_file = output_path / f"{input_path.stem}.{output_format}"
            else:
                output_file = output_path / input_path.name

            print(f"Processing: {input_path.name}")
            results[input_file] = self.convert(str(input_path), str(output_file), **options)

        return results

    def get_supported_formats(self) -> Dict[str, List[str]]:
        """Get list of supported formats"""
        return {
            'input': list(self.supported_input_formats),
            'output': list(self.supported_output_formats.keys())
        }

    def estimate_file_size(self, input_path: str, **options) -> Optional[int]:
        """
        Estimate output file size based on conversion options

        Args:
            input_path: Path to input image
            **options: Conversion options

        Returns:
            Estimated file size in bytes, or None if estimation fails
        """
        try:
            with Image.open(input_path) as img:
                # Create a copy for testing
                test_img = img.copy()

                # Apply resize if specified
                if options.get('resize'):
                    new_size = self._parse_resize(options['resize'], img.size)
                    test_img = test_img.resize(new_size, Image.Resampling.LANCZOS)

                # Determine output format
                output_format = options.get('format', 'jpeg')
                format_name = self.supported_output_formats.get(output_format.lower(), 'JPEG')

                # Get quality
                quality = options.get('quality', 85)
                if isinstance(quality, str) and quality in self.quality_presets:
                    quality = self.quality_presets[quality]

                # Optimize for target format
                test_img = self._optimize_image(test_img, format_name, **options)

                # Save to memory buffer to estimate size
                buffer = io.BytesIO()
                save_options = {}

                if format_name == 'JPEG':
                    save_options['quality'] = quality
                    save_options['optimize'] = options.get('optimize', True)
                elif format_name == 'PNG':
                    save_options['optimize'] = options.get('optimize', True)
                elif format_name == 'WebP':
                    save_options['quality'] = quality
                    save_options['optimize'] = options.get('optimize', True)

                test_img.save(buffer, format=format_name, **save_options)
                return len(buffer.getvalue())

        except Exception as e:
            print(f"Error estimating file size: {e}")
            return None
