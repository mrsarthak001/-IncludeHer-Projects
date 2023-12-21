import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()
def split_text(tokenized, budget):
    # Split the text into 4000 tokens chunks
    split = []
    for i in range(0, len(tokenized), budget):
        split.append(tokenized[i : i + budget])

    # If the last chunk is smaller than budget, pad it from the previous chunk up to budget
    if len(split[-1]) < budget and len(split) > 1:
        # Calculate the remaining budget
        remaining_budget = budget - len(split[-1])
        # Pad the last chunk with the remaining budget
        split[-1] = split[-2][-remaining_budget:] + split[-1]

    return split

def tokenize_gpt2(text):
    from transformers import GPT2TokenizerFast

    # Suppress warning: Token indices sequence length is longer than the specified maximum sequence length for this model (3874 > 1024). Running this sequence through the model will result in indexing errors
    import logging

    logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    return tokenizer.encode(text)

def detokenize_gpt2(text):
    from transformers import GPT2TokenizerFast

    # Suppress warning: Token indices sequence length is longer than the specified maximum sequence length for this model (3874 > 1024). Running this sequence through the model will result in indexing errors
    import logging

    logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    return tokenizer.decode(text)

def openai_inference_gpt3(prompt, max_new_tokens):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=max_new_tokens,
    )
    return response.choices[0].text

def inference(prompt, max_new_tokens):
    result = openai_inference_gpt3(prompt, max_new_tokens)

    with open("summary.txt", "a", encoding="utf-8", errors="replace") as f:
        f.write(result + "\n")
    return result
