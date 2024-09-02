from openai import OpenAI
import os
from datetime import datetime
import whisper
import argparse
import yt_dlp as youtube_dl

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Función para dividir el texto en fragmentos de hasta 1024 tokens
def split_text(text, max_tokens=1024):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield ' '.join(words[i:i + max_tokens])


# Función para limpiar el texto antes de resumir
def clean_text(text):
    # Remover caracteres innecesarios y limpiar el texto
    text = text.replace('\n', ' ').replace('\r', '')
    # Eliminar repeticiones y contenido irrelevante
    text = text.split()
    text = ' '.join([word for i, word in enumerate(text) if i == 0 or word != text[i - 1]])
    return text


# Función para resumir el texto desde un archivo de transcripción y guardar el resumen
def summarize_with_chatgpt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    text = clean_text(text)
    messages = [
        {"role": "system", "content": "Eres un asistente experto en resúmenes de texto."},
        {"role": "user", "content": f"De este texto, haz un resumen con los puntos más importantes:\n\n{text}"}
    ]

    # Solicitud de resumen a la API de ChatGPT
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Asegúrate de que este modelo esté disponible para tu cuenta
        messages=messages
    )

    # Obtener el contenido del resumen generado
    summary = completion.choices[0].message.content.strip()

    # Guardar el resumen generado en data/text-summaries
    os.makedirs("data/text-summaries", exist_ok=True)
    summary_file_path = file_path.replace("text-original", "text-summaries").replace("original", "summary")
    with open(summary_file_path, "w", encoding="utf-8") as file:
        file.write(summary)

    print(f"Resumen completo guardado en: {summary_file_path}")
    return summary_file_path



# Función para descargar el video de YouTube usando yt-dlp
def download_youtube_video(video_url, output_path='audio.mp3'):
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
        return output_path+'.mp3'
    except Exception as e:
        print('Error de descarga de video>', e)


# Función para transcribir el audio y guardar la transcripción en un archivo
def transcribe_audio(audio_path, model_name='base'):
    print('Iniciando transcripción del audio:', audio_path)
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    transcript = result['text']
    print(f"Transcripción completa:\n{transcript[:500]}...")  # Muestra las primeras 500 palabras

    # Crear directorio si no existe
    os.makedirs("data/text-original", exist_ok=True)
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_file_path = f"data/text-original/original_{current_date}.txt"

    # Guardar la transcripción en un archivo de texto
    with open(original_file_path, "w", encoding="utf-8") as file:
        file.write(transcript)

    print(f"Transcripción guardada en: {original_file_path}")
    return original_file_path

# Configuración de argumentos desde la terminal
def parse_arguments():
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = f"audio/audio_{current_date}"
    parser = argparse.ArgumentParser(description="Script para descargar, transcribir y resumir un video de YouTube.")
    parser.add_argument('--url', type=str, help='URL del video de YouTube', required=True)
    parser.add_argument('--output', type=str, default=default_output, help='Ruta de salida para el audio descargado')
    return parser.parse_args()

# Función principal
def main():
    args = parse_arguments()
    video_url = args.url
    output_path = args.output

    # Descargar el video
    audio_path = download_youtube_video(video_url, output_path)

    # Transcribir el audio
    if audio_path:
        transcription_path = transcribe_audio(audio_path)
        # Generar un resumen del texto transcrito
        #path_summary = summarize_text(transcription_path)
        path_summary = summarize_with_chatgpt(transcription_path)
        print('path de resumen===>', path_summary)
    else:
        print("No se pudo descargar el video. Verifica la URL y vuelve a intentarlo.")

if __name__ == '__main__':
    #main()
    # audio_path ='audio_20240901_184533.mp3'
    # transcription_path = transcribe_audio(audio_path)
    # Generar un resumen del texto transcrito
    path_summary = summarize_with_chatgpt('data/text-original/original_20240901_184953.txt')
    #print('path de resumen===>', path_summary)