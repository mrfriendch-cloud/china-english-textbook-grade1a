import unittest
import os
import json
import tempfile
from builder import build_app

class TestAppBuilder(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.pdf_data_path = os.path.join(self.test_dir.name, 'pdf_structure.json')
        self.quiz_data_path = os.path.join(self.test_dir.name, 'quiz_data.json')
        self.output_path = os.path.join(self.test_dir.name, 'index.html')
        self.css_path = os.path.join(self.test_dir.name, 'css', 'styles.css')

        # Create dummy test fixtures
        sample_pdf_data = [{"page": 1, "text": "Welcome to Unit 1"}]
        sample_quiz_data = {
            "unit-starter": {
                "title": "Starter Quiz",
                "questions": [
                    {
                        "q": "Test question?",
                        "opts": ["A", "B", "C", "D"],
                        "ans": 0
                    }
                ]
            }
        }

        with open(self.pdf_data_path, 'w', encoding='utf-8') as f:
            json.dump(sample_pdf_data, f)

        with open(self.quiz_data_path, 'w', encoding='utf-8') as f:
            json.dump(sample_quiz_data, f)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_build_app_generates_valid_output(self):
        result_path = build_app(
            pdf_data_path=self.pdf_data_path,
            quiz_data_path=self.quiz_data_path,
            output_path=self.output_path,
            css_output_path=self.css_path
        )
        self.assertTrue(os.path.exists(result_path))
        self.assertTrue(os.path.exists(self.css_path))

        with open(result_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert document structure and data injections
        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('Starter Quiz', content)
        self.assertIn('Welcome to Unit 1', content)

    def test_missing_data_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            build_app(pdf_data_path='non_existent.json', quiz_data_path=self.quiz_data_path, output_path=self.output_path)

if __name__ == '__main__':
    unittest.main()
