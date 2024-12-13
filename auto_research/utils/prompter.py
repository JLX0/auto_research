from __future__ import annotations

from copy import deepcopy
from typing import Any
from typing import Callable


class PromptBase:
    """
    A base class for managing and formatting prompts for Language Learning Models (LLMs).

    This class provides functionality to store, format, and display prompts in a format
    compatible with GPT-style language models. It maintains an internal list of formatted
    prompts and provides methods to manipulate and view them.

    Attributes:
        prompt (Any): The formatted prompts ready for being passed to the LLM.
        conversation_history (list[str]): The history of conversations recorded.

    Example:
        >>> prompt_manager = PromptBase()
        >>> formatted = prompt_manager.prompt_formatting_gpt(["Hello", "World"])
        >>> len(formatted)
        2
        >>> formatted[0]["content"]
        'Hello'
        >>> formatted[1]["content"]
        '\\nWorld'
    """

    def __init__(self) -> None:
        """
        Initialize a new PromptBase instance with an empty prompt list and conversation history.

        Example:
            >>> prompt_base = PromptBase()
            >>> prompt_base.prompt
            None
            >>> prompt_base.conversation_history
            []
        """
        self.prompt: Any = None
        self.input_history: list[str] = []
        self.output_history: list[str] = []
        self.conversation_history: list[str] = []

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
            '\\nSecond prompt'
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
        if self.prompt is not None:
            for prompt_segment in self.prompt:
                print(prompt_segment["content"])

    def conversation_prompting(
        self,
        sequence_assembler: Callable[[list[str], list[str]], str],
        current_input: str,
    ) -> str:
        """
        This method is a template for assembling the prompts for conversation-based methods
        for sequence generation. Conversation-based methods generate a new output sequence
        by interacting with the user and the LLM in a conversational manner.

        Formula:
            Y_i = f_lambda(Phi_i(X_<=i, Y<i))

        Explanation:
            - `Y_i`: The output sequence generated in the current (`i`th) iteration.
            - `f_lambda`: The LLM.
            - `Phi_i` (`sequence_assembler`): Combines:
                - `X_<=i`: Input sequences from all iterations (`inputs`).
                - `Y<i`: Output sequences from all previous iterations (`previous_outputs`).

        Args:
            sequence_assembler (callable):
                A function that takes all inputs and previous outputs and assembles
                the input for the current iteration.
            current_input (str):
                The raw current input sequence provided for the current iteration.

        Returns:
            str: The assembled input sequence for the current iteration.

        Example:
            >>> def example_sequence_assembler(inputs, past_outputs):
            ...     return " | ".join(inputs) + " | " + " | ".join(past_outputs)
            ...
            >>> processor = PromptBase()
            >>> processor.input_history = ["X0"]
            >>> processor.output_history = ["Y1", "Y2"]
            >>> current_input = "X_current"
            >>> assembled_input = processor.conversation_prompting(
            ...     sequence_assembler=example_sequence_assembler,
            ...     current_input=current_input
            ... )
            >>> print(assembled_input)
            X0 | X_current | Y1 | Y2
        """

        # Include the current input in the input history for evaluation
        inputs = deepcopy(self.input_history)
        inputs.append(current_input)

        # Use deepcopy to safely retrieve previous outputs
        previous_outputs = deepcopy(self.output_history)

        print("inputs:", inputs)
        print("previous_outputs:", previous_outputs)

        # Assemble the input using the provided assembler function
        assembled_input = sequence_assembler(inputs, previous_outputs)

        return assembled_input

    @staticmethod
    def sequence_assembler_default(inputs: list[str], previous_outputs: list[str]) -> str:
        """
        A default sequence assembler that concatenates the input and previous outputs for
        conversation-based methods with formatted separators and spacing.

        Args:
            inputs (list[str]): The input sequences from all iterations, including the current input.
            previous_outputs (list[str]): The output sequences from all previous iterations.

        Returns:
            str: The assembled input sequence for the current iteration in a nicely formatted string.

        Example:
            >>> inputs = ["What did I just say?", "Hi, my name is Tom"]
            >>> previous_outputs = ["Nice to meet you, Tom"]
            >>> result = PromptBase.sequence_assembler_default(inputs, previous_outputs)
            >>> print(result)
            ------ From the user: ------
            Hi, my name is Tom

            ------ Your response: ------
            Nice to meet you, Tom

            ------ From the user: ------
            What did I just say?
        """
        assembled_input = []

        # Combine inputs and outputs in conversation order
        for i, user_input in enumerate(inputs[:-1]):  # Include all inputs except the current
            if i > 0:
                assembled_input.append("\n------ From the user: ------")
            else:
                assembled_input.append("------ From the user: ------")
            assembled_input.append(f"\n{user_input}")

            if i < len(previous_outputs):  # Match response with user input if available
                assembled_input.append("\n------ Your response: ------")
                assembled_input.append(f"\n{previous_outputs[i]}")

        # Add the current user input
        if len(inputs) > 1:
            assembled_input.append("\n------ From the user: ------")
        else:
            assembled_input.append("------ From the user: ------")
        assembled_input.append(f"\n{inputs[-1]}")

        # Join the assembled input with newlines
        return "\n".join(assembled_input)

    def iterative_prompting(
        self,
        sequence_assembler: Callable[[str, list[str], list[any]], str],
        output_evaluator: Callable[[list[str]], list[any]],
    ) -> str:
        """
        This method is a template for assembling the prompts for iterative methods for sequence generation. Iterative
        method generates a new output sequence by assembling the input sequence for the current
        iteration based on previous iterations' outputs and their evaluations.

        The method hasn't been tested yet.

        Formula:
            Y_i = f_lambda(Phi_i(X_0, Y_<i, E(Y_<i)))

        Explanation:
            - `Y_i` is the output sequence generated in the current (`i`th) iteration.
            - `f_lambda` is the LLM.
            - `Phi_i` (`sequence_assembler`) is the mechanism that combines:
                - `X_0`: The initial input sequence
                - `Y_<i`: Output sequences from all previous iterations
                - `E(Y_<i)`: Evaluations of the output sequences from previous iterations
            - The assembled input (`assembled_input`) from `Phi_i` is passed to `f_lambda` to generate the next output.

        Args:
            sequence_assembler (callable):
                A function that takes the initial input, the list of previous outputs,
                and the list of evaluations of previous outputs, and assembles the input
                for the current iteration.
            output_evaluator (callable):
                A function that takes the list of outputs and produces evaluations for
                them.

        Returns:
            str: The assembled input sequence for the current iteration.

        Example:
            >>> def example_sequence_assembler(initial_input, previous_outputs, evaluations):
            ...     return initial_input + " | " + " | ".join(previous_outputs) + " | " + " | ".join(map(str, evaluations))
            ...
            >>> def example_output_evaluator(outputs):
            ...     return [len(output) for output in outputs]  # Simple evaluation: output length
            ...
            >>> processor = PromptBase()
            >>> processor.input_history = ["X0"]  # Initial input
            >>> processor.output_history = ["Y1", "Y2"]  # Outputs from previous iterations
            >>> assembled_input = processor.iterative_prompting(
            ...     sequence_assembler=example_sequence_assembler,
            ...     output_evaluator=example_output_evaluator
            ... )
            >>> print(assembled_input)
            X0 | Y1 | Y2 | 2 | 2
        """
        if not self.input_history or not self.output_history:
            raise ValueError("self.input_history and self.output_history must not be empty.")

        # Use deepcopy to be safe
        previous_outputs = deepcopy(self.output_history)
        evaluation_of_previous_outputs = output_evaluator(previous_outputs)

        # Assemble the input using the provided assembler function for the current iteration
        assembled_input = sequence_assembler(
            self.input_history[0],  # The initial input is the first entry in the input history
            previous_outputs,
            evaluation_of_previous_outputs,
        )

        # Return only the assembled input
        return assembled_input

    def general_interactive_prompting(
        self,
        sequence_assembler: Callable[[list[str], list[str], list[list[any], list[any]]], str],
        general_evaluator: Callable[[list[str], list[str]], list[list[any], list[any]]],
        current_input: str,
    ) -> str:
        """
        This method is a template for assembling the prompts for interactive methods in the most
        general case for sequence generation. It can be considered as a combination of
        `iterative_prompting` and `conversation_prompting`.

        The method hasn't been tested yet.

        Compared to `iterative_prompting`, it additionally
        allows other past input sequences, evaluation of the input sequences, and the current input
        sequence as elements to be assembled.

        Compared to `conversation_prompting`, it additionally allows the evaluation of the
        sequences.

        Formula:
            Y_i = f_lambda(Phi_i(X_<=i, Y_<i, E(X_<=i, Y_<i))))

        Explanation:
            - `Y_i`: The output sequence generated in the current (`i`th) iteration.
            - `f_lambda`: The LLM.
            - `Phi_i` (`sequence_assembler`): Combines:
                - `X_<=i`: Input sequences from all iterations (`inputs`).
                - `Y_<i`: Output sequences from all previous iterations (`previous_outputs`).
                - `E(X_<=i, Y_<i)`: Evaluations of the output sequences from previous iterations and
                input sequences from all iterations.

        Args:
            sequence_assembler (callable):
                A function that takes all inputs, previous outputs,
                and their evaluations, and assembles the input for the current iteration.
            general_evaluator (callable):
                A function that evaluates all inputs and past outputs, returning
                evaluations for each as a list of two elements.
            current_input (str):
                The raw current input sequence provided for the current iteration.

        Returns:
            str: The assembled input sequence for the current iteration.

        Example:
            >>> def example_sequence_assembler(inputs, past_outputs, evaluations):
            ...     inputs_eval, outputs_eval = evaluations
            ...     return " | ".join(inputs) + " | " + " | ".join(past_outputs) + " | " + " | ".join(map(str, inputs_eval)) + " | " + " | ".join(map(str, outputs_eval))
            ...
            >>> def example_general_evaluator(inputs, outputs):
            ...     inputs_eval = [len(inp) for inp in inputs]
            ...     outputs_eval = [len(out) for out in outputs]
            ...     return [inputs_eval, outputs_eval]
            ...
            >>> processor = PromptBase()
            >>> processor.input_history = ["X0"]  # Initial input history
            >>> processor.output_history = ["Y1", "Y2"]  # Outputs from previous iterations
            >>> current_input = "X_current"
            >>> assembled_input = processor.general_interactive_prompting(
            ...     sequence_assembler=example_sequence_assembler,
            ...     general_evaluator=example_general_evaluator,
            ...     current_input=current_input
            ... )
            >>> print(assembled_input)
            X0 | X_current | Y1 | Y2 | 2 | 9 | 2 | 2
        """
        # Include the current input in the input history for evaluation
        inputs = deepcopy(self.input_history)
        inputs.append(current_input)

        # Use deepcopy to safely copy outputs
        previous_outputs = deepcopy(self.output_history)

        # Evaluate all inputs and outputs together
        evaluations = general_evaluator(inputs, previous_outputs)

        # Assemble the input for the current iteration using the provided assembler function
        assembled_input = sequence_assembler(inputs, previous_outputs, evaluations)

        return assembled_input
