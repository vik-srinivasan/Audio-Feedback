import unittest
from backend.ner_manager import NERManager
import os
from dotenv import load_dotenv
load_dotenv()
google_key = os.getenv('GOOGLE_KEY')


class TestNERManager(unittest.TestCase):
    def setUp(self):
        """Set up the NERManager instance before each test."""
        self.ner_manager = NERManager(google_key)

    def test_extract_proper_nouns(self):
        """Test the extraction of proper nouns from a transcription."""
        transcription = "I met Vik Srinivasan in Palo Alto near Stanford."

        proper_nouns = self.ner_manager.extract_proper_nouns(transcription)

        expected_nouns = ["Vik Srinivasan", "Palo Alto", "Stanford"]
        self.assertListEqual(proper_nouns, expected_nouns)

    def test_update_memory(self):
        """Test that the memory is updated correctly with new proper nouns."""
        self.ner_manager.update_memory(["Vik Srinivasan", "Palo Alto"])

        self.assertEqual(self.ner_manager.get_memory()["Vik Srinivasan"], 1)
        self.assertEqual(self.ner_manager.get_memory()["Palo Alto"], 1)

        self.ner_manager.update_memory(["Vik Srinivasan"])

        self.assertEqual(self.ner_manager.get_memory()["Vik Srinivasan"], 2)

    def test_get_memory(self):
        """Test retrieving the current memory of proper nouns."""
        self.ner_manager.update_memory(["Vik Srinivasan", "Palo Alto"])
        memory = self.ner_manager.get_memory()

        self.assertIn("Vik Srinivasan", memory)
        self.assertIn("Palo Alto", memory)
        self.assertEqual(len(memory), 2)  # Should have two entries

if __name__ == "__main__":
    unittest.main()
