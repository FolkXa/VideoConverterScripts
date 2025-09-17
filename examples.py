#!/usr/bin/env python3
"""
Examples and demonstrations for the Media Converter tools
This script shows how to use the VideoConverter and ImageConverter classes programmatically
"""

import os
import time
from pathlib import Path
from video_converter import VideoConverter
from image_converter import ImageConverter


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def example_video_conversion():
    """Demonstrate video conversion examples"""
    print_section("VIDEO CONVERSION EXAMPLES")

    converter = VideoConverter()

    # Check if FFmpeg is available
    if not converter._check_dependencies():
        print("Skipping video examples - FFmpeg not available")
        return

    print("1. Basic Video Conversion")
    print("Converting sample.mp4 to compressed_sample.mp4 with medium quality...")

    # Create a sample input file path (you would replace this with actual file)
    input_video = "sample.mp4"
    output_video = "compressed_sample.mp4"

    if Path(input_video).exists():
        success = converter.convert(
            input_video,
            output_video,
            quality='medium',
            compress=True
        )
        print(f"✓ Conversion {'successful' if success else 'failed'}")
    else:
        print(f"Sample file '{input_video}' not found - skipping actual conversion")

    print("\n2. Advanced Video Conversion with Custom Settings")
    print("Example: Convert with H.265 codec, 1080p resolution, and custom bitrate...")

    # Example configuration
    advanced_options = {
        'video_codec': 'h265',
        'resolution': '1920x1080',
        'bitrate': '2M',
        'fps': 30,
        'audio_codec': 'aac',
        'preset': 'slow',
        'quality': 'high'
    }

    print("Options:", advanced_options)

    print("\n3. Video Clipping Example")
    clip_options = {
        'start_time': '00:00:30',  # Start at 30 seconds
        'duration': '00:01:00',   # 60 seconds duration
        'quality': 'medium'
    }

    print("Clipping options:", clip_options)

    print("\n4. Batch Video Processing")
    video_files = ["video1.mp4", "video2.avi", "video3.mov"]
    batch_options = {
        'format': 'mp4',
        'quality': 'medium',
        'resolution': '1280x720'
    }

    print(f"Batch processing {len(video_files)} files with options:", batch_options)
    print("Note: This would process all files in the list")


def example_image_conversion():
    """Demonstrate image conversion examples"""
    print_section("IMAGE CONVERSION EXAMPLES")

    converter = ImageConverter()

    if not converter._check_dependencies():
        print("Skipping image examples - Pillow not available")
        return

    print("1. Basic Image Conversion and Compression")

    input_image = "sample.jpg"
    output_image = "compressed_sample.jpg"

    # Create a sample image for demonstration
    create_sample_image(input_image)

    if Path(input_image).exists():
        success = converter.convert(
            input_image,
            output_image,
            quality=75,
            compress=True,
            optimize=True
        )
        print(f"✓ Compression {'successful' if success else 'failed'}")

        # Show file size comparison
        if success:
            original_size = Path(input_image).stat().st_size
            compressed_size = Path(output_image).stat().st_size
            reduction = ((original_size - compressed_size) / original_size) * 100
            print(f"  Original size: {original_size:,} bytes")
            print(f"  Compressed size: {compressed_size:,} bytes")
            print(f"  Size reduction: {reduction:.1f}%")

    print("\n2. Format Conversion Examples")
    conversion_examples = [
        {"from": "jpg", "to": "webp", "quality": 80},
        {"from": "png", "to": "jpg", "quality": 90},
        {"from": "jpg", "to": "png", "optimize": True}
    ]

    for example in conversion_examples:
        print(f"  {example['from'].upper()} → {example['to'].upper()}: {example}")

    print("\n3. Image Resizing Examples")
    resize_examples = [
        "1920x1080",  # Absolute dimensions
        "50%",        # Percentage
        "800",        # Width only (maintain aspect ratio)
        "x600"        # Height only (maintain aspect ratio)
    ]

    for resize in resize_examples:
        print(f"  Resize specification: '{resize}'")

    print("\n4. Advanced Image Processing")

    advanced_options = {
        'format': 'webp',
        'quality': 85,
        'resize': '1920x1080',
        'optimize': True,
        'strip_metadata': True,
        'progressive': False  # Not applicable to WebP
    }

    print("Advanced processing options:", advanced_options)

    # Demonstrate with actual conversion if sample exists
    if Path(input_image).exists():
        advanced_output = "advanced_sample.webp"
        success = converter.convert(input_image, advanced_output, **advanced_options)
        print(f"✓ Advanced processing {'successful' if success else 'failed'}")

    print("\n5. Batch Image Processing")
    image_files = ["image1.jpg", "image2.png", "image3.tiff"]
    batch_options = {
        'format': 'webp',
        'quality': 80,
        'resize': '1920x1080',
        'optimize': True
    }

    print(f"Batch processing {len(image_files)} files with options:", batch_options)


def create_sample_image(filename: str, size: tuple = (800, 600)):
    """Create a sample image for demonstration"""
    try:
        from PIL import Image, ImageDraw, ImageFont

        # Create a sample image
        img = Image.new('RGB', size, color='lightblue')
        draw = ImageDraw.Draw(img)

        # Add some content to the image
        draw.rectangle([50, 50, size[0]-50, size[1]-50], outline='navy', width=3)
        draw.ellipse([150, 150, size[0]-150, size[1]-150], fill='lightcoral', outline='darkred', width=2)

        # Add text
        try:
            # Try to use a default font
            font = ImageFont.load_default()
            text = "Sample Image for Conversion"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (size[0] - text_width) // 2
            text_y = 100
            draw.text((text_x, text_y), text, fill='navy', font=font)
        except:
            # Fallback without font
            draw.text((size[0]//2 - 100, 100), "Sample Image", fill='navy')

        img.save(filename, 'JPEG', quality=95)
        print(f"Created sample image: {filename} ({size[0]}x{size[1]})")

    except ImportError:
        print("PIL/Pillow not available - cannot create sample image")
    except Exception as e:
        print(f"Error creating sample image: {e}")


def example_utility_functions():
    """Demonstrate utility functions"""
    print_section("UTILITY FUNCTIONS")

    # Video converter utilities
    video_converter = VideoConverter()

    print("1. Video Information")
    sample_video = "sample.mp4"
    if Path(sample_video).exists():
        info = video_converter.get_video_info(sample_video)
        if info:
            print("Video info retrieved successfully")
            # Print some basic info
            if 'streams' in info:
                for stream in info['streams']:
                    if stream.get('codec_type') == 'video':
                        print(f"  Video codec: {stream.get('codec_name')}")
                        print(f"  Resolution: {stream.get('width')}x{stream.get('height')}")
                        print(f"  Frame rate: {stream.get('r_frame_rate')}")
                        break
    else:
        print(f"Sample video '{sample_video}' not found")

    print("\n2. Supported Formats")
    video_formats = video_converter.get_supported_formats()
    print(f"Video formats: {video_formats}")

    # Image converter utilities
    image_converter = ImageConverter()

    print("\n3. Image Information")
    sample_image = "sample.jpg"
    if Path(sample_image).exists():
        info = image_converter.get_image_info(sample_image)
        if info:
            print("Image info:")
            print(f"  Format: {info.get('format')}")
            print(f"  Size: {info.get('width')}x{info.get('height')}")
            print(f"  Mode: {info.get('mode')}")
            print(f"  File size: {info.get('file_size'):,} bytes")

    print("\n4. Image Format Support")
    image_formats = image_converter.get_supported_formats()
    print(f"Input formats: {image_formats['input']}")
    print(f"Output formats: {image_formats['output']}")

    print("\n5. File Size Estimation")
    if Path(sample_image).exists():
        estimated_size = image_converter.estimate_file_size(
            sample_image,
            format='webp',
            quality=80,
            resize='50%'
        )
        if estimated_size:
            original_size = Path(sample_image).stat().st_size
            print(f"Original size: {original_size:,} bytes")
            print(f"Estimated WebP size (80% quality, 50% resize): {estimated_size:,} bytes")
            print(f"Estimated reduction: {((original_size - estimated_size) / original_size * 100):.1f}%")


def example_error_handling():
    """Demonstrate error handling"""
    print_section("ERROR HANDLING EXAMPLES")

    converter = ImageConverter()

    print("1. Handling Missing Files")
    success = converter.convert("nonexistent.jpg", "output.jpg")
    print(f"Missing file result: {'Success' if success else 'Failed (as expected)'}")

    print("\n2. Handling Invalid Formats")
    # This would normally fail gracefully
    print("Attempting conversion with invalid output format...")

    print("\n3. Handling Invalid Options")
    # Example of how the system handles bad resize specifications
    print("Testing invalid resize specification...")

    print("\nThe converter classes include comprehensive error handling:")
    print("- File existence checking")
    print("- Format validation")
    print("- Dependency verification")
    print("- Graceful failure with informative messages")


def cleanup_demo_files():
    """Clean up demonstration files"""
    demo_files = [
        "sample.jpg",
        "compressed_sample.jpg",
        "compressed_sample.mp4",
        "advanced_sample.webp"
    ]

    print_section("CLEANUP")

    for file in demo_files:
        if Path(file).exists():
            try:
                os.remove(file)
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Could not remove {file}: {e}")


def main():
    """Main demonstration function"""
    print("Media Converter Examples and Demonstrations")
    print("=" * 60)

    print("\nThis script demonstrates the capabilities of the Media Converter classes.")
    print("Note: Some examples require actual media files to be present.")

    # Run examples
    example_video_conversion()
    example_image_conversion()
    example_utility_functions()
    example_error_handling()

    # Ask user if they want to cleanup
    print("\n" + "="*60)
    response = input("Clean up demonstration files? (y/n): ")
    if response.lower() in ['y', 'yes']:
        cleanup_demo_files()

    print("\nExamples completed!")
    print("\nTo use these tools in your own projects:")
    print("1. Import the classes: from video_converter import VideoConverter")
    print("2. Create an instance: converter = VideoConverter()")
    print("3. Use the convert method: converter.convert('input.mp4', 'output.mp4')")


if __name__ == "__main__":
    main()
