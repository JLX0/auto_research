"""
.. _summarize_a_paper_page:

Summarize a Paper
=====================================

This script demonstrates the usage of `AutoSurvey` from the :mod:`auto_research.survey.core` module to:

- Select a PDF file from a specified folder.
- Retrieve an API key for the LLM.
- Run an automated survey analysis on the selected PDF using the LLM.

To get started with the package, you need to set up API keys. For detailed instructions, see :ref:`setting_up_api_keys`.

This script assumes that:

- At least one valid PDF file of the article is available. (located at "sample_articles/")
- A valid `key.json` file is available (located at the current working directory (""))

The process involves user interaction, including selecting a PDF file.

Below is an example output from the following input:

- 3

"""

from __future__ import annotations

from LLM_utils.inquiry import get_api_key
from auto_research.survey.core import AutoSurvey
from auto_research.utils.files import select_pdf_file


def main() -> None:
    """
    Main function to run the auto survey process.

    This function handles the workflow of selecting a PDF file, getting the API key,
    and running the survey analysis.

    Example:
        # Sample usage:
        main()  # This will start the interactive process

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # Specify the folder containing the target PDF files.
    sample_folder = "sample_articles/"

    # Select a PDF file from the specified folder.
    selected_file, file_path = select_pdf_file(sample_folder)

    # Retrieve the API key for the LLM.
    # This script assumes a valid API key is located at the specified path.
    key = get_api_key("", "OpenAI")

    # Initialize the AutoSurvey instance with the specified parameters.
    auto_survey_instance = AutoSurvey(
        key, "gpt-4o-mini", file_path, False, "summarize_computer_science"
    )

    # Run the automated survey analysis.
    auto_survey_instance.run()


if __name__ == "__main__":
    main()