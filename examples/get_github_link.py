from __future__ import annotations

from auto_research.survey.core import AutoSurvey
from LLM_utils.inquiry import get_api_key
from auto_research.utils.files import select_pdf_file
from auto_research.reimplementation.code_availability_check import test_github_link, base_prompt_formatted

def main() -> None:
    """


    """
    sample_folder = "../auto_research/survey/sample_articles/"
    selected_file, file_path = select_pdf_file(sample_folder)

    key = get_api_key("../", "OpenAI")

    auto_survey_instance = AutoSurvey(
        key,
        "gpt-4o-mini",
        file_path,
        False,
        "information_retrieval",
    )


    prompt=base_prompt_formatted()
    auto_survey_instance.run(prompt,test_github_link)


if __name__ == "__main__":
    main()
