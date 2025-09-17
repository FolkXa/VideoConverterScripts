#!/usr/bin/env python3
"""
Test script for Media Converter CLI Tool
Simple verification that the installation is working correctly
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")

    try:
        from video_converter import VideoConverter
        from image_converter import ImageConverter
        from media_converter import MediaConverterCLI
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_image_converter():
    """Test basic image converter functionality"""
    print("\nTesting Image Converter...")

    try:
        from image_converter import ImageConverter
        converter = ImageConverter()

        # Test supported formats
        formats = converter.get_supported_formats()
        if formats and 'input' in formats and 'output' in formats:
            print("✅ Image converter: Supported formats retrieved")
            print(f"   Input formats: {len(formats['input'])} types")
            print(f"   Output formats: {len(formats['output'])} types")
        else:
            print("❌ Image converter: Could not retrieve supported formats")
            return False

        # Test dependencies
        if converter._check_dependencies():
            print("✅ Image converter: Dependencies check passed")
        else:
            print("❌ Image converter: Dependencies check failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Image converter test failed: {e}")
        return False

def test_video_converter():
    """Test basic video converter functionality"""
    print("\nTesting Video Converter...")

    try:
        from video_converter import VideoConverter
        converter = VideoConverter()

        # Test supported formats
        formats = converter.get_supported_formats()
        if formats:
            print(f"✅ Video converter: {len(formats)} supported formats")
        else:
            print("❌ Video converter: Could not retrieve supported formats")
            return False

        # Test FFmpeg availability
        if converter._check_dependencies():
            print("✅ Video converter: FFmpeg is available")
        else:
            print("⚠️  Video converter: FFmpeg not found (video features disabled)")
            print("   This is normal if FFmpeg is not installed")

        return True

    except Exception as e:
        print(f"❌ Video converter test failed: {e}")
        return False

def test_cli_interface():
    """Test CLI interface"""
    print("\nTesting CLI Interface...")

    try:
        from media_converter import MediaConverterCLI
        cli = MediaConverterCLI()

        # Test argument parser creation
        parser = cli.setup_parser()
        if parser:
            print("✅ CLI: Argument parser created successfully")
        else:
            print("❌ CLI: Could not create argument parser")
            return False

        # Test help output (should not raise exceptions)
        help_args = ['--help']
        try:
            parser.parse_args(help_args)
        except SystemExit:
            # This is expected for --help
            print("✅ CLI: Help system works correctly")
        except Exception as e:
            print(f"❌ CLI: Help system error: {e}")
            return False

        return True

    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def create_test_image():
    """Create a simple test image"""
    try:
        from PIL import Image

        # Create a simple test image
        test_image_path = "test_image.jpg"
        img = Image.new('RGB', (100, 100), color='red')
        img.save(test_image_path, 'JPEG')

        print(f"✅ Created test image: {test_image_path}")
        return test_image_path

    except Exception as e:
        print(f"❌ Could not create test image: {e}")
        return None

def test_image_conversion():
    """Test actual image conversion"""
    print("\nTesting Image Conversion...")

    # Create test image
    test_image = create_test_image()
    if not test_image:
        return False

    try:
        from image_converter import ImageConverter
        converter = ImageConverter()

        # Test conversion
        output_path = "test_image_converted.png"
        success = converter.convert(
            test_image,
            output_path,
            format='png',
            quality=85
        )

        if success and Path(output_path).exists():
            print("✅ Image conversion: Successfully converted JPG to PNG")

            # Clean up
            os.remove(test_image)
            os.remove(output_path)
            print("✅ Test files cleaned up")

            return True
        else:
            print("❌ Image conversion failed")
            return False

    except Exception as e:
        print(f"❌ Image conversion test failed: {e}")

        # Clean up on error
        for file in [test_image, "test_image_converted.png"]:
            if file and Path(file).exists():
                try:
                    os.remove(file)
                except:
                    pass

        return False

def main():
    """Main test function"""
    print("Media Converter CLI Tool - Test Suite")
    print("=" * 50)

    tests_passed = 0
    total_tests = 5

    # Run tests
    if test_imports():
        tests_passed += 1

    if test_image_converter():
        tests_passed += 1

    if test_video_converter():
        tests_passed += 1

    if test_cli_interface():
        tests_passed += 1

    if test_image_conversion():
        tests_passed += 1

    # Results
    print("\n" + "=" * 50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All tests passed! The Media Converter is ready to use.")
        print("\nNext steps:")
        print("1. Try: python media_converter.py --help")
        print("2. Run: python examples.py")
        print("3. Install FFmpeg for video conversion features")
        return True
    else:
        print("❌ Some tests failed. Please check the installation.")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check Python version (3.7+ required)")
        print("3. For video features, install FFmpeg")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
