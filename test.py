from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Set the Hugging Face token from environment
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    max_new_tokens=100,
    do_sample=False,
)
# 🧪 Run inference
response = llm.invoke("what is WASM")
print(response)
