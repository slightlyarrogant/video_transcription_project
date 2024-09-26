from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os

def extract_audio(video_path, audio_path):
    """
    Extract audio from a video file and save it as a WAV file.
    
    Args:
    video_path (str): Path to the input video file.
    audio_path (str): Path where the extracted audio will be saved.
    """
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()

def chunk_audio(audio_path, chunk_length_ms=60000, overlap_ms=1000):
    """
    Split an audio file into chunks.
    
    Args:
    audio_path (str): Path to the input audio file.
    chunk_length_ms (int): Length of each chunk in milliseconds.
    overlap_ms (int): Overlap between chunks in milliseconds.
    
    Returns:
    list: A list of AudioSegment objects representing the chunks.
    """
    audio = AudioSegment.from_wav(audio_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms - overlap_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunks.append(chunk)
    return chunks

def save_chunk(chunk, output_path):
    """
    Save an audio chunk to a file.
    
    Args:
    chunk (AudioSegment): The audio chunk to save.
    output_path (str): Path where the chunk will be saved.
    """
    chunk.export(output_path, format="wav")

# You might want to add more audio-related functions here as needed
