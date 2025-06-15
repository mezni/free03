from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=token
)

prompt = "List the main telecom operators in Tunisia."

output = client.text_generation(prompt, max_new_tokens=150)
print(output)
