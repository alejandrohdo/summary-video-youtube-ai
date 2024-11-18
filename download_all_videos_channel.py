import os
from datetime import datetime
import yt_dlp
import argparse


def download_youtube_channel_mp3(channel_url, output_dir='downloads'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'extract_flat': False,
        # 'outtmpl': f'{output_dir}/%(playlist_index)s-%(playlist_title)s/%(title)s.%(ext)s',
        'outtmpl': f'{output_dir}/%(playlist_title)s/%(title)s.%(ext)s',
        'quiet': False,
        'noplaylist': False,
        'verbose': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Descargando videos del canal: {channel_url}")
        ydl.download([channel_url])


def parse_arguments():
    """Parse command-line arguments for video URL and output path."""
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = f"youtube_downloads_audio_{current_date}"
    parser = argparse.ArgumentParser(description="Descarga todos los video de un canal de youtube, en formato mp3")
    parser.add_argument('--channel_url', '-channel_url', type=str, help='URL del canal de YouTube, ejem: https://www.youtube.com/@herostartup4493', required=True)
    parser.add_argument('--output', '-output', type=str, default=default_output, help='Ruta de salida para el audio descargado')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    download_youtube_channel_mp3(args.channel_url, args.output)
    print(f"Descarga completa. Los archivos están organizados en '{args.output}'")
