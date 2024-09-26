from openai import OpenAI
import os
from typing import List
from dotenv import load_dotenv, find_dotenv

client = None

def init_openai_client():
    global client
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        print(f"Summarization: Found .env file at: {dotenv_path}")
        load_dotenv(dotenv_path, override=True)
    else:
        print("Summarization: No .env file found!")

    api_key = os.getenv("OPENAI_API_KEY", "Not found")
    print(f"Summarization: Using API key (first 5 chars): {api_key[:5]}...")
    client = OpenAI(api_key=api_key)


def split_text(text: str, max_chunk_size: int = 8000) -> List[str]:
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        if current_size + len(word) + 1 > max_chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_size = len(word)
        else:
            current_chunk.append(word)
            current_size += len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def summarize_text(text: str, config: dict, verbose: bool = False, depth: int = 0, max_depth: int = 3) -> str:
    global client
    if client is None:
        init_openai_client()
    
    chunks = split_text(text, max_chunk_size=8000)
    summaries = []

    for i, chunk in enumerate(chunks):
        if verbose:
            print(f"Summarizing chunk {i+1} of {len(chunks)} (depth {depth})...")
        
        try:
            response = client.chat.completions.create(
                model=config['model'],
                messages=[
                    {"role": "system", "content": config['prompt']['system']},
                    {"role": "user", "content": config['prompt']['user'].format(text=chunk)}
                ],
                max_tokens=config['max_summary_length'],
            )

            summary = response.choices[0].message.content.strip()
            summaries.append(summary)

            if verbose:
                print(f"Chunk {i+1} summarized successfully (depth {depth}).")
        except Exception as e:
            print(f"Error summarizing chunk {i+1} (depth {depth}): {str(e)}")
            print("Skipping this chunk and continuing with the next...")

    final_summary = " ".join(summaries)

    if len(final_summary) > config['max_summary_length'] and depth < max_depth:
        if verbose:
            print(f"Summary still too long ({len(final_summary)} chars). Recursively summarizing (depth {depth + 1})...")
        final_summary = summarize_text(final_summary, config, verbose, depth + 1, max_depth)
    elif depth == max_depth:
        print(f"Reached maximum recursion depth ({max_depth}). Returning current summary.")

    if verbose and depth == 0:
        print("Summarization completed.")

    return final_summary
