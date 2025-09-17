# Media Converter CLI Tool

A powerful, class-based Python CLI tool for converting and compressing videos and images with support for batch processing, various formats, and quality presets.

## Features

### Video Processing
- Convert between multiple formats (MP4, AVI, MKV, WebM, MOV)
- Compress videos with quality presets (low, medium, high, lossless)
- Resize videos to specific resolutions
- Adjust bitrate, frame rate, and codecs
- Extract audio from videos
- Create thumbnails from videos
- Clip videos (start time and duration)
- Batch processing support

### Image Processing
- Convert between multiple formats (JPEG, PNG, WebP, TIFF, BMP)
- Compress images with quality control
- Resize images (absolute size, percentage, or aspect ratio)
- Strip EXIF metadata
- Add watermarks
- Apply filters (sharpen, blur, auto-enhance)
- Create thumbnails
- Batch processing support

## Installation

### Prerequisites

**For Video Processing:**
- FFmpeg must be installed on your system
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - Windows: Download from https://ffmpeg.org/download.html

**For Image Processing:**
- Python 3.7 or higher

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Pillow>=10.0.0 tqdm>=4.65.0
```

## Usage

### Basic Syntax

```bash
python media_converter.py [video|image] [input] [options]
```

### Video Examples

#### Basic Video Conversion
```bash
# Convert MOV to MP4
python media_converter.py video input.mov --output output.mp4

# Compress video with medium quality
python media_converter.py video large_video.mp4 --compress --quality medium

# Convert with custom resolution and bitrate
python media_converter.py video input.avi --resolution 1920x1080 --bitrate 2M
```

#### Advanced Video Processing
```bash
# Convert with specific codec and preset
python media_converter.py video input.mkv --video-codec h265 --preset slow

# Clip video (start at 30 seconds, duration 60 seconds)
python media_converter.py video input.mp4 --start 00:00:30 --duration 00:01:00

# Remove audio from video
python media_converter.py video input.mp4 --audio-codec none

# Convert to WebM with VP9 codec
python media_converter.py video input.mp4 --format webm --video-codec vp9
```

### Image Examples

#### Basic Image Conversion
```bash
# Convert PNG to JPEG with 85% quality
python media_converter.py image input.png --format jpg --quality 85

# Compress JPEG images
python media_converter.py image *.jpg --compress --quality 75

# Convert to WebP format
python media_converter.py image image.jpg --format webp --quality 80
```

#### Advanced Image Processing
```bash
# Resize image to specific dimensions
python media_converter.py image input.jpg --resize 1920x1080

# Resize by percentage
python media_converter.py image input.jpg --resize 50%

# Batch convert with watermark
python media_converter.py image *.jpg --format webp --watermark logo.png --output converted/

# Strip EXIF data and optimize
python media_converter.py image photos/*.jpg --strip-metadata --optimize
```

### Batch Processing

#### Process Multiple Videos
```bash
# Convert all videos in a folder
python media_converter.py video folder/*.mp4 --batch --quality high --output converted_videos/
```

#### Process Multiple Images
```bash
# Convert all images with specific settings
python media_converter.py image photos/*.jpg --batch --format webp --quality 80 --resize 1920x1080
```

## Command Line Options

### Video Options

| Option | Description | Example |
|--------|-------------|---------|
| `-o, --output` | Output file path | `--output result.mp4` |
| `-f, --format` | Output format | `--format mp4` |
| `-q, --quality` | Quality preset | `--quality high` |
| `-r, --resolution` | Output resolution | `--resolution 1920x1080` |
| `-b, --bitrate` | Video bitrate | `--bitrate 2M` |
| `--fps` | Frame rate | `--fps 30` |
| `--compress` | Enable compression | `--compress` |
| `--start` | Start time for clipping | `--start 00:01:30` |
| `--duration` | Duration for clipping | `--duration 00:02:00` |
| `--audio-codec` | Audio codec | `--audio-codec aac` |
| `--video-codec` | Video codec | `--video-codec h264` |
| `--preset` | Encoding preset | `--preset slow` |

### Image Options

| Option | Description | Example |
|--------|-------------|---------|
| `-o, --output` | Output file/directory | `--output converted/` |
| `-f, --format` | Output format | `--format webp` |
| `-q, --quality` | JPEG/WebP quality | `--quality 85` |
| `--compress` | Enable compression | `--compress` |
| `--resize` | Resize specification | `--resize 1920x1080` |
| `--optimize` | Optimize file size | `--optimize` |
| `--progressive` | Progressive JPEG | `--progressive` |
| `--strip-metadata` | Remove EXIF data | `--strip-metadata` |
| `--watermark` | Watermark image | `--watermark logo.png` |

## Quality Presets

### Video Quality Presets
- **low**: CRF 28, fast preset (smaller files, lower quality)
- **medium**: CRF 23, medium preset (balanced)
- **high**: CRF 18, slow preset (larger files, higher quality)
- **lossless**: CRF 0, veryslow preset (largest files, no quality loss)

### Image Quality Settings
- **low**: Quality 60
- **medium**: Quality 85
- **high**: Quality 95
- **maximum**: Quality 100

## Supported Formats

### Video Formats
- **Input**: Most formats supported by FFmpeg (MP4, AVI, MOV, MKV, WMV, FLV, etc.)
- **Output**: MP4, AVI, MKV, WebM, MOV

### Image Formats
- **Input**: JPEG, PNG, BMP, TIFF, WebP, GIF, ICO, PPM, PGM, PBM
- **Output**: JPEG, PNG, WebP, TIFF, BMP, GIF, ICO

## Programming Usage

You can also use the classes directly in your Python code:

### VideoConverter Class

```python
from video_converter import VideoConverter

converter = VideoConverter()

# Basic conversion
converter.convert('input.mov', 'output.mp4', quality='high')

# Advanced conversion
converter.convert(
    'input.avi', 
    'output.mp4',
    resolution='1920x1080',
    bitrate='2M',
    video_codec='h265',
    quality='high'
)

# Batch conversion
files = ['video1.mp4', 'video2.avi']
results = converter.batch_convert(files, 'output_dir/', quality='medium')
```

### ImageConverter Class

```python
from image_converter import ImageConverter

converter = ImageConverter()

# Basic conversion
converter.convert('input.png', 'output.jpg', quality=85)

# Advanced conversion
converter.convert(
    'input.jpg',
    'output.webp',
    format='webp',
    quality=80,
    resize='1920x1080',
    optimize=True,
    strip_metadata=True
)

# Batch conversion
files = ['image1.jpg', 'image2.png']
results = converter.batch_convert(files, 'output_dir/', format='webp', quality=80)
```

## Performance Tips

1. **Video Encoding**: Use appropriate presets - faster presets for quick tests, slower presets for final output
2. **Batch Processing**: Process multiple files in one command rather than individual conversions
3. **Quality Settings**: Use medium quality for most use cases - high and lossless significantly increase file size
4. **Image Optimization**: Enable `--optimize` flag for better compression without quality loss
5. **Resolution**: Downscale videos/images to reduce file size significantly

## Troubleshooting

### Common Issues

**FFmpeg not found**
```
Error: FFmpeg not found. Please install FFmpeg
```
Solution: Install FFmpeg using your package manager or download from the official website.

**Permission denied**
```
Error: Permission denied
```
Solution: Ensure you have write permissions to the output directory.

**Unsupported format**
```
Error: Unsupported input format '.xyz'
```
Solution: Check the supported formats list or convert the file to a supported format first.

**Out of memory**
```
Error: Cannot allocate memory
```
Solution: Reduce image resolution or video bitrate, or process files in smaller batches.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v1.0.0 (Current)
- Initial release
- Video conversion with FFmpeg
- Image conversion with Pillow
- Batch processing support
- CLI interface with comprehensive options
- Quality presets and format support