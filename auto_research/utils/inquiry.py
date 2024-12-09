from openai import OpenAI
import os
import json


def check_and_read_key_file(file_path , target_key) :
    """
    Checks if a file named `key.json` exists in the specified path, validates if
    it contains a Python dictionary, and retrieves the value associated with the
    specified key.

    :param file_path: The path where the `key.json` file is expected to be located.
    :type file_path: str
    :param target_key: The key in the dictionary whose value needs to be retrieved.
    :type target_key: str
    :return: The value associated with the specified key if all checks pass;
             -1 if the file does not exist, the contents are not a dictionary, or
             the key is missing.
    :rtype: Any or int
    """

    # Construct the full path to the file
    full_path = os.path.join(file_path , 'key.json')

    # Check if the file exists
    if not os.path.exists(full_path) :
        return -1  # Return -1 if the file does not exist

    # Open and read the file
    try :
        with open(full_path , 'r') as file :
            data = json.load(file)  # Attempt to parse JSON
    except (json.JSONDecodeError , IOError) :
        return -1  # Return -1 if the file contents cannot be read as valid JSON

    # Check if the data is a dictionary
    if not isinstance(data , dict) :
        return -1  # Return -1 if the data is not a dictionary

    # Check if the target key exists and return its value
    if target_key in data :
        return data[target_key]

    return -1  # Return -1 if the target key is not found


class gpt():
    def __init__(self, api_key, model='gpt-4o-mini',debug=False):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.debug = debug

    @staticmethod
    def print_prompt(message):
        for prompt_segment in message:
            print(prompt_segment["content"])

    def ask(self,message):
        if self.debug:
            print("-----Prompt beginning marker-----")
            self.print_prompt(message)
            print("-----Prompt ending marker-----")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message
        )
        response=response.choices[0].message.content
        if self.debug:
            print("------Response beginning marker-----")
            print(response)
            print("------Response ending marker-----")
        return response