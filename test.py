from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

# Load Hugging Face token from .env file
load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    task="text-generation",
    max_new_tokens=150,
    do_sample=False,
)

country = "Tunisia" 

prompt = f"List of telecom operators in {country}:"

response = llm.invoke(prompt)
print(response)
