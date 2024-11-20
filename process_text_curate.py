import os
from openai import OpenAI


def correct_text_with_openai(text):
    """Use OpenAI API to correct the text."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        {"role": "system", "content": "Eres un asistente experto en corrección de textos. Tu tarea es corregir errores gramaticales, ortográficos y de redacción, mejorando la lectura y manteniendo el significado original, sin agregar introducciones ni explicaciones."},
        {"role": "user", "content": f"""
        Corrige el siguiente texto aplicando los siguientes pasos:

        1. Convierte todo el texto a minúsculas para normalizarlo.
        2. Elimina caracteres especiales innecesarios (símbolos extraños o puntuación redundante).
        3. Reemplaza espacios múltiples por un único espacio.
        4. Corrige errores gramaticales, ortográficos y de redacción.
        5. Mejora la fluidez del texto, asegurándote de mantener el significado original.

        Devuelve únicamente el texto corregido:

        Texto a procesar:
        {text}
            """}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    corrected_text = completion.choices[0].message.content.strip()
    return corrected_text


def split_text_into_chunks(text, max_tokens=2048):
    """Split text into chunks that fit within the token limit."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def process_directory_for_correction(directory):
    """Process all text files in the given directory and its subdirectories for correction."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                
                # Split the text into chunks
                text_chunks = split_text_into_chunks(text)
                print(f"Text split into {len(text_chunks)} chunks.")
                corrected_chunks = []
                for i, chunk in enumerate(text_chunks):
                    print(f"Processing chunk {i + 1} of {len(text_chunks)}...")
                    corrected_chunk = correct_text_with_openai(chunk)
                    corrected_chunks.append(corrected_chunk)

                corrected_text = ' '.join(corrected_chunks)
                
                # Create the output_curate directory within the same directory as the output file
                output_curate_dir = root.replace("output", "output_curate")
                os.makedirs(output_curate_dir, exist_ok=True)
                corrected_file_path = os.path.join(output_curate_dir, file)
                with open(corrected_file_path, "w", encoding="utf-8") as f:
                    f.write(corrected_text)
                print(f"Texto corregido guardado en: {corrected_file_path}")


def main():
    """Main function to execute text correction for all text files in a directory."""
    import argparse
    parser = argparse.ArgumentParser(description="Script para corregir textos transcritos usando OpenAI API.")
    parser.add_argument('--input', '-input', type=str, required=True, help='Ruta de entrada para los textos transcritos')
    args = parser.parse_args()
    directory = args.input
    process_directory_for_correction(directory)
    print("Corrección completa de todos los textos en el directorio.")


if __name__ == '__main__':
    main()