# Media Converter CLI Tool - Project Overview

## 🎯 Purpose

A comprehensive, class-based Python CLI tool for converting and compressing videos and images. Designed for personal scripts with professional-grade functionality.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test installation
python3 test_converter.py

# Convert image
python3 media_converter.py image photo.jpg --format webp --quality 80

# Convert video (requires FFmpeg)
python3 media_converter.py video video.mp4 --quality medium --compress

# Use convenience script
./convert img photo.jpg --format webp --quality 80
```

## 📁 Project Structure

```
scripts/
├── 🎯 Core Application
│   ├── media_converter.py      # Main CLI application
│   ├── image_converter.py      # Image processing class
│   └── video_converter.py      # Video processing class
├── 🛠️ Utilities
│   ├── convert                 # Convenience shell script
│   ├── setup.py               # Installation helper
│   └── test_converter.py       # Test suite
├── 📚 Documentation
│   ├── README.md              # Comprehensive guide
│   ├── INSTALL.md             # Installation instructions
│   └── OVERVIEW.md            # This file
├── 🧪 Examples
│   └── examples.py            # Usage demonstrations
└── 📦 Configuration
    └── requirements.txt       # Python dependencies
```

## ⚡ Key Features

### Image Processing
- ✅ Format conversion (JPEG, PNG, WebP, TIFF, BMP, GIF)
- ✅ Quality-based compression
- ✅ Resize (absolute, percentage, aspect ratio)
- ✅ Metadata stripping (EXIF removal)
- ✅ Watermark addition
- ✅ Optimization algorithms
- ✅ Batch processing

### Video Processing
- ✅ Format conversion (MP4, AVI, MKV, WebM, MOV)
- ✅ Quality presets (low/medium/high/lossless)
- ✅ Resolution scaling
- ✅ Codec selection (H.264, H.265, VP9, AV1)
- ✅ Bitrate control
- ✅ Audio extraction/removal
- ✅ Video clipping (start/duration)
- ✅ Batch processing

## 🎨 Architecture

### Class-Based Design
```python
VideoConverter
├── convert()           # Main conversion method
├── compress()          # Compression wrapper
├── resize()            # Resolution change
├── extract_audio()     # Audio extraction
└── batch_convert()     # Multiple files

ImageConverter
├── convert()           # Main conversion method
├── compress()          # Compression wrapper
├── resize()            # Size change
├── create_thumbnail()  # Thumbnail generation
└── batch_convert()     # Multiple files

MediaConverterCLI
├── setup_parser()      # Argument parsing
├── run()              # Main entry point
├── _handle_video()    # Video processing
└── _handle_image()    # Image processing
```

### Dependencies
- **Required**: `Pillow` (image processing)
- **Optional**: `FFmpeg` (video processing)
- **Enhancement**: `tqdm` (progress bars)

## 🔧 Usage Patterns

### Command Line Interface
```bash
# Basic syntax
python3 media_converter.py [video|image] [input] [options]

# Image examples
python3 media_converter.py image photo.jpg --format webp --quality 80
python3 media_converter.py image *.jpg --compress --batch
python3 media_converter.py image large.png --resize 50% --optimize

# Video examples (requires FFmpeg)
python3 media_converter.py video input.mov --format mp4 --quality high
python3 media_converter.py video video.avi --resolution 1920x1080 --bitrate 2M
python3 media_converter.py video movie.mp4 --start 00:01:30 --duration 00:02:00
```

### Programmatic Usage
```python
from image_converter import ImageConverter
from video_converter import VideoConverter

# Image processing
img = ImageConverter()
img.convert('input.jpg', 'output.webp', format='webp', quality=80)
img.batch_convert(['img1.jpg', 'img2.png'], 'output/', format='webp')

# Video processing
vid = VideoConverter()
vid.convert('input.mp4', 'output.mp4', quality='high', resolution='1920x1080')
vid.extract_audio('movie.mp4', 'audio.mp3')
```

## 🎛️ Quality Presets

### Image Quality
- **low**: 60% (aggressive compression)
- **medium**: 85% (balanced - default)
- **high**: 95% (minimal compression)
- **maximum**: 100% (lossless for supported formats)

### Video Quality
- **low**: CRF 28, fast preset
- **medium**: CRF 23, medium preset (default)
- **high**: CRF 18, slow preset
- **lossless**: CRF 0, veryslow preset

## 📋 Common Use Cases

### Daily Workflows
```bash
# Compress photos for web
./convert img photos/*.jpg --format webp --quality 75 --output web/

# Resize screenshots
./convert img screenshot.png --resize 1920x1080 --format jpg

# Convert videos for sharing
./convert vid recording.mov --format mp4 --quality medium --resolution 1280x720

# Create thumbnails
python3 media_converter.py image video-frame.png --resize 200x150 --format jpg
```

### Batch Operations
```bash
# Process entire directories
python3 media_converter.py image photos/*.jpg --batch --format webp --compress
python3 media_converter.py video videos/*.avi --batch --format mp4 --quality medium
```

## 🔍 Testing & Verification

```bash
# Run comprehensive tests
python3 test_converter.py

# Check specific functionality
python3 examples.py

# Verify installation
python3 setup.py
```

## 🚨 Error Handling

The tool includes comprehensive error handling for:
- Missing input files
- Unsupported formats
- Dependency issues (FFmpeg/Pillow)
- Invalid parameters
- File permission problems
- Insufficient disk space

## 📈 Performance Considerations

### Optimization Tips
1. **Batch processing** is more efficient than individual files
2. **Resize before format conversion** for faster processing
3. **Use appropriate quality settings** - higher quality = longer processing time
4. **WebP format** often provides better compression than JPEG
5. **Video presets**: fast for testing, slow/slower for final output

### Resource Usage
- **Memory**: Scales with image resolution and video length
- **CPU**: Multi-threaded where supported (FFmpeg)
- **Disk**: Temporary files created during processing

## 🔄 Extensibility

The class-based architecture makes it easy to:
- Add new formats
- Implement custom filters
- Create new quality presets
- Extend CLI options
- Add progress callbacks

## 📞 Support & Maintenance

### Self-Diagnostics
- Built-in dependency checking
- Format compatibility verification
- Error reporting with suggestions
- Test suite for validation

### Customization Points
- Quality presets in converter classes
- CLI argument definitions
- Output filename patterns
- Error message formatting

## 🎉 Success Metrics

After installation, you should be able to:
✅ Convert images between formats with compression
✅ Resize and optimize images
✅ Process multiple files in batch
✅ Convert videos (with FFmpeg installed)
✅ Use both CLI and programmatic interfaces
✅ Handle errors gracefully

---

**Ready to use!** Start with `python3 test_converter.py` to verify everything works, then explore the examples in `examples.py`.