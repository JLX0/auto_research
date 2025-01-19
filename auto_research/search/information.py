from __future__ import annotations

import datetime
import json
import os
import re
from typing import Optional


def extract_exact_date(result: dict) -> Optional[datetime.date]:
    """
    Extracts the exact date from the abstract of a research paper result.

    Args:
        result (dict): A dictionary containing paper metadata, including the abstract.

    Returns:
        Optional[datetime.date]: The extracted date if found in the abstract, otherwise None.

    Example:
        >>> result = {"bib": {"abstract": "Published 3 days ago."}}
        >>> extract_exact_date(result)  # Today's date minus 3 days
        datetime.date(2023, 10, 7)
    """
    if "abstract" in result["bib"]:
        abstract = result["bib"]["abstract"]

        # Extract the number of days ago from the abstract.
        match = re.search(r"(\d+)\s+day[s]?\s+ago", abstract)
        if match:
            days_ago = int(match.group(1))
            result_datetime = datetime.datetime.now() - datetime.timedelta(days=days_ago)
            result_date = result_datetime.date()
            print(f"Found a paper published on {result_date}")
            return result_date
    return None


def extract_score(file_path: str) -> float:
    """
    Extracts the score from the filename of a PDF file.

    Args:
        file_path (str): The file path of the PDF file.

    Returns:
        float: The extracted score from the filename. Returns 0.0 if the extraction fails.

    Example:
        >>> extract_score("rank_0.85_title.pdf")
        0.85
    """
    filename = os.path.basename(file_path)
    try:
        # Extract the score from the filename (assuming the format is "rank_score_title.pdf").
        score_str = filename.split("_")[1]
        return float(score_str)
    except (IndexError, ValueError):
        return 0.0  # Default score if extraction fails.


def save_meta_data(meta_data_path: str, papers_info: list[dict]) -> None:
    """
    Saves paper metadata to a JSON file, ensuring no duplicate entries based on paper titles.

    Args:
        meta_data_path (str): The file path where the metadata should be saved.
        papers_info (list[dict]): A list of dictionaries containing paper metadata.

    Raises:
        ValueError: If either existing data or new data is not a list.

    Example:
        >>> papers_info = [{"title": "Paper 1", "abstract": "..."}]
        >>> save_meta_data("metadata.json", papers_info)
        Metadata saved to metadata.json
    """
    if os.path.exists(meta_data_path):
        with open(meta_data_path, "r") as json_file:
            existing_data = json.load(json_file)
        if isinstance(existing_data, list) and isinstance(papers_info, list):
            combined_data = existing_data + papers_info
        else:
            raise ValueError("Existing data and new data must be lists.")
    else:
        combined_data = papers_info

    # Remove duplicates based on paper titles.
    seen_titles: set[str] = set()
    unique_data: list[dict] = []
    for item in combined_data:
        title = item.get("title")
        if title:
            if title not in seen_titles:
                unique_data.append(item)
                seen_titles.add(title)
        else:
            unique_data.append(item)

    # Save the unique metadata to the file.
    with open(meta_data_path, "w") as json_file:
        json.dump(unique_data, json_file, indent=4)

    print(f"Metadata saved to {meta_data_path}")


def read_meta_data(meta_data_path: str) -> list[dict]:
    """
    Reads paper metadata from a JSON file.

    Args:
        meta_data_path (str): The file path from which to read the metadata.

    Returns:
        list[dict]: A list of dictionaries containing paper metadata. Returns an empty list if the
        file does not exist.

    Example:
        >>> read_meta_data("metadata.json")
        [{"title": "Paper 1", "abstract": "..."}]
    """
    if os.path.exists(meta_data_path):
        with open(meta_data_path, "r") as json_file:
            meta_data = json.load(json_file)
        return meta_data
    else:
        return []
