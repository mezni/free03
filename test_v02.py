from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"

# Load pipeline
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

# Define question and context
QA_input = {
    'question': 'List of mobile prefixes by operator in Morocco',
    'context': '''
    Maroc Telecom uses prefixes like 061, 062, 063. Orange Morocco uses 064, 065. Inwi uses 066, 067.
    These prefixes help identify the operator of a given mobile number.
    '''
}

# Get prediction
res = nlp(QA_input)

# Output
print(res)
