import os
from datetime import datetime
from dotenv import load_dotenv
from src.utils.config_loader import load_config
from src.video_processor import process_videos_in_folder

def main():
    start_time = datetime.now()
    print(f"Starting video transcription process at {start_time}")

    load_dotenv()  # Load environment variables
    config = load_config()  # Load configuration

    if config['general']['VERBOSE']:
        print("Starting video transcription process...")

    input_folder = config['video']['input_folder']
    output_folder = config['video']['output_folder']
    processed_folder = os.path.join(input_folder, "processed")

    process_videos_in_folder(input_folder, output_folder, processed_folder, config)

    finish_time = datetime.now()
    elapsed_time = finish_time - start_time

    if config['general']['VERBOSE']:
        print("Video transcription process completed.")
    
    print(f"Start Time: {start_time}")
    print(f"Finish Time: {finish_time}")
    print(f"Total Elapsed Time: {elapsed_time}")

if __name__ == "__main__":
    main()
