from __future__ import annotations

from typing import Optional

from auto_research.utils.prompter import PromptBase


class SurveyPrompt(PromptBase):
    """
    A class for generating prompts to automatically survey research articles.

    This class provides methods to generate various types of prompts for extracting and analyzing
    different sections of research papers.

    Attributes:
        general_text_cleaning (list[str]): A list of text cleaning instructions applied across all
            prompt types.

    Example:
        >>> prompt = SurveyPrompt()
        >>> prompt.extract_abstract("Sample paper text...")
        >>> print(prompt.prompt)  # Access the generated prompt
    """

    general_text_cleaning: list[str] = [
        "Your answer should not include any references marks, author information, page number, "
        "publisher information, figure captions, or table captions.",
        "Your answer should not paraphrase or summarize the text, but should be a direct "
        "extraction of text.",
    ]

    def extract_abstract(self, raw_text: str) -> None:
        """
        Generate a prompt for extracting the abstract from raw text.

        Args:
            raw_text (str): The raw text extracted from the first 2 pages of a PDF file.

        Example:
            >>> prompt = SurveyPrompt()
            >>> prompt.extract_abstract("Paper text including abstract...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the abstract.",
            "The raw text up to the first 2 pages of the PDF file is:",
            raw_text,
            "Your answer should be the abstract of the paper",
            *self.general_text_cleaning,
            "Here is the abstract:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def extract_introduction(self, raw_text: str) -> None:
        """
        Generate a prompt for extracting the introduction from raw text.

        Args:
            raw_text (str): The raw text extracted from the first 5 pages of a PDF file.

        Example:
            >>> prompt = SurveyPrompt()
            >>> prompt.extract_introduction("Paper text including introduction...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the "
            "introduction.",
            "The raw text up to the first 5 pages of the PDF file is:",
            raw_text,
            "Your answer should be the introduction of the paper",
            (
                "Note that the paper might not have a section named 'Introduction', but the first "
                "few pages usually contain the equivalent. For example, there might be a section "
                "named 'Background' or 'Related Work' that serves as the introduction."
            ),
            (
                "If the paper has more than one section related to the introduction, you should "
                "only include the first section that serves as the introduction."
            ),
            *self.general_text_cleaning,
            "Here is the introduction:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def extract_discussion(self, raw_text: str) -> None:
        """
        Generate a prompt for extracting the discussion section from raw text.

        Args:
            raw_text (str): The raw text extracted from the last 3 pages of a PDF file.

        Example:
            >>> prompt = SurveyPrompt()
            >>> prompt.extract_discussion("Paper text including discussion...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the "
            "discussion.",
            "The raw text of the last 3 pages of the PDF file is:",
            raw_text,
            "Your answer should be the discussion of the paper",
            (
                "Note that the paper might not have a section named 'Discussion', but the last "
                "few pages usually contain the equivalent. For example, there might be a section "
                "named 'Analysis', 'Limitations', or 'Future Work' that serves as the discussion."
            ),
            (
                "If the paper has more than one section related to the discussion, you should "
                "only include the first section that serves as the discussion."
            ),
            (
                "If the paper does not have a discussion section, or you cannot identify the "
                "discussion section from the provided text, your answer is simply 'N/A'."
            ),
            *self.general_text_cleaning,
            "Here is the discussion:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def extract_conclusion(self, raw_text: str) -> None:
        """
        Generate a prompt for extracting the conclusion from raw text.

        Args:
            raw_text (str): The raw text extracted from the last 3 pages of a PDF file.

        Example:
            >>> prompt = SurveyPrompt()
            >>> prompt.extract_conclusion("Paper text including conclusion...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the "
            "conclusion.",
            "The raw text of the last 3 pages of the PDF file is:",
            raw_text,
            "Your answer should be the conclusion of the paper",
            (
                "Note that the paper might not have a section named 'Conclusion', but the last "
                "few pages usually contain the equivalent. For example, there might be a section "
                "named 'Summary' or 'Concluding Remarks' that serves as the conclusion."
            ),
            (
                "If the paper has more than one section related to the conclusion, you should "
                "only include the last section that serves as the conclusion."
            ),
            (
                "If the paper does not have a conclusion section, or you cannot identify the "
                "conclusion section from the provided text, your answer is simply 'N/A'."
            ),
            *self.general_text_cleaning,
            "Here is the conclusion:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def extract_algorithm(self, raw_text: str) -> None:
        """
        Generate a prompt for extracting algorithms from raw text.

        Args:
            raw_text (str): The raw text extracted from the first 12 pages of a PDF file.

        Example:
            >>> prompt = SurveyPrompt()
            >>> prompt.extract_algorithm("Paper text including algorithms...")
        """
        prompt_string = [
            "Given some raw text extracted from a PDF file, your task is to extract the "
            "algorithm.",
            "The raw text up to the first 12 pages of the PDF file is:",
            raw_text,
            "Your answer should be a Python list of strings that describe the algorithm in "
            "pseudo-code format.",
            (
                "If the paper has more than one algorithm, your answer should be a Python list "
                "of strings, each string representing one algorithm."
            ),
            *self.general_text_cleaning,
            "Here is the Python list:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def explain_algorithm(self, paper: str, algorithm: str) -> None:
        """
        Generate a prompt to explain an algorithm using paper text.

        Args:
            paper (str): The text from the first 12 pages of the paper.
            algorithm (str): The algorithm text to be explained.

        Example:
            >>> prompt = SurveyPrompt()
            >>> prompt.explain_algorithm("Paper text...", "Algorithm description...")
        """
        prompt_string = [
            "Given the algorithm described in a paper, your task is to explain the algorithm "
            "by reading the first 12 pages of the paper.",
            "The first 12 pages of the paper is:",
            paper,
            "The algorithm is:",
            algorithm,
            "Your answer should include the following information:",
            "1. Meaning of each variable/part of the algorithm",
            "2. Explanation of any terms/concepts/operations that are beyond the common "
            "knowledge of an undergraduate computer science student",
            "3. A step-by-step explanation of the algorithm in layman's terms",
            "Your answer should be in the following format:",
            (
                "1. Meaning of each variable/parameter: [answer]\n\n"
                "2. Explanation of terms/concepts/operations: [answer]\n\n"
                "3. Step-by-step explanation: [answer]"
            ),
            (
                "Each one of the [answer] should be specific enough to enable the reader to "
                "implement the algorithm using code."
            ),
            "Here is the explanation:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def summarize_default_computer_science(
        self,
        abstract: str,
        introduction: str,
        discussion: str,
        conclusion: str,
    ) -> None:
        """
        Generate a prompt to comprehensively summarize a computer science paper.

        Args:
            abstract (str): The paper's abstract text.
            introduction (str): The paper's introduction text.
            discussion (str): The paper's discussion text.
            conclusion (str): The paper's conclusion text.

        Example:
            >>> prompt = SurveyPrompt()
            >>> prompt.summarize_default_computer_science(
            ...     "Abstract text...",
            ...     "Introduction text...",
            ...     "Discussion text...",
            ...     "Conclusion text...",
            ... )
        """
        prompt_string = [
            "Given the abstract, introduction, discussion, and conclusion of a paper, your "
            "task is to summarize the paper.",
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
            (
                "2. Existing problems in the field, such as limitations of previous studies or "
                "unsolved issues"
            ),
            (
                "3. The main contributions of the paper, such as new methods or insights, "
                "especially compared to previous studies and/or baselines"
            ),
            (
                "4. Experimental results, including datasets, benchmarks, evaluation metrics, "
                "and comparison with previous studies"
            ),
            (
                "5. Conclusions from the paper, such as major findings, implications, and "
                "future directions"
            ),
            (
                "Your answer should be in the following format:\n\n"
                "1. The main topic: [answer]\n\n"
                "2. Existing problems: [answer]\n\n"
                "3. The main contributions: [answer]\n\n"
                "4. Experimental results: [answer]\n\n"
                "5. Conclusions: [answer]"
            ),
            "Each one of the [answer] should have a length between 1 to 5 sentences.",
            "Each one of the [answer] should be specific.",
            "Here is the summary:",
        ]
        self.prompt = self.prompt_formatting_gpt(prompt_string)

    def explain_default_computer_science(
        self,
        abstract: str,
        introduction: str,
        discussion: str,
        conclusion: str,
        user_question: str,
        past_response: Optional[str],
    ) -> None:
        """
        Generate a prompt to comprehensively explain a computer science paper. This method keeps
        the user's question and the LLM's response from the past conversation.

        Args:
            abstract (str): The paper's abstract text.
            introduction (str): The paper's introduction text.
            discussion (str): The paper's discussion text.
            conclusion (str): The paper's conclusion text.
            user_question (str): The user's question about the paper.
            past_response (Optional[str]): The LLM's response from the past conversation.

        Example:
            >>> prompt = SurveyPrompt()
            >>> prompt.explain_default_computer_science(
            ...     "Abstract text...",
            ...     "Introduction text...",
            ...     "Discussion text...",
            ...     "Conclusion text...",
            ...     "User question...",
            ...     "Past response...",
            ... )
        """
        self.append_to_conversation(past_response, user_question)

        prompt_string = [
            "Given the abstract, introduction, discussion, and conclusion of a paper, your "
            "task is to explain the paper based on the user's question.",
            "The abstract of the paper is:",
            abstract,
            "The introduction of the paper is:",
            introduction,
            "The discussion of the paper is:",
            discussion,
            "The conclusion of the paper is:",
            conclusion,
        ]

        prompt_string += self.conversation_history

        prompt_string += [
            "Here is the explanation:",
        ]

        self.prompt = self.prompt_formatting_gpt(prompt_string)
