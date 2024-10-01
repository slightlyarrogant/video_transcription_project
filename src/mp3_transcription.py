import os
from pydub import AudioSegment
from transcription import transcribe_audio

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def main():
    # Get the absolute path of the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Set up file paths
    input_dir = os.path.join(project_root, "output", "audio_files")
    output_dir = os.path.join(project_root, "output")
    mp3_file = "audio.mp3"
    wav_file = "audio_temp.wav"
    transcript_file = "transcript.txt"

    mp3_path = os.path.join(input_dir, mp3_file)
    wav_path = os.path.join(input_dir, wav_file)
    transcript_path = os.path.join(output_dir, transcript_file)

    # Check if the MP3 file exists
    if not os.path.exists(mp3_path):
        print(f"Error: The file {mp3_path} does not exist.")
        return

    # Convert MP3 to WAV
    print(f"Converting MP3 to WAV... \nInput: {mp3_path}\nOutput: {wav_path}")
    convert_mp3_to_wav(mp3_path, wav_path)

    # Transcribe the audio
    print("Transcribing audio...")
    config = {}  # Add any necessary configuration options here
    transcription = transcribe_audio(wav_path, config, verbose=True)

    # Save the transcription
    print(f"Saving transcription to {transcript_path}...")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcription)

    # Clean up temporary WAV file
    os.remove(wav_path)

    print(f"Transcription complete. Output saved to {transcript_path}")

if __name__ == "__main__":
    main()
