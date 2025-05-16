import unittest
from unittest.mock import patch, MagicMock
from prompt import Prompt as prompt


class TestPrompt(unittest.TestCase):
    # @patch('prompt.requestResponse')
    
    @patch('ApiCaller.ApiCaler.requestResponse')
    @patch('fileManager.FileManager.saveResponse')
    def test_promptApi(self, mock_saveResponse, mock_requestResponse):
        """
        Test case: Simulates the promptApi function.
        What it does:
        - Mocks the `requestResponse` function to return a tuple (response text, model).
        - Verifies that the response is formatted correctly.
        - Ensures `saveResponse` is called when `save` or `batch` is True.
        """
        # Mock the response from requestResponse
        mock_requestResponse.return_value = ("response text", "test-model")

        # Call the function
        result = prompt.promptApi("test prompt", batch=True)

        # Assert the response is formatted correctly
        self.assertEqual(result, "\ntest-model: response text\n")

        # Assert saveResponse was called with correct arguments
        mock_saveResponse.assert_called_with(
            content="response text",
            prompt1="test prompt",
            model="test-model",
            batch=True
        )

    # @patch('ApiCaller.ApiCaler.requestResponse')
    # @patch('fileManager.FileManager.saveResponse')
    # def test_promptApi(self, mock_saveResponse, mock_requestResponse):
    #     """
    #     Test case: Simulates the promptApi function.
    #     What it does:
    #     - Mocks the `requestResponse` function to return a tuple (response text, model).
    #     - Verifies that the response is formatted correctly.
    #     - Ensures `saveResponse` is called when `save` or `batch` is True.
    #     """
    #     # Mock the response from requestResponse
    #     mock_requestResponse.return_value = ("response text", "test-model")

    #     # Create an instance of Prompt
    #     prompt_instance = Prompt()

    #     # Call the function
    #     result = prompt_instance.promptApi("test prompt", batch=True)

    #     # Assert the response is formatted correctly
    #     self.assertEqual(result, "\ntest-model: response text\n")

    #     # Assert saveResponse was called with correct arguments
    #     mock_saveResponse.assert_called_with(
    #         content="response text",
    #         prompt1="test prompt",
    #         model="test-model",
    #         batch=True
    #     )

    def test_dataset_format_error(self):
        """
        Test case: Simulates the dataset function with an invalid input string.
        What it does:
        - Calls the function with an incorrectly formatted string.
        - Verifies that the function returns the correct error message.
        """
        result = prompt.dataset("invalid input")
        self.assertEqual(
            result,
            "\n format error: \n example usage: name=AlignmentResearch/JailbreakCompletions column=content split=train limit=1 config="
        )

    # @patch('datasets.load_dataset')
    # @patch('prompt.Prompt.promptApi')
    @patch('datasets.load_dataset')
    @patch('prompt.Prompt.promptApi')
    def test_dataset2(self, mock_promptApi, mock_load_dataset):
        """
        Test case: Simulates the dataset2 function.
        What it does:
        - Mocks the `datasets.load_dataset` function to return a mock dataset.
        - Mocks the `promptApi` function to ensure it is called with the correct arguments.
        - Verifies that the function processes all prompts in the dataset.
        """
        # Mock the dataset
        mock_dataset = [{"content": "test content"}]
        mock_load_dataset.return_value = mock_dataset

        # Call the function
        result = prompt.dataset2("test-name", "content", "train", 1, "test-config")

        # Assert dataset2 processes all prompts
        self.assertEqual(result, "\n number of prompts: 1")

        # Assert promptApi was called with the correct arguments
        mock_promptApi.assert_called_with("test content", True)

    @patch('builtins.open', new_callable=MagicMock)
    def test_reviewResponse(self, mock_open):
        """
        Test case: Simulates the reviewResponse function.
        What it does:
        - Mocks the file reading process to provide JSON lines.
        - Verifies that the function correctly filters and returns matching responses.
        """
        # Mock the file content
        mock_open.return_value.__enter__.return_value = [
            '{"t_id": "request-123", "content": "response 1"}\n',
            '{"t_id": "file-456", "content": "response 2"}\n',
            '{"t_id": "request-789", "content": "response 3"}\n'
        ]

        
        # prompt_instance = Prompt()
        # Call the function
        result = prompt.reviewResponse("test.jsonl", "123")

        # Assert the function returns the correct matches
        self.assertEqual(result, [{"t_id": "request-123", "content": "response 1"}])
    # @patch('builtins.open', new_callable=MagicMock)
    # def test_reviewResponse(self, mock_open):
    #     """
    #     Test case: Simulates the reviewResponse function.
    #     What it does:
    #     - Mocks the file reading process to provide JSON lines.
    #     - Verifies that the function correctly filters and returns matching responses.
    #     """
    #     # Mock the file content
    #     mock_open.return_value.__enter__.return_value = [
    #         '{"t_id": "request-123", "content": "response 1"}\n',
    #         '{"t_id": "file-456", "content": "response 2"}\n',
    #         '{"t_id": "request-789", "content": "response 3"}\n'
    #     ]

    #     # Create an instance of Prompt
    #     prompt_instance = Prompt()

    #     # Call the function
    #     result = prompt_instance.reviewResponse("test.jsonl", "123")

    #     # Assert the function returns the correct matches
    #     self.assertEqual(result, [{"t_id": "request-123", "content": "response 1"}])


if __name__ == "__main__":
    unittest.main()