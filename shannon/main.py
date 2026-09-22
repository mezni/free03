


from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5-20251001"

def add_user_message(messages, text):
    user_message = {"role":"user", "content":text}
    messages.append(user_message)

def add_assinstant_message(messages, text):
    assistant_message = {"role":"assistant", "content":text}
    messages.append(assistant_message)

def chat(messages):
    result = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages
    )
    print (result.content[0].text)
messages = []
add_user_message(messages,"What is quantum computing? Answer in one sentence")
chat(messages)