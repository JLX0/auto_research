import os

from LLM_utils.inquiry import get_api_key

from auto_research.reimplementation.code_availability_check import base_prompt_formatted
from auto_research.reimplementation.code_availability_check import test_github_link
from auto_research.search.core import AutoSearch
from auto_research.search.keywords import suggest_keywords
from auto_research.search.post_processing import ArticleOrganizer
from auto_research.survey.core import AutoSurvey
from auto_research.utils.files import get_all_pdf_files
from auto_research.utils.files import print_summaries
from auto_research.utils.files import select_pdf_file


def main() -> None:
    """
    Main function to execute the automated research process.
    This function guides the user through keyword selection, article search, organization, summarization, and code availability checks.
    """
    # Settings
    num_results = 30  # Number of search results to retrieve
    sort_by = "relevance"  # Sorting criteria for search results
    date_cutoff = "2024-12-01"  # Cutoff date for search results
    score_threshold = 0.5  # Minimum score threshold for articles
    destination_folder = "papers"  # Folder to store downloaded articles
    key = get_api_key("../", "OpenAI")  # Retrieve API key for OpenAI
    model = "gpt-4o-mini"  # Model to use for summarization and keyword suggestions

    # It is recommended to use Deepseek V3 or GPT-4o to increase accuracy, especially for code
    # availability check
    # key = get_api_key("../", "DeepSeek") # If you are using DeepSeek models
    # model = "deepseek-chat" # If you are using DeepSeek models

    # Ask for user_prompt from the user
    user_prompt = input(
        "Please enter your research topic or question (e.g., 'Applications of AI in healthcare'): "
    )

    # Generate keyword list based on user_prompt
    keyword_list = suggest_keywords(user_prompt=user_prompt, model=model, api_key=key)

    print("\nSuggested keywords for searching articles based on your input:")
    for i, keyword in enumerate(keyword_list, 1):
        print(f"{i}. {keyword}")

    # Step 2: Ask the user for their preferred option with detailed explanations
    print("\nHow would you like to proceed with the suggested keywords?")
    print("1. 'all': Use all the suggested keywords for searching.")
    print(
        "   Example: If the suggested keywords are ['AI in healthcare', 'machine learning in medicine'], all of them will be used."
    )
    print("2. 'select': Choose specific keywords by their ranks.")
    print("   Example: If you enter '1,3,5', keywords with those ranks will be used.")
    print("3. 'custom': Enter your own list of keywords manually.")
    print(
        "   Example: You can type 'AI in diagnostics, healthcare automation' to use these specific keywords."
    )

    while True:
        option = input("\nChoose an option ('all', 'select', or 'custom'): ").strip().lower()
        if option in ["all", "select", "custom"]:
            break
        print("Invalid option. Please try again.")

    # Determine the final list of keywords based on the user's choice
    if option == "all":
        keywords = keyword_list
        print("\nUsing all suggested keywords for the search.")
    elif option == "select":
        # Print all keywords with their ranks
        print("\nAvailable keywords with their ranks:")
        for i, keyword in enumerate(keyword_list, 1):
            print(f"{i}. {keyword}")
        # Ask the user to input ranks
        while True:
            custom_ranks = input(
                "\nEnter the ranks of the keywords you want to use, separated by commas (e.g., 1,3,5): "
            )
            try:
                selected_ranks = [
                    int(rank.strip()) for rank in custom_ranks.split(",") if rank.strip()
                ]
                if all(1 <= rank <= len(keyword_list) for rank in selected_ranks):
                    keywords = [keyword_list[rank - 1] for rank in selected_ranks]
                    print("\nUsing the following keywords:", keywords)
                    break
                else:
                    print(f"Please enter ranks between 1 and {len(keyword_list)}.")
            except ValueError:
                print("Invalid input. Please enter valid integers separated by commas.")
    elif option == "custom":
        while True:
            custom_input = input(
                "\nEnter your custom keywords, separated by commas without quotation marks (e.g., 'AI in diagnostics, healthcare automation'): "
            )
            keywords = [kw.strip() for kw in custom_input.split(",") if kw.strip()]
            if keywords:
                print("\nUsing custom keywords for the search:", keywords)
                break
            else:
                print("No valid keywords entered. Please try again.")

    print("\nFinal keywords to search:", keywords)

    # Initialize and run the AutoSearch to find and download articles
    paper_search = AutoSearch(
        keywords=keywords,
        num_results=num_results,
        sort_by=sort_by,
        date_cutoff=date_cutoff,
        score_threshold=score_threshold,
        destination_folder=destination_folder,
    )
    paper_search.run()

    # Organize the downloaded articles based on rank and score
    paper_organizer = ArticleOrganizer(
        source_folder=destination_folder,
        target_folder="papers_organized",
        threshold_type="rank",
        score_threshold=score_threshold,
        rank_threshold=num_results,
        organize_files=True,
        order_by_score=True,
        zip_folder=True,
    )
    paper_organizer.organize_and_visualize()

    # Get the list of all PDF files in the organized folder
    organized_folder = os.path.join(destination_folder, "papers_organized")
    pdf_files = get_all_pdf_files(organized_folder)

    if not pdf_files:
        print(f"\nError: No downloaded articles found in '{organized_folder}'.")
        print("Possible reasons:")
        print("- The search did not return any results matching your criteria.")
        print("- The score threshold or rank threshold may be too high.")
        print("- Try increasing 'num_results' or lowering 'score_threshold' in the settings.")
        print("- The files are not accessible for download or are corrupted.")
        return

    # Ask the user how they would like to summarize the papers
    print("\nHow would you like to summarize the papers?")
    print("1. 'all': Summarize all papers in the organized folder.")
    print("2. 'select': Choose specific papers by their ranks to summarize.")

    while True:
        summary_option = input("\nChoose an option ('all' or 'select'): ").strip().lower()
        if summary_option in ["all", "select"]:
            break
        print("Invalid option. Please try again.")

    if summary_option == "all":
        target_files = pdf_files
        print("\nSummarizing all papers in the organized folder.")
    elif summary_option == "select":
        print("\nAvailable papers with their ranks:")
        for i, file_path in enumerate(pdf_files, 1):
            print(f"{i}. {os.path.basename(file_path)}")
        while True:
            custom_ranks = input(
                "\nEnter the ranks of the papers you want to summarize, separated by commas (e.g., 1,3,5): "
            )
            try:
                selected_ranks = [
                    int(rank.strip()) for rank in custom_ranks.split(",") if rank.strip()
                ]
                if all(1 <= rank <= len(pdf_files) for rank in selected_ranks):
                    target_files = [pdf_files[rank - 1] for rank in selected_ranks]
                    print(
                        "\nSummarizing the following papers:",
                        [os.path.basename(file) for file in target_files],
                    )
                    break
                else:
                    print(f"Please enter ranks between 1 and {len(pdf_files)}.")
            except ValueError:
                print("Invalid input. Please enter valid integers separated by commas.")

    # Summarize the selected papers and accumulate the cost
    summary_cost = 0
    for file_path in target_files:
        print(f"\nProcessing file: {os.path.basename(file_path)}")
        auto_survey_instance = AutoSurvey(
            key,
            model,
            file_path,
            False,
            "summarize_computer_science",
            storage_path=os.path.join(destination_folder, "summaries.json"),
        )
        auto_survey_instance.run()
        summary_cost += auto_survey_instance.cost_accumulation

    print(f"\nTotal cost for summarizing all files: {summary_cost}")
    print("\nThe summaries for all selected files are printed below:")
    print_summaries(os.path.join(destination_folder, "summaries.json"))

    # Ask the user if they want to check the code availability of the articles
    while True:
        check_code = (
            input("\nWould you like to check the code availability of the articles? (yes/no): ")
            .strip()
            .lower()
        )
        if check_code in ["yes", "no"]:
            break
        print("Invalid input. Please enter 'yes' or 'no'.")

    # Check code availability for the summarized articles and accumulate the cost
    code_check_cost = 0
    if check_code == "yes":
        print("\nChecking code availability for the summarized articles...")
        for file_path in target_files:
            print(f"\nChecking code availability for: {os.path.basename(file_path)}")
            auto_survey_instance = AutoSurvey(
                key, model, file_path, False, "information_retrieval"
            )
            prompt = base_prompt_formatted()
            auto_survey_instance.run(prompt, test_github_link)
            code_check_cost += auto_survey_instance.cost_accumulation

    print(f"\nTotal cost for checking code availability: {code_check_cost} USD")
    print(
        f"Total cost for the entire process (summaries + code availability check): {summary_cost + code_check_cost} USD"
    )


if __name__ == "__main__":
    main()
