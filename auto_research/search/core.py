from __future__ import annotations

import datetime
import os
import shutil
import time
import traceback
from typing import Any

from scholarly import scholarly
from tqdm import tqdm

from auto_research.search.data_retrival import download_pdf
from auto_research.search.data_retrival import get_arxiv_paper_details
from auto_research.search.data_retrival import get_paper_details_from_semantic_scholar
from auto_research.search.files_management import sanitize_filename
from auto_research.search.information import extract_exact_date
from auto_research.search.information import save_meta_data


class AutoSearch:
    r"""
    A class to search for academic papers by keyword(s), retrieve their details, and optionally
    download them.

    Attributes:
        keywords (str | list[str]): The keyword(s) to search for. If a string, performs a single
        search.
            If a list, performs multiple searches.
        num_results (int): The number of results to retrieve.
        delay (int): Added delay (in seconds) between requests to avoid rate limiting.
        sort_by (str): Sorting criteria for the Google Scholar search engine ("date" or
        "relevance").
        date_cutoff (str): The cutoff date for papers when sorting by date (format: "YYYY-MM-DD").
        score_threshold (float): The minimum combined score for papers to be displayed/downloaded.
            The combined score is calculated differently based on the sorting criteria:
            - If sorting by "date":
              \[
              \text{combined\_score} = \frac{\text{citation\_count}}{\left(\frac{365 +
              \text{days\_ago}}{365}\right)^{\text{recency\_weight}}}
              \]
              where `days_ago` is the number of days since the paper was published.
            - If sorting by "relevance":
              \[
              \text{combined\_score} = \frac{\text{citation\_count}}{\text{recency}
              ^{\text{recency\_weight}}}
              \]
              where `recency` is the number of years since the paper was published.
            The `recency_weight` parameter controls how much weight is given to the recency
             of the paper.
        recency_weight (float): The weight given to recency when calculating the combined score.
        auto_destination (bool): Whether to automatically generate the destination folder name.
        destination_folder (str): The folder where downloaded papers will be saved.
        zip_folder (bool): Whether to zip the downloaded papers.

    Example:
        >>> search = AutoSearch("machine learning", num_results=10)
        >>> search.run()
    """

    def __init__(
        self,
        keywords: str | list[str],
        num_results: int = 30,
        delay: int = 1,
        sort_by: str = "relevance",
        date_cutoff: str = "2024-01-01",
        score_threshold: float = 0.5,
        recency_weight: float = 3.5,
        auto_destination: bool = False,
        destination_folder: str = "search_results",
        zip_folder: bool = True,
    ) -> None:
        """
        Initialize the AutoSearch class with the given parameters.

        Args:
            keywords (str | list[str]): The keyword(s) to search for.
            num_results (int): The number of results to retrieve.
            delay (int): Delay between requests.
            sort_by (str): Sorting criteria ("date" or "relevance").
            date_cutoff (str): Cutoff date for date-based search (format: "YYYY-MM-DD").
            score_threshold (float): Minimum combined score for papers.
            recency_weight (float): Weight for recency in combined score calculation.
            auto_destination (bool): Whether to auto-generate the destination folder name.
            destination_folder (str): Folder to save downloaded papers.
            zip_folder (bool): Whether to zip the downloaded papers.
        """
        self.keywords = keywords
        self.num_results = num_results
        self.delay = delay
        self.sort_by = sort_by
        self.date_cutoff = date_cutoff
        self.score_threshold = score_threshold
        self.recency_weight = recency_weight
        self.auto_destination = auto_destination
        self.destination_folder = destination_folder
        self.zip_folder = zip_folder

    def search_papers_by_keyword(self, keyword: str) -> list[dict[str, Any]]:
        """
        Search for papers by a given keyword and retrieve their details.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing paper details.

        Example:
            >>> search = AutoSearch("machine learning")
            >>> papers = search.search_papers_by_keyword("machine learning")
            >>> len(papers) > 0
            True
        """
        search_query = scholarly.search_pubs(keyword, sort_by=self.sort_by)
        papers_info: list[dict[str, Any]] = []

        if self.sort_by == "date":
            print(f"Begin searching all papers up until {self.date_cutoff}")
            date_cutoff = datetime.datetime.strptime(self.date_cutoff, "%Y-%m-%d").date()
            disable = False  # Enable progress bar for date-based search
            total = None  # No total for date-based search
        else:
            disable = False
            total = self.num_results  # Total number of results for non-date-based search

        # Initialize tqdm progress bar
        with tqdm(total=total, desc="Searching papers", disable=disable) as pbar:
            count = 0
            try:
                for paper in search_query:
                    title = paper.get("bib", {}).get("title", "Title not available")
                    citation_count = paper.get("num_citations", 0)
                    publication_year = paper.get("bib", {}).get(
                        "pub_year", datetime.datetime.now().year
                    )
                    authors = paper.get("bib", {}).get("author", "Authors not available")
                    venue = paper.get("bib", {}).get("venue", "Venue not available")

                    # Handle date-based search
                    if self.sort_by == "date":
                        date = extract_exact_date(paper)
                        if date is None:
                            # Skip this paper if no valid date is found
                            continue
                        if date < date_cutoff:  # Stop if the paper is older than the cutoff date
                            break

                    # Format authors if they are in a list
                    if isinstance(authors, list):
                        authors = ", ".join(authors)

                    # Get the paper's link
                    link = paper.get("eprint_url", paper.get("pub_url", "Link not available"))

                    # Ensure publication_year is an integer
                    if isinstance(publication_year, str):
                        try:
                            publication_year = int(publication_year)
                        except ValueError:
                            publication_year = datetime.datetime.now().year

                    # Calculate combined score based on sorting criteria
                    if self.sort_by == "date":
                        date = extract_exact_date(paper)
                        if date is None:
                            # Skip this paper if no valid date is found
                            continue

                        current_date = datetime.datetime.now().date()
                        days_ago = (current_date - date).days  # This is now type-safe
                        combined_score = citation_count / (
                            ((365 + days_ago) / 365) ** self.recency_weight
                        )
                    else:
                        current_year = datetime.datetime.now().year
                        recency = current_year + 1 - publication_year
                        combined_score = citation_count / (recency**self.recency_weight)

                    # Get additional details from Semantic Scholar
                    semantic_scholar_results = get_paper_details_from_semantic_scholar(title)
                    if semantic_scholar_results is not None:
                        _, venue_new = semantic_scholar_results
                        if venue_new:
                            venue = venue_new

                    # Get details from arXiv
                    arxiv_results = get_arxiv_paper_details(title)
                    if arxiv_results is not None:
                        _, abstract, arxiv_link, _ = arxiv_results
                    else:
                        abstract = "Abstract not available"
                        arxiv_link = "Link not available"

                    # Append paper details to the list
                    papers_info.append(
                        {
                            "title": title,
                            "abstract": abstract,
                            "citation_count": citation_count,
                            "publication_year": publication_year,
                            "venue": venue,
                            "authors": authors,
                            "link": link,
                            "arxiv_link": arxiv_link,
                            "combined_score": combined_score,
                        }
                    )

                    # Impose a delay between requests to avoid rate limiting
                    time.sleep(self.delay)

                    # Update progress bar
                    pbar.update(1)

                    # Increment the count of retrieved papers
                    count += 1

                    # Stop if we have enough results for non-date-based search
                    if self.sort_by != "date" and count >= self.num_results:
                        break

            except StopIteration:
                pass  # No more papers to retrieve
            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()

        # Sort papers by combined score in descending order
        papers_info.sort(key=lambda x: x["combined_score"], reverse=True)
        return papers_info

    def display_and_download(
        self, papers_info: list[dict[str, Any]], verbose: bool = True
    ) -> None:
        """
        Display the details of the papers and optionally download them.

        Args:
            papers_info (list[dict[str, Any]]): A list of dictionaries containing paper details.
            verbose (bool): Whether to display detailed information.

        Example:
            >>> search = AutoSearch("machine learning")
            >>> papers = search.search_papers_by_keyword("machine learning")
            >>> search.display_and_download(papers)
        """
        break_flag = False
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        for idx, paper in enumerate(papers_info, start=1):
            papers_info[idx - 1]["search_date"] = current_date
            if paper["combined_score"] >= self.score_threshold:
                print(f"\n\nPaper {idx}:")
                print(f"Title: {paper['title']}")
                if verbose:
                    print(f"Abstract:\n\n{paper['abstract']}")
                print(f"Combined Score: {paper['combined_score']}")
                if verbose:
                    print(f"Citation count: {paper['citation_count']}")
                    print(f"Year of publication: {paper['publication_year']}")
                    print(f"Publication venue: {paper['venue']}")
                    print(f"Authors: {paper['authors']}\n\n")
                    print(f"Link: {paper['link']}")
                    print(f"ArXiv Link: {paper['arxiv_link']}")
                    if paper["link"] != "Link not available":
                        sanitized_title = sanitize_filename(paper["title"])
                        filename = f"{sanitized_title}.pdf"
                        papers_info[idx - 1]["downloaded"] = True
                        papers_info[idx - 1]["file_name"] = filename
                        if not download_pdf(
                            paper["link"], filename, folder=self.destination_folder
                        ):
                            print(f"Trying to download from ArXiv link: {paper['arxiv_link']}")
                            if not download_pdf(
                                paper["arxiv_link"], filename, folder=self.destination_folder
                            ):
                                papers_info[idx - 1]["downloaded"] = False
            else:
                print()
                print(
                    f"The above displays all paper with a combined score no less "
                    f"than {self.score_threshold}"
                )
                break_flag = True
                break

        if not break_flag:
            print()
            print(
                f"The above displays all paper with a combined score no less "
                f"than {self.score_threshold}"
            )

    def perform_a_search(self, keyword: str) -> None:
        """
        Perform a single search for a given keyword and process the results.

        Args:
            keyword (str): The keyword to search for.

        Example:
            >>> search = AutoSearch("machine learning")
            >>> search.perform_a_search("machine learning")
        """
        papers_info = self.search_papers_by_keyword(keyword)
        self.display_and_download(papers_info)

        # Add search settings to the papers_info list
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        search_settings = {
            "keyword": keyword,
            "num_results": self.num_results,
            "delay": self.delay,
            "sort_by": self.sort_by,
            "date_cutoff": self.date_cutoff,
            "current_date": current_date,
            "score_threshold": self.score_threshold,
        }
        papers_info.append(search_settings)

        # Save metadata
        os.makedirs(self.destination_folder, exist_ok=True)
        meta_data_path = os.path.join(self.destination_folder, "metadata.json")
        save_meta_data(meta_data_path, papers_info)  # Use the imported function

        # Zip the folder if required
        if self.zip_folder:
            shutil.make_archive(self.destination_folder, "zip", self.destination_folder)
            print(f"\nFolder saved to {self.destination_folder}.zip")

    def run(self) -> None:
        """
        Execute the search based on the initialized parameters.

        Example:
            >>> search = AutoSearch("machine learning")
            >>> search.run()
        """
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if self.auto_destination:
            if self.sort_by == "date":
                self.destination_folder = (
                    f"{self.keywords}_{current_date}_{self.sort_by}_{self.date_cutoff}_"
                    f"{self.score_threshold}"
                )
            else:
                self.destination_folder = (
                    f"{self.keywords}_{current_date}_{self.sort_by}_{self.num_results}_"
                    f"{self.score_threshold}"
                )
        else:
            self.destination_folder = self.destination_folder

        # Check if keywords is a string or a list
        if isinstance(self.keywords, str):
            print(f"------Searching for the keyword '{self.keywords}'------")
            self.perform_a_search(self.keywords)
        elif isinstance(self.keywords, list):
            for idx, keyword in enumerate(self.keywords, start=1):
                print(f"------Searching for the {idx}th keyword '{keyword}'------")
                self.perform_a_search(keyword)
        else:
            raise ValueError("keywords must be a string or a list of strings.")
