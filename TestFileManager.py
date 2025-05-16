import unittest
from unittest.mock import patch, mock_open, MagicMock
from fileManager import FileManager as fileManager
import datetime
from datetime import datetime

# class TestFileManager(unittest.TestCase):
#     @patch('builtins.open', new_callable=mock_open, read_data='{"body": {"messages": [{"content": "test content"}]}}')
#     @patch('prompt.Pompt.promptApi')
#     def test_parseFile(self, mock_promptApi, mock_open_file):
#         """
#         Test case: Simulates parsing a JSONL file.
#         What it does:
#         - Mocks the file reading process to provide a JSONL line.
#         - Mocks the `prompt.promptApi` function to ensure it is called with the correct arguments.
#         - Verifies that the function correctly counts the number of prompts.
#         """
#         # Mock promptApi
#         mock_promptApi.return_value = None

#         # Call the function
#         result = fileManager.parseFile("test.jsonl")

#         # Assert the number of prompts is correct
#         self.assertEqual(result, ": number of prompts: 1")

#         # Assert promptApi was called with the correct arguments
#         mock_promptApi.assert_called_with("test content", True)
    

#     @patch('builtins.open', new_callable=mock_open, read_data='// This is a comment\n{"body": {"messages": [{"content": "test content"}]}}\n// Another comment\n')
#     def test_parseFile_skips_commented_lines(self, mock_open_file):
#         """
#         Test case: Verifies that parseFile skips commented lines in the input file.
#         What it does:
#         - Mocks the file reading process to include commented lines (starting with "//").
#         - Ensures that only valid JSON lines are processed.
#         """
#         # Call the function
#         result = fileManager.parseFile("test.jsonl")

#         # Assert the function processes only valid JSON lines
#         self.assertEqual(result, ": number of prompts: 1")



#     @patch('builtins.open', new_callable=mock_open)
#     @patch('fileManager.datetime')
#     def test_saveResponse(self, mock_datetime, mock_open_file):
#         # Create mock datetime instance
#         mock_now = MagicMock()
#         mock_now.strftime.return_value = "04052025:12:00:00"
#         mock_datetime.now.return_value = mock_now

#         fileManager.saveResponse(
#             content="response content",
#             prompt1="test prompt",
#             model="test model",
#             batch=True,
#             file="output.jsonl"
#         )

#         mock_open_file().write.assert_called_with(
#             '{"content": "response content", "prompt": "test prompt", "model": "test model", "t_id": "file-04052025:12:00:00"}\n'
#         )
import unittest
from unittest.mock import patch, mock_open, MagicMock
from fileManager import FileManager


class TestFileManager(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"body": {"messages": [{"content": "test content"}]}}\n// This is a comment\n')
    @patch('prompt.Prompt.promptApi')
    def test_parseFile(self, mock_promptApi, mock_open_file):
        """
        Test case: Verifies that parseFile processes valid JSON lines and skips commented lines.
        """
        # Mock the promptApi function
        mock_promptApi.return_value = None

        # Call the parseFile function
        result = FileManager.parseFile("test.jsonl")

        # Assert the number of prompts processed
        self.assertEqual(result, ": number of prompts: 1")

        # Assert promptApi was called with the correct arguments
        mock_promptApi.assert_called_once_with("test content", True)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('fileManager.datetime')
    def test_saveResponse(self, mock_datetime, mock_open_file):
        # Create mock datetime instance
        mock_now = MagicMock()
        mock_now.strftime.return_value = "04052025:12:00:00"
        mock_datetime.now.return_value = mock_now

        fileManager.saveResponse(
            content="response content",
            prompt1="test prompt",
            model="test model",
            batch=True,
            file="output.jsonl"
        )

        mock_open_file().write.assert_called_with(
            '{"content": "response content", "prompt": "test prompt", "model": "test model", "t_id": "file-04052025:12:00:00"}\n'
        )
    
    @patch('builtins.open', new_callable=mock_open, read_data='// This is a comment\n{"body": {"messages": [{"content": "test content"}]}}\n// Another comment\n')
    def test_parseFile_skips_commented_lines(self, mock_open_file):
        """
        Test case: Verifies that parseFile skips commented lines in the input file.
        What it does:
        - Mocks the file reading process to include commented lines (starting with "//").
        - Ensures that only valid JSON lines are processed.
        """
        # Call the function
        result = fileManager.parseFile("test.jsonl")

        # Assert the function processes only valid JSON lines
        self.assertEqual(result, ": number of prompts: 1")


    # @patch('builtins.open', new_callable=mock_open)
    # @patch('datetime.datetime')
    # def test_saveResponse(self, mock_datetime, mock_open_file):
    #     """
    #     Test case: Verifies that saveResponse writes the correct JSON object to the file.
    #     """
    #     mock_now = MagicMock()
    #     mock_now.strftime.return_value = "04052025:12:00:00"
    #     mock_datetime.now.return_value = mock_now

    #     # Call the saveResponse function
    #     FileManager.saveResponse(
    #         content="response content",
    #         prompt1="test prompt",
    #         model="test model",
    #         batch=True,
    #         file="output.jsonl"
    #     )

    #     # Construct the expected JSON line
    #     expected_json_line = {
    #         "content": "response content",
    #         "prompt": "test prompt",
    #         "model": "test model",
    #         "t_id": "file-04052025:12:00:00"
    #     }

    #     # Assert the file was written with the correct JSON line
    #     mock_open_file().write.assert_called_once_with(json.dumps(expected_json_line) + '\n')


if __name__ == "__main__":
    unittest.main()