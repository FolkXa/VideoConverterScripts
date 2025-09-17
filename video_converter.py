#!/usr/bin/env python3
"""
Video Converter Class
Handles video conversion, compression, and manipulation using FFmpeg
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional, Union, Tuple
import json


class VideoConverter:
    """A class for converting and compressing videos using FFmpeg"""

    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        self.ffprobe_path = self._find_ffprobe()

        # Quality presets
        self.quality_presets = {
            'low': {'crf': 28, 'preset': 'fast'},
            'medium': {'crf': 23, 'preset': 'medium'},
            'high': {'crf': 18, 'preset': 'slow'},
            'lossless': {'crf': 0, 'preset': 'veryslow'}
        }

    def _find_ffmpeg(self) -> Optional[str]:
        """Find FFmpeg executable"""
        return shutil.which('ffmpeg')

    def _find_ffprobe(self) -> Optional[str]:
        """Find FFprobe executable"""
        return shutil.which('ffprobe')

    def _check_dependencies(self) -> bool:
        """Check if required dependencies are available"""
        if not self.ffmpeg_path:
            print("Error: FFmpeg not found. Please install FFmpeg:")
            print("  macOS: brew install ffmpeg")
            print("  Ubuntu/Debian: sudo apt install ffmpeg")
            print("  Windows: Download from https://ffmpeg.org/download.html")
            return False
        return True

    def get_video_info(self, input_path: str) -> Optional[Dict]:
        """Get video information using ffprobe"""
        if not self.ffprobe_path:
            print("Warning: ffprobe not available, cannot get video info")
            return None

        try:
            cmd = [
                self.ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                input_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error getting video info: {e}")
            return None

    def _parse_resolution(self, resolution: str) -> Tuple[int, int]:
        """Parse resolution string to width, height tuple"""
        if 'x' in resolution.lower():
            width, height = map(int, resolution.lower().split('x'))
            return width, height
        else:
            raise ValueError(f"Invalid resolution format: {resolution}")

    def _build_ffmpeg_command(self, input_path: str, output_path: str, **options) -> list:
        """Build FFmpeg command based on options"""
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg not available")

        cmd = [self.ffmpeg_path, '-i', input_path]

        # Add start time if specified
        if options.get('start_time'):
            cmd.extend(['-ss', options['start_time']])

        # Add duration if specified
        if options.get('duration'):
            cmd.extend(['-t', options['duration']])

        # Video codec
        video_codec = options.get('video_codec', 'h264')
        codec_map = {
            'h264': 'libx264',
            'h265': 'libx265',
            'vp9': 'libvpx-vp9',
            'av1': 'libaom-av1'
        }
        cmd.extend(['-c:v', codec_map.get(video_codec, 'libx264')])

        # Quality settings
        quality = options.get('quality', 'medium')
        if quality in self.quality_presets:
            preset_settings = self.quality_presets[quality]
            if video_codec != 'av1':  # AV1 doesn't use CRF the same way
                cmd.extend(['-crf', str(preset_settings['crf'])])
            cmd.extend(['-preset', preset_settings['preset']])

        # Bitrate (overrides CRF if specified)
        if options.get('bitrate'):
            cmd.extend(['-b:v', options['bitrate']])

        # Resolution
        if options.get('resolution'):
            width, height = self._parse_resolution(options['resolution'])
            cmd.extend(['-vf', f'scale={width}:{height}'])

        # Frame rate
        if options.get('fps'):
            cmd.extend(['-r', str(options['fps'])])

        # Audio codec
        audio_codec = options.get('audio_codec', 'aac')
        if audio_codec == 'none':
            cmd.extend(['-an'])  # No audio
        else:
            codec_map = {
                'aac': 'aac',
                'mp3': 'libmp3lame',
                'opus': 'libopus'
            }
            cmd.extend(['-c:a', codec_map.get(audio_codec, 'aac')])

        # Preset for encoding speed
        preset = options.get('preset', 'medium')
        if video_codec in ['h264', 'h265']:
            cmd.extend(['-preset', preset])

        # Output format
        output_format = options.get('format', 'mp4')
        if output_format == 'mp4':
            cmd.extend(['-movflags', '+faststart'])  # Optimize for streaming

        # Overwrite output file
        cmd.extend(['-y'])

        # Output file
        cmd.append(output_path)

        return cmd

    def convert(self, input_path: str, output_path: str, **options) -> bool:
        """
        Convert video with specified options

        Args:
            input_path: Path to input video file
            output_path: Path to output video file
            **options: Conversion options

        Returns:
            bool: True if successful, False otherwise
        """
        if not self._check_dependencies():
            return False

        if not Path(input_path).exists():
            print(f"Error: Input file '{input_path}' not found")
            return False

        try:
            # Create output directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            # Build and execute FFmpeg command
            cmd = self._build_ffmpeg_command(input_path, output_path, **options)

            print(f"Executing: {' '.join(cmd[:3])} ... {' '.join(cmd[-10:])}")

            # Run with progress if possible
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Monitor progress
            while True:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output and 'time=' in output:
                    # Extract and display progress
                    for part in output.split():
                        if part.startswith('time='):
                            time_str = part.split('=')[1]
                            print(f"\rProgress: {time_str}", end='', flush=True)

            process.wait()
            print()  # New line after progress

            if process.returncode == 0:
                # Verify output file was created and has size > 0
                output_file = Path(output_path)
                if output_file.exists() and output_file.stat().st_size > 0:
                    return True
                else:
                    print("Error: Output file was not created properly")
                    return False
            else:
                stderr_output = process.stderr.read() if process.stderr else "Unknown error"
                print(f"FFmpeg error: {stderr_output}")
                return False

        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def compress(self, input_path: str, output_path: str, quality: str = 'medium', **options) -> bool:
        """
        Compress video file

        Args:
            input_path: Path to input video
            output_path: Path to output video
            quality: Compression quality ('low', 'medium', 'high')
            **options: Additional options

        Returns:
            bool: True if successful, False otherwise
        """
        options['quality'] = quality
        options['compress'] = True
        return self.convert(input_path, output_path, **options)

    def resize(self, input_path: str, output_path: str, resolution: str, **options) -> bool:
        """
        Resize video

        Args:
            input_path: Path to input video
            output_path: Path to output video
            resolution: Target resolution (e.g., '1920x1080')
            **options: Additional options

        Returns:
            bool: True if successful, False otherwise
        """
        options['resolution'] = resolution
        return self.convert(input_path, output_path, **options)

    def extract_audio(self, input_path: str, output_path: str, audio_format: str = 'mp3') -> bool:
        """
        Extract audio from video

        Args:
            input_path: Path to input video
            output_path: Path to output audio file
            audio_format: Audio format ('mp3', 'aac', 'wav')

        Returns:
            bool: True if successful, False otherwise
        """
        if not self._check_dependencies():
            return False

        try:
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-vn',  # No video
                '-acodec', 'libmp3lame' if audio_format == 'mp3' else audio_format,
                '-y',
                output_path
            ]

            subprocess.run(cmd, check=True, capture_output=True)
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")
            return False

    def create_thumbnail(self, input_path: str, output_path: str, timestamp: str = '00:00:01') -> bool:
        """
        Create thumbnail from video

        Args:
            input_path: Path to input video
            output_path: Path to output image
            timestamp: Time position for thumbnail

        Returns:
            bool: True if successful, False otherwise
        """
        if not self._check_dependencies():
            return False

        try:
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-ss', timestamp,
                '-vframes', '1',
                '-y',
                output_path
            ]

            subprocess.run(cmd, check=True, capture_output=True)
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error creating thumbnail: {e}")
            return False

    def get_supported_formats(self) -> list:
        """Get list of supported output formats"""
        return ['mp4', 'avi', 'mkv', 'webm', 'mov', 'flv', 'm4v']

    def batch_convert(self, input_files: list, output_dir: str, **options) -> Dict[str, bool]:
        """
        Batch convert multiple video files

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
            output_format = options.get('format', 'mp4')
            output_file = output_path / f"{input_path.stem}.{output_format}"

            print(f"\nProcessing: {input_path.name}")
            results[input_file] = self.convert(str(input_path), str(output_file), **options)

        return results
