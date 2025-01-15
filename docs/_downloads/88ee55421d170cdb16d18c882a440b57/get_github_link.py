"""
.. _get_github_link_page:

Code Availability Check
====================================================================

This script demonstrates the usage of `AutoSurvey` in the :mod:`auto_research.survey.core` module to:

- Select a PDF file from a specified folder.

- Retrieve an API key for the LLM (Large Language Model).

- Format a base prompt for code availability checks.

- Test the availability of code on GitHub.

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

from auto_research.reimplementation.code_availability_check import base_prompt_formatted
from auto_research.reimplementation.code_availability_check import test_github_link
from auto_research.survey.core import AutoSurvey
from auto_research.utils.files import select_pdf_file


def main() -> None:
    """
    Main function to execute the code availability check and survey analysis.

    This function:
    - Selects a PDF file from the specified folder.
    - Retrieves the API key for the LLM.
    - Formats the base prompt for code availability checks.
    - Initializes the AutoSurvey instance.
    - Checks whether GitHub link is available
    """
    # Specify the folder containing the target PDF files
    sample_folder = "sample_articles/"

    # Select a PDF file from the specified folder
    selected_file, file_path = select_pdf_file(sample_folder)

    # Retrieve the API key for the LLM
    # This script assumes a valid key.json file is located at the current working directory ("")
    # Modify the path to key.json ("") and the value for LLMs category ("OpenAI") if needed
    key = get_api_key("", "OpenAI")

    # Initialize the AutoSurvey instance
    auto_survey_instance = AutoSurvey(
        key,
        "gpt-4o-mini",
        file_path,
        False,
        "information_retrieval",
    )

    # Format the base prompt for code availability checks
    prompt = base_prompt_formatted()

    # Check whether GitHub link is available
    auto_survey_instance.run(prompt, test_github_link)


if __name__ == "__main__":
    main()