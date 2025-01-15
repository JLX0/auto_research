"""
.. _summarize_all_papers_page:

Summarize All Papers in a Folder
=====================================

This script demonstrates the usage of `AutoSurvey` from :mod:`auto_research.survey.core` module to:

- Iterate through all PDF files in a specified folder.
- Retrieve an API key for the LLM (Large Language Model).
- Run an automated survey analysis on each PDF file using the LLM.
- Accumulate and display the total cost of running the analysis.
- Print summaries for all processed PDF files.

To get started with the package, you need to set up API keys. For detailed instructions, see :ref:`setting_up_api_keys`.

This script assumes that:

- At least one valid PDF file of the article is available. (located at "sample_articles/")
- A valid `key.json` file is available (located at the current working directory (""))

"""

from __future__ import annotations

from LLM_utils.inquiry import get_api_key
from auto_research.survey.core import AutoSurvey
from auto_research.utils.files import get_all_pdf_files
from auto_research.utils.files import print_summaries


def main() -> None:
    """
    Main function to run the auto survey process over all PDF files in the directory.

    This function handles the workflow of iterating through all PDF files,
    getting the API key, and running the survey analysis for each file.

    Example:
        # Sample usage:
        main()  # This will start the process for all PDFs in the directory

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # Specify the folder containing the target PDF files.
    sample_folder = "sample_articles/"

    try:
        # Retrieve all PDF files from the specified folder.
        pdf_files = get_all_pdf_files(sample_folder)
    except ValueError as e:
        # Handle the case where no PDF files are found.
        print(e)
        return

    # Retrieve the API key for the LLM.
    # This script assumes a valid API key is located at the specified path.
    key = get_api_key("", "OpenAI")

    # Initialize a variable to accumulate the total cost of running the analysis.
    final_cost = 0

    # Iterate through each PDF file and run the survey analysis.
    for file_path in pdf_files:
        print(f"Processing file: {file_path}")

        # Initialize the AutoSurvey instance with the specified parameters.
        auto_survey_instance = AutoSurvey(
            key, "gpt-4o-mini", file_path, False, "summarize_computer_science"
        )

        # Run the automated survey analysis for the current PDF file.
        auto_survey_instance.run()

        # Accumulate the cost of running the analysis.
        final_cost += auto_survey_instance.cost_accumulation

    # Print the total cost for all files.
    print(f"Total cost for all files: {final_cost}")

    # Print summaries for all processed PDF files.
    print("The summaries for all files are printed below:")
    print_summaries()


if __name__ == "__main__":
    main()