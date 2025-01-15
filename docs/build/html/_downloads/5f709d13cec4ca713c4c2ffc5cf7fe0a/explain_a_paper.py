"""

.. _explain_a_paper_page:

Explain a Paper with LLMs
=====================================

This script demonstrates the usage of `AutoSurvey` in the :mod:`auto_research.survey.core` module to:

- Select a PDF file from a specified folder.

- Retrieve an API key for the LLM (Large Language Model).

- Run an automated survey analysis using the selected PDF and the LLM.

To get started with the package, you need to set up API keys. For detailed instructions, see :ref:`setting_up_api_keys`.

This script assumes that

- At least one valid PDF file of the article is available. (located at "sample_articles/")

- A valid key.json file is available (located at the current working directory (""))

The process involves user interaction, including selecting a PDF file and asking questions about its content.

"""

from LLM_utils.inquiry import get_api_key
from auto_research.survey.core import AutoSurvey
from auto_research.utils.files import select_pdf_file


def main() -> None:

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
        "explain_computer_science",
    )

    # Run the automated survey analysis
    auto_survey_instance.run()


if __name__ == "__main__":
    main()