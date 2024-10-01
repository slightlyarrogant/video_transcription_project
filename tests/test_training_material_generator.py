import unittest
import json
import time
from datetime import datetime
from unittest.mock import patch
from src.training_material_generator import generate_training_material
from src.utils.config_loader import load_config

class TestTrainingMaterialGenerator(unittest.TestCase):
    def setUp(self):
        self.config = load_config()
        with open('tests/sample_transcript.txt', 'r', encoding='utf-8') as f:
            self.transcript = f.read()

    def test_generate_training_material(self):
        start_time = time.time()
        
        result = generate_training_material(self.transcript, self.config, "Test Video Title")
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Collect metadata
        metadata = {
            "model": self.config['training_material']['model'],
            "version": "1.0",  # You might want to store this in config or elsewhere
            "elapsed_time": f"{elapsed_time:.2f} seconds",
            "timestamp": datetime.now().isoformat(),
            "prompts": self.config['training_material']['prompts']
        }

        # Create Markdown output
        markdown_output = f"""# Training Material Generation Report

## Metadata
```json
{json.dumps(metadata, indent=2)}
```

## Generated Training Material

{result}
"""

        # Save to file
        with open('test_output_training_material.md', 'w', encoding='utf-8') as f:
            f.write(markdown_output)

        # Print to console
        print(markdown_output)

        # Assertions
        self.assertIn("Wprowadzenie", result)
        self.assertIn("Podsumowanie menedżerskie", result)
        self.assertIn("Kluczowe koncepcje", result)
        self.assertIn("Praktyczne zastosowania", result)
        self.assertIn("Studia przypadków", result)
        self.assertIn("Pytania kontrolne", result)
        self.assertIn("Ćwiczenia praktyczne", result)
        self.assertIn("Dalsza lektura", result)
        self.assertIn("Zakończenie", result)

        # Add more specific assertions based on your requirements

if __name__ == '__main__':
    unittest.main()
