import os
from dotenv import load_dotenv
from src.utils.config_loader import load_config
from src.video_processor import process_videos_in_folder

def main():
    load_dotenv()  # Load environment variables
    config = load_config()  # Load configuration

    if config['general']['VERBOSE']:
        print("Starting video transcription process...")

    input_folder = config['video']['input_folder']
    output_folder = config['video']['output_folder']

    process_videos_in_folder(input_folder, output_folder, config)

    if config['general']['VERBOSE']:
        print("Video transcription process completed.")

if __name__ == "__main__":
    main()
