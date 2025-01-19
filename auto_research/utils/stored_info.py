from __future__ import annotations

import os
from typing import Optional
from typing import Union

from LLM_utils.storage import Storage_base


class Storage(Storage_base):
    """
    A class for managing and storing information about papers in a structured format.

    This class provides functionality to add, retrieve, and check information about
    papers stored in a JSON-like structure. It supports adding papers by path or name,
    adding information to specific papers, and retrieving or checking information
    based on specified criteria.

    Attributes:
        information (dict): A dictionary storing paper information, where keys are
                            paper names and values are nested dictionaries containing
                            information types and their corresponding trials.

    Example:
        >>> storage = Storage()
        >>> storage.add_papers_by_name(["paper1.pdf", "paper2.pdf"])
        >>> storage.add_info_to_a_paper("paper1.pdf", "summary", "This is a summary.")
        >>> storage.get_info(paper_list=["paper1.pdf"], type_list=["summary"])
        ---Paper name: paper1.pdf, Info type: summary, Trial number: 1---
        This is a summary.
    """

    def add_papers_by_path(self, path_to_paper: str) -> None:
        """
        Add the file names of all papers in a specified directory as keys to the info dictionary.

        Args:
            path_to_paper (str): The path to the directory containing the paper files.

        Returns:
            None

        Example:
            >>> storage = Storage()
            >>> storage.add_papers_by_path("/path/to/papers")
        """
        files = os.listdir(path_to_paper)
        for file in files:
            self.information[file] = {}

    def add_papers_by_name(self, list_of_papers: list[str]) -> None:
        """
        Add the file names of all papers in a provided list as keys to the info dictionary.

        Args:
            list_of_papers (list[str]): A list of paper file names to be added to the info dictionary.

        Returns:
            None

        Example:
            >>> storage = Storage()
            >>> storage.add_papers_by_name(["paper1.pdf", "paper2.pdf"])
        """  # noqa: E501
        for paper in list_of_papers:
            self.information[paper] = {}

    def add_info_to_a_paper(
        self, paper_name: str, info_type: str, info_content: str, info_trial: Optional[int] = None
    ) -> None:
        """
        Add information to a specific paper in the info dictionary.

        If the paper or info type does not exist, they are initialized. If a trial number
        is not provided, the next available trial number is automatically assigned.

        Args:
            paper_name (str): The name of the paper to which information will be added.
            info_type (str): The type of information to be added (e.g., 'summary', 'analysis').
            info_content (str): The content of the information to be stored.
            info_trial (Optional[int]): The trial number for the information. If None, the
                                        next available trial number is used.

        Returns:
            None

        Raises:
            ValueError: If the specified trial number already exists for the given paper
                       and info type.

        Example:
            >>> storage = Storage()
            >>> storage.add_papers_by_name(["paper1.pdf"])
            >>> storage.add_info_to_a_paper("paper1.pdf", "summary", "This is a summary.")
        """
        self.load_info()

        if paper_name not in self.information:
            self.information[paper_name] = {}

        if info_type not in self.information[paper_name]:
            self.information[paper_name][info_type] = {}

        if info_trial in self.information[paper_name][info_type]:
            raise ValueError(
                f"This trial already exists for the paper {paper_name} and info type {info_type}."
            )

        if info_trial is None:
            existing_trials = list(map(int, self.information[paper_name][info_type].keys()))
            info_trial = max(existing_trials) + 1 if existing_trials else 1

        self.information[paper_name][info_type][str(info_trial)] = info_content
        self.save_info()

    def get_info(
        self,
        paper_list: Optional[list[str]] = None,
        type_list: Optional[list[str]] = None,
        trial_list: Optional[list[int]] = None,
        verbose: bool = False,
    ) -> None:
        """
        Retrieve information from the info dictionary based on the specified criteria.

        Args:
            paper_list (Optional[list[str]]): List of paper names to retrieve info for.
                                              If None, all papers are included.
            type_list (Optional[list[str]]): List of info types to retrieve info for.
                                             If None, all types are included.
            trial_list (Optional[list[int]]): List of trial numbers to retrieve info for.
                                              If None, all trials are included.
            verbose (bool): If True, prints messages for missing data.

        Returns:
            None

        Example:
            >>> storage = Storage()
            >>> storage.add_papers_by_name(["paper1.pdf"])
            >>> storage.add_info_to_a_paper("paper1.pdf", "summary", "This is a summary.")
            >>> storage.get_info(paper_list=["paper1.pdf"], type_list=["summary"])
            ---Paper name: paper1.pdf, Info type: summary, Trial number: 1---
            This is a summary.
        """
        if paper_list is None:
            paper_list = list(self.information.keys())

        for paper in paper_list:
            if paper not in self.information:
                raise ValueError(f'Paper "{paper}" not found in the info dictionary.')

            current_types = type_list or list(self.information[paper].keys())
            for info_type in current_types:
                if info_type not in self.information[paper]:
                    if verbose:
                        print(f'No info type "{info_type}" in paper "{paper}".')
                    continue

                current_trials = trial_list or list(self.information[paper][info_type].keys())
                for trial in current_trials:
                    if trial in self.information[paper][info_type]:
                        print(
                            f"---Paper name: {paper}, Info type: {info_type}, Trial number: "
                            f"{trial}"
                            f"---"
                        )
                        print(self.information[paper][info_type][trial])
                    else:
                        if verbose:
                            print(
                                f'No trial {trial} for info type "{info_type}" in paper "{paper}".'
                            )

    def check_info(
        self,
        paper_list: Optional[list[str]] = None,
        type_list: Optional[list[str]] = None,
        trial_list: Optional[list[int]] = None,
        verbose: bool = False,
    ) -> Union[bool, dict]:
        """
        Check if the info dictionary contains the specified information.

        Args:
            paper_list (Optional[list[str]]): List of paper names to check. If None, checks all
            papers.
            type_list (Optional[list[str]]): List of info types to check. If None, checks all
            types.
            trial_list (Optional[list[int]]): List of trial numbers to check. If None, checks all
            trials.
            verbose (bool): If True, returns a detailed results dictionary; if False, returns a
            boolean.

        Returns:
            Union[bool, dict]: If verbose=True, returns a nested dictionary with results of the
            existence check.
                               If verbose=False, returns a boolean indicating if all checks passed.

        Example:
            >>> storage = Storage()
            >>> storage.add_papers_by_name(["paper1.pdf"])
            >>> storage.add_info_to_a_paper("paper1.pdf", "summary", "This is a summary.")
            >>> storage.check_info(paper_list=["paper1.pdf"], type_list=["summary"])
            True
        """
        results: dict = {}

        papers_to_check = paper_list or list(self.information.keys())
        for paper in papers_to_check:
            if paper not in self.information:
                results[paper] = False
                continue

            if type_list is None:
                results[paper] = True
                continue

            results[paper] = {}
            for info_type in type_list:
                if info_type not in self.information[paper]:
                    results[paper][info_type] = False
                    continue

                if trial_list is None:
                    results[paper][info_type] = True
                    continue

                results[paper][info_type] = {}
                for trial in trial_list:
                    results[paper][info_type][trial] = (
                        str(trial) in self.information[paper][info_type]
                    )

        if verbose:
            return results

        for paper, paper_data in results.items():
            if isinstance(paper_data, bool) and not paper_data:
                return False
            if isinstance(paper_data, dict):
                for info_type, type_data in paper_data.items():
                    if isinstance(type_data, bool) and not type_data:
                        return False
                    if isinstance(type_data, dict):
                        for trial, trial_result in type_data.items():
                            if not trial_result:
                                return False

        return True

    @staticmethod
    def get_latest_trial(info_papers: dict) -> Optional[str]:
        """
        Retrieve the latest trial information from a given dictionary of trials.

        Args:
            info_papers (dict): A dictionary containing trial information.

        Returns:
            Optional[str]: The value corresponding to the latest trial. Returns None if the
            dictionary is empty.

        Example:
            >>> storage = Storage()
            >>> storage.get_latest_trial({"1": "Trial 1", "2": "Trial 2"})
            'Trial 2'
        """
        if not info_papers:
            return None
        largest_key = max(info_papers.keys())
        return info_papers[largest_key]
