from transformers import pipeline

# Load a pre-trained model and tokenizer
model_name = "deepset/bert-base-cased-squad2"
qa_model = pipeline('question-answering', model=model_name)

# Define a question and context
question = "What is the capital of France?"
context = "France is a country in Europe. Its capital is Paris."

# Get the answer
result = qa_model(question=question, context=context)

# Print the answer
print("Answer:", result['answer'])
print("Score:", result['score'])