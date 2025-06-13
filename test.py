from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Set your Google API key as an environment variable or getpass
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
response = llm.invoke("What is the capital of France?")
print(response.content)