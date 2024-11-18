from openai import OpenAI
import os
from datetime import datetime
import whisper
import argparse
import yt_dlp as youtube_dl

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def split_text(text, max_tokens=1024):
    """Split the text into chunks of up to 1024 tokens."""
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield ' '.join(words[i:i + max_tokens])


def clean_text(text):
    """Clean and preprocess the text by removing unnecessary characters and repetitions."""
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join([word for i, word in enumerate(text.split()) if i == 0 or word != text[i - 1]])
    return text


def summarize_text(file_path):
    """Summarize the text using a local model like facebook/bart-large-cnn and save the summary."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    text = clean_text(text)
    summaries = []
    for chunk in split_text(text, max_tokens=450):
        summary = summarizer(chunk, max_length=250, min_length=50, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    combined_summary = ' '.join(summaries)
    os.makedirs("data/text-summaries", exist_ok=True)
    summary_file_path = file_path.replace("text-original", "text-summaries").replace("original", "summary")
    with open(summary_file_path, "w", encoding="utf-8") as file:
        file.write(combined_summary)
    print(f"Resumen completo guardado en: {summary_file_path}")
    return summary_file_path


def summarize_with_chatgpt(file_path):
    """Summarize the text from a transcription file using ChatGPT and save the summary."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    text = clean_text(text)
    messages = [
        {"role": "system", "content": "Eres un asistente experto en resúmenes de texto."},
        {"role": "user", "content": f"De este texto, haz un resumen con los puntos más importantes:\n\n{text}"}
    ]
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    summary = completion.choices[0].message.content.strip()
    os.makedirs("data/text-summaries", exist_ok=True)
    summary_file_path = file_path.replace("text-original", "text-summaries").replace("original", "summary")
    with open(summary_file_path, "w", encoding="utf-8") as file:
        file.write(summary)
    print(f"Resumen completo guardado en: {summary_file_path}")
    return summary_file_path


def download_youtube_video(video_url, output_path='audio.mp3'):
    """Download a YouTube video and save it as an MP3 file."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Video descargado en: {output_path}")
        return output_path + '.mp3'
    except Exception as e:
        print('Error de descarga de video>', e)


def transcribe_audio(audio_path, model_name='base'):
    """Transcribe audio from a file and save the transcription as text."""
    print('Iniciando transcripción del audio:', audio_path)
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    transcript = result['text']
    print(f"Transcripción completa:\n{transcript[:500]}...")
    os.makedirs("data/text-original", exist_ok=True)
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_file_path = f"data/text-original/original_{current_date}.txt"
    with open(original_file_path, "w", encoding="utf-8") as file:
        file.write(transcript)
    print(f"Transcripción guardada en: {original_file_path}")
    return original_file_path


def parse_arguments():
    """Parse command-line arguments for video URL and output path."""
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = f"audio/audio_{current_date}"
    parser = argparse.ArgumentParser(description="Script para descargar, transcribir y resumir un video de YouTube.")
    parser.add_argument('--url', '-url', type=str, help='URL del video de YouTube', required=True)
    parser.add_argument('--output', '-output', type=str, default=default_output, help='Ruta de salida para el audio descargado')
    return parser.parse_args()


def main():
    """Main function to execute video download, transcription, and summarization."""
    args = parse_arguments()
    video_url = args.url
    output_path = args.output
    audio_path = download_youtube_video(video_url, output_path)
    if audio_path:
        transcription_path = transcribe_audio(audio_path)
        path_summary = summarize_with_chatgpt(transcription_path)
        print('path de resumen===>', path_summary)
    else:
        print("No se pudo descargar el video. Verifica la URL y vuelve a intentarlo.")
    

if __name__ == '__main__':
    main()
