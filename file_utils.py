import openai

TOKEN_LIMIT = 32000

def count_tokens(text):
    return len(openai.api_client().tokens(text))

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
