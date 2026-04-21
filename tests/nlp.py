from rs_bpe.bpe import openai

# Load the tokenizer (choose one)
encoder = openai.cl100k_base()      # Most common: GPT-4, GPT-3.5, etc.
# encoder = openai.o200k_base()     # Newer models like GPT-4o

text = "Your long prompt here with contractions don't and punctuation!"

tokens = encoder.encode(text)
token_count = len(tokens)

print("Token count:", token_count)
print("First 10 token IDs:", tokens[:10])
