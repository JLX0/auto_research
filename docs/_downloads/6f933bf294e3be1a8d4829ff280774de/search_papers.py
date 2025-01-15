"""
.. _search_papers_page:

Automatically Search and Download Papers
=====================================

This script demonstrates the usage of `AutoSearch` from the :mod:`auto_research.search.core` module to:

- Perform a search for research papers based on specified keywords.
- Retrieve a specified number of articles.
- Sort the results by relevance or date.
- Apply filters such as a date cutoff and a minimum score threshold (:mod:`auto_research.search.core.AutoSearch.score_threshold`).
- Save the downloaded articles and metadata to a specified folder.


This script assumes that:

- The destination folder for storing search results exists or will be created.

"""

from auto_research.search.core import AutoSearch


def main() -> None:
    """
    Main function to execute the AutoSearch process.

    This function initializes the search parameters, creates an instance of the `AutoSearch` class,
    and runs the search to retrieve and store the articles.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # Keywords can be a string or a list of strings. If keywords is a string, then perform a
    # search over the single keyword. If keywords is a list of strings, then perform a
    # search over each keyword in the list. Same articles from the search based on
    # different keywords will not be downloaded twice.
    keywords = ["Diffusion models", "Generative modeling for computer vision"]

    # Number of articles to retrieve at maximum.
    num_results = 3

    # Choose one between "relevance" and "date" for Google Scholar search engine
    sort_by = "relevance"

    # Date cutoff is relevant only when sort_by is set as "date".
    date_cutoff = "2024-12-01"

    # Minimum score that the article must have to be downloaded.
    score_threshold = 0.5

    # Path where the downloaded articles and metadata will be stored.
    destination_folder = "search_results"

    # Initialize the AutoSearch instance with the specified parameters.
    paper_search = AutoSearch(
        keywords=keywords,
        num_results=num_results,
        sort_by=sort_by,
        date_cutoff=date_cutoff,
        score_threshold=score_threshold,
        destination_folder=destination_folder,
    )

    # Run the search to retrieve and store the articles.
    paper_search.run()


if __name__ == "__main__":
    main()