from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from auto_research.utils.fault_tolerance import retry_overtime_decorator


def check_and_read_key_file(file_path: str, target_key: str) -> Any:
    """Checks and reads a key from a JSON file.

    Checks if a file named `key.json` exists in the specified path, validates if
    it contains a Python dictionary, and retrieves the value associated with the
    specified key.

    Args:
        file_path:
            The path where the `key.json` file is expected to be located.
        target_key:
            The key in the dictionary whose value needs to be retrieved.

    Returns:
        The value associated with the specified key if all checks pass,
        or -1 if any validation fails.

    Example:
        .. testcode::

            # Assuming key.json contains {"api_key": "abc123"}
            value = check_and_read_key_file("/path/to/file", "api_key")
            if value != -1:
                print(f"Found key: {value}")
            else:
                print("Key not found or invalid file")
    """
    # Construct the full path to the file
    full_path = os.path.join(file_path, 'key.json')

    # Check if the file exists
    if not os.path.exists(full_path):
        return -1

    # Open and read the file
    try:
        with open(full_path, 'r') as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError):
        return -1

    # Check if the data is a dictionary
    if not isinstance(data, dict):
        return -1

    # Check if the target key exists and return its value
    if target_key in data:
        return data[target_key]

    return -1


class GPT:
    """A client for interacting with OpenAI's GPT models.

    This class provides methods to communicate with GPT models through OpenAI's API,
    with built-in retry functionality for handling timeouts.

    Args:
        api_key:
            The OpenAI API key for authentication.
        model:
            The GPT model identifier to use.
        debug:
            Enable debug mode for detailed logging.

    Attributes:
        client:
            OpenAI client instance.
        model:
            The GPT model identifier being used.
        debug:
            Flag indicating if debug mode is enabled.
        timeout:
            Maximum time limit for API calls.
        maximum_retry:
            Maximum number of retry attempts.

    Example:
        .. testcode::

            gpt_client = GPT(api_key="your-api-key", model="gpt-4")
            message = [{"role": "user", "content": "Hello!"}]
            response = gpt_client.ask(message)
            print(response)
    """

    # Settings for the retry decorator
    timeout: int = 60
    maximum_retry: int = 3

    def __init__(
        self,
        api_key: str,
        model: str = 'gpt-4-mini',
        debug: bool = False
    ) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.debug = debug

    @staticmethod
    def print_prompt(message: list[dict[str, str]]) -> None:
        """Print each segment of a message prompt.

        Args:
            message:
                List of message segments to print.

        Example:
            .. testcode::

                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello!"}
                ]
                GPT.print_prompt(messages)
        """
        for prompt_segment in message:
            print(prompt_segment["content"])

    @retry_overtime_decorator(time_limit=timeout, maximum_retry=maximum_retry, ret=True)
    def ask(self, message: list[dict[str, str]], ret_dict: dict | None = None) -> str | None:
        """Send a message to the chat model and capture the response.

        Args:
            message:
                The message to be sent to the chat model.
            ret_dict:
                A dictionary to capture the method's return value (if needed by the decorator).

        Returns:
            The chat model's response text, or None if the request fails.

        Example:
            .. testcode::

                gpt_client = GPT(api_key="your-api-key")
                message = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What's the weather like?"}
                ]
                response = gpt_client.ask(message)
                if response:
                    print(f"Got response: {response}")
        """
        if self.debug:
            print("---Prompt beginning marker---")
            self.print_prompt(message)
            print("---Prompt ending marker---")

        # Call the client to get the response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message
        )
        response_text = response.choices[0].message.content

        if self.debug:
            print("---Response beginning marker---")
            print(response_text)
            print("---Response ending marker---")

        # Store the result in ret_dict if it exists
        if ret_dict is not None:
            ret_dict['result'] = response_text

        return response_text