from __future__ import annotations

from typing import Optional

from LLM_utils.inquiry import OpenAI_interface

from auto_research.survey.paper_reader import Paper
from auto_research.survey.prompts import SurveyPrompt
from auto_research.utils.stored_info import Storage


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
            "explain_computer_science", "explain_algorithm", and "information_retrieval".
            Defaults to "summarize_computer_science".
        approach (str, optional): Approach to use for extraction. Supports "load" and "new_trial".
            Defaults to "load".
        storage_path (str, optional): Path to the storage file for saving extracted information.
            Defaults to "papers.json".

    Attributes:
        OpenAI_instance (OpenAI_interface): Instance of GPT handler for text processing.
        paper_path (str): Path to the research paper being analyzed.
        paper_name (str): Name of the research paper file.
        paper_instance (Paper): Instance of Paper class for PDF processing.
        prompt_instance (SurveyPrompt): Instance for generating prompts.
        mode (str): Current analysis mode.
        approach (str): Current extraction approach.
        output (Optional[str]): Storage for analysis results.
        ending_pages (Optional[str]): Content of the paper's final pages.
        storage_instance (Storage): Instance for storing and retrieving extracted information.
        cost_accumulation (float): Accumulated cost of API usage.

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
        approach: str = "load",
        storage_path: str = "papers.json",
    ) -> None:

        self.OpenAI_instance = OpenAI_interface(api_key, model=model, debug=debug)
        self.paper_path = paper_path
        self.paper_name = paper_path.split("/")[-1]
        self.paper_instance = Paper(paper_path, model=model)
        self.paper_instance.read_pymupdf()
        self.prompt_instance = SurveyPrompt()
        self.mode = mode
        self.approach = approach
        self.output: Optional[str] = None
        self.ending_pages: Optional[str] = None
        self.paper_instance.extracted_information = {
            "abstract": "",
            "introduction": "",
            "discussion": "",
            "conclusion": "",
            "algorithm": "",
        }
        self.storage_instance = Storage(storage_path)
        self.cost_accumulation = 0

    def run(self, target_information: Optional[str] = None, tests: Optional[list] = None) -> None:
        """
        Execute the paper analysis based on the selected mode.

        Args:
            target_information (Optional[str]): Specific information to retrieve when mode is
            "information_retrieval".
            tests (Optional[list]): List of tests to run when sending inquiries.

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
        elif self.mode == "information_retrieval":
            if target_information is None:
                raise ValueError(
                    "target_information cannot be None when mode is 'information_retrieval'"
                )
            self.information_retrieval(target_information, tests)
            print("The retrieved information is:")
            print()
            print(self.output)

        print(f"The total cost is {self.cost_accumulation} USD")

    def send_inquiry(self, tests: Optional[list] = None) -> str:
        """
        Send an inquiry to the GPT model.

        Args:
            tests (Optional[list]): List of tests to run when sending inquiries.

        Returns:
            str: The response from the GPT model.
        """
        if tests:
            response, cost = self.OpenAI_instance.ask_with_test(self.prompt_instance.prompt, tests)
        else:
            response, cost = self.OpenAI_instance.ask(self.prompt_instance.prompt)
        self.cost_accumulation += cost
        return response

    def information_retrieval(self, target_information: str, tests: Optional[list] = None) -> None:
        """
        Retrieve specific information from the paper.

        Args:
            target_information (str): The specific information to retrieve.
            tests (Optional[list]): List of tests to run when sending inquiries.
        """
        if target_information is None:
            raise ValueError("target_information cannot be None")

        raw_text = self.paper_instance.get_whole_paper()
        if raw_text is None:
            raise ValueError("Failed to extract text from the paper. raw_text is None.")

        self.prompt_instance.information_retrieval(raw_text, target_information)
        self.output = self.send_inquiry(tests)

        self.storage_instance.add_info_to_a_paper(
            self.paper_name, f"information_retrieval:{target_information}", self.output
        )

    def extract_algorithm(self) -> None:
        """
        Extract algorithm descriptions from the paper.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.extract_algorithm()
        """
        raw_text = self.paper_instance.first_n_pages(12)
        self.prompt_instance.extract_algorithm(raw_text)
        response = self.send_inquiry()
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
        print(self.OpenAI_instance.ask(self.prompt_instance.prompt))

    def review(self) -> None:
        """Review the paper content (placeholder for future implementation)."""
        pass

    def extraction_key_information(self) -> None:
        """Extract key information from the paper, including abstract, introduction, discussion,
        and conclusion."""
        print("Extracting from paper.")
        self.extract_abstract()
        self.extract_introduction()
        ending_pages = self.paper_instance.extract_ending_pages(3)
        if ending_pages:
            self.ending_pages = ending_pages
            self.extract_discussion()
            self.extract_conclusion()

    def extraction(self) -> None:
        """
        Extract main sections from the paper.

        This method coordinates the extraction of abstract, introduction,
        discussion, and conclusion sections.

        Example:
            >>> survey = AutoSurvey(api_key, model, paper_path)
            >>> survey.extraction()
        """
        if self.approach == "load":
            self.storage_instance.load_info()
            try:
                abstract = self.storage_instance.information[self.paper_name]["abstract"]
                abstract = Storage.get_latest_trial(abstract)
                self.paper_instance.extracted_information["abstract"] = abstract
                introduction = self.storage_instance.information[self.paper_name]["introduction"]
                introduction = Storage.get_latest_trial(introduction)
                self.paper_instance.extracted_information["introduction"] = introduction
                discussion = self.storage_instance.information[self.paper_name]["discussion"]
                discussion = Storage.get_latest_trial(discussion)
                self.paper_instance.extracted_information["discussion"] = discussion
                conclusion = self.storage_instance.information[self.paper_name]["conclusion"]
                conclusion = Storage.get_latest_trial(conclusion)
                self.paper_instance.extracted_information["conclusion"] = conclusion
                print("Summary information loaded from storage.")
            except KeyError:
                print("Summary information not found in storage")
                self.extraction_key_information()
            except FileNotFoundError:
                print("Storage file not found")
                self.extraction_key_information()
        if self.approach == "new_trial":
            self.extraction_key_information()

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
        response = self.send_inquiry()
        if response:
            self.paper_instance.extracted_information["abstract"] = response
            self.storage_instance.add_info_to_a_paper(self.paper_name, "abstract", response)

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
        response = self.send_inquiry()
        if response:
            self.paper_instance.extracted_information["introduction"] = response
            self.storage_instance.add_info_to_a_paper(self.paper_name, "introduction", response)

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
            response = self.send_inquiry()
            if response:
                self.paper_instance.extracted_information["discussion"] = response
                self.storage_instance.add_info_to_a_paper(self.paper_name, "discussion", response)

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
            response = self.send_inquiry()
            if response:
                self.paper_instance.extracted_information["conclusion"] = response
                self.storage_instance.add_info_to_a_paper(self.paper_name, "conclusion", response)

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

        self.output = self.send_inquiry()
        # TODO: change the output style

        self.storage_instance.add_info_to_a_paper(self.paper_name, "summary", self.output)

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

            response = self.send_inquiry()

            self.prompt_instance.input_history.append(question)
            self.prompt_instance.output_history.append(response)

            print(response)

    def findings(self) -> None:
        """Extract key findings from the paper (placeholder for future implementation)."""
        raise NotImplementedError
