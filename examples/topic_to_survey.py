from auto_research.applications.surveys import topic_to_survey


if __name__ == "__main__":
    topic_to_survey(
        num_results=5,  # Number of search results to retrieve. Defaults to 30.
        sort_by="relevance",  # Sorting criteria for search results. Options: "relevance", "date". Defaults to "relevance".
        date_cutoff="2024-12-01",  # Cutoff date for search results. Only articles published before this date will be included. Defaults to "2024-12-01". Only relevant when `sort_by` is set as "date"
        score_threshold=0,  # Minimum score threshold for articles. Articles with a score below this will be excluded. Defaults to 0.5.
        destination_folder="papers",  # Folder to store downloaded articles. Defaults to "papers".
        model="gpt-4o-mini",  # Model to use for summarization and keyword suggestions. Defaults to "gpt-4o-mini".
        api_key_path="../",  # Path to the directory containing the API key. Defaults to "../". Set it as "" if the file is located at the current directory
        api_key_type="OpenAI",  # Type of API key to retrieve. Options: "OpenAI", "DeepSeek". Defaults to "OpenAI".
        organize_files=True,  # Whether to organize the downloaded articles into subfolders based on their rank and score. Defaults to True.
        order_by_score=True,  # Whether to order articles by their score when organizing. Defaults to True.
        zip_folder=True,  # Whether to zip the organized folder after processing. Defaults to True.
    )