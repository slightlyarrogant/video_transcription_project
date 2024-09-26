import unittest
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.summarization import summarize_text
from src.training_material_generator import generate_training_material
from src.utils.config_loader import load_config

class TestSummarizationAndTraining(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        
        # Set up paths
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        transcript_path = os.path.join(project_root, 'output', 'zmiany w Vendo202203p6', 'transcript.txt')

        # Read transcript
        with open(transcript_path, 'r', encoding='utf-8') as file:
            cls.transcript = file.read()

        print(f"Transcript length: {len(cls.transcript)}")

    def test_summarization(self):
        print("Testing Summarization...")
        try:
            summary = summarize_text(self.transcript, self.config['summarization'])
            self.assertIsNotNone(summary)
            self.assertTrue(len(summary) > 0)
            print(f"Summary length: {len(summary)}")
            print("Summary preview:")
            print(summary[:500] + "..." if len(summary) > 500 else summary)
        except Exception as e:
            self.fail(f"Error in summarization: {str(e)}")

    def test_training_material_generation(self):
        print("\nTesting Training Material Generation...")
        try:
            # Create a combined config for training material generation
            combined_config = self.config['training_material'].copy()
            combined_config['summarization'] = self.config['summarization']
            
            training_material = generate_training_material(self.transcript, combined_config)
            self.assertIsNotNone(training_material)
            self.assertTrue(len(training_material) > 0)
            print(f"Training material length: {len(training_material)}")
            print("Training material preview:")
            print(training_material[:500] + "..." if len(training_material) > 500 else training_material)
        except Exception as e:
            self.fail(f"Error in training material generation: {str(e)}")

if __name__ == "__main__":
    unittest.main()
