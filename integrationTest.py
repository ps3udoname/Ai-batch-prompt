import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from ui import gui
import prompt
import fileManager
import ApiCaller


class TestIntegration(unittest.TestCase):
    def setUp(self):
        """
        Set up the GUI instance for testing.
        """
        self.app = gui()
        self.app.text_box = MagicMock()  # Mock the text box
        self.app.button_refs = [MagicMock() for _ in range(6)]  # Mock the buttons

    @patch('ApiCaller.requestResponse')
    def test_prompt_integration(self, mock_requestResponse):
        """
        Test case: Simulates the integration of the prompt API call.
        What it does:
        - Mocks the `requestResponse` function to return a test response.
        - Simulates user input in the text box and triggers the "Prompt" button.
        - Verifies that the response is displayed in the text box.
        """
        # Mock the API response
        mock_requestResponse.return_value = ("response text", "test-model")

        # Simulate user input in the text box
        self.app.text_box.get.return_value = "test prompt"

        # Trigger the "Prompt" button
        self.app.button_refs[0].config(text="loading...")
        response = prompt.promptApi("test prompt")
        self.app.setText(response)

        # Assert the API was called with the correct arguments
        mock_requestResponse.assert_called_with("test prompt", "deepseek/deepseek-r1:free")

        # Assert the response was displayed in the text box
        self.app.text_box.insert.assert_called_with(tk.END, "\ntest-model: response text\n")

    @patch('fileManager.parseFile')
    def test_file_integration(self, mock_parseFile):
        """
        Test case: Simulates the integration of file parsing.
        What it does:
        - Mocks the `parseFile` function to return a test response.
        - Simulates user input in the text box and triggers the "File" button.
        - Verifies that the response is displayed in the text box.
        """
        # Mock the file parsing response
        mock_parseFile.return_value = ": number of prompts: 1"

        # Simulate user input in the text box
        self.app.text_box.get.return_value = "test_file.jsonl"

        # Trigger the "File" button
        self.app.fileparse()

        # Assert the file parsing function was called with the correct arguments
        mock_parseFile.assert_called_with("test_file.jsonl")

        # Assert the response was displayed in the text box
        self.app.text_box.insert.assert_called_with(tk.END, ": number of prompts: 1")

    @patch('prompt.dataset2')
    def test_dataset_integration(self, mock_dataset2):
        """
        Test case: Simulates the integration of dataset processing.
        What it does:
        - Mocks the `dataset2` function to return a test response.
        - Simulates user input in the text box and triggers the "Dataset" button.
        - Verifies that the response is displayed in the text box.
        """
        # Mock the dataset processing response
        mock_dataset2.return_value = "number of prompts: 5"

        # Simulate user input in the text box
        self.app.text_box.get.return_value = "name=test_dataset column=content split=train config=test_config"

        # Trigger the "Dataset" button
        self.app.dataset()

        # Assert the dataset processing function was called with the correct arguments
        mock_dataset2.assert_called_with("test_dataset", "content", "train", "test_config")

        # Assert the response was displayed in the text box
        self.app.text_box.insert.assert_called_with(tk.END, "number of prompts: 5")

    @patch('prompt.reviewResponse')
    def test_review_response_integration(self, mock_reviewResponse):
        """
        Test case: Simulates the integration of the review response functionality.
        What it does:
        - Mocks the `reviewResponse` function to return a list of responses.
        - Simulates user input in the text box and triggers the "Review" button.
        - Verifies that the responses are displayed in the text box.
        """
        # Mock the review response
        mock_reviewResponse.return_value = [
            {"t_id": "request-123", "content": "response 1"},
            {"t_id": "file-456", "content": "response 2"}
        ]

        # Simulate user input in the text box
        self.app.text_box.get.return_value = "123"

        # Trigger the "Review" button
        self.app.review_response()

        # Assert the reviewResponse function was called with the correct arguments
        mock_reviewResponse.assert_called_with("output.jsonl", "123")

        # Assert the responses were displayed in the text box
        self.app.text_box.insert.assert_any_call(tk.END, "response 1\n")
        self.app.text_box.insert.assert_any_call(tk.END, "response 2\n")
        self.app.text_box.insert.assert_any_call(tk.END, "**********************************************************************************\n")

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.app.root.destroy()


if __name__ == "__main__":
    unittest.main()