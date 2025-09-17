#!/usr/bin/env python3
"""
Media Converter CLI Tool
A comprehensive video and image converter/compressor with class-based architecture
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional

try:
    from video_converter import VideoConverter
    from image_converter import ImageConverter
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from video_converter import VideoConverter
    from image_converter import ImageConverter


class MediaConverterCLI:
    """Main CLI interface for the media converter tool"""

    def __init__(self):
        self.video_converter = VideoConverter()
        self.image_converter = ImageConverter()

    def setup_parser(self) -> argparse.ArgumentParser:
        """Setup command line argument parser"""
        parser = argparse.ArgumentParser(
            description="Convert and compress videos and images",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Convert video to MP4 with compression
  python media_converter.py video input.mov --output output.mp4 --quality medium

  # Compress images in bulk
  python media_converter.py image *.jpg --compress --quality 85

  # Convert video with custom settings
  python media_converter.py video input.avi --output output.mp4 --resolution 1920x1080 --bitrate 2M

  # Batch convert images to WebP
  python media_converter.py image folder/*.png --format webp --output converted/
            """
        )

        subparsers = parser.add_subparsers(dest='media_type', help='Media type to process')

        # Video converter subcommand
        video_parser = subparsers.add_parser('video', help='Convert and compress videos')
        self._setup_video_parser(video_parser)

        # Image converter subcommand
        image_parser = subparsers.add_parser('image', help='Convert and compress images')
        self._setup_image_parser(image_parser)

        return parser

    def _setup_video_parser(self, parser: argparse.ArgumentParser):
        """Setup video-specific arguments"""
        parser.add_argument('input', help='Input video file(s)')
        parser.add_argument('-o', '--output', help='Output file path')
        parser.add_argument('-f', '--format', choices=['mp4', 'avi', 'mkv', 'webm', 'mov'],
                          default='mp4', help='Output video format')
        parser.add_argument('-q', '--quality', choices=['low', 'medium', 'high', 'lossless'],
                          default='medium', help='Compression quality')
        parser.add_argument('-r', '--resolution', help='Output resolution (e.g., 1920x1080, 1280x720)')
        parser.add_argument('-b', '--bitrate', help='Video bitrate (e.g., 2M, 1000k)')
        parser.add_argument('--fps', type=int, help='Frame rate')
        parser.add_argument('--compress', action='store_true', help='Enable compression')
        parser.add_argument('--start', help='Start time for clipping (HH:MM:SS)')
        parser.add_argument('--duration', help='Duration for clipping (HH:MM:SS)')
        parser.add_argument('--audio-codec', choices=['aac', 'mp3', 'opus', 'none'],
                          help='Audio codec (none to remove audio)')
        parser.add_argument('--video-codec', choices=['h264', 'h265', 'vp9', 'av1'],
                          help='Video codec')
        parser.add_argument('--preset', choices=['ultrafast', 'superfast', 'veryfast', 'faster',
                          'fast', 'medium', 'slow', 'slower', 'veryslow'],
                          default='medium', help='Encoding preset')
        parser.add_argument('--batch', action='store_true', help='Batch process multiple files')

    def _setup_image_parser(self, parser: argparse.ArgumentParser):
        """Setup image-specific arguments"""
        parser.add_argument('input', nargs='+', help='Input image file(s) or pattern')
        parser.add_argument('-o', '--output', help='Output file/directory path')
        parser.add_argument('-f', '--format', choices=['jpg', 'jpeg', 'png', 'webp', 'tiff', 'bmp'],
                          help='Output image format')
        parser.add_argument('-q', '--quality', type=int, default=85,
                          help='JPEG/WebP quality (1-100)')
        parser.add_argument('--compress', action='store_true', help='Enable compression')
        parser.add_argument('--resize', help='Resize image (e.g., 1920x1080, 50%%)')
        parser.add_argument('--optimize', action='store_true', help='Optimize file size')
        parser.add_argument('--progressive', action='store_true', help='Create progressive JPEG')
        parser.add_argument('--strip-metadata', action='store_true', help='Remove EXIF data')
        parser.add_argument('--watermark', help='Add watermark image')
        parser.add_argument('--batch', action='store_true', help='Batch process multiple files')

    def run(self, args: List[str] = None) -> int:
        """Main entry point"""
        parser = self.setup_parser()
        parsed_args = parser.parse_args(args)

        if not parsed_args.media_type:
            parser.print_help()
            return 1

        try:
            if parsed_args.media_type == 'video':
                return self._handle_video(parsed_args)
            elif parsed_args.media_type == 'image':
                return self._handle_image(parsed_args)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 1

        return 0

    def _handle_video(self, args) -> int:
        """Handle video conversion"""
        input_path = Path(args.input)

        if not input_path.exists():
            print(f"Error: Input file '{args.input}' not found")
            return 1

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.with_suffix(f'.{args.format}')
            if output_path == input_path:
                output_path = input_path.with_stem(f"{input_path.stem}_converted")

        print(f"Converting video: {input_path} -> {output_path}")

        # Build conversion options
        options = {
            'format': args.format,
            'quality': args.quality,
            'compress': args.compress,
            'preset': args.preset
        }

        if args.resolution:
            options['resolution'] = args.resolution
        if args.bitrate:
            options['bitrate'] = args.bitrate
        if args.fps:
            options['fps'] = args.fps
        if args.start:
            options['start_time'] = args.start
        if args.duration:
            options['duration'] = args.duration
        if args.audio_codec:
            options['audio_codec'] = args.audio_codec
        if args.video_codec:
            options['video_codec'] = args.video_codec

        success = self.video_converter.convert(str(input_path), str(output_path), **options)

        if success:
            print(f"✓ Video converted successfully: {output_path}")
            return 0
        else:
            print("✗ Video conversion failed")
            return 1

    def _handle_image(self, args) -> int:
        """Handle image conversion"""
        input_files = []

        # Expand input patterns
        for pattern in args.input:
            if '*' in pattern or '?' in pattern:
                from glob import glob
                input_files.extend(glob(pattern))
            else:
                input_files.append(pattern)

        if not input_files:
            print("Error: No input files found")
            return 1

        # Filter existing files
        existing_files = [f for f in input_files if Path(f).exists()]
        if not existing_files:
            print("Error: No valid input files found")
            return 1

        print(f"Processing {len(existing_files)} image(s)")

        success_count = 0

        for input_file in existing_files:
            input_path = Path(input_file)

            # Determine output path
            if args.output:
                output_path = Path(args.output)
                if output_path.is_dir() or len(existing_files) > 1:
                    # Output is directory or multiple files
                    output_path = output_path / input_path.name
                    if args.format:
                        output_path = output_path.with_suffix(f'.{args.format}')
            else:
                output_path = input_path
                if args.format:
                    output_path = input_path.with_suffix(f'.{args.format}')
                if output_path == input_path and (args.compress or args.resize or args.quality != 85):
                    output_path = input_path.with_stem(f"{input_path.stem}_converted")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            print(f"Processing: {input_path} -> {output_path}")

            # Build conversion options
            options = {
                'quality': args.quality,
                'compress': args.compress,
                'optimize': args.optimize,
                'progressive': args.progressive,
                'strip_metadata': args.strip_metadata
            }

            if args.format:
                options['format'] = args.format
            if args.resize:
                options['resize'] = args.resize
            if args.watermark:
                options['watermark'] = args.watermark

            success = self.image_converter.convert(str(input_path), str(output_path), **options)

            if success:
                print(f"  ✓ Converted successfully")
                success_count += 1
            else:
                print(f"  ✗ Conversion failed")

        print(f"\nCompleted: {success_count}/{len(existing_files)} files processed successfully")
        return 0 if success_count > 0 else 1


def main():
    """Main entry point"""
    cli = MediaConverterCLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
