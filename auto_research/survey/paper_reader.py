from __future__ import annotations

from typing import Optional

import fitz
from PyPDF2 import PdfReader
import tiktoken


class Paper:
    """
    A class for reading and extracting information from research articles in PDF format.

    This class provides functionality to read PDF files using different libraries (PyPDF2 and
    PyMuPDF), extract specific sections, and analyze the content of research papers.

    Args:
        paper_path: Path to the PDF file containing the research paper.
        model: Name of the GPT model to use for token counting. Defaults to 'gpt-4o-mini'.

    Attributes:
        paper_path: Path to the PDF file.
        whole_paper: List containing the text content of each page.
        paper_length: Total number of tokens in the paper based on the specified model.
        model: Name of the GPT model used for token counting.
        extracted_information: Dictionary containing extracted sections of the paper.

    Example:
        >>> paper = Paper("example.pdf", model="gpt-4")
        >>> paper.read_pymupdf()
        >>> paper.calculate_token_length()
        >>> print(paper.paper_length)
        1234

    Notes:
        The class supports both PyPDF2 and PyMuPDF (fitz) for PDF processing,
        allowing flexibility in PDF parsing approaches.
    """

    # Class-level constants for section markers
    _END_MARKERS: list[str] = ["references", "acknowledgement", "bibliography"]

    def __init__(self, paper_path: str, model: str = "gpt-4o-mini") -> None:
        """Initialize the Paper instance with the given PDF path and model."""
        self.paper_path: str = paper_path
        self.whole_paper: list[str] = []
        self.paper_length: int = 0
        self.model: str = model
        self.extracted_information: dict[str, str] = {
            "abstract": "",
            "introduction": "",
            "discussion": "",
            "conclusion": "",
            "algorithm": "",
        }

    def read_pypdf2(self) -> None:
        """
        Read PDF content using PyPDF2 library.

        This method extracts text from each page of the PDF using PyPDF2 and stores
        it in the whole_paper list.

        Example:
            >>> paper = Paper("example.pdf")
            >>> paper.read_pypdf2()
        """
        pdf_obj = PdfReader(self.paper_path)
        self.whole_paper = []
        for page in pdf_obj.pages:
            text = page.extract_text()
            self.whole_paper.append(text)

    def read_pymupdf(self) -> None:
        """
        Read PDF content using PyMuPDF library.

        This method extracts text from each page of the PDF using PyMuPDF (fitz)
        and stores it in the whole_paper list.

        Example:
            >>> paper = Paper("example.pdf")
            >>> paper.read_pymupdf()
        """
        pdf_document = fitz.open(self.paper_path)
        self.whole_paper = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            self.whole_paper.append(text)

    def first_n_pages(self, n: int) -> str:
        """
        Return the concatenated text of the first n pages.

        Args:
            n: Number of pages to include.

        Returns:
            str: Concatenated text of the first n pages.

        Example:
            >>> paper = Paper("example.pdf")
            >>> paper.read_pymupdf()
            >>> first_three = paper.first_n_pages(3)
        """
        return "".join(self.whole_paper[:n])

    def get_whole_paper(self , print_mode: bool = False) -> None | str :
        """
        Print the entire paper content with page markers or return it as a formatted string.

        This method either prints the content of each page with clear beginning and
        ending markers for better visualization or returns the entire content as a
        single string in the same format.

        Args:
            print_mode (bool): If True, print the content. If False, return the content as a formatted string.

        Example:
            >>> paper = Paper("example.pdf")
            >>> paper.read_pymupdf()
            >>> paper.get_whole_paper(print_mode=True)  # Prints the content
            >>> full_text = paper.get_whole_paper(print_mode=False)  # Returns the content as a formatted string
        """
        result = []
        for idx , text in enumerate(self.whole_paper) :
            page_content = f"-----Page {idx + 1} beginning marker-----\n{text}\n-----Page {idx + 1} ending marker-----"
            result.append(page_content)

        formatted_string = "\n".join(result)

        if print_mode :
            print(formatted_string)
        else :
            return formatted_string

    @staticmethod
    def extract_up_to_first_match_exclude_list(a: list[str], b_list: list[str]) -> list[str]:
        """
        Extract content up to the first occurrence of any marker in the exclude list.

        Args:
            a: List of strings to concatenate and search within.
            b_list: List of substrings to search for.

        Returns:
            list[str]: List of strings from input up to but not including the first
            occurrence of any substring in b_list.

        Example:
            >>> text_list = ["Page 1", "Page 2", "References", "Page 3"]
            >>> result = Paper.extract_up_to_first_match_exclude_list(text_list, ["references"])
        """
        concatenated_a = "".join(a)
        first_three_pages = "".join(a[:3])
        lower_concatenated_a = concatenated_a.lower()

        first_index: Optional[int] = None
        for b in b_list:
            lower_b = b.lower()
            index = lower_concatenated_a.find(lower_b)
            if (
                index != -1
                and (index > len(first_three_pages))
                and (first_index is None or index < first_index)
            ):
                first_index = index

        if first_index is not None:
            extracted_string = concatenated_a[:first_index]
        else:
            extracted_string = concatenated_a

        result: list[str] = []
        current_string = ""
        for char in extracted_string:
            current_string += char
            if current_string in a:
                result.append(current_string)
                current_string = ""

        if current_string:
            result.append(current_string)

        return result

    def extract_ending_pages(self, page_number: int = 3) -> str:
        """
        Extract the specified number of ending pages before references section.

        Args:
            page_number: Number of pages to extract from the end. Defaults to 3.

        Returns:
            str: Concatenated text of the specified number of ending pages.

        Example:
            >>> paper = Paper("example.pdf")
            >>> paper.read_pymupdf()
            >>> ending_pages = paper.extract_ending_pages(2)
        """
        ending_pages = self.extract_up_to_first_match_exclude_list(
            self.whole_paper, self._END_MARKERS
        )
        ending_pages = ending_pages[-page_number:]
        return "".join(ending_pages)

    def calculate_token_length(self) -> None:
        """
        Calculate the total number of tokens in the paper using the specified model.

        This method uses the tiktoken library to encode and count tokens according
        to the specified model's tokenization scheme.

        Example:
            >>> paper = Paper("example.pdf")
            >>> paper.read_pymupdf()
            >>> paper.calculate_token_length()
        """
        encoder = tiktoken.encoding_for_model(self.model)
        self.paper_length = 0
        for text in self.whole_paper:
            length = len(encoder.encode(text))
            self.paper_length += length
