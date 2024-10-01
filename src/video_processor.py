import os
from datetime import datetime
from src.audio_handler import extract_audio, chunk_audio
from src.transcription import transcribe_audio
from src.summarization import summarize_text
from src.training_material_generator import generate_training_material
from src.utils.file_operations import ensure_dir, list_files, safe_move, get_file_extension

def process_video(video_path, output_folder, config):
    # Create a subfolder for audio files
    audio_folder = os.path.join(output_folder, "audio_files")
    ensure_dir(audio_folder)

    # Extract audio from video
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(audio_folder, f"{base_name}.wav")
    extract_audio(video_path, audio_path)

    # Transcribe audio
    transcript = transcribe_audio(audio_path, config)

    return transcript, base_name

def process_videos_in_folder(input_folder, output_folder, processed_folder, config):
    ensure_dir(output_folder)
    ensure_dir(processed_folder)

    video_extensions = ['.mp4', '.avi', '.mov']  # Add or remove video formats as needed
    videos = [f for f in list_files(input_folder) if get_file_extension(f).lower() in video_extensions]

    for video_path in videos:
        filename = os.path.basename(video_path)
        start_time = datetime.now()
        print(f"Starting processing of {filename} at {start_time}")

        try:
            # Process the video
            transcript, base_name = process_video(video_path, output_folder, config)

            # Generate summary
            summary = summarize_text(transcript, config, title=base_name)

            # Generate training material
            training_material = generate_training_material(transcript, config, title=base_name)

            # Save outputs
            with open(os.path.join(output_folder, f"{base_name}_summary.md"), "w", encoding="utf-8") as f:
                f.write(summary)
            with open(os.path.join(output_folder, f"{base_name}_training_material.md"), "w", encoding="utf-8") as f:
                f.write(training_material)

            # Move processed video to the processed folder
            safe_move(video_path, os.path.join(processed_folder, filename))

            finish_time = datetime.now()
            elapsed_time = finish_time - start_time
            print(f"Finished processing {filename}")
            print(f"Start time: {start_time}")
            print(f"Finish time: {finish_time}")
            print(f"Elapsed time: {elapsed_time}")
            print("------------------------")

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            import traceback
            traceback.print_exc()  # This will print the full stack trace
