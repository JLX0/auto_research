from __future__ import annotations

import os

from auto_research.survey.core import AutoSurvey
from auto_research.utils.inquiry import check_and_read_key_file


def select_pdf_file(folder_path: str) -> tuple[str, str]:
    """
    Present available PDF files to the user and handle file selection.

    Args:
        folder_path (str): Path to the folder containing PDF files.

    Returns:
        tuple[str, str]: A tuple containing the selected file name and its full path.

    Raises:
        ValueError: If no PDF files are found or if user input is invalid.

    Example:
        # Sample usage:
        folder = "./sample_articles"
        filename, filepath = select_pdf_file(folder)
        # This will display available PDFs and prompt for selection
    """
    file_list = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

    if not file_list:
        raise ValueError("No PDF files found in the sample folder.")

    print("Available PDF files:")
    for i, fname in enumerate(file_list):
        print(f"{i}: {fname}")

    try:
        choice_index = int(input("Enter the index of the file you want to process: "))
        if not 0 <= choice_index < len(file_list):
            raise ValueError
    except ValueError:
        raise ValueError("Invalid choice. Please enter a valid index number.")

    selected_file = file_list[choice_index]
    file_path = os.path.join(folder_path, selected_file)

    return selected_file, file_path


def get_api_key(base_path: str, default_key: str = "type_your_key_here_or_use_key.json") -> str:
    """
    Retrieve the API key from a file or use a default value.

    Args:
        base_path (str): Base path to search for the key file.
        default_key (str): Default key to use if file reading fails.

    Returns:
        str: The API key string.

    Example:
        # Sample usage:
        key = get_api_key("../", "default_key")
        # Returns either the key from file or the default key
    """
    key = check_and_read_key_file(base_path, "OpenAI")
    return default_key if key == -1 else key


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

    key = get_api_key("../")

    auto_survey_instance = AutoSurvey(
        key, "gpt-4o-mini", file_path, False, "summarize_computer_science"
    )
    auto_survey_instance.run()


if __name__ == "__main__":
    main()
