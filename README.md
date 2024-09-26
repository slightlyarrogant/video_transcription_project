# Video Transcription and Training Material Generator

## Overview

This project is an automated system for transcribing videos, generating summaries, and creating training materials. It uses OpenAI's GPT models for natural language processing tasks and provides a streamlined workflow for processing video content into useful textual formats.

## Features

- Video to audio extraction
- Audio transcription using OpenAI's Whisper model
- Text summarization using GPT models
- Training material generation based on transcripts and summaries
- Configurable settings through YAML configuration
- Environment variable management for API keys

## Project Structure

```
video_transcription_project/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── config/
│   └── config.yaml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── video_processor.py
│   ├── audio_handler.py
│   ├── transcription.py
│   ├── summarization.py
│   ├── training_material_generator.py
│   └── utils/
│       ├── __init__.py
│       ├── file_operations.py
│       └── config_loader.py
├── tests/
│   ├── __init__.py
│   ├── test_video_processor.py
│   ├── test_audio_handler.py
│   ├── test_transcription.py
│   ├── test_summarization.py
│   └── test_training_material_generator.py
├── input_videos/
│   └── .gitkeep
└── output/
    └── .gitkeep
```

## Prerequisites

- Python 3.8+
- FFmpeg (for audio extraction)
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/video_transcription_project.git
   cd video_transcription_project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install FFmpeg:
   - On Ubuntu: `sudo apt-get install ffmpeg`
   - On macOS with Homebrew: `brew install ffmpeg`
   - On Windows: Download from the official FFmpeg website and add to PATH

5. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Configuration

Edit the `config/config.yaml` file to customize the behavior of the application. You can modify:

- Input and output folder paths
- Audio chunk settings
- Transcription model
- Summarization settings
- Training material generation prompts

## Usage

1. Place your video files in the `input_videos/` directory.

2. Run the main script:
   ```
   python -m src.main
   ```

3. Check the `output/` directory for the generated transcripts, summaries, and training materials.

## Testing

To run the test suite:

```
python -m unittest discover tests
```

To run a specific test file:

```
python -m unittest tests.test_summarization
```

## Troubleshooting

If you encounter issues with API key recognition:

1. Ensure your `.env` file is in the project root and contains the correct API key.
2. Try printing the API key in the script to verify it's being read correctly.
3. Check that the `.env` file is being loaded before any API calls are made.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT and Whisper models
- FFmpeg for audio processing capabilities

## Contact

Your Name - slightlyarrogant@gmail.com

Project Link: [https://github.com/yourusername/video_transcription_project](https://github.com/yourusername/video_transcription_project)
