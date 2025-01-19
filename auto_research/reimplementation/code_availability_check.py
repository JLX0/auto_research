from __future__ import annotations

from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """
    Validate whether the provided string is a valid URL.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid (contains both a scheme and a netloc), False otherwise.

    Example:
        >>> is_valid_url("https://github.com")
        True
        >>> is_valid_url("invalid-url")
        False
    """
    try:
        result = urlparse(url)
        # Check if the scheme (e.g., 'http') and netloc (domain) are present.
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def test_github_link(response: str) -> str:
    """
    Test if the provided response is a valid GitHub URL.

    Args:
        response (str): The response to test. Expected to be a GitHub URL or "not available".

    Returns:
        str: The original response if it passes the validation.

    Raises:
        AssertionError: If the response is not a valid URL or does not contain "github.com".

    Example:
        >>> test_github_link("https://github.com/user/repo")
        'https://github.com/user/repo'
        >>> test_github_link("not available")
        'not available'
    """
    if response != "not available":
        assert is_valid_url(response), f"The information is\n{response}\ninstead of a valid URL."
        assert (
            "github.com" in response
        ), f"The information is\n{response}\ninstead of a valid GitHub link."
    return response


def base_prompt_formatted() -> str:
    """
    Generate a formatted prompt string requesting information about the availability of a
    GitHub link.

    Returns:
        str: A string containing the formatted prompt instructions.

    Example:
        >>> base_prompt_formatted()
        'Information about the availability of a GitHub link for the code that implements the
         method. If the link is not available, your answer should be "not available". Your answer
          should only be the GitHub link or "not available" and nothing else.'
    """
    target_information = (
        "Information about the availability of a GitHub link for the code that implements the"
        " method. "
        'If the link is not available, your answer should be "not available". '
        "Your answer should only be the GitHub link or 'not available' and nothing else."
    )
    return target_information
