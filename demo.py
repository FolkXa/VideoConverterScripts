#!/usr/bin/env python3
"""
Media Converter CLI Tool - Interactive Demo
Demonstrates all features with real examples and user interaction
"""

import os
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from image_converter import ImageConverter
    from video_converter import VideoConverter
    from media_converter import MediaConverterCLI
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this from the scripts directory")
    sys.exit(1)


class MediaConverterDemo:
    """Interactive demonstration of the Media Converter tool"""

    def __init__(self):
        self.image_converter = ImageConverter()
        self.video_converter = VideoConverter()
        self.demo_files = []

    def print_header(self, title: str):
        """Print a formatted section header"""
        print("\n" + "="*60)
        print(f" {title}")
        print("="*60)

    def print_step(self, step: str, description: str):
        """Print a formatted step"""
        print(f"\n🔸 {step}: {description}")

    def wait_for_user(self, message: str = "Press Enter to continue..."):
        """Wait for user input"""
        try:
            input(f"\n{message}")
        except KeyboardInterrupt:
            print("\n\n👋 Demo cancelled by user")
            self.cleanup()
            sys.exit(0)

    def create_demo_image(self, filename: str, size: tuple = (800, 600), color: str = 'lightblue'):
        """Create a demonstration image"""
        try:
            img = Image.new('RGB', size, color=color)
            draw = ImageDraw.Draw(img)

            # Add decorative elements
            draw.rectangle([50, 50, size[0]-50, size[1]-50], outline='navy', width=4)
            draw.ellipse([150, 150, size[0]-150, size[1]-150], fill='lightcoral', outline='darkred', width=3)

            # Add text
            try:
                font = ImageFont.load_default()
                text = f"Demo Image {size[0]}x{size[1]}"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_x = (size[0] - text_width) // 2
                draw.text((text_x, 100), text, fill='navy', font=font)

                # Add timestamp
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                draw.text((60, size[1]-80), f"Created: {timestamp}", fill='darkblue', font=font)

            except Exception:
                draw.text((size[0]//2 - 100, 100), "Demo Image", fill='navy')

            img.save(filename, 'JPEG', quality=95)
            self.demo_files.append(filename)
            print(f"✅ Created demo image: {filename}")
            return True

        except Exception as e:
            print(f"❌ Failed to create demo image: {e}")
            return False

    def demo_image_conversion(self):
        """Demonstrate image conversion features"""
        self.print_header("IMAGE CONVERSION DEMO")

        print("This section demonstrates comprehensive image processing capabilities:")
        print("• Format conversion (JPEG ↔ PNG ↔ WebP)")
        print("• Quality-based compression")
        print("• Resizing and optimization")
        print("• Metadata handling")

        self.wait_for_user()

        # Create demo images
        self.print_step("1", "Creating demo images")
        demo_images = [
            ("demo_large.jpg", (1600, 1200), 'lightblue'),
            ("demo_photo.jpg", (800, 600), 'lightgreen'),
            ("demo_small.jpg", (400, 300), 'lightcoral')
        ]

        for filename, size, color in demo_images:
            if self.create_demo_image(filename, size, color):
                file_size = Path(filename).stat().st_size
                print(f"   Size: {file_size:,} bytes ({size[0]}x{size[1]})")

        self.wait_for_user("Press Enter to start conversions...")

        # Demonstrate format conversion
        self.print_step("2", "Format Conversion (JPEG → WebP)")
        success = self.image_converter.convert(
            "demo_photo.jpg",
            "demo_photo.webp",
            format='webp',
            quality=80,
            optimize=True
        )

        if success:
            original_size = Path("demo_photo.jpg").stat().st_size
            converted_size = Path("demo_photo.webp").stat().st_size
            reduction = ((original_size - converted_size) / original_size) * 100
            print(f"✅ Conversion successful!")
            print(f"   Original (JPEG): {original_size:,} bytes")
            print(f"   Converted (WebP): {converted_size:,} bytes")
            print(f"   Size reduction: {reduction:.1f}%")
            self.demo_files.append("demo_photo.webp")

        # Demonstrate resizing
        self.print_step("3", "Image Resizing (50% reduction)")
        success = self.image_converter.convert(
            "demo_large.jpg",
            "demo_resized.jpg",
            resize="50%",
            quality=85,
            optimize=True
        )

        if success:
            original_info = self.image_converter.get_image_info("demo_large.jpg")
            resized_info = self.image_converter.get_image_info("demo_resized.jpg")
            print(f"✅ Resize successful!")
            print(f"   Original: {original_info['width']}x{original_info['height']} ({original_info['file_size']:,} bytes)")
            print(f"   Resized:  {resized_info['width']}x{resized_info['height']} ({resized_info['file_size']:,} bytes)")
            self.demo_files.append("demo_resized.jpg")

        # Demonstrate compression levels
        self.print_step("4", "Quality Comparison")
        qualities = [60, 80, 95]

        for quality in qualities:
            output_file = f"demo_quality_{quality}.jpg"
            success = self.image_converter.convert(
                "demo_photo.jpg",
                output_file,
                quality=quality,
                optimize=True
            )

            if success:
                file_size = Path(output_file).stat().st_size
                print(f"   Quality {quality}%: {file_size:,} bytes")
                self.demo_files.append(output_file)

        # Demonstrate batch processing
        self.print_step("5", "Batch Processing")
        batch_files = ["demo_large.jpg", "demo_photo.jpg", "demo_small.jpg"]
        os.makedirs("batch_output", exist_ok=True)

        results = self.image_converter.batch_convert(
            batch_files,
            "batch_output",
            format='png',
            quality=90,
            optimize=True
        )

        successful = sum(1 for result in results.values() if result)
        print(f"✅ Batch conversion: {successful}/{len(batch_files)} files processed")

        # Add batch output to cleanup
        for file in batch_files:
            batch_file = Path("batch_output") / f"{Path(file).stem}.png"
            if batch_file.exists():
                self.demo_files.append(str(batch_file))

        print("\n📊 Image Demo Summary:")
        print(f"• Created {len(demo_images)} demo images")
        print(f"• Performed format conversion with {reduction:.1f}% size reduction")
        print(f"• Demonstrated resizing and quality control")
        print(f"• Batch processed {successful} files")

    def demo_video_features(self):
        """Demonstrate video processing features"""
        self.print_header("VIDEO PROCESSING DEMO")

        # Check if FFmpeg is available
        if not self.video_converter._check_dependencies():
            print("❌ FFmpeg not available - skipping video demos")
            print("\nTo enable video features:")
            print("• macOS: brew install ffmpeg")
            print("• Ubuntu: sudo apt install ffmpeg")
            print("• Windows: Download from https://ffmpeg.org/")
            return

        print("This section would demonstrate video processing capabilities:")
        print("• Format conversion (AVI → MP4)")
        print("• Quality-based compression")
        print("• Resolution scaling")
        print("• Audio extraction")
        print("• Video clipping")

        print("\n⚠️  Note: Video demos require sample video files")
        print("For now, we'll show the available capabilities:")

        # Show supported formats
        formats = self.video_converter.get_supported_formats()
        print(f"\n📹 Supported video formats: {', '.join(formats)}")

        # Show example usage
        print("\n💡 Example video operations:")
        print("   python3 media_converter.py video input.mov --format mp4 --quality medium")
        print("   python3 media_converter.py video large.avi --resolution 1280x720 --compress")
        print("   python3 media_converter.py video movie.mp4 --start 00:01:00 --duration 00:02:00")

    def demo_cli_interface(self):
        """Demonstrate CLI interface"""
        self.print_header("CLI INTERFACE DEMO")

        print("The tool provides a comprehensive command-line interface:")

        # Create a sample image for CLI demo
        self.create_demo_image("cli_demo.jpg", (600, 400), 'lightyellow')

        self.print_step("1", "Help System")
        print("Available help commands:")
        print("   python3 media_converter.py --help")
        print("   python3 media_converter.py image --help")
        print("   python3 media_converter.py video --help")

        self.print_step("2", "Basic CLI Usage")
        print("Example commands you can try:")
        print("   python3 media_converter.py image cli_demo.jpg --format webp --quality 80")
        print("   python3 media_converter.py image *.jpg --compress --batch")
        print("   ./convert img cli_demo.jpg --format png")

        # Actually run a CLI command
        self.print_step("3", "Live CLI Demonstration")
        print("Running: python3 media_converter.py image cli_demo.jpg --format webp --quality 75")

        try:
            cli = MediaConverterCLI()
            result = cli.run(['image', 'cli_demo.jpg', '--format', 'webp', '--quality', '75'])
            if result == 0:
                print("✅ CLI command executed successfully!")
                self.demo_files.append("cli_demo.webp")
        except Exception as e:
            print(f"❌ CLI demo failed: {e}")

    def demo_programmatic_usage(self):
        """Demonstrate programmatic API"""
        self.print_header("PROGRAMMATIC API DEMO")

        print("The converters can be used directly in Python code:")

        self.print_step("1", "Direct API Usage")

        # Create a demo image programmatically
        self.create_demo_image("api_demo.jpg", (500, 300), 'lavender')

        # Demonstrate direct converter usage
        print("Converting using ImageConverter class directly...")

        success = self.image_converter.convert(
            "api_demo.jpg",
            "api_demo.png",
            format='png',
            quality=90,
            optimize=True
        )

        if success:
            print("✅ Direct API conversion successful!")
            self.demo_files.append("api_demo.png")

            # Show file info
            info = self.image_converter.get_image_info("api_demo.png")
            if info:
                print(f"   Result: {info['format']} {info['width']}x{info['height']}")
                print(f"   File size: {info['file_size']:,} bytes")

        self.print_step("2", "Error Handling")
        print("Testing error handling with invalid input...")

        success = self.image_converter.convert("nonexistent.jpg", "output.jpg")
        print(f"   Missing file handled: {'✅' if not success else '❌'}")

        self.print_step("3", "Utility Functions")

        # Demonstrate utility functions
        formats = self.image_converter.get_supported_formats()
        print(f"   Supported input formats: {len(formats['input'])}")
        print(f"   Supported output formats: {len(formats['output'])}")

        # File size estimation
        if Path("api_demo.jpg").exists():
            estimated_size = self.image_converter.estimate_file_size(
                "api_demo.jpg",
                format='webp',
                quality=70
            )
            if estimated_size:
                original_size = Path("api_demo.jpg").stat().st_size
                print(f"   Estimated WebP size: {estimated_size:,} bytes")
                print(f"   Estimated reduction: {((original_size - estimated_size) / original_size * 100):.1f}%")

    def show_performance_comparison(self):
        """Show performance comparison between formats"""
        self.print_header("PERFORMANCE COMPARISON")

        print("Comparing different formats and quality settings:")

        # Create a test image
        test_image = "perf_test.jpg"
        self.create_demo_image(test_image, (1200, 800), 'lightsteelblue')

        # Test different formats and qualities
        test_configs = [
            ('jpg', 60, 'JPEG Low'),
            ('jpg', 85, 'JPEG Medium'),
            ('jpg', 95, 'JPEG High'),
            ('webp', 60, 'WebP Low'),
            ('webp', 80, 'WebP Medium'),
            ('webp', 95, 'WebP High'),
            ('png', None, 'PNG Lossless')
        ]

        original_size = Path(test_image).stat().st_size
        results = []

        print(f"\nOriginal JPEG: {original_size:,} bytes")
        print("\nConversion Results:")
        print("-" * 50)

        for fmt, quality, label in test_configs:
            output_file = f"perf_{fmt}_{quality or 'lossless'}.{fmt}"

            start_time = time.time()
            options = {'format': fmt, 'optimize': True}
            if quality is not None:
                options['quality'] = quality

            success = self.image_converter.convert(test_image, output_file, **options)
            end_time = time.time()

            if success:
                file_size = Path(output_file).stat().st_size
                reduction = ((original_size - file_size) / original_size) * 100
                processing_time = end_time - start_time

                print(f"{label:12}: {file_size:7,} bytes ({reduction:+5.1f}%) {processing_time:.2f}s")
                results.append((label, file_size, reduction))
                self.demo_files.append(output_file)

        # Find best compression
        if results:
            best_compression = min(results, key=lambda x: x[1])
            print(f"\n🏆 Best compression: {best_compression[0]} ({best_compression[2]:.1f}% reduction)")

    def show_summary(self):
        """Show demo summary"""
        self.print_header("DEMO SUMMARY")

        print("🎉 Demo completed successfully!")
        print("\nWhat we demonstrated:")
        print("• ✅ Image format conversion (JPEG, PNG, WebP)")
        print("• ✅ Quality-based compression")
        print("• ✅ Image resizing and optimization")
        print("• ✅ Batch processing capabilities")
        print("• ✅ CLI interface usage")
        print("• ✅ Programmatic API")
        print("• ✅ Performance comparisons")
        print("• ✅ Error handling")

        if self.video_converter._check_dependencies():
            print("• ✅ Video processing ready (FFmpeg available)")
        else:
            print("• ⚠️  Video processing needs FFmpeg installation")

        print(f"\n📁 Created {len(self.demo_files)} demonstration files")

        print("\n🚀 Next Steps:")
        print("1. Try your own files with the CLI tool")
        print("2. Integrate the classes into your Python projects")
        print("3. Install FFmpeg for video processing")
        print("4. Check README.md for comprehensive documentation")

        print("\n💡 Quick Commands to Try:")
        print("   python3 media_converter.py image your_photo.jpg --format webp --quality 80")
        print("   python3 media_converter.py image *.jpg --compress --batch")
        print("   ./convert img photo.png --resize 1920x1080")

    def cleanup(self):
        """Clean up demo files"""
        print(f"\n🧹 Cleaning up {len(self.demo_files)} demo files...")

        removed = 0
        for file_path in self.demo_files:
            try:
                if Path(file_path).exists():
                    os.remove(file_path)
                    removed += 1
            except Exception as e:
                print(f"   ⚠️  Could not remove {file_path}: {e}")

        # Clean up batch_output directory
        try:
            batch_dir = Path("batch_output")
            if batch_dir.exists():
                for file in batch_dir.iterdir():
                    file.unlink()
                batch_dir.rmdir()
                print("   ✅ Removed batch_output directory")
        except Exception as e:
            print(f"   ⚠️  Could not clean batch_output: {e}")

        print(f"✅ Cleaned up {removed} files")

    def run_full_demo(self):
        """Run the complete demonstration"""
        try:
            print("🎬 Media Converter CLI Tool - Interactive Demo")
            print("=" * 60)
            print("This demo will showcase all features of the media converter tool.")
            print("Demo files will be created and cleaned up automatically.")

            self.wait_for_user("Press Enter to start the demo...")

            # Run all demo sections
            self.demo_image_conversion()
            self.wait_for_user("Press Enter for video demo...")

            self.demo_video_features()
            self.wait_for_user("Press Enter for CLI demo...")

            self.demo_cli_interface()
            self.wait_for_user("Press Enter for API demo...")

            self.demo_programmatic_usage()
            self.wait_for_user("Press Enter for performance comparison...")

            self.show_performance_comparison()

            self.show_summary()

            # Ask about cleanup
            self.wait_for_user("Press Enter to clean up demo files...")
            self.cleanup()

            print("\n🎉 Demo completed! Thank you for trying the Media Converter CLI Tool.")

        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted by user")
            self.cleanup()
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            self.cleanup()

def main():
    """Main demo function"""
    try:
        demo = MediaConverterDemo()
        demo.run_full_demo()
    except Exception as e:
        print(f"Demo initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
