from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "Eres un asistente útil"}
]

user_input = input("Tu: ")
messages.append({"role": "user", "content": user_input})

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)
print('respuestas:', completion.choices[0].message.content)
