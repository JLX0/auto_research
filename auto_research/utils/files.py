import os
import json

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



def get_all_pdf_files(folder_path: str) -> list[str]:
    """
    Retrieve all PDF files in the specified folder.

    Args:
        folder_path (str): Path to the folder containing PDF files.

    Returns:
        list[str]: A list of full paths to the PDF files.

    Raises:
        ValueError: If no PDF files are found.

    Example:
        # Sample usage:
        folder = "./sample_articles"
        pdf_files = get_all_pdf_files(folder)
        # Returns a list of full paths to the PDFs
    """
    file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]

    if not file_list:
        raise ValueError("No PDF files found in the sample folder.")

    return file_list

def print_summaries(storage_path="papers.json"):
    with open(storage_path, "r") as file:
        input_data = json.load(file)

    # Filter to retain only summaries
    filtered_data = {key: {"summary": value["summary"]} for key, value in input_data.items()}

    # Output the filtered dictionary in a nicely formatted manner
    for paper, details in filtered_data.items():
        print("------Paper title: "f"{paper}------\n")
        for _, summary in details["summary"].items():
            print(f"{summary}\n")
        print("\n")