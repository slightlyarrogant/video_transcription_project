from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

client = None

def init_openai_client():
    global client
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        print(f"Training Material Generator: Found .env file at: {dotenv_path}")
        load_dotenv(dotenv_path, override=True)
    else:
        print("Training Material Generator: No .env file found!")

    api_key = os.getenv("OPENAI_API_KEY", "Not found")
    print(f"Training Material Generator: Using API key (first 5 chars): {api_key[:5]}...")
    client = OpenAI(api_key=api_key)

def extract_key_points(transcript: str, config: dict, verbose: bool = False) -> str:
    """
    Extract key points from the transcript using the model specified in the config.
    
    Args:
    transcript (str): The full transcript of the video.
    config (dict): Configuration dictionary containing API details.
    verbose (bool): Whether to print verbose output.
    
    Returns:
    str: Extracted key points.
    """
    global client
    if client is None:
        init_openai_client()

    if verbose:
        print("Extracting key points from transcript...")
    
    try:
        response = client.chat.completions.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": config['prompts']['system']},
                {"role": "user", "content": config['prompts']['key_points'].format(transcript=transcript)}
            ],
            max_tokens=config['max_tokens'],
        )

        if verbose:
            print("Key points extraction completed.")

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error extracting key points: {str(e)}")
        return "Error: Unable to extract key points."

def generate_training_material(transcript: str, summary: str, config: dict) -> str:
    if config['general']['VERBOSE']:
        print("Generating training material...")

    key_points = extract_key_points(transcript, config['training_material'], config['general']['VERBOSE'])
    
    prompts = config['training_material']['prompts']
    
    training_material = f"""
# Comprehensive Training Material

{prompts['intro'].format(title='Video Title')}

## Executive Summary

{prompts['summary'].format(summary=summary)}

## Key Concepts and Detailed Explanations

{prompts['key_points_section'].format(points=key_points)}

## Additional Notes

- [Include any additional notes or observations here]

## Practical Applications

- [Suggest practical applications or exercises related to the content]

## Further Reading

- [Provide links or references for further reading on the topics covered]

{prompts['conclusion']}
"""

    if config['general']['VERBOSE']:
        print("Training material generation completed.")

    return training_material
