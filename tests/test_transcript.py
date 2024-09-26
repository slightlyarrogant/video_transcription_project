import unittest
import os
import tracemalloc
from src.transcription import transcribe_audio
from src.utils.config_loader import load_config

class TestTranscription(unittest.TestCase):
    def setUp(self):
        self.config = load_config()
        self.audio_path = os.path.join('output', 'zmiany w Vendo202203p6', 'extracted_audio.wav')
        
    def test_transcribe_audio(self):
        print(f"Testing audio file: {self.audio_path}")
        self.assertTrue(os.path.exists(self.audio_path), f"Audio file not found: {self.audio_path}")
        
        tracemalloc.start()
        
        try:
            transcription = transcribe_audio(self.audio_path, self.config, verbose=True)
            
            print(f"Transcription length: {len(transcription)}")
            self.assertIsNotNone(transcription)
            self.assertNotEqual(transcription.strip(), "")
            
            print("Transcription result (first 500 characters):")
            print(transcription[:500] + "..." if len(transcription) > 500 else transcription)
            
        except Exception as e:
            self.fail(f"Transcription failed with error: {str(e)}")
        finally:
            current, peak = tracemalloc.get_traced_memory()
            print(f"Current memory usage: {current / 10**6:.2f} MB")
            print(f"Peak memory usage: {peak / 10**6:.2f} MB")
            
            print("\nTop 5 memory allocations:")
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            for stat in top_stats[:5]:
                print(stat)
            
            tracemalloc.stop()

if __name__ == '__main__':
    unittest.main()
