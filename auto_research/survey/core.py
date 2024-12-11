from __future__ import annotations

from typing import Optional

from auto_research.survey.paper_reader import Paper
from auto_research.survey.prompts import SurveyPrompt
from auto_research.utils.inquiry import GPT


class AutoSurvey:
    """
    A class for automating the process of surveying research papers.

    This class integrates and streamlines functionalities for analyzing research papers,
    including text extraction, summarization, algorithm analysis, and explanation.

    Args:
        api_key (str): The API key for GPT model access.
        model (str): The GPT model identifier to use.
        paper_path (str): Path to the research paper PDF file.
        debug (bool, optional): Enable debug mode for detailed logging. Defaults to False.
        mode (str, optional): Analysis mode to use. Supports "summarize_computer_science",
            "explain_computer_science", and "explain_algorithm". Defaults to
            "summarize_computer_science".

    Attributes:
        gpt_instance (GPT): Instance of GPT handler for text processing.
        paper_path (str): Path to the research paper being analyzed.
        paper_instance (Paper): Instance of Paper class for PDF processing.
        prompt_instance (SurveyPrompt): Instance for generating prompts.
        mode (str): Current analysis mode.
        output (Optional[str]): Storage for analysis results.
        ending_pages (Optional[str]): Content of the paper's final pages.

    Example:
        >>> survey = AutoSurvey(
        ...     api_key="your-api-key", model="gpt-4", paper_path="path/to/paper.pdf"
        ... )
        >>> survey.run()
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        paper_path: str,
        debug: bool = False,
        mode: str = "summarize_computer_science",
    ) -> None:
        self.gpt_instance = GPT(api_key, model=model, debug=debug)
        self.paper_path = paper_path
        self.paper_instance = Paper(paper_path, model=model)
        self.paper_instance.read_pymupdf()
        self.prompt_instance = SurveyPrompt()
        self.mode = mode
        self.output: Optional[str] = None
        self.ending_pages: Optional[str] = None
        self.paper_instance.extracted_information = {
            "abstract": "",
            "introduction": "",
            "discussion": "",
            "conclusion": "",
            "algorithm": "",
        }

    def run(self) -> None:
        """
        Execute the paper analysis based on the selected mode.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.run()
        """
        if self.mode == "summarize_computer_science":
            print(f"Begin analyzing the article located at {self.paper_path}")
            self.extraction()
            self.summarize_computer_science()
            print("The summary is:")
            print()
            print(self.output)
        elif self.mode == "explain_computer_science":
            print(f"Begin analyzing the article located at {self.paper_path}")
            self.extraction()
            self.explain_computer_science()
        elif self.mode == "explain_algorithm":
            self.extract_algorithm()
            self.explain_algorithm()

    def extract_algorithm(self) -> None:
        """
        Extract algorithm descriptions from the paper.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.extract_algorithm()
        """
        raw_text = self.paper_instance.first_n_pages(12)
        self.prompt_instance.extract_algorithm(raw_text)
        response = self.gpt_instance.ask(self.prompt_instance.prompt)
        print(response)
        if response:
            self.paper_instance.extracted_information["algorithm"] = response

    def explain_algorithm(self) -> None:
        """
        Generate explanations for extracted algorithms.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.explain_algorithm()
        """
        self.prompt_instance.explain_algorithm(
            self.paper_instance.first_n_pages(12),
            self.paper_instance.extracted_information["algorithm"],
        )
        print(self.gpt_instance.ask(self.prompt_instance.prompt))

    def review(self) -> None:
        """Review the paper content (placeholder for future implementation)."""
        pass

    def extraction(self) -> None:
        """
        Extract main sections from the paper.

        This method coordinates the extraction of abstract, introduction,
        discussion, and conclusion sections.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.extraction()
        """
        self.extract_abstract()
        self.extract_introduction()
        ending_pages = self.paper_instance.extract_ending_pages(3)
        if ending_pages:
            self.ending_pages = ending_pages
            self.extract_discussion()
            self.extract_conclusion()

    def extract_abstract(self) -> None:
        """
        Extract the abstract section from the paper.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.extract_abstract()
        """
        print("---extracting abstract---")
        raw_text = self.paper_instance.first_n_pages(2)
        self.prompt_instance.extract_abstract(raw_text)
        response = self.gpt_instance.ask(self.prompt_instance.prompt)
        if response:
            self.paper_instance.extracted_information["abstract"] = response

    def extract_introduction(self) -> None:
        """
        Extract the introduction section from the paper.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.extract_introduction()
        """
        print("---extracting introduction---")
        raw_text = self.paper_instance.first_n_pages(5)
        self.prompt_instance.extract_introduction(raw_text)
        response = self.gpt_instance.ask(self.prompt_instance.prompt)
        if response:
            self.paper_instance.extracted_information["introduction"] = response

    def extract_discussion(self) -> None:
        """
        Extract the discussion section from the paper.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.extract_discussion()
        """
        print("---extracting discussion---")
        if self.ending_pages:
            self.prompt_instance.extract_discussion(self.ending_pages)
            response = self.gpt_instance.ask(self.prompt_instance.prompt)
            if response:
                self.paper_instance.extracted_information["discussion"] = response

    def extract_conclusion(self) -> None:
        """
        Extract the conclusion section from the paper.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.extract_conclusion()
        """
        print("---extracting conclusion---")
        if self.ending_pages:
            self.prompt_instance.extract_conclusion(self.ending_pages)
            response = self.gpt_instance.ask(self.prompt_instance.prompt)
            if response:
                self.paper_instance.extracted_information["conclusion"] = response

    def summarize_computer_science(self) -> None:
        """
        Generate a summary of computer science papers.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.summarize_computer_science()
        """
        print("---summarizing---")
        self.prompt_instance.summarize_default_computer_science(
            self.paper_instance.extracted_information["abstract"],
            self.paper_instance.extracted_information["introduction"],
            self.paper_instance.extracted_information["discussion"],
            self.paper_instance.extracted_information["conclusion"],
        )
        self.output = self.gpt_instance.ask(self.prompt_instance.prompt)

    def explain_computer_science(self) -> None:
        """
        Generate explanations for computer science papers.

        This method allows the user to input questions about the paper, then sends
        the paper content and the question to the LLM for an answer. The process
        loops until the user cancels it.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.explain_computer_science()
        """
        response = None
        while True:
            print("Please input your question (type 'exit' to quit):")
            question = input()
            if question.lower() == "exit":
                break

            self.prompt_instance.explain_default_computer_science(
                self.paper_instance.extracted_information["abstract"],
                self.paper_instance.extracted_information["introduction"],
                self.paper_instance.extracted_information["discussion"],
                self.paper_instance.extracted_information["conclusion"],
                question,
                response,
            )
            response = self.gpt_instance.ask(self.prompt_instance.prompt)
            print(response)

    def findings(self) -> None:
        """Extract key findings from the paper (placeholder for future implementation)."""
        pass
