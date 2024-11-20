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
        {"role": "system", "content": "Eres un asistente experto en correcion de texto."},
        {"role": "user", "content": f"De este texto, haz una correcion de errores de gramatica, ortografia y de redaccion, ademas de mejorar la lectura, y que se mantenga el significado original:\n{text}"}
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


def transcribe_audio(audio_path, model_name='base', language='es'):
    """Transcribe audio from a file and save the transcription as text."""
    print('Iniciando transcripción del audio:', audio_path)
    model = whisper.load_model(model_name)
    transcription = model.transcribe(audio_path, language=language)
    transcript = transcription['text']
    print(f"Transcripción completa:\n{transcript[:500]}...")

    # Create the output directory within the same directory as the audio file
    base_dir = os.path.dirname(audio_path)
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Create the output path with the same name as the audio file, but with a .txt extension
    file_name = os.path.splitext(os.path.basename(audio_path))[0]  # Get the file name without extension
    original_file_path = os.path.join(output_dir, f"{file_name}.txt")

    with open(original_file_path, "w", encoding="utf-8") as file:
        file.write(transcript)
    print(f"Transcripción guardada en: {original_file_path}")
    return original_file_path


def parse_arguments():
    """Parse command-line arguments for video URL and output path."""
    parser = argparse.ArgumentParser(description="Script para procesar audios .mp3 descargados y convierte en texto, y opcionalnamente puede corregir el texto extraido.")
    parser.add_argument('--input', '-input', type=str, required=True, help='Ruta de entrada para el audio descargado')
    return parser.parse_args()


def process_directory(directory):
    """Process all audio files in the given directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp3', '.wav', '.m4a')):  # Add other audio file extensions if needed
                audio_path = os.path.join(root, file)
                transcribe_audio(audio_path)
                # Optionally summarize the transcription
                # path_summary = summarize_with_chatgpt(transcription_path)
                # print('path de resumen===>', path_summary)


def main():
    """Main function to execute transcription and summarization for all audio files in a directory."""
    args = parse_arguments()
    directory = args.input
    process_directory(directory)
    print("Procesamiento completo de todos los audios en el directorio.")


if __name__ == '__main__':
    main()
