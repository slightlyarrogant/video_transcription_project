import os
from src.audio_handler import extract_audio, chunk_audio
from src.transcription import transcribe_audio
from src.summarization import summarize_text
from src.training_material_generator import generate_training_material
from src.utils.file_operations import ensure_dir, list_files, safe_move

def process_video(video_path, output_folder, config):
    if config['general']['VERBOSE']:
        print(f"Processing video: {video_path}")

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    video_output_folder = os.path.join(output_folder, base_name)
    ensure_dir(video_output_folder)
    
    if config['general']['VERBOSE']:
        print("Extracting audio...")
    audio_path = os.path.join(video_output_folder, "extracted_audio.wav")
    extract_audio(video_path, audio_path)
    
    if config['general']['VERBOSE']:
        print("Transcribing audio...")
    chunks = chunk_audio(audio_path, config['audio']['chunk_length_ms'], config['audio']['overlap_ms'])
    transcript = transcribe_audio(chunks, config['transcription'], config['general']['VERBOSE'])
    
    if config['general']['VERBOSE']:
        print("Summarizing transcript...")
    summary = summarize_text(transcript, config['summarization'], config['general']['VERBOSE'])
    
    if config['general']['VERBOSE']:
        print("Generating training material...")
    training_material = generate_training_material(transcript, summary, config)
    
    if config['general']['VERBOSE']:
        print("Saving outputs...")
    with open(os.path.join(video_output_folder, "transcript.txt"), "w") as f:
        f.write(transcript)
    with open(os.path.join(video_output_folder, "summary.txt"), "w") as f:
        f.write(summary)
    with open(os.path.join(video_output_folder, "training_material.md"), "w") as f:
        f.write(training_material)

    if config['general']['VERBOSE']:
        print(f"Finished processing video: {video_path}")

def process_videos_in_folder(input_folder, output_folder, config):
    video_files = list_files(input_folder, extensions=[".mp4", ".avi", ".mov"])
    for video_path in video_files:
        process_video(video_path, output_folder, config)
        if config['general']['VERBOSE']:
            print(f"Moving processed video to 'processed' folder: {video_path}")
        processed_folder = os.path.join(input_folder, "processed")
        ensure_dir(processed_folder)
        safe_move(video_path, os.path.join(processed_folder, os.path.basename(video_path)))
