import unittest
from unittest.mock import patch, MagicMock
from ApiCaller import ApiCaler

class TestRequestResponse(unittest.TestCase):
    @patch('ApiCaller.OpenAI')
    def test_requestResponse_success(self, mock_OpenAI):
        """
        Test case: Simulates a successful API call.
        What it does:
        - Mocks the OpenAI client to return a valid response.
        - Verifies that the function returns the correct response content and model.
        """
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_OpenAI.return_value = mock_client
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="response text"))]
        )

        # Call the function
        response, model = ApiCaler.requestResponse("test prompt", "test-model")

        # Assert the response is correct
        self.assertEqual(response, "response text")
        self.assertEqual(model, "test-model")


    @patch('ApiCaller.OpenAI')
    def test_requestResponse_exception(self, mock_OpenAI):
        """
        Test case: Simulates a scenario where the API raises an exception.
        What it does:
        - Mocks the OpenAI client to raise an exception (e.g., network error).
        - Verifies that the function handles the exception and returns the error message.
        """
        # Mock the OpenAI client to raise an exception
        mock_client = MagicMock()
        mock_OpenAI.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API error")

        # Call the function
        response, model = ApiCaler.requestResponse("test prompt", "test-model")

        # Assert the function handles the exception and returns the error message
        self.assertEqual(response, "API error")
        self.assertEqual(model, "test-model")
    
    @patch('ApiCaller.OpenAI')
    def test_requestResponse_blank_prompt(self, mock_OpenAI):
        """
        Test case: Simulates a scenario where the prompt is blank.
        What it does:
        - Calls the function with an empty prompt.
        - Verifies that the function returns the correct error message.
        """
        # Call the function with a blank prompt
        response, model = ApiCaler.requestResponse("", "test-model")

        # Assert the function returns the correct error message
        self.assertEqual(response, "Error: No prompt provided")
        self.assertEqual(model, "test-model")

if __name__ == "__main__":
    unittest.main()