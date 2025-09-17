#!/usr/bin/env python3
"""
Setup and Installation Utility for Media Converter CLI Tool
Handles dependency installation, system checks, and initial configuration
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path


class MediaConverterSetup:
    """Setup utility for the Media Converter tool"""

    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.script_dir = Path(__file__).parent
        self.requirements_file = self.script_dir / "requirements.txt"

    def print_header(self):
        """Print setup header"""
        print("=" * 60)
        print("Media Converter CLI Tool - Setup")
        print("=" * 60)
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print(f"Script directory: {self.script_dir}")
        print()

    def check_python_version(self):
        """Check if Python version is compatible"""
        print("Checking Python version...")

        if self.python_version < (3, 7):
            print("❌ Python 3.7 or higher is required")
            print(f"   Current version: {sys.version}")
            return False

        print(f"✅ Python {self.python_version.major}.{self.python_version.minor} is compatible")
        return True

    def check_pip(self):
        """Check if pip is available"""
        print("Checking pip availability...")

        try:
            import pip
            print("✅ pip is available")
            return True
        except ImportError:
            print("❌ pip is not available")
            print("   Please install pip first")
            return False

    def install_python_dependencies(self):
        """Install Python dependencies from requirements.txt"""
        print("Installing Python dependencies...")

        if not self.requirements_file.exists():
            print("❌ requirements.txt not found")
            return False

        try:
            # Use pip to install requirements
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)]

            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Python dependencies installed successfully")
                return True
            else:
                print("❌ Failed to install Python dependencies")
                print(f"Error: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False

    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        print("Checking FFmpeg installation...")

        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            print(f"✅ FFmpeg found at: {ffmpeg_path}")

            # Check FFmpeg version
            try:
                result = subprocess.run(['ffmpeg', '-version'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    print(f"   {version_line}")
                    return True
            except Exception as e:
                print(f"   Warning: Could not get FFmpeg version: {e}")
                return True
        else:
            print("❌ FFmpeg not found")
            return False

    def install_ffmpeg_instructions(self):
        """Provide FFmpeg installation instructions"""
        print("\nFFmpeg Installation Instructions:")
        print("-" * 40)

        if self.system == "darwin":  # macOS
            print("For macOS:")
            print("1. Install Homebrew if not already installed:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            print("2. Install FFmpeg:")
            print("   brew install ffmpeg")

        elif self.system == "linux":
            print("For Ubuntu/Debian:")
            print("   sudo apt update && sudo apt install ffmpeg")
            print()
            print("For CentOS/RHEL/Fedora:")
            print("   sudo dnf install ffmpeg")
            print("   # or")
            print("   sudo yum install ffmpeg")

        elif self.system == "windows":
            print("For Windows:")
            print("1. Download FFmpeg from: https://ffmpeg.org/download.html")
            print("2. Extract to a folder (e.g., C:\\ffmpeg)")
            print("3. Add C:\\ffmpeg\\bin to your PATH environment variable")
            print("4. Restart your command prompt/terminal")

        else:
            print("Please visit https://ffmpeg.org/download.html for installation instructions")

    def test_installation(self):
        """Test the installation by importing modules"""
        print("\nTesting installation...")

        # Test PIL/Pillow
        try:
            from PIL import Image
            print("✅ Pillow (PIL) import successful")
        except ImportError as e:
            print(f"❌ Pillow (PIL) import failed: {e}")
            return False

        # Test our modules
        try:
            sys.path.insert(0, str(self.script_dir))
            from image_converter import ImageConverter
            from video_converter import VideoConverter
            print("✅ Media converter modules import successful")
        except ImportError as e:
            print(f"❌ Media converter modules import failed: {e}")
            return False

        # Test basic functionality
        try:
            img_converter = ImageConverter()
            vid_converter = VideoConverter()

            # Test image converter
            formats = img_converter.get_supported_formats()
            if formats and 'input' in formats and 'output' in formats:
                print("✅ Image converter functionality test passed")
            else:
                print("❌ Image converter functionality test failed")
                return False

            # Test video converter (just check if FFmpeg is available)
            if vid_converter._check_dependencies():
                print("✅ Video converter functionality test passed")
            else:
                print("⚠️  Video converter test: FFmpeg not available (video features disabled)")

        except Exception as e:
            print(f"❌ Functionality test failed: {e}")
            return False

        return True

    def create_sample_files(self):
        """Create sample files for testing"""
        print("\nCreating sample files for testing...")

        try:
            from PIL import Image, ImageDraw

            # Create a sample image
            sample_image_path = self.script_dir / "sample_image.jpg"
            img = Image.new('RGB', (800, 600), color='lightblue')
            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 50, 750, 550], outline='navy', width=3)
            draw.text((100, 100), "Sample Image for Testing", fill='navy')
            img.save(sample_image_path, 'JPEG', quality=95)
            print(f"✅ Created sample image: {sample_image_path}")

        except Exception as e:
            print(f"❌ Could not create sample image: {e}")

    def create_launcher_script(self):
        """Create a launcher script for easy access"""
        print("\nCreating launcher script...")

        if self.system == "windows":
            launcher_path = self.script_dir / "media_converter.bat"
            launcher_content = f"""@echo off
cd /d "{self.script_dir}"
python media_converter.py %*
"""
        else:
            launcher_path = self.script_dir / "media_converter.sh"
            launcher_content = f"""#!/bin/bash
cd "{self.script_dir}"
python3 media_converter.py "$@"
"""

        try:
            with open(launcher_path, 'w') as f:
                f.write(launcher_content)

            if self.system != "windows":
                os.chmod(launcher_path, 0o755)  # Make executable

            print(f"✅ Created launcher script: {launcher_path}")

        except Exception as e:
            print(f"❌ Could not create launcher script: {e}")

    def print_usage_instructions(self):
        """Print usage instructions"""
        print("\n" + "=" * 60)
        print("SETUP COMPLETE!")
        print("=" * 60)
        print()
        print("Usage Examples:")
        print("-" * 20)
        print()
        print("Image Conversion:")
        print(f"  cd {self.script_dir}")
        print("  python media_converter.py image sample.jpg --format webp --quality 80")
        print("  python media_converter.py image *.jpg --compress --quality 75")
        print()
        print("Video Conversion (requires FFmpeg):")
        print("  python media_converter.py video sample.mp4 --quality medium --compress")
        print("  python media_converter.py video input.avi --format mp4 --resolution 1920x1080")
        print()
        print("Batch Processing:")
        print("  python media_converter.py image *.jpg --batch --format webp --output converted/")
        print()
        print("For more options:")
        print("  python media_converter.py --help")
        print("  python media_converter.py video --help")
        print("  python media_converter.py image --help")
        print()
        print("Example Scripts:")
        print("  python examples.py  # Run demonstration examples")

    def run_setup(self):
        """Run the complete setup process"""
        self.print_header()

        success = True

        # Check Python version
        if not self.check_python_version():
            success = False
            return success

        # Check pip
        if not self.check_pip():
            success = False
            return success

        # Install Python dependencies
        if not self.install_python_dependencies():
            success = False
            print("\n⚠️  Python dependency installation failed.")
            print("You may need to install them manually:")
            print("  pip install Pillow tqdm")

        # Check FFmpeg
        ffmpeg_available = self.check_ffmpeg()
        if not ffmpeg_available:
            print("\n⚠️  FFmpeg not found - video conversion features will be disabled")
            self.install_ffmpeg_instructions()

        # Test installation
        if success and self.test_installation():
            print("\n✅ Installation test passed!")

            # Create sample files
            self.create_sample_files()

            # Create launcher script
            self.create_launcher_script()

            # Print usage instructions
            self.print_usage_instructions()

        else:
            print("\n❌ Installation test failed!")
            success = False

        return success


def main():
    """Main setup function"""
    try:
        setup = MediaConverterSetup()
        success = setup.run_setup()

        if success:
            print(f"\n🎉 Setup completed successfully!")
            sys.exit(0)
        else:
            print(f"\n💥 Setup completed with errors!")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
