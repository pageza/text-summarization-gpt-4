import openai

import os
from dotenv import load_dotenv

def get_openai_api_key():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    model_list = openai.Model.list()
    print(model_list)
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not found.")
    return api_key

TOKEN_LIMIT = 32000

def count_tokens(text, model='gpt-4'):
    response = openai.Completion.create(
        engine=model,
        prompt=text,
        max_tokens=1,
        n=0,
        stop=None,
        temperature=0
    )

    return response.choices[0].logprobs.token_logprobs.shape[0]


def read_file_and_split(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    token_count = count_tokens(content)

    if token_count <= TOKEN_LIMIT:
        return [content]

    chunks = []
    current_chunk = ""
    current_chunk_token_count = 0

    for word in content.split():
        word_token_count = count_tokens(word)

        if current_chunk_token_count + word_token_count <= TOKEN_LIMIT:
            current_chunk += " " + word
            current_chunk_token_count += word_token_count
        else:
            chunks.append(current_chunk)
            current_chunk = word
            current_chunk_token_count = word_token_count

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
