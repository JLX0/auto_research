from __future__ import annotations


class Prompt:
    """A class for generating prompts to automatically survey research articles.

    This class provides methods to generate various types of prompts for extracting and analyzing
    different sections of research papers, including abstract, introduction, discussion, conclusion,
    and algorithms.

    Args:
        None

    Attributes:
        general_text_cleaning:
            A list of text cleaning instructions applied across all prompt types.
        prompt:
            The formatted prompt string for GPT models. Initially empty.

    Example:
        .. testcode::

            prompt_generator = Prompt()
            prompt_generator.extract_abstract("Sample paper text...")
            prompt_generator.print_prompt()
    """

    general_text_cleaning = [
        "Your answer should not include any references marks, author information, page number, "
        "publisher information, figure captions, or table captions.",
        "Your answer should not paraphrase or summarize the text, but should be a direct extraction of text.",
    ]

    def __init__(self) -> None:
        self.prompt: str = ""

    def prompt_formatting_gpt(self, prompt: list[str]) -> list[dict[str, str]]:
        """Formats a list of prompt strings into GPT-compatible format.

        Args:
            prompt:
                A list of strings representing the prompt segments.

        Returns:
            A list of dictionaries containing role and content for GPT format.

        Example:
            .. testcode::

                prompts = ["System message 1", "System message 2"]
                formatted = Prompt().prompt_formatting_gpt(prompts)
                print(formatted[0]["role"])  # Outputs: system
        """
        for idx, n in enumerate(prompt):
            if idx > 0:
                n = "\n" + n
            prompt[idx] = {"role": "system", "content": n}
        return prompt

    def print_prompt(self) -> None:
        """Prints the content of all formatted prompts.

        Example:
            .. testcode::

                prompt = Prompt()
                prompt.extract_abstract("Sample text")
                prompt.print_prompt()
        """
        for prompt_segment in self.prompt:
            print(prompt_segment["content"])

    def extract_abstract(self, raw_text: str) -> None:
        """Generates a prompt for extracting the abstract from raw text.

        Args:
            raw_text:
                The raw text extracted from the first 2 pages of a PDF file.

        Example:
            .. testcode::

                prompt = Prompt()
                prompt.extract_abstract("Paper introduction and abstract...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the abstract from the raw text.",
            "The raw text up to the first 2 pages of the PDF file is:",
            raw_text,
            "Your answer should be the abstract of the paper",
            *self.general_text_cleaning,
            "Here is the abstract:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def extract_introduction(self, raw_text: str) -> None:
        """Generates a prompt for extracting the introduction from raw text.

        Args:
            raw_text:
                The raw text extracted from the first 5 pages of a PDF file.

        Example:
            .. testcode::

                prompt = Prompt()
                prompt.extract_introduction("First few pages of paper...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the introduction from the raw text.",
            "The raw text up to the first 5 pages of the PDF file is:",
            raw_text,
            "Your answer should be the introduction of the paper",
            (
                "Note that the paper might not have a section named 'Introduction', but the first few pages of the "
                "paper usually contain the equivalent of an introduction. For example, there might be a section named "
                "'Background' or 'Related Work' that serves as the introduction."
            ),
            (
                "If the paper has more than one sections related to the introduction, you should only include the first "
                "section that serves as the introduction."
            ),
            *self.general_text_cleaning,
            "Here is the introduction:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def extract_discussion(self, raw_text: str) -> None:
        """Generates a prompt for extracting the discussion section from raw text.

        Args:
            raw_text:
                The raw text extracted from the last 3 pages of a PDF file.

        Example:
            .. testcode::

                prompt = Prompt()
                prompt.extract_discussion("Last pages of paper...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the discussion from the raw text.",
            "The raw text of the last 3 pages of the PDF file is:",
            raw_text,
            "Your answer should be the discussion of the paper",
            (
                "Note that the paper might not have a section named 'Discussion', but the last few pages of the paper "
                "usually contain the equivalent of a discussion. For example, there might be a section named 'Analysis', "
                "'Limitations', or 'Future Work' that serves as the discussion."
            ),
            (
                "If the paper has more than one sections related to the discussion, you should only include the first "
                "section that serves as the discussion."
            ),
            (
                "If the paper does not have a discussion section, or you cannot identify the discussion section from "
                "the provided text, your answer is simply 'N/A'."
            ),
            *self.general_text_cleaning,
            "Here is the discussion:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def extract_conclusion(self, raw_text: str) -> None:
        """Generates a prompt for extracting the conclusion from raw text.

        Args:
            raw_text:
                The raw text extracted from the last 3 pages of a PDF file.

        Example:
            .. testcode::

                prompt = Prompt()
                prompt.extract_conclusion("Last pages of paper...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the conclusion from the raw text.",
            "The raw text of the last 3 pages of the PDF file is:",
            raw_text,
            "Your answer should be the conclusion of the paper",
            (
                "Note that the paper might not have a section named 'Conclusion', but the last few pages of the paper "
                "usually contain the equivalent of a conclusion. For example, there might be a section named 'Summary' "
                "or 'Concluding Remarks' that serves as the conclusion."
            ),
            (
                "If the paper has more than one sections related to the conclusion, you should only include the last "
                "section that serves as the conclusion."
            ),
            (
                "If the paper does not have a conclusion section, or you cannot identify the conclusion section from "
                "the provided text, your answer is simply 'N/A'."
            ),
            *self.general_text_cleaning,
            "Here is the conclusion:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def extract_algorithm(self, raw_text: str) -> None:
        """Generates a prompt for extracting algorithms from raw text.

        Args:
            raw_text:
                The raw text extracted from the first 12 pages of a PDF file.

        Example:
            .. testcode::

                prompt = Prompt()
                prompt.extract_algorithm("Paper content with algorithms...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the algorithm from the raw text.",
            "The raw text up to the first 12 pages of the PDF file is:",
            raw_text,
            "Your answer should be a Python list of strings that describe the algorithm in the format of pseudo-code.",
            "If the paper has more than one algorithm, your answer should be a Python list of strings, each string "
            "representing one algorithm.",
            *self.general_text_cleaning,
            "Here is the Python list:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def explain_algorithm(self, paper: str, algorithm: str) -> None:
        """Generates a prompt to explain an algorithm using paper text.

        Args:
            paper:
                The text from the first 12 pages of the paper.
            algorithm:
                The algorithm text to be explained.

        Example:
            .. testcode::

                prompt = Prompt()
                prompt.explain_algorithm("Paper text...", "Algorithm steps...")
        """
        prompt_string = [
            "Given the algorithm described in a paper, your task is to explain the algorithm by reading the first 12 "
            "pages of the paper.",
            "The first 12 pages of the paper is:",
            paper,
            "The algorithm is:",
            algorithm,
            "Your answer should include the following information:",
            "1. Meaning of each variable/part of the algorithm",
            "2. Explanation of any terms/concepts/operations that are beyond the common knowledge of an undergraduate "
            "computer science student",
            "3. A step-by-step explanation of the algorithm in layman's terms",
            "Your answer should be in the following format:",
            (
                "1. Meaning of each variable/parameter: [answer]\n\n"
                "2. Explanation of terms/concepts/operations: [answer]\n\n"
                "3. Step-by-step explanation: [answer]"
            ),
            "Each one of the [answer] should be specific enough to enable the reader to implement the algorithm using code.",
            "Here is the explanation:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def summarize_default_computer_science(
        self, abstract: str, introduction: str, discussion: str, conclusion: str
    ) -> None:
        """Generates a comprehensive summary of a computer science paper.

        Args:
            abstract:
                The paper's abstract text.
            introduction:
                The paper's introduction text.
            discussion:
                The paper's discussion text.
            conclusion:
                The paper's conclusion text.

        Example:
            .. testcode::

                prompt = Prompt()
                prompt.summarize_default_computer_science(
                    "Abstract text...",
                    "Introduction text...",
                    "Discussion text...",
                    "Conclusion text..."
                )
        """
        prompt_string = [
            "Given the abstract, introduction, discussion, and conclusion of a paper, your task is to summarize the paper.",
            "The abstract of the paper is:",
            abstract,
            "The introduction of the paper is:",
            introduction,
            "The discussion of the paper is:",
            discussion,
            "The conclusion of the paper is:",
            conclusion,
            "Your answer should include the following information:",
            "1. The main topic of the paper",
            "2. Existing problems in the field, such as limitations of previous studies or unsolved issues",
            "3. The main contributions of the paper, such as new methods or insights, especially compared to previous "
            "studies and/or baselines",
            "4. Experimental results, which include the datasets or benchmarks used, the evaluation metrics, and the "
            "comparison with previous studies and/or baselines",
            "5. Conclusions from the paper, such as the major findings, implications, and future directions",
            (
                "Your answer should be in the following format:\n\n"
                "1. The main topic: [answer]\n\n"
                "2. Existing problems: [answer]\n\n"
                "3. The main contributions: [answer]\n\n"
                "4. Experimental results: [answer]]\n\n"
                "5. Conclusions: [answer]"
            ),
            "Each one of the [answer] should have a length between 1 to 5 sentences.",
            "Each one of the [answer] should be specific.",
            "Here is the summary:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)