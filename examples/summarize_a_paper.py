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
    """
    sample_folder = "../auto_research/survey/sample_articles/"
    selected_file, file_path = select_pdf_file(sample_folder)

    key = get_api_key("../", "OpenAI")

    auto_survey_instance = AutoSurvey(
        key, "gpt-4o-mini", file_path, False, "summarize_computer_science"
    )
    auto_survey_instance.run()


if __name__ == "__main__":
    main()
