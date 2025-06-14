from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import os

# Load Hugging Face token from .env file
load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Define a prompt template
template = """Answer the following question clearly and concisely:

Question: {question}
Answer:"""

prompt = PromptTemplate.from_template(template)
#repo_id = "HuggingFaceH4/zephyr-7b-beta"
#repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1" 

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    task="text-generation",
    max_new_tokens=150,
    do_sample=False,
)

prompt = "List of telecom operators in Tunisia:"

response = llm.invoke(prompt)
print(response)
