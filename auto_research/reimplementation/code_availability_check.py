from __future__ import annotations
from LLM_utils.prompter import PromptBase


from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        # Check if the scheme and netloc (domain) are present
        return all([result.scheme, result.netloc])
    except:
        return False


def test_github_link(response):
    if response != "not available":
        assert is_valid_url(response), f"The information is\n{response}\ninstead of a valid url"
        assert "github.com" in response, f"The information is\n{response}\ninstead of a valid github link"
    return response

def base_prompt_formatted():
    target_information=\
        ("Information about the availability of Github link for the code that implements the method."
         " If the link is not available, your answer should be 'not available'. Your answer should"
         " only be the Github link or 'not available' and nothing else")
    return target_information

