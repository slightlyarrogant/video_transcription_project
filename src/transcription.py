import os
import time
import io
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pydub import AudioSegment
import concurrent.futures

MAX_RETRIES = 5
INITIAL_RETRY_DELAY = 1
MAX_RETRY_DELAY = 60
CHUNK_LENGTH_MS = 60000  # 1 minute

client = None

def init_openai_client():
    global client
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        print(f"Transcription: Found .env file at: {dotenv_path}")
        load_dotenv(dotenv_path, override=True)
    else:
        print("Transcription: No .env file found!")

    api_key = os.getenv("OPENAI_API_KEY", "Not found")
    print(f"Transcription: Using API key (first 10 chars): {api_key[:10]}...")
    client = OpenAI(api_key=api_key)

def format_timestamp(milliseconds):
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"

def transcribe_audio(audio_input, config, verbose=False):
    global client
    if client is None:
        init_openai_client()

    if verbose:
        print(f"Transcribing audio input: {audio_input}")

    try:
        audio = AudioSegment.from_wav(audio_input)
        chunks = [audio[i:i+CHUNK_LENGTH_MS] for i in range(0, len(audio), CHUNK_LENGTH_MS)]
        
        if verbose:
            print(f"Audio split into {len(chunks)} chunks of 1 minute each")

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_chunk = {executor.submit(transcribe_chunk, chunk, i, config, verbose): i for i, chunk in enumerate(chunks)}
            transcriptions = []

            for future in concurrent.futures.as_completed(future_to_chunk):
                chunk_index = future_to_chunk[future]
                try:
                    timestamp, transcription = future.result()
                    transcriptions.append((timestamp, transcription))
                    if verbose:
                        print(f"Chunk {chunk_index + 1} transcribed successfully")
                except Exception as e:
                    print(f"Chunk {chunk_index + 1} generated an exception: {str(e)}")

        # Sort transcriptions by timestamp and join
        transcriptions.sort(key=lambda x: x[0])
        full_transcription = " ".join(f"{timestamp} {text}" for timestamp, text in transcriptions)
        
        if verbose:
            print("Full transcription with timestamps completed successfully")
        
        return full_transcription

    except Exception as e:
        print(f"Error in transcribe_audio: {str(e)}")
        raise

def transcribe_chunk(chunk, chunk_number, config, verbose=False):
    global client
    if client is None:
        init_openai_client()

    # Calculate timestamp for the chunk
    timestamp = format_timestamp(chunk_number * CHUNK_LENGTH_MS)

    # Export chunk to an in-memory file-like object
    buffer = io.BytesIO()
    chunk.export(buffer, format="wav")
    buffer.seek(0)

    try:
        for attempt in range(MAX_RETRIES):
            try:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=("audio.wav", buffer, "audio/wav")
                )
                return timestamp, response.text
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    delay = min(INITIAL_RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                    if verbose:
                        print(f"Retrying chunk {chunk_number} in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise
    except Exception as e:
        print(f"Error transcribing chunk {chunk_number}: {str(e)}")
        raise
    finally:
        buffer.close()
