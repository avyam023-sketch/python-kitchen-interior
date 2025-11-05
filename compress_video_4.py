"""
Compress python kitchen video 4 for web use
"""
import subprocess
import sys
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def compress_video_ffmpeg(input_path, output_path):
    """Compress video using ffmpeg"""
    # Web-optimized compression settings:
    # - Codec: H.264 (compatible with all browsers)
    # - CRF: 28 (good quality/size balance for web)
    # - Preset: medium (good balance of speed/compression)
    # - Max resolution: 1920x1080 (Full HD)
    cmd = [
        'ffmpeg',
        '-i', str(input_path),
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '28',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',  # Web optimization
        '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease',
        '-y',  # Overwrite output file
        str(output_path)
    ]
    
    print(f"Compressing {input_path.name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error compressing video:")
        print(result.stderr)
        return False
    
    print(f"[OK] Compressed video saved to {output_path.name}")
    
    # Show file sizes
    original_size = input_path.stat().st_size / (1024 * 1024)  # MB
    compressed_size = output_path.stat().st_size / (1024 * 1024)  # MB
    reduction = (1 - compressed_size / original_size) * 100
    
    print(f"  Original size: {original_size:.2f} MB")
    print(f"  Compressed size: {compressed_size:.2f} MB")
    print(f"  Reduction: {reduction:.1f}%")
    
    return True

def compress_video_moviepy(input_path, output_path):
    """Compress video using moviepy as fallback"""
    try:
        # Import moviepy (v2.x uses direct imports)
        from moviepy import VideoFileClip
        
        print(f"Compressing {input_path.name} using moviepy...")
        
        clip = VideoFileClip(str(input_path))
        
        # Resize if too large (max 1920x1080)
        if clip.w > 1920 or clip.h > 1080:
            clip = clip.resize(height=1080) if clip.h > clip.w else clip.resize(width=1920)
        
        # Write compressed video with more aggressive settings
        clip.write_videofile(
            str(output_path),
            codec='libx264',
            bitrate='1500k',  # Lower bitrate for better compression
            audio_codec='aac',
            audio_bitrate='96k',  # Lower audio bitrate
            preset='medium',
            threads=4,
            logger=None,  # Suppress verbose output
            ffmpeg_params=['-crf', '28']  # Constant Rate Factor for better compression
        )
        
        clip.close()
        
        # Show file sizes
        original_size = input_path.stat().st_size / (1024 * 1024)  # MB
        compressed_size = output_path.stat().st_size / (1024 * 1024)  # MB
        reduction = (1 - compressed_size / original_size) * 100
        
        print(f"[OK] Compressed video saved to {output_path.name}")
        print(f"  Original size: {original_size:.2f} MB")
        print(f"  Compressed size: {compressed_size:.2f} MB")
        print(f"  Reduction: {reduction:.1f}%")
        
        return True
        
    except ImportError as e:
        print(f"moviepy import error: {e}")
        print("Try: pip install moviepy")
        return False
    except Exception as e:
        print(f"Error compressing video: {e}")
        return False

def main():
    root = Path(__file__).parent
    input_file = root / "python kitchen video 4.mp4"
    output_file = root / "compressed_python_kitchen_video_4.mp4"
    
    if not input_file.exists():
        print(f"Error: {input_file.name} not found!")
        sys.exit(1)
    
    # Try ffmpeg first (preferred method)
    if check_ffmpeg():
        if compress_video_ffmpeg(input_file, output_file):
            print("\n[OK] Video compression complete!")
            return
    
    # Fallback to moviepy
    print("\nffmpeg not found, trying moviepy...")
    if compress_video_moviepy(input_file, output_file):
        print("\n[OK] Video compression complete!")
        return
    
    print("\n[ERROR] Video compression failed. Please install ffmpeg or moviepy:")
    print("  - ffmpeg: Download from https://ffmpeg.org/download.html")
    print("  - moviepy: pip install moviepy")
    sys.exit(1)

if __name__ == "__main__":
    main()

