from auto_research.search.core import AutoSearch
from auto_research.search.keywords import suggest_keywords
from auto_research.search.post_processing import ArticleOrganizer
from auto_research.survey.core import AutoSurvey
from LLM_utils.inquiry import get_api_key
from auto_research.utils.files import get_all_pdf_files, print_summaries, select_pdf_file
from auto_research.reimplementation.code_availability_check import test_github_link, base_prompt_formatted
import os

def main() -> None:
    # Settings
    num_results = 3
    sort_by = "relevance"
    date_cutoff = "2024-12-01"
    score_threshold = 0.5
    destination_folder = "papers"
    key = get_api_key("../", "OpenAI")
    # It is recommended to use models like Deepseek-V3 (deepseek-chat) or gpt-4o
    # to increase accuracy, especially for checking code availability
    model = "gpt-4o-mini"


    # Ask for user_prompt from the user
    user_prompt = input("Please enter your research topic or question (e.g., 'Applications of AI in healthcare'): ")

    # Generate keyword list based on user_prompt
    keyword_list = suggest_keywords(user_prompt=user_prompt, model=model, api_key=key)

    print("\nSuggested keywords for searching articles based on your input:")
    for i, keyword in enumerate(keyword_list, 1):
        print(f"{i}. {keyword}")

    # Step 2: Ask the user for their preferred option with detailed explanations
    print("\nHow would you like to proceed with the suggested keywords?")
    print("1. 'all': Use all the suggested keywords for searching.")
    print("   Example: If the suggested keywords are ['AI in healthcare', 'machine learning in medicine'], all of them will be used.")
    print("2. 'select': Choose the first N keywords from the suggested list.")
    print("   Example: If you enter 2, the first 2 keywords from the list will be used.")
    print("3. 'custom': Enter your own list of keywords manually.")
    print("   Example: You can type 'AI in diagnostics, healthcare automation' to use these specific keywords.")

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
        while True:
            try:
                N = int(input(f"\nEnter the number of keywords to select (1-{len(keyword_list)}): "))
                if 1 <= N <= len(keyword_list):
                    keywords = keyword_list[:N]
                    print(f"\nUsing the first {N} keywords: {keywords}")
                    break
                else:
                    print(f"Please enter a number between 1 and {len(keyword_list)}.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
    elif option == "custom":
        while True:
            custom_input = input("\nEnter your custom keywords, separated by commas without quotation marks (e.g., 'AI in diagnostics, healthcare automation'): ")
            keywords = [kw.strip() for kw in custom_input.split(",") if kw.strip()]
            if keywords:
                print("\nUsing custom keywords for the search:", keywords)
                break
            else:
                print("No valid keywords entered. Please try again.")

    print("\nFinal keywords to search:", keywords)

    # Perform the search
    paper_search = AutoSearch(
        keywords=keywords,
        num_results=num_results,
        sort_by=sort_by,
        date_cutoff=date_cutoff,
        score_threshold=score_threshold,
        destination_folder=destination_folder
    )
    paper_search.run()

    # Organize the downloaded papers
    paper_organizer = ArticleOrganizer(
        source_folder=destination_folder,
        target_folder="papers_organized",
        threshold_type="rank",
        score_threshold=score_threshold,
        rank_threshold=num_results,
        organize_files=True,
        order_by_score=True,
        zip_folder=True
    )
    paper_organizer.organize_and_visualize()

    # Check if there are any PDF files in the organized folder
    organized_folder = os.path.join(destination_folder, "papers_organized")
    pdf_files = get_all_pdf_files(organized_folder)

    if not pdf_files:
        print(f"\nError: No downloaded articles found in '{organized_folder}'.")
        print("Possible reasons:")
        print("- The search did not return any results matching your criteria.")
        print("- The score threshold or rank threshold may be too high.")
        print("- Try increasing 'num_results' or lowering 'score_threshold' in the settings.")
        return

    # Step 3: Ask the user how they want to summarize the papers
    print("\nHow would you like to summarize the papers?")
    print("1. 'all': Summarize all papers in the organized folder.")
    print("2. 'select': Select the top N articles to summarize.")
    print("3. 'custom': Choose specific papers by their ranks to summarize.")

    while True:
        summary_option = input("\nChoose an option ('all', 'select', or 'custom'): ").strip().lower()
        if summary_option in ["all", "select", "custom"]:
            break
        print("Invalid option. Please try again.")

    # Determine which papers to summarize based on the user's choice
    if summary_option == "all":
        target_files = pdf_files
        print("\nSummarizing all papers in the organized folder.")
    elif summary_option == "select":
        while True:
            try:
                N = int(input(f"\nEnter the number of top articles to summarize (1-{len(pdf_files)}): "))
                if 1 <= N <= len(pdf_files):
                    target_files = pdf_files[:N]
                    print(f"\nSummarizing the top {N} articles: {[os.path.basename(file) for file in target_files]}")
                    break
                else:
                    print(f"Please enter a number between 1 and {len(pdf_files)}.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
    elif summary_option == "custom":
        # Print all papers with their ranks
        print("\nAvailable papers with their ranks:")
        for i, file_path in enumerate(pdf_files, 1):
            print(f"{i}. {os.path.basename(file_path)}")
        # Ask the user to input ranks
        while True:
            custom_ranks = input("\nEnter the ranks of the papers you want to summarize, separated by commas (e.g., 1,3,5): ")
            try:
                selected_ranks = [int(rank.strip()) for rank in custom_ranks.split(",") if rank.strip()]
                if all(1 <= rank <= len(pdf_files) for rank in selected_ranks):
                    target_files = [pdf_files[rank - 1] for rank in selected_ranks]
                    print("\nSummarizing the following papers:", [os.path.basename(file) for file in target_files])
                    break
                else:
                    print(f"Please enter ranks between 1 and {len(pdf_files)}.")
            except ValueError:
                print("Invalid input. Please enter valid integers separated by commas.")

    # Perform summarization on the targeted papers
    final_cost = 0
    for file_path in target_files:
        print(f"\nProcessing file: {os.path.basename(file_path)}")
        auto_survey_instance = AutoSurvey(
            key, model, file_path, False, "summarize_computer_science",
            storage_path=os.path.join(destination_folder, "summaries.json")
        )
        auto_survey_instance.run()
        final_cost += auto_survey_instance.cost_accumulation

    print(f"\nTotal cost for all files: {final_cost}")
    print("\nThe summaries for all selected files are printed below:")
    print_summaries(os.path.join(destination_folder, "summaries.json"))

    # Step 4: Ask the user if they want to check code availability
    while True:
        check_code = input("\nWould you like to check the code availability of the articles? (yes/no): ").strip().lower()
        if check_code in ["yes", "no"]:
            break
        print("Invalid input. Please enter 'yes' or 'no'.")

    if check_code == "yes":
        print("\nChecking code availability for the summarized articles...")
        for file_path in target_files:
            print(f"\nChecking code availability for: {os.path.basename(file_path)}")
            auto_survey_instance = AutoSurvey(
                key, model, file_path, False, "information_retrieval"
            )
            prompt = base_prompt_formatted()
            auto_survey_instance.run(prompt, test_github_link)

if __name__ == "__main__":
    main()