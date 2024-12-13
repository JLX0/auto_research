from __future__ import annotations

import json
import os
from typing import Any
from typing import Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat import ChatCompletionMessageParam

from auto_research.utils.cost import Calculator
from auto_research.utils.fault_tolerance import retry_overtime_decorator


def check_and_read_key_file(file_path: str, target_key: str) -> Any:
    """
    Check and read a key from a JSON file.

    Checks if a file named `key.json` exists in the specified path, validates if
    it contains a Python dictionary, and retrieves the value associated with the
    specified key.

    Args:
        file_path (str): The path where the `key.json` file is expected to be located.
        target_key (str): The key in the dictionary whose value needs to be retrieved.

    Returns:
        Any: The value associated with the specified key if all checks pass,
            or -1 if any validation fails.

    Example:
        >>> # Assuming key.json contains {"api_key": "abc123"}
        >>> value = check_and_read_key_file("/path/to/file", "api_key")
        >>> if value != -1:
        ...     print(f"Found key: {value}")
        ... else:
        ...     print("Key not found or invalid file")
        ...
    """
    full_path = os.path.join(file_path, "key.json")

    if not os.path.exists(full_path):
        return -1

    try:
        with open(full_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError):
        return -1

    if not isinstance(data, dict):
        return -1

    return data.get(target_key, -1)


class LLMBase:
    """
    Base class for all LLMs.

    This class serves as the foundation for different language model implementations,
    providing common functionality and attributes.

    Attributes:
        api_key (Optional[str]): The API key for authentication.
        model (str): The LLM model identifier being used.
        debug (bool): Flag indicating if debug mode is enabled.

    Example:
        >>> base_llm = LLMBase(api_key="your-key", model="gpt-4", debug=True)
        >>> print(base_llm.model)
        'gpt-4'
    """

    def __init__(
        self,
        api_key: Optional[str],
        model: str = "gpt-4-mini",
        debug: bool = False,
    ) -> None:
        """
        Initialize the base LLM.

        Args:
            api_key (Optional[str]): The API key for authentication.
            model (str, optional): The LLM model identifier to use. Defaults to 'gpt-4-mini'.
            debug (bool, optional): Enable debug mode for detailed logging. Defaults to False.
        """
        self.api_key = api_key
        self.model = model
        self.debug = debug


class GPT(LLMBase):
    """
    A client for interacting with OpenAI's GPT models.

    This class provides methods to communicate with GPT models through OpenAI's API,
    with built-in retry functionality for handling timeouts.

    Attributes:
        timeout (int): Maximum time limit for API calls.
        maximum_retry (int): Maximum number of retry attempts.
        client (OpenAI): The OpenAI client instance for making API calls.

    Example:
        >>> gpt = GPT(api_key="your-key", model="gpt-4")
        >>> messages = [{"role": "user", "content": "Hello!"}]
        >>> response = gpt.ask(messages)
    """

    timeout: int = 60
    maximum_retry: int = 3

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-mini",
        debug: bool = False,
    ) -> None:
        """
        Initialize the GPT client.

        Args:
            api_key (str): The OpenAI API key for authentication.
            model (str, optional): The GPT model identifier to use. Defaults to 'gpt-4-mini'.
            debug (bool, optional): Enable debug mode for detailed logging. Defaults to False.
        """
        super().__init__(api_key, model, debug)
        self.client = OpenAI(api_key=api_key)

    @staticmethod
    def print_prompt(messages: list[ChatCompletionMessageParam]) -> None:
        """
        Print each segment of a message prompt.

        Args:
            messages (list[ChatCompletionMessageParam]): List of message segments to print.

        Example:
            >>> messages = [
            ...     {"role": "system", "content": "You are a helpful assistant."},
            ...     {"role": "user", "content": "Hello!"},
            ... ]
            >>> GPT.print_prompt(messages)
        """
        for message in messages:
            if isinstance(message["content"], str):
                print(message["content"])

    @retry_overtime_decorator(time_limit=timeout, maximum_retry=maximum_retry, ret=True)
    def ask(
        self,
        messages: list[ChatCompletionMessageParam],
        ret_dict: Optional[dict[str, any]] = None,
    ) -> Optional[str]:
        """
        Send a message to the chat model and capture the response.

        Args:
            messages (list[ChatCompletionMessageParam]): The messages to be sent to the chat model.
            ret_dict (Optional[dict[str, str]], optional): A dictionary to capture the
                method's return value. Defaults to None.

        Returns:
            Optional[str]: The chat model's response text, or None if the request fails.

        Example:
            >>> gpt_client = GPT(api_key="your-api-key")
            >>> messages = [
            ...     {"role": "system", "content": "You are a helpful assistant."},
            ...     {"role": "user", "content": "What's the weather like?"},
            ... ]
            >>> response = gpt_client.ask(messages)
            >>> if response:
            ...     print(f"Got response: {response}")
            ...
        """
        if self.debug:
            print("---Prompt beginning marker---")
            self.print_prompt(messages)
            print("---Prompt ending marker---")

        response: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        if response.choices[0].message.content is None:
            return None

        response_text: str = response.choices[0].message.content

        if self.debug:
            print("---Response beginning marker---")
            print(response_text)
            print("---Response ending marker---")

        calculator_instance = Calculator(self.model, messages, response_text)
        cost = calculator_instance.calculate_cost_OpenAI()

        if ret_dict is not None:
            ret_dict["result"] = (
                response_text,
                cost,
            )

        return response_text
