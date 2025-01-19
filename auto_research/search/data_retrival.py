from __future__ import annotations

import os
from typing import Optional
from typing import Tuple

import arxiv
import requests
from requests.exceptions import RequestException
from requests.exceptions import Timeout

from auto_research.search.files_management import is_pdf_uncorrupted


def download_pdf(url: str, filename: str, folder: Optional[str] = None, timeout: int = 10) -> bool:
    """
    Downloads a PDF file from the specified URL and saves it to the given filename and folder.

    Args:
        url (str): The URL of the PDF file to download.
        filename (str): The name of the file to save the PDF as.
        folder (Optional[str]): The folder to save the PDF in. If None, saves in the current
        directory.
        timeout (int): The timeout for the request in seconds. Defaults to 10.

    Returns:
        bool: True if the download was successful and the file is not corrupted, False otherwise.

    Example:
        >>> download_pdf("http://example.com/sample.pdf", "sample.pdf", folder="pdfs")
        Downloaded: sample.pdf
        True
    """
    try:
        print(f"Downloading {filename}... with upper time limit: {timeout} seconds")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Check if the request was successful.

        # Create the folder if it doesn't exist and construct the file path.
        if folder is not None:
            os.makedirs(folder, exist_ok=True)
            file_path = os.path.join(folder, filename)
        else:
            file_path = filename

        # Save the PDF file.
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}.")

        # Check if the downloaded PDF file is uncorrupted.
        if not is_pdf_uncorrupted(file_path):
            print(f"The downloaded PDF file '{filename}' is corrupted.")
            os.remove(file_path)  # Delete the corrupted file.
            print(f"File removed: {filename}")
            return False
    except Timeout:
        print(f"Timeout occurred while downloading {filename} from {url}")
        return False
    except RequestException as e:
        print(f"Failed to download {filename} from {url}: {e}")
        return False
    return True


def get_paper_details_from_semantic_scholar(
    title: str, verbose: bool = False
) -> Optional[Tuple[str, str]]:
    """
    Retrieves paper details (abstract and venue) from Semantic Scholar based on the paper title.

    Args:
        title (str): The title of the paper to search for.
        verbose (bool): If True, prints error messages. Defaults to False.

    Returns:
        Optional[Tuple[str, str]]: A tuple containing the abstract and venue of the paper.
        Returns None if no data is found or if an error occurs.

    Example:
        >>> get_paper_details_from_semantic_scholar("Attention is All You Need")
        ("Abstract text...", "NeurIPS")
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": title, "fields": "title,abstract,venue"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            paper = data["data"][0]
            abstract = paper.get("abstract", "Abstract not available")
            venue = paper.get("venue", "Venue not available")
            return abstract, venue
    elif verbose:
        print(f"Error: {response.status_code}")
    return None


def get_arxiv_paper_details(title: str) -> Optional[Tuple[str, str, str, str]]:
    """
    Retrieves paper details (title, abstract, PDF link, and venue) from arXiv based on the paper
    title.

    Args:
        title (str): The title of the paper to search for.

    Returns:
        Optional[Tuple[str, str, str, str]]: A tuple containing the paper title, abstract, PDF
        link,and venue. Returns None if no data is found.

    Example:
        >>> get_arxiv_paper_details("Attention is All You Need")
        ("Attention is All You Need", "Abstract text...", "http://arxiv.org/pdf/...", "arXiv")
    """
    client = arxiv.Client()
    search = arxiv.Search(query=title, max_results=1, sort_by=arxiv.SortCriterion.Relevance)
    results = client.results(search)
    for result in results:
        paper_title = result.title
        abstract = result.summary
        pdf_link = result.pdf_url
        venue = result.journal_ref if result.journal_ref else "arXiv"
        return paper_title, abstract, pdf_link, venue
    return None
