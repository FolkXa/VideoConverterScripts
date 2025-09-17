# Installation and Getting Started Guide

## Media Converter CLI Tool

A powerful Python-based command-line tool for converting and compressing videos and images with class-based architecture.

## Quick Start

### 1. Check Prerequisites

**System Requirements:**
- Python 3.7 or higher
- macOS, Linux, or Windows

**For Video Processing (Optional):**
- FFmpeg (for video conversion features)

### 2. Install Dependencies

```bash
# Navigate to the scripts directory
cd scripts

# Install Python dependencies
pip install -r requirements.txt
```

**Manual installation if requirements.txt is not available:**
```bash
pip install Pillow>=10.0.0 tqdm>=4.65.0
```

### 3. Install FFmpeg (Optional - For Video Features)

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to a folder (e.g., C:\ffmpeg)
3. Add C:\ffmpeg\bin to your PATH environment variable
4. Restart your command prompt

### 4. Verify Installation

```bash
# Run the test suite
python3 test_converter.py

# Check if everything is working
python3 media_converter.py --help
```

## Basic Usage

### Image Conversion Examples

```bash
# Convert JPEG to WebP with compression
python3 media_converter.py image photo.jpg --format webp --quality 80

# Batch compress all JPEG files
python3 media_converter.py image *.jpg --compress --quality 75

# Resize and convert
python3 media_converter.py image large_image.png --resize 1920x1080 --format jpg

# Strip metadata and optimize
python3 media_converter.py image photo.jpg --strip-metadata --optimize
```

### Video Conversion Examples (Requires FFmpeg)

```bash
# Convert video with medium compression
python3 media_converter.py video input.mov --format mp4 --quality medium

# Resize video and compress
python3 media_converter.py video large_video.avi --resolution 1280x720 --compress

# Extract audio from video
python3 media_converter.py video movie.mp4 --audio-codec mp3 --output audio.mp3
```

### Using the Convenience Script

```bash
# Make the script executable (Unix/Linux/macOS)
chmod +x convert

# Use shortcuts
./convert img photo.jpg --format webp --quality 80
./convert vid video.mp4 --quality medium --compress
```

## Advanced Usage

### Batch Processing

```bash
# Process multiple images
python3 media_converter.py image folder/*.jpg --batch --format webp --output converted/

# Convert all videos in a directory
python3 media_converter.py video *.mp4 --batch --quality high --output processed/
```

### Custom Settings

```bash
# Image with watermark
python3 media_converter.py image photo.jpg --watermark logo.png --format png

# Video with specific codec and bitrate
python3 media_converter.py video input.avi --video-codec h265 --bitrate 2M --preset slow
```

## Programmatic Usage

You can also use the classes directly in your Python code:

```python
from image_converter import ImageConverter
from video_converter import VideoConverter

# Image conversion
img_converter = ImageConverter()
img_converter.convert('input.jpg', 'output.webp', format='webp', quality=80)

# Video conversion
vid_converter = VideoConverter()
vid_converter.convert('input.mp4', 'output.mp4', quality='high', resolution='1920x1080')
```

## File Structure

```
scripts/
├── media_converter.py      # Main CLI application
├── image_converter.py      # Image processing class
├── video_converter.py      # Video processing class
├── convert                 # Convenience shell script
├── test_converter.py       # Test suite
├── examples.py            # Usage examples
├── setup.py               # Setup utility
├── requirements.txt       # Python dependencies
├── README.md             # Comprehensive documentation
└── INSTALL.md            # This file
```

## Configuration Options

### Image Quality Presets
- **low**: 60% quality (smallest files)
- **medium**: 85% quality (balanced)
- **high**: 95% quality (larger files)
- **maximum**: 100% quality (largest files)

### Video Quality Presets
- **low**: CRF 28, fast encoding
- **medium**: CRF 23, balanced
- **high**: CRF 18, slow encoding
- **lossless**: CRF 0, very slow encoding

### Supported Formats

**Images:**
- Input: JPEG, PNG, BMP, TIFF, WebP, GIF, ICO, PPM, PGM, PBM
- Output: JPEG, PNG, WebP, TIFF, BMP, GIF, ICO

**Videos:**
- Input: Most formats supported by FFmpeg
- Output: MP4, AVI, MKV, WebM, MOV

## Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. "FFmpeg not found" (for video features)**
```bash
# Check if FFmpeg is installed
ffmpeg -version

# If not installed, follow the FFmpeg installation instructions above
```

**3. Permission denied errors**
```bash
# Make scripts executable
chmod +x convert
chmod +x media_converter.py
```

**4. "Python not found"**
```bash
# Try different Python commands
python3 --version
python --version

# Use the one that works in your commands
```

### Performance Tips

1. **Use appropriate quality settings** - Higher quality = larger files
2. **Batch process when possible** - More efficient than individual conversions
3. **Consider output format** - WebP often provides better compression than JPEG
4. **Resize before converting** - Reduces processing time and file size

## Getting Help

```bash
# General help
python3 media_converter.py --help

# Image-specific help
python3 media_converter.py image --help

# Video-specific help
python3 media_converter.py video --help

# Run examples
python3 examples.py
```

## Uninstallation

To remove the tool:

```bash
# Remove Python dependencies (optional)
pip uninstall Pillow tqdm

# Remove the scripts directory
rm -rf /path/to/scripts
```

## Support and Contributing

This is a standalone tool designed for personal use. Feel free to modify and extend it according to your needs.

### Development Setup

```bash
# Install development dependencies
pip install pytest black flake8

# Run tests
python3 test_converter.py

# Format code
black *.py
```

## License

This project is provided as-is for personal and educational use.