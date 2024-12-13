import json
import os


class Storage:
    """This class is used to read and write information about papers in a json file"""

    def __init__(self, path):
        self.path = path
        self.paper_info = {}

    def load_info(self):
        """
        This method loads the info dictionary from a json file.

        Args:

        Returns:

        """

        try:
            with open(self.path, "r") as file:
                self.paper_info = json.load(file)
            print(f"Information is loaded from {self.path}.")
        except:
            print(f"No existing stored information is found in {self.path}.")

    def save_info(self):
        """
        This method saves the info dictionary to a JSON file in a nicely formatted way.

        Args:

        Returns:

        """
        with open(self.path, "w") as file:
            json.dump(self.paper_info, file, indent=4)  # Use indent=4 for pretty formatting
        print(f"Information is saved to {self.path}.")

    def add_papers_by_path(self, path_to_paper):
        """
        This method adds the file names of all papers in a directory as keys to the info dictionary.

        Args:
            path_to_paper:

        Returns:

        """

        # get all files in the directory
        files = os.listdir(path_to_paper)
        # add the file names to the info dictionary
        for file in files:
            self.paper_info[file] = {}

    def add_papers_by_name(self, list_of_papers):
        """
        This method adds the file names of all papers in a list as keys to the info dictionary.

        Args:
            names:

        Returns:

        """
        for paper in list_of_papers:
            self.paper_info[paper] = {}

    def add_info_to_a_paper(self, paper_name, info_type, info_content, info_trial=None):
        """
        This method adds information to a paper in the info dictionary.

        Args:
            paper_name:
            info:

        Returns:

        """

        self.load_info()

        if paper_name not in self.paper_info:
            self.paper_info[paper_name] = {}

        if info_type not in self.paper_info[paper_name]:
            self.paper_info[paper_name][info_type] = {}

        if info_trial in self.paper_info[paper_name][info_type]:
            raise ValueError(
                f"This trial already exists for the paper {paper_name} and info type "
                f"{info_type}"
            )

        if info_trial is None:
            existing_trials = list(map(int, self.paper_info[paper_name][info_type].keys()))
            if len(existing_trials) == 0:
                info_trial = 1
            else:
                info_trial = max(existing_trials) + 1

        self.paper_info[paper_name][info_type][str(info_trial)] = info_content

        self.save_info()

    def get_info(self, paper_list=None, type_list=None, trial_list=None, verbose=False):
        """
        This method gets the information in the info dictionary according to the specified range.

        Args:
            paper_list: List of paper names to retrieve info for. If None, all papers are included.
            type_list: List of types to retrieve info for. If None, all types are included.
            trial_list: List of trial numbers to retrieve info for. If None, all trials are included.
            verbose: If True, prints messages for missing data.

        Returns:
            None
        """
        # If paper_list is None, include all papers
        if paper_list is None:
            paper_list = list(self.paper_info.keys())

        for paper in paper_list:
            if paper not in self.paper_info:
                raise ValueError(f'Paper "{paper}" not found in the info dictionary.')

            # If type_list is None, include all types for this paper
            current_types = type_list or list(self.paper_info[paper].keys())
            for info_type in current_types:
                if info_type not in self.paper_info[paper]:
                    if verbose:
                        print(f'No info type "{info_type}" in paper "{paper}".')
                    continue

                # If trial_list is None, include all trials for this type
                current_trials = trial_list or list(self.paper_info[paper][info_type].keys())
                for trial in current_trials:
                    if trial in self.paper_info[paper][info_type]:
                        print(
                            f"---Paper name: {paper}, Info type: {info_type}, Trial number: {trial}---"
                        )
                        print(self.paper_info[paper][info_type][trial])
                    else:
                        if verbose:
                            print(
                                f'No trial {trial} for info type "{info_type}" in paper "{paper}".'
                            )

    def check_info(self, paper_list=None, type_list=None, trial_list=None, verbose=False):
        """
        This method checks if the info dictionary contains the information for the specified ranges.

        Args:
            paper_list: List of paper names to check. If None, checks all papers.
            type_list: List of info types to check. If None, checks all types.
            trial_list: List of trial numbers to check. If None, checks all trials.
            verbose: If True, returns the detailed results dictionary; if False, returns a boolean.

        Returns:
            If verbose=True, returns a nested dictionary with results of the existence check.
            If verbose=False, returns a boolean indicating if all checks passed.
        """
        results = {}

        # If paper_list is None, check all papers
        papers_to_check = paper_list or list(self.paper_info.keys())

        for paper in papers_to_check:
            if paper not in self.paper_info:
                results[paper] = False
                continue

            if type_list is None:
                results[paper] = True
                continue

            results[paper] = {}
            for info_type in type_list:
                if info_type not in self.paper_info[paper]:
                    results[paper][info_type] = False
                    continue

                if trial_list is None:
                    results[paper][info_type] = True
                    continue

                results[paper][info_type] = {}
                for trial in trial_list:
                    results[paper][info_type][trial] = (
                        str(trial) in self.paper_info[paper][info_type]
                    )

        if verbose:
            return results

        # Return False if any value in the results is False
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
    def get_latest_trial(info_papers):
        if not info_papers:
            return None  # Return None if the info_papers is empty
        largest_key = max(info_papers.keys())  # Find the largest key
        return info_papers[largest_key]  # Return the value corresponding to the largest key


#
# storage_instance = Storage('info.json')
#
# storage_instance.load_info()
#
# storage_instance.add_papers_by_path('/home/j/experiments/auto_research/auto_research/survey/sample_articles')
#
# print(storage_instance.paper_info)
#
# storage_instance.add_info_to_a_paper('example.pdf', 'abstract', 'This is an abstract')
# storage_instance.add_info_to_a_paper('example.pdf', 'abstract', 'This is an abstract')
# storage_instance.get_info(None , ['abstract'] , [1])
# storage_instance.get_info()
#
# storage_instance.save_info()
#
# # Check if specific papers, types, and trials exist
# result = storage_instance.check_info(
#     ['example.pdf', 'another_paper.pdf'],
#     ['abstract', 'summary'],
# )
#
# print(result)
