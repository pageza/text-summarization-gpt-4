import openai
import openai_secret_manager

assert "openai" in openai_secret_manager.get_services()
secrets = openai_secret_manager.get_secret("openai")
TOKEN_LIMIT = 32000

def count_tokens(text, model='davinci'):
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
