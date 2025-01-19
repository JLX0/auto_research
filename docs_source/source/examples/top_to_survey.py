"""
.. _top_to_survey_page:

Automatically converts a topic or question of interests into a survey over relevant papers
==========================================

When searching for research papers, the results from a search engine can vary significantly
depending on the specific keywords used, even if those keywords are conceptually similar.
For instance, searching for "LLMs" versus "Large Language Models" may yield different sets
of papers. Additionally, when experimenting with new keywords, it can be challenging to
remember whether a particular paper has already been checked. Furthermore, the process
of downloading papers and organizing them with appropriate filenames can be tedious and
time-consuming.

The function `topic_to_survey` streamlines the entire process by automating several key tasks.
It suggests multiple related keywords to ensure comprehensive coverage of the topic,
merges duplicate results to avoid redundancy, automatically names downloaded files
using the paper titles for easy reference, and automatically ranks the papers based on their impacts
(see :mod:`auto_research.search.core.AutoSearch.score_threshold`). Moreover, it leverages LLMs
to generate summaries of each paper, saving researchers valuable time and effort.

This script demonstrates the usage of the `topic_to_survey` function from the :mod:`auto_research.applications.surveys` module to:

- Conduct an automated research process based on a user-provided topic.
- Generate and refine a list of keywords for searching research articles.
- Retrieve and download articles based on the specified search criteria.
- Rank, organize, and summarize the downloaded articles.
- Check the code availability of the summarized articles (optional).

To get started with the package, you need to set up API keys. For detailed instructions, see :ref:`setting_up_api_keys`.

This script assumes that:

- A valid `key.json` file is available (located at the current working directory (""))

The process involves user interaction, including selecting keywords, summarizing articles, and optionally checking code availability.

Below is an example output from the following input:

- generate code with LLMs
- select
- 1,3
- select
- 2,3
- yes


"""

from auto_research.applications.surveys import topic_to_survey


if __name__ == "__main__":
    """
    Main execution block for the `topic_to_survey` function.

    This block initializes the `topic_to_survey` function with the specified parameters and runs the automated research process.

    Example:
        # Sample usage:
        topic_to_survey(
            num_results=5,
            sort_by="relevance",
            date_cutoff="2024-12-01",
            score_threshold=0,
            destination_folder="papers",
            model="gpt-4o-mini",
            api_key_path="",
            api_key_type="OpenAI",
            organize_files=True,
            order_by_score=True,
            zip_folder=True,
            api_key=None,  # Directly provide the API key as a string. If None, the key will be retrieved from the file.
        )

    Parameters
    ----------
    num_results : int, optional
        Number of search results to retrieve. Defaults to 30.
    sort_by : str, optional
        Sorting criteria for search results. Options: "relevance", "date". Defaults to "relevance".
    date_cutoff : str, optional
        Cutoff date for search results. Only articles published before this date will be included. Defaults to "2024-12-01". Only relevant when `sort_by` is set as "date".
    score_threshold : float, optional
        Minimum score threshold for articles. Articles with a score below this will be excluded. Defaults to 0.5.
    destination_folder : str, optional
        Folder to store downloaded articles. Defaults to "papers".
    model : str, optional
        Model to use for summarization and keyword suggestions. Defaults to "gpt-4o-mini".
    api_key_path : str, optional
        Path to the directory containing the API key. Defaults to "../". Set it as "" if the file is located at the current directory.
    api_key_type : str, optional
        Type of API key to retrieve. Options: "OpenAI", "DeepSeek". Defaults to "OpenAI".
    organize_files : bool, optional
        Whether to organize the downloaded articles into subfolders based on their rank and score. Defaults to True.
    order_by_score : bool, optional
        Whether to order articles by their score when organizing. Defaults to True.
    zip_folder : bool, optional
        Whether to zip the organized folder after processing. Defaults to True.
    api_key : str, optional
        Directly provide the API key as a string. If None, the key will be retrieved from the file. Defaults to None.

    Returns
    -------
    None
    """
    topic_to_survey(
        num_results=5,
        sort_by="relevance",
        date_cutoff="2024-12-01",
        score_threshold=0,
        destination_folder="papers",
        model="gpt-4o-mini",
        api_key_path="",
        api_key_type="OpenAI",
        organize_files=True,
        order_by_score=True,
        zip_folder=True,
        api_key=None,
    )