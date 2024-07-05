import pandas as pd
import tiktoken

file_path = 'remotive_jobs.csv'
df = pd.read_csv(file_path)

#cl100k_base = encoder for gpt4
enc = tiktoken.get_encoding("cl100k_base")

#Count tokens in text
def count_tokens(text):
    tokens = enc.encode(text)
    return len(tokens)
total_tokens = 0
for column in df.columns:
    print(f"Processing column: {column}")
    for text in df[column].dropna():  # Skip missing values
        # Ensure the text is a string
        if not isinstance(text, str):
            text = str(text)
        total_tokens += count_tokens(text)

print(f"Total number of tokens in the CSV file: {total_tokens}")
