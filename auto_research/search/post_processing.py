from __future__ import annotations

import os
import shutil

import matplotlib.pyplot as plt

from auto_research.search.files_management import sanitize_filename
from auto_research.search.information import read_meta_data


class ArticleOrganizer:
    """
    A class to organize, filter, and visualize academic papers based on their combined scores.

    This class provides functionality to filter papers by score or rank, organize files
    into a target folder, and visualize the distribution of paper scores.

    Attributes:
        source_folder (str): The folder where the original papers and metadata are stored.
        target_folder (str): The folder where organized papers will be saved.
        threshold_type (str): The filtering method ("rank" or "score").
        score_threshold (float): The minimum combined score for filtering when threshold_type
            is "score".
        rank_threshold (int): The number of top papers to filter when threshold_type is "rank".
        organize_files (bool): Whether to organize files into the target folder.
        order_by_score (bool): Whether to rename files with their combined score.
        zip_folder (bool): Whether to zip the target folder and source folder.
        plotting (bool): Whether to plot the combined scores of papers.

    Example:
        >>> organizer = ArticleOrganizer(
        ...     source_folder="papers",
        ...     target_folder="top_papers",
        ...     threshold_type="rank",
        ...     rank_threshold=10,
        ... )
        >>> organizer.organize_and_visualize()
    """

    def __init__(
        self,
        source_folder: str,
        target_folder: str = "top_articles",
        threshold_type: str = "rank",
        score_threshold: float = 0.5,
        rank_threshold: int = 30,
        organize_files: bool = True,
        order_by_score: bool = True,
        zip_folder: bool = True,
        plotting: bool = True,
    ) -> None:
        """
        Initialize the ArticleOrganizer class with the given parameters.

        Args:
            source_folder (str): The folder where the original papers and metadata are stored.
            target_folder (str): The folder where organized papers will be saved.
                Defaults to "top_articles".
            threshold_type (str): The filtering method ("rank" or "score").
                Defaults to "rank".
            score_threshold (float): The minimum combined score for filtering when threshold_type
                is "score". Defaults to 0.5.
            rank_threshold (int): The number of top papers to filter when threshold_type is "rank".
                Defaults to 30.
            organize_files (bool): Whether to organize files into the target folder.
                Defaults to True.
            order_by_score (bool): Whether to rename files with their combined score.
                Defaults to True.
            zip_folder (bool): Whether to zip the target folder and source folder.
                Defaults to True.
            plotting (bool): Whether to plot the combined scores of papers.
                Defaults to True.

        Example:
            >>> organizer = ArticleOrganizer("papers", "top_papers")
            >>> isinstance(organizer, ArticleOrganizer)
            True
        """
        self.source_folder = source_folder
        self.target_folder = os.path.join(source_folder, target_folder)
        self.threshold_type = threshold_type
        self.score_threshold = score_threshold
        self.rank_threshold = rank_threshold
        self.organize_files = organize_files
        self.order_by_score = order_by_score
        self.zip_folder = zip_folder
        self.plotting = plotting

        # Create the target folder if it doesn't exist
        if not os.path.exists(self.target_folder):
            os.makedirs(self.target_folder)

    def draw(self, paper_list: list[dict], title: str) -> None:
        """
        Plot the combined scores of papers and save the plot as an image.

        Args:
            paper_list (list[dict]): A list of dictionaries containing paper details.
            title (str): The title of the plot.

        Example:
            >>> organizer = ArticleOrganizer("papers")
            >>> papers = [{"title": "Paper 1", "combined_score": 0.9, "downloaded": True}]
            >>> organizer.draw(papers, "Test Plot")
        """
        boolean_list = [paper.get("downloaded", False) for paper in paper_list]
        x_values = list(range(1, len(paper_list) + 1))
        y_values = [paper["combined_score"] for paper in paper_list]

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker="o", linestyle="-", color="black")

        # Highlight downloaded papers in green
        for i, is_true in enumerate(boolean_list):
            if is_true:
                plt.plot(
                    x_values[i],
                    y_values[i],
                    marker="o",
                    linestyle="None",
                    color="green",
                    label="downloaded",
                )

        # Set plot labels and title
        plt.xlabel("Rank")
        plt.ylabel("Combined Score")
        plt.title(title)
        plt.yscale("log")  # Set y-axis to logarithmic scale
        plt.grid(True)

        # Handle legend to avoid duplicate labels
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())

        # Save the plot as an image
        plt.savefig(f"{self.target_folder}/{title}.png")
        print(f"Plot of score vs rank saved to {self.target_folder}/{title}.png")

    def organize_and_visualize(self) -> None:
        """
        Organize, filter, and visualize the papers based on the initialized parameters.

        Steps:
        1. Read metadata from the source folder.
        2. Sort papers by combined score in descending order.
        3. Draw a plot of the unfiltered papers if plotting is True.
        4. Filter papers based on the selected threshold type ("rank" or "score").
        5. Draw a plot of the filtered papers if plotting is True.
        6. Organize files into the target folder if required, preventing duplicates.
        7. Zip the target folder and source folder if required.

        Example:
            >>> organizer = ArticleOrganizer("papers")
            >>> organizer.organize_and_visualize()  # This would process all papers in "papers"
        """
        # Read metadata
        meta_data_path = os.path.join(self.source_folder, "metadata.json")
        meta_data = read_meta_data(meta_data_path)

        # Sort papers by combined score in descending order and remove duplicates
        original_list = sorted(
            [paper for paper in meta_data if "combined_score" in paper],
            key=lambda x: x["combined_score"],
            reverse=True,
        )

        # Remove duplicates based on title while keeping the highest scoring version
        seen_titles: dict[str, dict] = {}
        unique_list = []
        for paper in original_list:
            title = paper.get("title", "").strip()
            if title and (
                title not in seen_titles
                or paper["combined_score"] > seen_titles[title]["combined_score"]
            ):
                seen_titles[title] = paper
                unique_list.append(paper)

        original_list = unique_list

        # Draw the unfiltered plot if plotting is True
        if self.plotting:
            self.draw(original_list, "Unfiltered")

        # Filter papers based on the selected method
        if self.threshold_type == "score":
            filtered_list = [
                paper for paper in original_list if paper["combined_score"] > self.score_threshold
            ]
        else:  # "rank"
            filtered_list = original_list[: self.rank_threshold]

        # Draw the filtered plot if plotting is True
        if self.plotting:
            self.draw(filtered_list, "Filtered")

        # Organize files if required
        if self.organize_files:
            # Clear the target folder first
            if os.path.exists(self.target_folder):
                shutil.rmtree(self.target_folder)
            os.makedirs(self.target_folder)

            # Process each paper
            processed_files = set()  # Track processed files to avoid duplicates
            for idx, paper in enumerate(filtered_list):
                try:
                    title = paper["title"]
                    score = paper["combined_score"]
                    downloaded = paper.get("downloaded", False)
                    if downloaded:
                        sanitized_title = sanitize_filename(title)
                        base_filename = f"{sanitized_title}.pdf"

                        # Check if this file has already been processed
                        if base_filename in processed_files:
                            continue

                        source_path = os.path.join(self.source_folder, base_filename)
                        if not os.path.exists(source_path):
                            continue

                        # Create new filename with consistent ranking
                        if self.order_by_score:
                            rank = str(idx + 1).zfill(3)  # Use 3 digits for ranking
                            new_filename = f"{rank}_{score:.3g}_{base_filename}"
                        else:
                            new_filename = base_filename

                        # Copy file and mark as processed
                        shutil.copy(source_path, os.path.join(self.target_folder, new_filename))
                        processed_files.add(base_filename)

                except Exception as e:
                    print(f"Error organizing file: {e}")
                    continue
