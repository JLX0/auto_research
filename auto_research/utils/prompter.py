from __future__ import annotations


class PromptBase:
    """
    A base class for managing and formatting prompts for Language Learning Models (LLMs).

    This class provides functionality to store, format, and display prompts in a format
    compatible with GPT-style language models. It maintains an internal list of formatted
    prompts and provides methods to manipulate and view them.

    Attributes:
        prompt (list[dict[str, str]]): A list of dictionaries containing formatted prompts,
            where each dictionary has 'role' and 'content' keys.

    Example:
        >>> prompt_manager = PromptBase()
        >>> formatted = prompt_manager.prompt_formatting_gpt(["Hello", "World"])
        >>> len(formatted)
        2
        >>> formatted[0]["content"]
        'Hello'
        >>> formatted[1]["content"]
        '\nWorld'
    """

    def __init__(self) -> None:
        """
        Initialize a new PromptBase instance with an empty prompt list.

        Example:
            >>> prompt_base = PromptBase()
            >>> prompt_base.prompt
            []
        """
        self.prompt: list[dict[str, str]] = []

    def prompt_formatting_gpt(self, prompt: list[str]) -> list[dict[str, str]]:
        """
        Format a list of prompt strings into GPT-compatible format.

        This method takes a list of strings and converts them into the format expected
        by GPT-style models, where each prompt segment is represented as a dictionary
        with 'role' and 'content' keys. For all segments after the first one, a newline
        character is prepended to the content.

        Args:
            prompt (list[str]): A list of strings representing the prompt segments to
                be formatted.

        Returns:
            list[dict[str, str]]: A list of dictionaries where each dictionary contains
                'role' and 'content' keys formatted for GPT models.

        Example:
            >>> base = PromptBase()
            >>> result = base.prompt_formatting_gpt(["First prompt", "Second prompt"])
            >>> result[0]["content"]
            'First prompt'
            >>> result[1]["content"]
            '\nSecond prompt'
        """
        formatted_prompt: list[dict[str, str]] = []
        for idx, content in enumerate(prompt):
            if idx > 0:
                content = "\n" + content
            formatted_prompt.append({"role": "system", "content": content})
        return formatted_prompt

    def print_prompt(self) -> None:
        """
        Print the content of all formatted prompts.

        This method iterates through the stored prompts and prints their content
        to standard output.

        Example:
            >>> base = PromptBase()
            >>> base.prompt = [{"role": "system", "content": "Test prompt"}]
            >>> base.print_prompt()
            Test prompt
        """
        for prompt_segment in self.prompt:
            print(prompt_segment["content"])
