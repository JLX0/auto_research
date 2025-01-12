from auto_research.search.core import AutoSearch

def main() -> None:

        # keywords can be string or list of strings. If keywords is a string, then perform a
        # search over the single keyword. If keywords is a list of strings, then perform a
        # search over each keyword in the list. Same articles from the search based on
        # different keywords will not be downloaded twice
        keywords=["Diffusion models", "Generative modeling for computer vision"]
        # number of articles to retrieve at maximum
        num_results=3
        # choose one between "relevance" and "date"
        sort_by="relevance"
        # date_cutoff is relevant only when sort_by is set as "date"
        date_cutoff="2024-12-01"
        # minimum score that the article must have to be downloaded
        score_threshold=0.5
        # path where the downloaded articles and metadata will be stored
        destination_folder="search_results"

        paper_search = AutoSearch(keywords=keywords, num_results=num_results,sort_by=sort_by,
                                  date_cutoff=date_cutoff, score_threshold=score_threshold,
                                  destination_folder=destination_folder)
        paper_search.run()

if __name__ == "__main__":
    main()