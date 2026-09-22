from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5-20251001"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }

    if system:
        params["system"] = system 
    message = client.messages.create(**params)

    return message.content[0].text

# 1. Define your dynamic variables
question = "What is quantum computing? Answer in one sentence"

# 2. Use an f-string to inject the variable directly into the template
prompt = f"""
Act as an expert. Please answer the user's question:

{question}
"""

messages = []
add_user_message(messages, prompt)

result = chat(messages)
print(result)