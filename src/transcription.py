import os
import requests
import time
from pydub import AudioSegment

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def transcribe_chunk(chunk, chunk_number, config):
    """
    Transcribe a single audio chunk using the Whisper API.
    
    Args:
    chunk (AudioSegment): The audio chunk to transcribe.
    chunk_number (int): The number of the current chunk.
    config (dict): Configuration dictionary containing API details.
    
    Returns:
    str: The transcribed text for the chunk.
    """
    temp_path = f"temp_chunk_{chunk_number}.wav"
    chunk.export(temp_path, format="wav")
    
    for attempt in range(MAX_RETRIES):
        try:
            with open(temp_path, "rb") as audio_file:
                response = requests.post(
                    config['api_url'],
                    headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
                    files={"file": audio_file},
                    data={"model": config['model']}
                )
            
            if response.status_code == 200:
                os.remove(temp_path)
                return response.json()["text"]
            elif response.status_code == 429:
                print(f"Rate limit exceeded. Waiting for {RETRY_DELAY} seconds before retrying...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"API request failed with status code {response.status_code}. Attempt {attempt + 1} of {MAX_RETRIES}.")
                print(f"Response: {response.text}")
                if attempt < MAX_RETRIES - 1:
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise Exception(f"API request failed after {MAX_RETRIES} attempts. Last error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {str(e)}. Attempt {attempt + 1} of {MAX_RETRIES}.")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                raise Exception(f"Network error persisted after {MAX_RETRIES} attempts. Last error: {str(e)}")
    
    os.remove(temp_path)
    raise Exception(f"Failed to transcribe chunk after {MAX_RETRIES} attempts.")

def transcribe_audio(chunks, config, verbose=False):
    """
    Transcribe a list of audio chunks.
    
    Args:
    chunks (list): A list of AudioSegment objects representing the audio chunks.
    config (dict): Configuration dictionary containing API details.
    verbose (bool): Whether to print verbose output.
    
    Returns:
    str: The full transcription of all chunks combined.
    """
    transcriptions = []
    for i, chunk in enumerate(chunks):
        if verbose:
            print(f"Transcribing chunk {i+1} of {len(chunks)}...")
        try:
            transcription = transcribe_chunk(chunk, i, config)
            transcriptions.append(transcription)
            if verbose:
                print(f"Chunk {i+1} transcribed successfully.")
        except Exception as e:
            print(f"Error transcribing chunk {i+1}: {str(e)}")
            print("Skipping this chunk and continuing with the next...")
    
    return " ".join(transcriptions)
