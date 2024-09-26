import os
import sys
from dotenv import load_dotenv, find_dotenv

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Attempt to load environment variables from .env file
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    print(f"Test Script: Found .env file at: {dotenv_path}")
    load_dotenv(dotenv_path, override=True)
else:
    print("Test Script: No .env file found!")

from src.utils.config_loader import load_config
from src.summarization import summarize_text, init_openai_client as init_summarization
from src.training_material_generator import generate_training_material, init_openai_client as init_training_material

def test_summarization_and_training():
    # Initialize OpenAI clients
    init_summarization()
    init_training_material()

    # Load configuration
    config = load_config()

    # Path to the transcript file
    transcript_path = os.path.join(project_root, "output", "zoom_0", "transcript.txt")

    # Read the transcript
    with open(transcript_path, 'r') as file:
        transcript = file.read()

    print("Transcript length:", len(transcript))

    # Test summarization
    print("\nTesting Summarization...")
    summary = summarize_text(transcript, config['summarization'], verbose=True, max_depth=3)
    
    print("\nGenerated Summary:")
    print(summary)
    print("\nSummary length:", len(summary))

    # Test training material generation
    print("\nTesting Training Material Generation...")
    training_material = generate_training_material(transcript, summary, config)
    
    print("\nGenerated Training Material:")
    print(training_material)
    print("\nTraining Material length:", len(training_material))

    # Save the results
    output_dir = os.path.join(project_root, "output", "zoom_0")
    with open(os.path.join(output_dir, "test_summary.txt"), "w") as f:
        f.write(summary)
    with open(os.path.join(output_dir, "test_training_material.md"), "w") as f:
        f.write(training_material)

    print("\nTest results have been saved in the output directory.")

if __name__ == "__main__":
    test_summarization_and_training()
