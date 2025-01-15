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
    """
    sample_folder = "../auto_research/survey/sample_articles/"

    try:
        pdf_files = get_all_pdf_files(sample_folder)
    except ValueError as e:
        print(e)
        return

    key = get_api_key("../", "OpenAI")
    final_cost = 0
    for file_path in pdf_files:
        print(f"Processing file: {file_path}")
        auto_survey_instance = AutoSurvey(
            key, "gpt-4o-mini", file_path, False, "summarize_computer_science"
        )
        auto_survey_instance.run()
        final_cost += auto_survey_instance.cost_accumulation
    print(f"Total cost for all files: {final_cost}")

    print("The summaries for all files are printed below:")
    print_summaries()


if __name__ == "__main__":
    main()
